import streamlit as st
import random

# 页面基础设置
st.set_page_config(page_title="AI口算错题本", layout="centered")

# 1. 还原你截图的暖黄风格样式
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background: linear-gradient(180deg, #fff3d9 0%, #ffe9c2 100%);
    padding: 1rem;
}

/* 主卡片 */
.main-card {
    background: #fff9e8;
    border-radius: 24px;
    padding: 24px;
    max-width: 500px;
    margin: 0 auto;
    box-shadow: 0 8px 24px rgba(139, 60, 28, 0.15);
}

/* 标题 */
.title {
    text-align: center;
    font-size: 24px;
    color: #8b3c1c;
    font-weight: bold;
    margin-bottom: 16px;
}

/* 输入框行 */
.input-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
}
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 1px solid #e6c89c;
    text-align: center;
}

/* 难度按钮 */
.difficulty-buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 12px;
}
.diff-btn {
    padding: 8px 20px;
    border-radius: 20px;
    border: none;
    font-weight: bold;
    cursor: pointer;
}
.diff-btn.active {
    background-color: #d97706;
    color: white;
}
.diff-btn:not(.active) {
    background-color: #f0e2ca;
    color: #8b3c1c;
}

/* 一键出题按钮 */
.gen-btn {
    display: block;
    margin: 0 auto 16px auto;
    background-color: #2f855a;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 20px;
    font-weight: bold;
}

/* 诊断提示 */
.diagnose-box {
    background-color: #fff3d9;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    color: #8b3c1c;
    margin-bottom: 16px;
}

