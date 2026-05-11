import streamlit as st
import random

# -------------------------- 页面配置与样式（和截图完全一致） --------------------------
st.set_page_config(page_title="AI口算错题本", layout="centered")

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

/* 姓名班级输入框 */
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

/* AI薄弱诊断框 */
.diagnose-box {
    background-color: #fff3d9;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    color: #8b3c1c;
    margin-bottom: 16px;
}

/* 题目列表区域 */
.question-list-card {
    background-color: #fff3d9;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
}
.question-item {
    font-size: 18px;
    color: #8b3c1c;
    margin: 8px 0;
    padding: 6px 10px;
    border-radius: 8px;
}
.question-item.active {
    background-color: #fcd34d;
    font-weight: bold;
}

/* 单题作答区域 */
.answer-area-card {
    background-color: #fff3d9;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
}
.current-question-text {
    font-size: 48px;
    color: #8b3c1c;
    font-weight: bold;
    margin-bottom: 16px;
}
.answer-input {
    width: 120px;
    margin: 0 auto;
}

/* 操作按钮组 */
.action-buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 16px;
}
.btn-check {
    background-color: #d97706;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: bold;
}
.btn-next {
    background-color: #9ca3af;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: bold;
}
.btn-redo {
    background-color: #e11d48;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: bold;
}
.btn-reset {
    background-color: #4b5563;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: bold;
}

/* 统计行 */
.stats-row {
    display: flex;
    justify-content: space-around;
    background-color: #f0e2ca;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    margin-top: 16px;
}
.stat-item {
    background-color: #fff3d9;
    padding: 6px 10px;
    border-radius: 10px;
    color: #8b3c1c;
    font-weight: bold;
}

