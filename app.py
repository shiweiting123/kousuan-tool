import streamlit as st
import random
from datetime import datetime

# -------------------------- 页面配置与样式 --------------------------
st.set_page_config(
    page_title="AI口算错题本", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 优化的CSS样式
st.markdown("""
<style>
/* 全局背景动画效果 */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 1rem;
    position: relative;
    overflow-x: hidden;
}

/* 装饰性背景元素 */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,165.3C1248,149,1344,107,1392,85.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
    background-size: cover;
    pointer-events: none;
    z-index: 0;
}

/* 主卡片 - 毛玻璃效果 */
.main-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 32px;
    padding: 32px;
    max-width: 650px;
    margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.3);
    position: relative;
    z-index: 1;
    animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 标题样式 */
.title {
    text-align: center;
    font-size: 32px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

/* 输入框美化 */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 2px solid #e0e7ff;
    padding: 10px;
    font-size: 16px;
    transition: all 0.3s ease;
    text-align: center;
    background: white;
}

.stTextInput>div>div>input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    transform: scale(1.02);
}

/* 难度按钮容器 */
.difficulty-container {
    display: flex;
    gap: 12px;
    margin: 20px 0;
}

/* 难度按钮基础样式 */
.difficulty-btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    color: #4b5563;
}

/* 不同难度按钮的特殊样式 */
.difficulty-btn[data-difficulty="基础"]:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
}

.difficulty-btn[data-difficulty="进阶"]:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
}

.difficulty-btn[data-difficulty="困难"]:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
}

/* 激活的难度按钮 */
.difficulty-btn.active {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.difficulty-btn.active[data-difficulty="基础"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
}

.difficulty-btn.active[data-difficulty="进阶"] {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
}

.difficulty-btn.active[data-difficulty="困难"] {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
}

/* 题目列表卡片 */
.question-list-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
    border: 2px solid #fbbf24;
}

.question-list-title {
    font-weight: bold;
    font-size: 18px;
    color: #92400e;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 题目项 */
.question-item {
    font-size: 16px;
    color: #78350f;
    padding: 10px;
    margin: 6px 0;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.6);
    transition: all 0.3s ease;
    cursor: pointer;
}

.question-item:hover {
    transform: translateX(5px);
    background: rgba(255, 255, 255, 0.9);
}

.question-item.active {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: white;
    font-weight: bold;
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

/* 作答区域 */
.answer-area-card {
    background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
    border-radius: 24px;
    padding: 30px;
    text-align: center;
    margin: 20px 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    50% {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
}

.current-question-text {
    font-size: 56px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold;
    margin-bottom: 20px;
}

/* 诊断框 */
.diagnose-box {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    color: #92400e;
    margin: 20px 0;
    border-left: 4px solid #f59e0b;
    font-size: 14px;
    line-height: 1.6;
}

/* 统计行 */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
    padding: 16px;
    border-radius: 16px;
    margin: 20px 0;
}

.stat-item {
    text-align: center;
    padding: 10px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stat-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #7c3aed;
}

.stat-label {
    font-size: 12px;
    color: #6b21a5;
    margin-top: 4px;
}

/* 鼓励语 */
.encourage {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    padding: 16px;
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-radius: 16px;
    color: #065f46;
    margin-top: 20px;
    animation: bounce 1s ease;
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* 按钮通用样式 */
.stButton > button {
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
    border: none;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 成功/错误消息美化 */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
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
if "is_review_mode" not in st.session_state:
    st.session_state.is_review_mode = False
if "show_answer_feedback" not in st.session_state:
    st.session_state.show_answer_feedback = False
if "answer_message" not in st.session_state:
    st.session_state.answer_message = ""

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

def gen10(level): 
    return [gen_q(level) for _ in range(10)]

# -------------------------- 错题重做删除（自动移除做对的题）--------------------------
def remove_from_errors(q_remove):
    """从错题库中移除指定的题目"""
    new_err = []
    for q in st.session_state.error_list:
        if not (q["a"]==q_remove["a"] and q["b"]==q_remove["b"] and q["opt"]==q_remove["opt"]):
            new_err.append(q)
    st.session_state.error_list = new_err

# -------------------------- AI诊断 --------------------------
def ai_diagnose():
    err = st.session_state.error_list
    if len(err)==0: 
        return "✅ 暂无错题，太棒啦！继续保持！"

    cnt = {"normal_add":0,"carry_add":0,"normal_sub":0,"carry_sub":0}
    for q in err: 
        cnt[q["type"]] +=1
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
        reason = f"🔴 你**最薄弱**的是【{type_name[max_type]}】，占总错题{rate}%"
    elif rate >=30:
        reason = f"🟡 你主要错在【{type_name[max_type]}】，需要加强练习"
    else:
        reason = f"🟢 你错得比较平均，重点加强【{type_name[max_type]}】"

    suggestion = f"💡 建议：{advise[max_type]}"
    return f"{reason}\n{suggestion}"

# -------------------------- 清空答案函数 --------------------------
def clear_answer():
    """清空答案输入框"""
    st.session_state.user_ans = ""
    st.session_state.checked = False

# -------------------------- 界面 --------------------------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # 标题区域
    st.markdown("""
    <div class="title">
        🧮 AI智能口算错题本
        <span style="font-size: 24px;">✨</span>
    </div>
    """, unsafe_allow_html=True)

    # 姓名班级输入
    col1,col2 = st.columns(2)
    with col1:
        st.session_state.student_name = st.text_input(
            "👤 姓名", 
            value=st.session_state.student_name, 
            placeholder="请输入姓名",
            key="name_input"
        )
    with col2:
        st.session_state.student_class = st.text_input(
            "📚 班级", 
            value=st.session_state.student_class, 
            placeholder="请输入班级",
            key="class_input"
        )

    # 难度选择（使用HTML/CSS实现鼠标悬停和点击变色）
    st.markdown('<div class="difficulty-container">', unsafe_allow_html=True)
    cols = st.columns(3)
    difficulty_list = ["基础", "进阶", "困难"]
    
    # 为每个难度创建按钮并添加自定义样式
    for i, diff in enumerate(difficulty_list):
        with cols[i]:
            # 使用自定义HTML按钮来实现更好的交互效果
            is_active = st.session_state.difficulty == diff
            button_style = "active" if is_active else ""
            if st.button(
                diff, 
                key=f"difficulty_{diff}",
                use_container_width=True,
                help=f"选择{diff}难度"
            ):
                st.session_state.difficulty = diff
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 添加JavaScript来实现按钮悬停和激活效果
    st.markdown("""
    <script>
    // 为难度按钮添加悬停效果
    const buttons = document.querySelectorAll('.stButton button');
    buttons.forEach(btn => {
        if (['基础', '进阶', '困难'].includes(btn.innerText)) {
            btn.classList.add('difficulty-btn');
            btn.setAttribute('data-difficulty', btn.innerText);
            if (btn.innerText === '""" + st.session_state.difficulty + """') {
                btn.classList.add('active');
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)

    # 一键出题按钮
    if st.button("🎲 一键出10道题", use_container_width=True, type="primary"):
        st.session_state.questions = gen10(st.session_state.difficulty)
        st.session_state.current_idx = 0
        clear_answer()
        st.session_state.checked = False
        st.session_state.is_review_mode = False
        st.session_state.show_answer_feedback = False
        st.rerun()

    # AI诊断区域
    st.markdown(f'<div class="diagnose-box">🤖 AI智能诊断：<br>{ai_diagnose()}</div>', unsafe_allow_html=True)

    # 题目列表和作答区域
    if st.session_state.questions:
        # 题目列表
        st.markdown("""
        <div class="question-list-card">
            <div class="question-list-title">
                📋 题目列表
                <span style="font-size: 12px;">(点击题目可跳转)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示题目列表，添加点击跳转功能
        cols_per_row = 2
        for i in range(0, len(st.session_state.questions), cols_per_row):
            row_cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx < len(st.session_state.questions):
                    q = st.session_state.questions[idx]
                    with row_cols[j]:
                        is_active = idx == st.session_state.current_idx
                        if st.button(
                            f"{idx+1}. {q['a']}{q['opt']}{q['b']}=?", 
                            key=f"q_{idx}",
                            use_container_width=True,
                            help="点击跳转到此题"
                        ):
                            st.session_state.current_idx = idx
                            clear_answer()
                            st.session_state.checked = False
                            st.rerun()

        # 当前题目
        qnow = st.session_state.questions[st.session_state.current_idx]
        st.markdown(f"""
        <div class="answer-area-card">
            <div class="current-question-text">
                {qnow["a"]}{qnow["opt"]}{qnow["b"]} = ?
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 答案输入
        st.session_state.user_ans = st.text_input(
            "✏️ 输入答案", 
            value=st.session_state.user_ans, 
            placeholder="请输入得数",
            key="ans_input"
        )

        # 按钮区域
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ 核对答案", use_container_width=True):
                st.session_state.checked = True
                st.session_state.total += 1
                try:
                    user_input = int(st.session_state.user_ans)
                    if user_input == qnow["ans"]:
                        st.session_state.right += 1
                        st.success(f"🎉 回答正确！ {qnow['a']}{qnow['opt']}{qnow['b']}={qnow['ans']}")
                        
                        # 如果是错题重做模式，自动从错题库移除
                        if st.session_state.is_review_mode:
                            remove_from_errors(qnow)
                            st.info("✅ 此题已从错题库中移除！")
                        
                        # 自动清空答案
                        clear_answer()
                    else:
                        st.error(f"❌ 回答错误！ 正确答案是：{qnow['ans']}")
                        
                        # 添加到错题库（仅在非重做模式下）
                        if not st.session_state.is_review_mode:
                            # 检查是否已存在
                            exist = any(
                                x["a"] == qnow["a"] and 
                                x["b"] == qnow["b"] and 
                                x["opt"] == qnow["opt"] 
                                for x in st.session_state.error_list
                            )
                            if not exist:
                                st.session_state.error_list.append(qnow)
                                st.warning("📝 此题已加入错题库")
                        
                        # 保留答案，不清空，方便用户对比
                except ValueError:
                    st.warning("⚠️ 请输入数字答案！")
        
        with col2:
            if st.button("➡️ 下一题", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_idx += 1
                    clear_answer()
                    st.session_state.checked = False
                    st.rerun()
                else:
                    st.balloons()
                    st.success("🎉 恭喜你完成了所有题目！")
        
        with col3:
            if st.button("📚 错题重做", use_container_width=True):
                if len(st.session_state.error_list) > 0:
                    st.session_state.questions = st.session_state.error_list.copy()
                    st.session_state.current_idx = 0
                    clear_answer()
                    st.session_state.checked = False
                    st.session_state.is_review_mode = True
                    st.info(f"📖 进入错题重做模式，共 {len(st.session_state.error_list)} 道错题")
                    st.rerun()
                else:
                    st.info("✨ 太棒了！暂无错题需要重做~")

    # 重置数据按钮
    if st.button("🔄 重置所有数据", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.success("数据已重置！")
        st.rerun()

    # 统计信息
    acc = round(st.session_state.right / st.session_state.total * 100) if st.session_state.total > 0 else 0
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">
            <div class="stat-value">{st.session_state.total}</div>
            <div class="stat-label">总题数</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{st.session_state.right}</div>
            <div class="stat-label">做对</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{len(st.session_state.error_list)}</div>
            <div class="stat-label">错题本</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{acc}%</div>
            <div class="stat-label">正确率</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 鼓励语（根据正确率动态显示）
    if st.session_state.total > 0:
        if acc == 100:
            msg = "🏆 口算天才！完美通关！太厉害了！"
            emoji = "🌟"
        elif acc >= 90:
            msg = "🎉 太优秀了！继续努力，冲击满分！"
            emoji = "💪"
        elif acc >= 80:
            msg = "👍 很不错！再细心一点就更完美了！"
            emoji = "✨"
        elif acc >= 60:
            msg = "📚 继续加油！多练习会越来越棒！"
            emoji = "🌱"
        else:
            msg = "💪 别灰心！错题是我们的朋友，再练习一次吧！"
            emoji = "🌸"
        
        st.markdown(f'<div class="encourage">{emoji} {msg} {emoji}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
