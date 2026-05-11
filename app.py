import streamlit as st
import random

# 页面设置
st.set_page_config(page_title="AI口算错题本", layout="centered")

# 样式（干净无多余框）
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff3d9 0%, #ffe9c2 100%);
    padding: 1rem;
}
.main-card {
    background: #fff9e8;
    border-radius: 24px;
    padding: 24px;
    max-width: 500px;
    margin: 0 auto;
}
.title {
    text-align: center;
    font-size: 24px;
    color: #8b3c1c;
    font-weight: bold;
    margin-bottom: 16px;
}
.q-card {
    background: #fff3d9;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}
.q-text {
    font-size: 22px;
    color: #8b3c1c;
    font-weight: bold;
    text-align: center;
}
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

# 初始化
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "基础"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "checked" not in st.session_state:
    st.session_state.checked = False
if "error_list" not in st.session_state:
    st.session_state.error_list = []
if "total" not in st.session_state:
    st.session_state.total = 0
if "right" not in st.session_state:
    st.session_state.right = 0

# 出题
def get_kind(a,b,opt):
    if opt == "+":
        return "carry_add" if (a%10 + b%10)>=10 else "normal_add"
    else:
        return "carry_sub" if (a%10 < b%10) else "normal_sub"

def gen_q(level):
    opt = "+" if random.random()>0.5 else "-"
    a=b=ans=0
    if level=="基础":
        if opt=="+":
            while True:
                a,b = random.randint(1,10),random.randint(1,10)
                if a+b<=20: break
        else:
            while True:
                a,b = random.randint(5,15),random.randint(1,10)
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
    return {"a":a,"b":b,"opt":opt,"ans":ans,"kind":get_kind(a,b,opt)}

def gen10(level):
    return [gen_q(level) for _ in range(10)]

# 界面
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="title">📚 AI口算错题本</div>', unsafe_allow_html=True)

# 姓名班级
col1,col2 = st.columns(2)
with col1: st.text_input("姓名", placeholder="姓名", label_visibility="collapsed")
with col2: st.text_input("班级", placeholder="班级", label_visibility="collapsed")

# 难度
dif = st.radio("难度",["基础","进阶","困难"],horizontal=True,label_visibility="collapsed")
st.session_state.difficulty = dif

# 一键出10题
if st.button("📝 一键出10道题",use_container_width=True):
    st.session_state.questions = gen10(dif)
    st.session_state.user_answers = {i:"" for i in range(10)}
    st.session_state.checked = False

# 显示全部10题
if st.session_state.questions:
    for i,q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><div class="q-text">第{i+1}题：{q["a"]}{q["opt"]}{q["b"]}=?</div></div>',unsafe_allow_html=True)
        st.session_state.user_answers[i] = st.text_input("答案",key=f"a{i}",label_visibility="collapsed",placeholder="得数",disabled=st.session_state.checked)

    # 核对
    if not st.session_state.checked and st.button("✅ 核对全部答案",use_container_width=True):
        st.session_state.checked=True
        right=0
        for i,q in enumerate(st.session_state.questions):
            try:
                u=int(st.session_state.user_answers[i])
                if u==q["ans"]: right+=1
                else: st.session_state.error_list.append(q)
            except: pass
        st.session_state.total +=10
        st.session_state.right +=right

# 统计
acc = round(st.session_state.right/st.session_state.total*100) if st.session_state.total>0 else 0
st.markdown(f"""
<div class="stats-row">
    <div class="stat-item">总题 {st.session_state.total}</div>
    <div class="stat-item">做对 {st.session_state.right}</div>
    <div class="stat-item">错题 {len(st.session_state.error_list)}</div>
    <div class="stat-item">正确率 {acc}%</div>
</div>
""",unsafe_allow_html=True)

# —————— 鼓励话语（自动根据正确率变化）——————
msg = ""
if acc == 0:
    msg = "💪 别灰心，多练习一定会进步！"
elif acc < 60:
    msg = "👍 很棒啦！继续加油，一定会更厉害！"
elif acc < 80:
    msg = "👏 表现优秀，再细心一点就完美啦！"
elif acc < 95:
    msg = "🌟 太厉害啦！你是口算小能手！"
else:
    msg = "🏆 满分学霸！你简直是口算天才！"

st.markdown(f'<div class="encourage">{msg}</div>', unsafe_allow_html=True)
# ————————————————————————————————————————

if st.button("🔄 重置数据",use_container_width=True):
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

st.markdown("</div>",unsafe_allow_html=True)