/* 鼓励语 */
.encourage {
    text-align:center;
    font-size:16px;
    font-weight:bold;
    color:#8b3c1c;
    margin-top:12px;
    padding:8px;
    background:#fff3d9;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- 初始化会话状态 --------------------------
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

# -------------------------- 题目生成与AI诊断核心逻辑 --------------------------
def get_question_type(a, b, opt):
    """判断题目类型，用于薄弱点诊断"""
    if opt == "+":
        if (a % 10 + b % 10) >= 10:
            return "carry_add"
        else:
            return "normal_add"
    else:
        if (a % 10) < (b % 10):
            return "carry_sub"
        else:
            return "normal_sub"

def generate_single_question(level):
    """生成单道题"""
    opt = "+" if random.random() > 0.5 else "-"
    a, b, ans = 0, 0, 0
    if level == "基础":
        if opt == "+":
            while True:
                a, b = random.randint(1, 10), random.randint(1, 10)
                if a + b <= 20: break
        else:
            while True:
                a, b = random.randint(5, 15), random.randint(1, 10)
                if a - b >= 0: break
    elif level == "进阶":
        if opt == "+":
            a, b = random.randint(10, 35), random.randint(5, 30)
            ans = a + b
        else:
            a, b = random.randint(15, 50), random.randint(5, 30)
            ans = a - b
        if ans < 0:
            return generate_single_question(level)
    else: # 困难
        if opt == "+":
            while True:
                a, b = random.randint(30, 70), random.randint(20, 60)
                if a + b <= 100: break
        else:
            while True:
                a, b = random.randint(50, 99), random.randint(10, 49)
                if a - b >= 0: break
    ans = a + b if opt == "+" else a - b
    return {
        "a": a, "b": b, "opt": opt, "ans": ans, "type": get_question_type(a, b, opt)
    }

def generate_10_questions(level):
    """一次性生成10道题"""
    return [generate_single_question(level) for _ in range(10)]

def ai_weakness_diagnosis():
    """AI薄弱点诊断"""
    if not st.session_state.error_list:
        return "暂无错题，太棒啦！"
    type_count = {"normal_add":0, "carry_add":0, "normal_sub":0, "carry_sub":0}
    for q in st.session_state.error_list:
        type_count[q["type"]] += 1
    max_err = max(type_count.values())
    if max_err == 0:
        return "暂无错题，太棒啦！"
    type_info = {
        "normal_add": "不进位加法", "carry_add": "进位加法",
        "normal_sub": "不退位减法", "carry_sub": "退位减法"
    }
    weak_types = [k for k, v in type_count.items() if v == max_err]
    weak_text = "、".join([type_info[t] for t in weak_types])
    return f"薄弱点：{weak_text}（错{max_err}道），建议加强练习！"

# -------------------------- 界面主体 --------------------------
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

    # 难度选择
    cols = st.columns(3)
    for i, diff in enumerate(["基础", "进阶", "困难"]):
        with cols[i]:
            if st.button(diff, key=diff, use_container_width=True):
                st.session_state.difficulty = diff
                st.rerun()
    # 高亮当前难度
    st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child({["1","2","3"][["基础","进阶","困难"].index(st.session_state.difficulty)]}) {{
        background-color: #d97706;
        color: white;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 一键出10道题按钮
    if st.button("📝 一键出10道题", use_container_width=True, type="primary"):
        st.session_state.questions = generate_10_questions(st.session_state.difficulty)
        st.session_state.current_idx = 0
        st.session_state.user_ans = ""
        st.session_state.checked = False
        st.rerun()

    # AI薄弱诊断
    st.markdown(f'<div class="diagnose-box">AI薄弱诊断：{ai_weakness_diagnosis()}</div>', unsafe_allow_html=True)

    # 题目列表（一键出题后显示10道题）
    if st.session_state.questions:
        st.markdown('<div class="question-list-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight:bold; margin-bottom:8px;'>本次10道题：</div>", unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.questions):
            is_active = i == st.session_state.current_idx
            st.markdown(f"""
            <div class="question-item {'active' if is_active else ''}">
                {i+1}. {q['a']} {q['opt']} {q['b']} = ?
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 当前单题作答区域
        q = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f"""
        <div class="answer-area-card">
            <div class="current-question-text">{q['a']} {q['opt']} {q['b']} = ?</div>
        </div>
        """, unsafe_allow_html=True)

        # 答案输入框
        st.session_state.user_ans = st.text_input("答案", value=st.session_state.user_ans, label_visibility="collapsed", placeholder="得数", key="ans_input")

        # 操作按钮组（核对、下一题、错题重做）
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ 核对", key="check", use_container_width=True):
                st.session_state.checked = True
                st.session_state.total += 1
                try:
                    user_ans = int(st.session_state.user_ans)
                    if user_ans == q["ans"]:
                        st.session_state.right += 1
                        st.success("🎉 回答正确！")
                    else:
                        st.error(f"❌ 正确答案是：{q['ans']}")
                        if not any(x["a"]==q["a"] and x["b"]==q["b"] and x["opt"]==q["opt"] for x in st.session_state.error_list):
                            st.session_state.error_list.append(q)
                except:
                    st.warning("⚠️ 请输入数字！")
        with col2:
            if st.button("➡️ 下一题", key="next", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.questions)-1:
                    st.session_state.current_idx += 1
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.info("✅ 已完成所有题目！")
        with col3:
            if st.button("📚 错题重做", key="redo", use_container_width=True):
                if st.session_state.error_list:
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.info("暂无错题可重做~")

    # 重置数据按钮
    if st.button("🔄 重置数据", use_container_width=True):
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

    # 鼓励语
    if st.session_state.total > 0:
        if acc == 100:
            msg = "🏆 满分学霸！你简直是口算天才！"
        elif acc >= 90:
            msg = "🌟 太厉害啦！你是口算小能手！"
        elif acc >= 80:
            msg = "👏 表现优秀，再细心一点就完美啦！"
        elif acc >= 60:
            msg = "👍 很棒啦！继续加油，一定会更厉害！"
        else:
            msg = "💪 别灰心，多练习一定会进步！"
        st.markdown(f'<div class="encourage">{msg}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
