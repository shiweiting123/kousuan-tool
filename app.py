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

# -------------------------- 状态初始化（安全版） --------------------------
default_state = {
    "student_name": "",
    "student_class": "",
    "difficulty": "基础",
    "questions": [],
    "current_idx": 0,
    "user_ans": "",
    "checked": False,
    "error_list": [],
    "total": 0,
    "right": 0,
    "is_review_mode": False
}

for key, val in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -------------------------- 题型分类 --------------------------
def get_qtype(a, b, opt):
    if opt == "+":
        return "carry_add" if (a % 10 + b % 10) >= 10 else "normal_add"
    else:
        return "carry_sub" if (a % 10 < b % 10) else "normal_sub"

# -------------------------- 出题逻辑（修复负数、重复计算） --------------------------
def gen_q(level):
    opt = random.choice(["+", "-"])
    a, b, ans = 0, 0, 0

    if level == "基础":
        if opt == "+":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            ans = a + b
        else:
            a = random.randint(5, 15)
            b = random.randint(1, 10)
            ans = a - b

    elif level == "进阶":
        if opt == "+":
            a = random.randint(10, 50)
            b = random.randint(5, 50)
            ans = a + b
        else:
            a = random.randint(15, 60)
            b = random.randint(5, 40)
            ans = a - b
            if ans < 0:
                return gen_q(level)

    else:  # 困难
        if opt == "+":
            a = random.randint(30, 70)
            b = random.randint(20, 60)
            ans = a + b
            if ans > 100:
                return gen_q(level)
        else:
            a = random.randint(50, 99)
            b = random.randint(10, 50)
            ans = a - b

    return {
        "a": a,
        "b": b,
        "opt": opt,
        "ans": ans,
        "type": get_qtype(a, b, opt)
    }

def gen10(level):
    return [gen_q(level) for _ in range(10)]

# -------------------------- 错题移除 --------------------------
def remove_from_errors(q_remove):
    new_err = []
    for q in st.session_state.error_list:
        if not (q["a"] == q_remove["a"] and q["b"] == q_remove["b"] and q["opt"] == q_remove["opt"]):
            new_err.append(q)
    st.session_state.error_list = new_err

# -------------------------- AI诊断 --------------------------
def ai_diagnose():
    err = st.session_state.error_list
    if len(err) == 0:
        return "✅ 暂无错题，太棒啦！"
    cnt = {"normal_add": 0, "carry_add": 0, "normal_sub": 0, "carry_sub": 0}
    for q in err:
        cnt[q["type"]] += 1
    total_err = len(err)
    type_name = {
        "normal_add": "不进位加法",
        "carry_add": "进位加法",
        "normal_sub": "不退位减法",
        "carry_sub": "退位减法"
    }
    advise = {
        "normal_add": "基础简单，注意看清数字即可",
        "carry_add": "个位满十要进1，重点练进位规则",
        "normal_sub": "直接相减，注意不要写反数字",
        "carry_sub": "个位不够减要借1，十位记得减1"
    }
    max_type = max(cnt, key=cnt.get)
    max_num = cnt[max_type]
    rate = int(max_num / total_err * 100)
    if rate >= 60:
        reason = f"你**最薄弱**的是【{type_name[max_type]}】，占总错题{rate}%"
    elif rate >= 30:
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
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.student_name = st.text_input(
            "姓名", value=st.session_state.student_name,
            label_visibility="collapsed", placeholder="姓名"
        )
    with col2:
        st.session_state.student_class = st.text_input(
            "班级", value=st.session_state.student_class,
            label_visibility="collapsed", placeholder="班级"
        )

    # 难度选择（稳定高亮）
    cols = st.columns(3)
    difficulty_list = ["基础", "进阶", "困难"]
    for i, diff in enumerate(difficulty_list):
        with cols[i]:
            btn_color = "primary" if st.session_state.difficulty == diff else "secondary"
            if st.button(diff, key=f"d_{diff}", type=btn_color, use_container_width=True):
                st.session_state.difficulty = diff

    # 一键出题
    if st.button("📝 一键出10道题", use_container_width=True, type="primary"):
        st.session_state.questions = gen10(st.session_state.difficulty)
        st.session_state.current_idx = 0
        st.session_state.user_ans = ""
        st.session_state.checked = False
        st.session_state.is_review_mode = False

    # AI诊断
    st.markdown(f'<div class="diagnose-box">AI智能诊断：{ai_diagnose()}</div>', unsafe_allow_html=True)

    # 题目列表 + 答题
    if st.session_state.questions:
        st.markdown('<div class="question-list-card"><div style="font-weight:bold;">本次10道题：</div></div>', unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.questions):
            active_cls = "active" if i == st.session_state.current_idx else ""
            st.markdown(f'<div class="question-item {active_cls}">{i+1}. {q["a"]}{q["opt"]}{q["b"]}=?</div>', unsafe_allow_html=True)

        qnow = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f'<div class="answer-area-card"><div class="current-question-text">{qnow["a"]}{qnow["opt"]}{qnow["b"]}=?</div></div>', unsafe_allow_html=True)

        st.session_state.user_ans = st.text_input(
            "答案", value=st.session_state.user_ans,
            label_visibility="collapsed", placeholder="得数", key="ans_input"
        )

        # 按钮组
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ 核对", use_container_width=True):
                st.session_state.checked = True
                st.session_state.total += 1
                try:
                    u = int(st.session_state.user_ans)
                    if u == qnow["ans"]:
                        st.session_state.right += 1
                        st.success("🎉 回答正确！")
                        if st.session_state.is_review_mode:
                            remove_from_errors(qnow)
                            st.info("✅ 此题已从错题库移除")
                    else:
                        st.error(f"❌ 正确答案：{qnow['ans']}")
                        if not st.session_state.is_review_mode:
                            exist = any(
                                x["a"] == qnow["a"] and x["b"] == qnow["b"] and x["opt"] == qnow["opt"]
                                for x in st.session_state.error_list
                            )
                            if not exist:
                                st.session_state.error_list.append(qnow)
                except:
                    st.warning("⚠️ 请输入数字！")

        with c2:
            if st.button("➡️ 下一题", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_idx += 1
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                else:
                    st.info("✅ 已完成所有题目！")

        with c3:
            if st.button("📚 错题重做", use_container_width=True):
                if len(st.session_state.error_list) > 0:
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    st.session_state.user_ans = ""
                    st.session_state.checked = False
                    st.session_state.is_review_mode = True
                else:
                    st.info("暂无错题可重做~")

    # 安全重置（不崩溃）
    if st.button("🔄 重置数据", use_container_width=True):
        for key in default_state:
            st.session_state[key] = default_state[key]

    # 统计
    acc = round(st.session_state.right / st.session_state.total * 100) if st.session_state.total > 0 else 0
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
            msg = "🏆 满分学霸！口算天才！"
        elif acc >= 90:
            msg = "🌟 太厉害！口算小能手！"
        elif acc >= 80:
            msg = "👏 优秀！再细心就完美！"
        elif acc >= 60:
            msg = "👍 很棒！继续加油！"
        else:
            msg = "💪 别灰心，多练必进步！"
        st.markdown(f'<div class="encourage">{msg}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
