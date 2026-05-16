import streamlit as st
import random

# -------------------------- 页面配置 --------------------------
st.set_page_config(page_title="AI口算错题本", layout="centered")

# -------------------------- 样式（彻底修复布局） --------------------------
st.markdown("""
<style>
.main-box {
    max-width: 520px;
    margin: 30px auto;
    background: #ffffff;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}
.title {
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
}
.sub-title {
    font-size: 14px;
    color: #7f8c8d;
    text-align: center;
    margin-bottom: 25px;
}
.stButton>button {
    border-radius: 12px;
    height: 46px;
    font-weight: bold;
    transition: 0.2s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
/* 题目卡片 */
.question-card {
    background: #eef5ff;
    border-radius: 16px;
    padding: 30px 20px;
    text-align: center;
    margin: 20px 0;
}
.question-text {
    font-size: 42px;
    font-weight: bold;
    color: #2b7bff;
}
/* 输入框 */
.stTextInput input {
    border-radius: 12px;
    height: 48px;
    font-size: 18px;
    text-align: center;
}
/* 横向题目列表（真·横排） */
.question-horizontal {
    display: flex;
    gap: 6px;
    margin: 10px 0;
    flex-wrap: wrap;
}
.q-num {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
}
.q-num.active {
    background: #2b7bff;
    color: white;
}
/* 提示框（固定位置，不乱跑） */
.message-box {
    padding: 10px 14px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    margin: 10px 0;
}
.success { background: #e6f7ef; color: #065f46; }
.error { background: #fef2f2; color: #b91c1c; }
.tip { background: #fffbeb; color: #92400e; }
/* 统计 */
.stats {
    display: flex;
    justify-content: space-between;
    background: #f8f9fd;
    border-radius: 14px;
    padding: 16px;
    margin-top: 20px;
}
.stat-item {
    text-align: center;
    flex: 1;
}
.stat-num {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
}
.stat-label {
    font-size: 12px;
    color: #7f8c8d;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- 状态初始化 --------------------------
defaults = {
    "difficulty":"基础",
    "questions":[],
    "current_idx":0,
    "user_ans":"",
    "error_list":[],
    "total":0,
    "right":0,
    "is_review":False,
    "msg":"",
    "msg_type":"tip",
    "has_checked":False  # 控制下一题按钮
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------- 出题 --------------------------
def get_qtype(a,b,opt):
    if opt == "+":
        return "carry_add" if (a%10 + b%10)>=10 else "normal_add"
    else:
        return "carry_sub" if (a%10 < b%10) else "normal_sub"

def gen_q(level):
    opt = random.choice(["+", "-"])
    a,b,ans = 0,0,0
    if level == "基础":
        if opt == "+":
            a,b = random.randint(1,10), random.randint(1,10)
            ans = a+b
        else:
            a,b = random.randint(5,15), random.randint(1,10)
            ans = a-b
    elif level == "进阶":
        a = random.randint(10,60)
        b = random.randint(5,40)
        ans = a+b if opt == "+" else a-b
        if ans < 0: return gen_q(level)
    else:
        if opt == "+":
            a,b = random.randint(30,70), random.randint(20,60)
            ans = a+b
            if ans>100: return gen_q(level)
        else:
            a,b = random.randint(50,99), random.randint(10,50)
            ans = a-b
    return {"a":a,"b":b,"opt":opt,"ans":ans,"type":get_qtype(a,b,opt)}

def gen10(level):
    return [gen_q(level) for _ in range(10)]

# -------------------------- 错题删除 --------------------------
def remove_error(q):
    new_err = []
    for e in st.session_state.error_list:
        if not (e["a"]==q["a"] and e["b"]==q["b"] and e["opt"]==q["opt"]):
            new_err.append(e)
    st.session_state.error_list = new_err

# -------------------------- 界面 --------------------------
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">🧮 AI口算错题本</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">100以内加减法｜三级难度｜智能错题本</div>', unsafe_allow_html=True)

    # 难度
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("基础", use_container_width=True, type="primary" if st.session_state.difficulty=="基础" else "secondary"):
            st.session_state.difficulty = "基础"
    with c2:
        if st.button("进阶", use_container_width=True, type="primary" if st.session_state.difficulty=="进阶" else "secondary"):
            st.session_state.difficulty = "进阶"
    with c3:
        if st.button("困难", use_container_width=True, type="primary" if st.session_state.difficulty=="困难" else "secondary"):
            st.session_state.difficulty = "困难"

    # 生成题目
    if st.button("📝 生成10道题", use_container_width=True):
        st.session_state.questions = gen10(st.session_state.difficulty)
        st.session_state.current_idx = 0
        st.session_state.user_ans = ""
        st.session_state.is_review = False
        st.session_state.has_checked = False
        st.session_state.msg = "题目已生成！"
        st.session_state.msg_type = "tip"

    # ====================== 题目列表（真·横排） ======================
    if st.session_state.questions:
        st.markdown('<div style="font-weight: bold; margin-bottom:6px;">📋 题目列表</div>', unsafe_allow_html=True)
        st.markdown('<div class="question-horizontal">', unsafe_allow_html=True)
        for i in range(len(st.session_state.questions)):
            active = "active" if i == st.session_state.current_idx else ""
            st.markdown(f'<div class="q-num {active}">{i+1}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 题目
        qnow = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f'''
        <div class="question-card">
            <div class="question-text">{qnow["a"]} {qnow["opt"]} {qnow["b"]} = ?</div>
        </div>
        ''', unsafe_allow_html=True)

        # 答案
        st.session_state.user_ans = st.text_input("答案", value=st.session_state.user_ans, placeholder="请输入得数", label_visibility="collapsed")

        # 按钮组
        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            if st.button("✅ 核对", use_container_width=True):
                st.session_state.total += 1
                try:
                    u = int(st.session_state.user_ans)
                    if u == qnow["ans"]:
                        st.session_state.right += 1
                        st.session_state.msg = "🎉 回答正确！"
                        st.session_state.msg_type = "success"
                        if st.session_state.is_review:
                            remove_error(qnow)
                    else:
                        st.session_state.msg = f"❌ 错误，正确：{qnow['ans']}"
                        st.session_state.msg_type = "error"
                        if not st.session_state.is_review:
                            exist = any(x["a"]==qnow["a"] and x["b"]==qnow["b"] and x["opt"]==qnow["opt"] for x in st.session_state.error_list)
                            if not exist:
                                st.session_state.error_list.append(qnow)
                    st.session_state.has_checked = True
                except:
                    st.session_state.msg = "⚠️ 请输入数字！"
                    st.session_state.msg_type = "tip"

        # ====================== 下一题按钮：必须核对后才能点 ======================
        with bc2:
            last_one = st.session_state.current_idx >= len(st.session_state.questions)-1
            next_disabled = not st.session_state.has_checked or last_one
            if st.button("➡️ 下一题", use_container_width=True, disabled=next_disabled):
                st.session_state.current_idx += 1
                st.session_state.user_ans = ""
                st.session_state.has_checked = False
                st.session_state.msg = ""

        with bc3:
            if st.button("📚 错题重做", use_container_width=True):
                if st.session_state.error_list:
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    st.session_state.user_ans = ""
                    st.session_state.is_review = True
                    st.session_state.has_checked = False
                    st.session_state.msg = f"错题重做（共{len(st.session_state.error_list)}题）"
                    st.session_state.msg_type = "tip"
                else:
                    st.session_state.msg = "✨ 太棒了！没有错题！"
                    st.session_state.msg_type = "success"

    # ====================== 提示框（固定在按钮下方，绝不乱跑） ======================
    if st.session_state.msg:
        cls = st.session_state.msg_type
        txt = st.session_state.msg
        st.markdown(f'<div class="message-box {cls}">{txt}</div>', unsafe_allow_html=True)

    # 统计
    acc = round(st.session_state.right/st.session_state.total*100) if st.session_state.total>0 else 0
    st.markdown(f'''
    <div class="stats">
        <div class="stat-item"><div class="stat-num">{st.session_state.total}</div><div class="stat-label">总题</div></div>
        <div class="stat-item"><div class="stat-num">{st.session_state.right}</div><div class="stat-label">做对</div></div>
        <div class="stat-item"><div class="stat-num">{len(st.session_state.error_list)}</div><div class="stat-label">错题</div></div>
        <div class="stat-item"><div class="stat-num">{acc}%</div><div class="stat-label">正确率</div></div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
