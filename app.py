import streamlit as st
import random

# -------------------------- 页面配置与样式 --------------------------
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

/* 输入框 */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 1px solid #e6c89c;
    text-align: center;
}

/* 题目列表 */
.question-list-card {
    background: #fff3d9;
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
    background: #fcd34d;
    font-weight: bold;
}

/* 作答区域 */
.answer-area-card {
    background: #fff3d9;
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

/* 诊断框 */
.diagnose-box {
    background: #fff3d9;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    color: #8b3c1c;
    margin-bottom: 16px;
    line-height:1.6;
}

/* 统计行 */
.stats-row {
    display: flex;
    justify-content: space-around;
    background: #f0e2ca;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    margin-top:10px;
}
.stat-item {
    background: #fff3d9;
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

# -------------------------- 状态初始化 --------------------------
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
if "checked" not in st.session_state:
    st.session_state.checked = False
if "error_list" not in st.session_state:
    st.session_state.error_list = []
if "total" not in st.session_state:
    st.session_state.total = 0
if "right" not in st.session_state:
    st.session_state.right = 0
if "is_review_mode" not in st.session_state:
    st.session_state.is_review_mode = False

# -------------------------- 题型分类 --------------------------
def get_qtype(a,b,opt):
    if opt == "+":
        return "carry_add" if (a%10 + b%10)>=10 else "normal_add"
    else:
        return "carry_sub" if (a%10 < b%10) else "normal_sub"

# -------------------------- 出题 --------------------------
def gen_q(level):
    opt = "+" if random.random()>0.5 else "-"
    a=b=ans=0
    if level=="基础":
        if opt=="+":
            while True:
                a,b=random.randint(1,10),random.randint(1,10)
                if a+b<=20: break
        else:
            while True:
                a,b=random.randint(5,15),random.randint(1,10)
                if a-b>=0: break
    elif level=="进阶":
        a = random.randint(10,35) if opt=="+" else random.randint(15,50)
        b = random.randint(5,30)
        ans = a+b if opt=="+" else a-b
        if ans<0: return gen_q(level)
    else:
        if opt=="+":
            while True:
                a,b=random.randint(30,70),random.randint(20,60)
                if a+b<=100: break
        else:
            while True:
                a,b=random.randint(50,99),random.randint(10,49)
                if a-b>=0: break
    ans = a+b if opt=="+" else a-b
    return {"a":a,"b":b,"opt":opt,"ans":ans,"type":get_qtype(a,b,opt)}

def gen10(level): return [gen_q(level) for _ in range(10)]

# -------------------------- 🔴 核心：错题重做删除（会更新列表） --------------------------
def remove_from_errors(q_remove):
    new_err = []
    for q in st.session_state.error_list:
        if not (q["a"] == q_remove["a"] and q["b"] == q_remove["b"] and q["opt"] == q_remove["opt"]):
            new_err.append(q)
    st.session_state.error_list = new_err
    # 错题重做模式下，更新当前题目列表
    if st.session_state.is_review_mode:
        st.session_state.questions = st.session_state.error_list.copy()
        if st.session_state.current_idx >= len(st.session_state.questions):
            st.session_state.current_idx = max(0, len(st.session_state.questions)-1)

# -------------------------- AI诊断 --------------------------
def ai_diagnose():
    err = st.session_state.error_list
    if len(err)==0: return "✅ 暂无错题，太棒啦！"

    cnt = {"normal_add":0,"carry_add":0,"normal_sub":0,"carry_sub":0}
    for q in err: cnt[q["type"]] +=1
    total_err = len(err)

    type_name = {
        "normal_add":"不进位加法",
        "carry_add":"进位加法",
        "normal_sub":"不退位减法",
        "carry_sub":"退位减法"
    }

    advise = {
        "normal_add":"基础简单，注意看清数字即可",
        "carry_add":"个位满十要进1，重点练进位规则",
        "normal_sub":"直接相减，注意不要写反数字",
        "carry_sub":"个位不够减要借1，十位记得减1"
    }

    max_type = max(cnt, key=cnt.get)
    max_num = cnt[max_type]
    rate = int(max_num / total_err *100)

    if rate >= 60:
        reason = f"你**最薄弱**的是【{type_name[max_type]}】，占总错题{rate}%"
    elif rate >=30:
        reason = f"你主要错在【{type_name[max_type]}】，需要加强练习"
    else:
        reason = f"你错得比较平均，重点加强【{type_name[max_type]}】"

    suggestion = f"💡 建议：{advise[max_type]}"
    return f"{reason}\n{suggestion}"

# -------------------------- 界面 --------------------------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📚 AI口算错题本</div>', unsafe_allow_html=True)

    # 姓名班级
    col1,col2 = st.columns(2)
    with col1:
        st.session_state.student_name = st.text_input("姓名", value=st.session_state.student_name, label_visibility="collapsed", placeholder="姓名")
    with col2:
        st.session_state.student_class = st.text_input("班级", value=st.session_state.student_class, label_visibility="collapsed", placeholder="班级")

    # 难度按钮（已修复点击变色）
    cols = st.columns(3)
    difficulty_list = ["基础", "进阶", "困难"]
    for i, diff in enumerate(difficulty_list):
        with cols[i]:
            if st.button(diff, key=diff, use_container_width=True):
                st.session_state.difficulty = diff
                st.rerun()

    # 高亮当前选中的难度按钮
    active_index = difficulty_list.index(st.session_state.difficulty)
    st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) button:nth-child({active_index + 1}) {{
        background-color: #d97706 !important;
        color: white !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 一键出题（只在非错题模式可用）
    if not st.session_state.is_review_mode:
        if st.button("📝 一键出10道题", use_container_width=True, type="primary"):
            st.session_state.questions = gen10(st.session_state.difficulty)
            st.session_state.current_idx = 0
            st.session_state.checked = False
            st.rerun()

    # AI诊断
    st.markdown(f'<div class="diagnose-box">AI智能诊断：{ai_diagnose()}</div>', unsafe_allow_html=True)

    # 题目列表
    if st.session_state.questions:
        st.markdown('<div class="question-list-card"><div style="font-weight:bold;">本次题目：</div></div>', unsafe_allow_html=True)
        for i,q in enumerate(st.session_state.questions):
            active = "active" if i==st.session_state.current_idx else ""
            st.markdown(f'<div class="question-item {active}">{i+1}. {q["a"]}{q["opt"]}{q["b"]}=?</div>', unsafe_allow_html=True)

        qnow = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f'<div class="answer-area-card"><div class="current-question-text">{qnow["a"]}{qnow["opt"]}{qnow["b"]}=?</div></div>', unsafe_allow_html=True)

        # 答案输入框（按题目索引清空）
        user_ans = st.text_input(
            "答案", 
            value="", 
            label_visibility="collapsed", 
            placeholder="得数",
            key=f"ans_{st.session_state.current_idx}"
        )

        col1,col2,col3 = st.columns(3)
        with col1:
            if st.button("✅ 核对", use_container_width=True):
                st.session_state.checked = True
                st.session_state.total +=1
                try:
                    u = int(user_ans)
                    if u == qnow["ans"]:
                        st.session_state.right +=1
                        st.success("🎉 回答正确！")
                        # 错题重做做对，自动从错题库移除并更新列表
                        if st.session_state.is_review_mode:
                            remove_from_errors(qnow)
                            st.info("✅ 此题已从错题库移除")
                            if len(st.session_state.questions) == 0:
                                st.info("🎉 所有错题已全部订正完成！")
                    else:
                        st.error(f"❌ 正确答案：{qnow['ans']}")
                        # 正常练习模式，做错则加入错题本
                        if not st.session_state.is_review_mode:
                            exist = any(x["a"]==qnow["a"] and x["b"]==qnow["b"] and x["opt"]==qnow["opt"] for x in st.session_state.error_list)
                            if not exist:
                                st.session_state.error_list.append(qnow)
                except:
                    st.warning("⚠️ 请输入数字！")
        with col2:
            if st.button("➡️ 下一题", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.questions)-1:
                    st.session_state.current_idx +=1
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.info("✅ 已完成所有题目！")
        with col3:
            if st.button("📚 错题重做", use_container_width=True):
                if len(st.session_state.error_list) > 0:
                    # 🔴 只加载错题列表，不再加载之前的10题
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    st.session_state.checked = False
                    st.session_state.is_review_mode = True
                    st.rerun()
                else:
                    st.info("暂无错题可重做~")

    if st.button("🔄 重置数据", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # 统计
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
    if st.session_state.total>0:
        if acc==100: msg="🏆 满分学霸！口算天才！"
        elif acc>=90: msg="🌟 太厉害！口算小能手！"
        elif acc>=80: msg="👏 优秀！再细心就完美！"
        elif acc>=60: msg="👍 很棒！继续加油！"
        else: msg="💪 别灰心，多练必进步！"
        st.markdown(f'<div class="encourage">{msg}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
