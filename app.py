import streamlit as st
import random

# -------------------------- 页面配置 --------------------------
st.set_page_config(page_title="AI口算错题本", layout="centered")

# -------------------------- 初始化状态 --------------------------
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_class' not in st.session_state:
    st.session_state.student_class = ""
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "基础"
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q_idx' not in st.session_state:
    st.session_state.current_q_idx = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'wrong_questions' not in st.session_state:
    st.session_state.wrong_questions = []
if 'mode' not in st.session_state:
    st.session_state.mode = "练习"  # 练习/错题重做

# -------------------------- 生成口算题 --------------------------
def generate_question(difficulty):
    if difficulty == "基础":
        max_num = 10
    elif difficulty == "进阶":
        max_num = 20
    else:
        max_num = 100
    
    op_type = random.choice(["加法", "减法"])
    a = random.randint(1, max_num)
    b = random.randint(1, max_num)
    
    if op_type == "加法":
        ans = a + b
        if difficulty == "基础":
            q_type = "不进位加法" if a % 10 + b % 10 < 10 else "进位加法"
        else:
            q_type = "加法"
        return f"{a} + {b} = ?", ans, q_type
    else:
        if a < b:
            a, b = b, a
        ans = a - b
        if difficulty == "基础":
            q_type = "不退位减法" if a % 10 >= b % 10 else "退位减法"
        else:
            q_type = "减法"
        return f"{a} - {b} = ?", ans, q_type

# -------------------------- 重置数据 --------------------------
def reset_data():
    st.session_state.questions = []
    st.session_state.current_q_idx = 0
    st.session_state.answers = []
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.wrong_questions = []
    st.session_state.mode = "练习"

# -------------------------- 主界面 --------------------------
st.title("📚 AI口算错题本")

# 基础信息输入（已禁用自动填充）
col1, col2 = st.columns(2)
with col1:
    st.session_state.student_name = st.text_input(
        "姓名", 
        value=st.session_state.student_name,
        autocomplete="off"
    )
with col2:
    st.session_state.student_class = st.text_input(
        "班级", 
        value=st.session_state.student_class,
        autocomplete="off"
    )

# 难度选择
difficulty = st.selectbox(
    "难度", 
    ["基础", "进阶", "困难"], 
    index=["基础", "进阶", "困难"].index(st.session_state.difficulty)
)
st.session_state.difficulty = difficulty

# 一键出题按钮
if st.button("一键出10道题", use_container_width=True):
    reset_data()
    st.session_state.mode = "练习"
    for _ in range(10):
        q, ans, q_type = generate_question(difficulty)
        st.session_state.questions.append({
            "question": q,
            "answer": ans,
            "type": q_type
        })

# 错题重做按钮
if st.button("错题重做", use_container_width=True):
    if st.session_state.wrong_questions:
        st.session_state.mode = "错题重做"
        st.session_state.questions = st.session_state.wrong_questions.copy()
        st.session_state.current_q_idx = 0
        st.session_state.answers = []
    else:
        st.info("还没有错题，快去练习吧！")

# 答题区
if st.session_state.questions:
    q_idx = st.session_state.current_q_idx
    if q_idx < len(st.session_state.questions):
        q = st.session_state.questions[q_idx]
        st.subheader(f"第 {q_idx + 1}/{len(st.session_state.questions)} 题")
        st.markdown(f"### {q['question']}")
        
        # 用text_input代替number_input，同时禁用自动填充
        user_ans_str = st.text_input(
            "你的答案", 
            key=f"ans_{q_idx}",
            autocomplete="off"
        )
        user_ans = None
        if user_ans_str.strip().isdigit():
            user_ans = int(user_ans_str)
        
        if st.button("提交答案", use_container_width=True):
            if user_ans is not None:
                st.session_state.total_count += 1
                st.session_state.answers.append(user_ans)
                if user_ans == q["answer"]:
                    st.success("✅ 回答正确！太棒了！")
                    st.session_state.correct_count += 1
                    if st.session_state.mode == "错题重做":
                        if q in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.remove(q)
                else:
                    st.error(f"❌ 回答错误，正确答案是：{q['answer']}")
                    if q not in st.session_state.wrong_questions:
                        st.session_state.wrong_questions.append(q)
                st.session_state.current_q_idx += 1
                st.rerun()
            else:
                st.warning("请输入有效的数字答案哦！")
    else:
        # 练习结束，显示结果
        st.balloons()
        st.subheader("🎉 练习完成！")
        accuracy = (st.session_state.correct_count / st.session_state.total_count) * 100 if st.session_state.total_count > 0 else 0
        st.write(f"✅ 做对题数：{st.session_state.correct_count}")
        st.write(f"❌ 做错题数：{st.session_state.total_count - st.session_state.correct_count}")
        st.write(f"📊 正确率：{accuracy:.1f}%")
        
        # 鼓励语
        if accuracy >= 90:
            st.success("🌟 太厉害了！你是口算小天才！")
        elif accuracy >= 70:
            st.info("👍 表现不错！再练习一下错题就更棒了！")
        else:
            st.warning("💪 别灰心，错题多练几次就会啦！")
        
        # 薄弱点分析
        if st.session_state.wrong_questions:
            st.subheader("🔍 AI薄弱点诊断")
            type_counts = {}
            for wrong_q in st.session_state.wrong_questions:
                q_type = wrong_q["type"]
                type_counts[q_type] = type_counts.get(q_type, 0) + 1
            max_type = max(type_counts, key=type_counts.get)
            st.write(f"你最薄弱的题型是：**{max_type}**，建议多练习这类题目哦！")

# 重置所有数据
if st.button("重置数据", use_container_width=True):
    reset_data()
    st.rerun()