/* 题目卡片 */
.q-card {
    background-color: #fff3d9;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}
.q-text {
    font-size: 48px;
    color: #8b3c1c;
    font-weight: bold;
    margin-bottom: 16px;
}
.ans-input {
    width: 120px;
    margin: 0 auto;
}

/* 操作按钮组 */
.action-buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 16px;
}
.btn {
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    font-weight: bold;
    color: white;
}
.btn-check { background-color: #d97706; }
.btn-next { background-color: #718096; }
.btn-redo { background-color: #e53e3e; }
.btn-reset { background-color: #4a5568; }

/* 提示文字 */
.tip-text {
    text-align: center;
    color: #8b3c1c;
    margin-bottom: 16px;
}

/* 统计行 */
.stats-row {
    display: flex;
    justify-content: space-around;
    background-color: #f0e2ca;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 16px;
}
.stat-item {
    background-color: #fff3d9;
    padding: 6px 12px;
    border-radius: 10px;
    color: #8b3c1c;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 2. 初始化会话状态
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "student_class" not in st.session_state:
    st.session_state.student_class = ""
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "基础"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "user_ans" not in st.session_state:
    st.session_state.user_ans = ""
if "checked" not in st.session_state:
    st.session_state.checked = False
if "error_list" not in st.session_state:
    st.session_state.error_list = []
if "total" not in st.session_state:
    st.session_state.total = 0
if "right" not in st.session_state:
    st.session_state.right = 0

# 3. 题目生成与分类
def get_kind(a, b, opt):
    if opt == "+":
        return "carry_add" if (a % 10 + b % 10) >= 10 else "normal_add"
    else:
        return "carry_sub" if (a % 10) < (b % 10) else "normal_sub"

def gen_single_q(level):
    opt = "+" if random.random() > 0.5 else "-"
    if level == "基础":
        if opt == "+":
            a, b = random.randint(1, 10), random.randint(1, 10)
            while a + b > 20:
                a, b = random.randint(1, 10), random.randint(1, 10)
        else:
            a, b = random.randint(5, 15), random.randint(1, 10)
            while a - b < 0:
                a, b = random.randint(5, 15), random.randint(1, 10)
    elif level == "进阶":
        a = random.randint(10, 35) if opt == "+" else random.randint(15, 50)
        b = random.randint(5, 30)
        ans = a + b if opt == "+" else a - b
        if ans < 0:
            return gen_single_q(level)
    else: # 困难
        if opt == "+":
            a, b = random.randint(30, 70), random.randint(20, 60)
            while a + b > 100:
                a, b = random.randint(30, 70), random.randint(20, 60)
        else:
            a, b = random.randint(50, 99), random.randint(10, 49)
            while a - b < 0:
                a, b = random.randint(50, 99), random.randint(10, 49)
    ans = a + b if opt == "+" else a - b
    return {"a":a, "b":b, "opt":opt, "ans":ans, "kind":get_kind(a,b,opt)}

def gen_10_questions(level):
    return [gen_single_q(level) for _ in range(10)]

def diagnose():
    if not st.session_state.error_list:
        return "暂无错题，太棒啦！"
    kind_map = {"normal_add":"不进位加法","carry_add":"进位加法","normal_sub":"不退位减法","carry_sub":"退位减法"}
    cnt = {k:0 for k in kind_map}
    for q in st.session_state.error_list:
        cnt[q["kind"]] += 1
    weak = [f"{kind_map[k]}错{cnt[k]}道" for k in cnt if cnt[k]>0]
    return f"薄弱点：{', '.join(weak)}" if weak else "暂无错题，太棒啦！"

# 4. 界面主体
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # 标题
    st.markdown('<div class="title">📚 AI口算错题本</div>', unsafe_allow_html=True)

    # 姓名/班级输入
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.student_name = st.text_input("姓名", value=st.session_state.student_name, label_visibility="collapsed", placeholder="姓名")
    with col2:
        st.session_state.student_class = st.text_input("班级", value=st.session_state.student_class, label_visibility="collapsed", placeholder="班级")

    # 难度选择按钮
    cols = st.columns(3)
    for i, diff in enumerate(["基础", "进阶", "困难"]):
        with cols[i]:
            if st.button(diff, key=diff, use_container_width=True):
                st.session_state.difficulty = diff
                st.rerun()
    st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child({["1","2","3"][["基础","进阶","困难"].index(st.session_state.difficulty)]}) {{
        background-color: #d97706;
        color: white;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 一键出题按钮
    if st.button("📝 一键出10道题", use_container_width=True, type="primary"):
        st.session_state.questions = gen_10_questions(st.session_state.difficulty)
        st.session_state.current_idx = 0
        st.session_state.user_ans = ""
        st.session_state.checked = False
        st.rerun()

    # 诊断提示
    st.markdown(f'<div class="diagnose-box">AI薄弱诊断：{diagnose()}</div>', unsafe_allow_html=True)

    # 题目区域
    if st.session_state.questions:
        q = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f"""
        <div class="q-card">
            <div class="q-text">{q['a']} {q['opt']} {q['b']} = ?</div>
        </div>
        """, unsafe_allow_html=True)

        # 答案输入
        st.session_state.user_ans = st.text_input("答案", value=st.session_state.user_ans, label_visibility="collapsed", placeholder="得数", key="ans_input")

        # 操作按钮组
        col_check, col_next, col_redo = st.columns(3)
        with col_check:
            if st.button("✅ 核对", key="check", use_container_width=True, type="primary"):
                st.session_state.checked = True
                st.session_state.total += 1
                try:
                    u = int(st.session_state.user_ans)
                    if u == q["ans"]:
                        st.session_state.right += 1
                        st.success("🎉 回答正确！")
                    else:
                        st.error(f"❌ 正确答案：{q['ans']}")
                        if not any(x["a"]==q["a"] and x["b"]==q["b"] and x["opt"]==q["opt"] for x in st.session_state.error_list):
                            st.session_state.error_list.append(q)
                except:
                    st.warning("⚠️ 请输入数字！")
        with col_next:
            if st.button("➡️ 下一题", key="next", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.questions)-1:
                    st.session_state.current_idx += 1
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.info("✅ 10道题已完成！")
        with col_redo:
            if st.button("📚 错题重做", key="redo", use_container_width=True):
                if st.session_state.error_list:
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.info("暂无错题可重做~")
    else:
        st.markdown('<div class="tip-text">💡 点击“一键出10道题”开始练习</div>', unsafe_allow_html=True)

    # 重置按钮
    if st.button("🔄 重置数据", key="reset", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 统计信息
    acc = round(st.session_state.right/st.session_state.total*100) if st.session_state.total>0 else 0
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">总题 {st.session_state.total}</div>
        <div class="stat-item">做对 {st.session_state.right}</div>
        <div class="stat-item">错题 {len(st.session_state.error_list)}</div>
        <div class="stat-item">正确率 {acc}%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
