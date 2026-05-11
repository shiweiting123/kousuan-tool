import streamlit as st
import random
import json
from datetime import datetime

# 页面设置
st.set_page_config(page_title="AI口算错题本", layout="centered")

# 样式
st.markdown("""
<style>
.main {
    background: linear-gradient(145deg, #f9f0d4 0%, #f4e5c1 100%);
    padding: 1rem;
    border-radius: 24px;
}
.q-text {
    font-size: 2.8rem;
    text-align: center;
    color: #8b3c1c;
    font-weight: bold;
    margin: 1rem 0;
}
.feedback {
    padding: 0.8rem;
    border-radius: 16px;
    text-align: center;
    font-weight: bold;
}
.correct {
    background: #e2f3e2;
    color: #1f6d2b;
}
.wrong {
    background: #ffe6e6;
    color: #b13e3e;
}
.weak-tag {
    background: #e86c3a;
    color: white;
    padding: 4px 10px;
    border-radius: 12px;
    margin: 3px;
    display: inline-block;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# 初始化状态
if "total" not in st.session_state:
    st.session_state.total = 0
if "right" not in st.session_state:
    st.session_state.right = 0
if "error_list" not in st.session_state:
    st.session_state.error_list = []
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_ans" not in st.session_state:
    st.session_state.user_ans = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = "💡 认真计算，细心答题"
if "feedback_cls" not in st.session_state:
    st.session_state.feedback_cls = "feedback"

# 题型分类
def get_kind(a, b, opt):
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

kind_map = {
    "normal_add": {"text": "不进位加法", "color": "#e65100"},
    "carry_add": {"text": "进位加法", "color": "#d83a34"},
    "normal_sub": {"text": "不退位减法", "color": "#0a79a2"},
    "carry_sub": {"text": "退位减法", "color": "#7e4bb2"}
}

# 出题
def gen_q(level="基础"):
    a, b, opt, ans = 0, 0, "+", 0
    if level == "基础":
        opt = "+" if random.random() > 0.5 else "-"
        if opt == "+":
            while True:
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                ans = a + b
                if ans <= 20:
                    break
        else:
            while True:
                a = random.randint(5, 15)
                b = random.randint(1, 10)
                ans = a - b
                if ans >= 0:
                    break
    elif level == "进阶":
        opt = "+" if random.random() > 0.5 else "-"
        if opt == "+":
            a = random.randint(10, 35)
            b = random.randint(5, 30)
            ans = a + b
        else:
            a = random.randint(15, 50)
            b = random.randint(5, 30)
            ans = a - b
        if ans < 0:
            return gen_q("进阶")
    else:
        opt = "+" if random.random() > 0.5 else "-"
        if opt == "+":
            while True:
                a = random.randint(30, 70)
                b = random.randint(20, 60)
                ans = a + b
                if ans <= 100:
                    break
        else:
            while True:
                a = random.randint(50, 99)
                b = random.randint(10, 49)
                ans = a - b
                if ans >= 0:
                    break
    kind = get_kind(a, b, opt)
    return {"a": a, "b": b, "opt": opt, "ans": ans, "kind": kind}

# 诊断
def diagnose():
    errs = st.session_state.error_list
    if not errs:
        return "暂无错题，太棒啦！", ""
    cnt = {"normal_add":0, "carry_add":0, "normal_sub":0, "carry_sub":0}
    for q in errs:
        cnt[q["kind"]] += 1
    tags = ""
    for k in cnt:
        if cnt[k] > 0:
            tags += f'<span class="weak-tag" style="background:{kind_map[k]["color"]}">{kind_map[k]["text"]} 错{cnt[k]}道</span>'
    return f"共{len(errs)}道错题", tags

# 界面
st.title("📚 AI口算错题本")

# 难度
level = st.radio("难度", ["基础", "进阶", "困难"], horizontal=True)

# 诊断
tip, tags = diagnose()
st.markdown(f"""
<div style="background:#fef5e6; padding:12px; border-radius:16px;">
    <div>AI薄弱诊断：{tip}</div>
    <div>{tags}</div>
</div>
""", unsafe_allow_html=True)

# 生成题目
if st.button("📝 开始出题"):
    st.session_state.current_q = gen_q(level)
    st.session_state.answered = False
    st.session_state.user_ans = ""
    st.session_state.feedback = "💡 请输入答案"
    st.session_state.feedback_cls = "feedback"

# 显示题目
if st.session_state.current_q:
    q = st.session_state.current_q
    st.markdown(f'<div class="q-text">{q["a"]} {q["opt"]} {q["b"]} = ?</div>', unsafe_allow_html=True)
    ans = st.text_input("答案", value=st.session_state.user_ans, key="ans_input")

    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.answered and st.button("✅ 核对"):
            st.session_state.answered = True
            st.session_state.total += 1
            try:
                u = int(ans)
            except:
                st.session_state.feedback = "⚠️ 请输入数字"
                st.session_state.feedback_cls = "feedback wrong"
                st.rerun()
            if u == q["ans"]:
                st.session_state.right += 1
                st.session_state.feedback = "🎉 回答正确！"
                st.session_state.feedback_cls = "feedback correct"
            else:
                st.session_state.feedback = f"❌ 正确答案：{q['ans']}"
                st.session_state.feedback_cls = "feedback wrong"
                exist = any(x["a"]==q["a"] and x["b"]==q["b"] and x["opt"]==q["opt"] for x in st.session_state.error_list)
                if not exist:
                    st.session_state.error_list.append(q)
    with col2:
        if st.session_state.answered and st.button("➡️ 下一题"):
            st.session_state.current_q = gen_q(level)
            st.session_state.answered = False
            st.session_state.user_ans = ""
            st.session_state.feedback = "💡 请输入答案"
            st.session_state.feedback_cls = "feedback"
            st.rerun()

# 反馈
st.markdown(f'<div class="{st.session_state.feedback_cls}">{st.session_state.feedback}</div>', unsafe_allow_html=True)

# 统计
acc = round(st.session_state.right/st.session_state.total*100) if st.session_state.total>0 else 0
st.markdown(f"""
<div style="background:#f0e2ca; padding:12px; border-radius:16px; text-align:center;">
总题：{st.session_state.total} | 做对：{st.session_state.right} | 错题：{len(st.session_state.error_list)} | 正确率：{acc}%
</div>
""", unsafe_allow_html=True)

# 重置
if st.button("🔄 重置所有数据"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
