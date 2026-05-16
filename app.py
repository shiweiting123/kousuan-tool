import streamlit as st
import random
import time
from PIL import Image, ImageDraw
import io

# -------------------------- 页面配置与样式 --------------------------
st.set_page_config(page_title="AI智趣图形王国", layout="centered")
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background: linear-gradient(180deg, #e6f7ff 0%, #f0f9ff 100%);
    padding: 1rem;
}
/* 主卡片 */
.main-card {
    background: white;
    border-radius: 24px;
    padding: 24px;
    max-width: 600px;
    margin: 0 auto;
    box-shadow: 0 8px 24px rgba(0, 100, 200, 0.1);
}
/* 标题 */
.title {
    text-align: center;
    font-size: 26px;
    color: #1e6bb8;
    font-weight: bold;
    margin-bottom: 20px;
}
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #4a7caf;
    margin-bottom: 20px;
}
/* 按钮样式 */
.stButton>button {
    border-radius: 12px;
    background-color: #1e6bb8;
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px 20px;
    width: 100%;
    margin: 5px 0;
}
.stButton>button:hover {
    background-color: #2b85d6;
}
/* 互动区域 */
.canvas-area {
    background: #f0f9ff;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    margin: 16px 0;
}
/* 反馈区域 */
.feedback-box {
    background: #e6f7ff;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    color: #1e6bb8;
    margin: 16px 0;
    line-height:1.6;
}
/* 闯关进度 */
.progress-bar {
    background: #e0efff;
    border-radius: 10px;
    padding: 8px;
    margin: 10px 0;
}
.progress-fill {
    background: #1e6bb8;
    height: 10px;
    border-radius: 5px;
}
/* 教师面板样式 */
.teacher-panel {
    background: #f5faff;
    border-radius: 16px;
    padding: 16px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- 初始化会话状态 --------------------------
if "game_state" not in st.session_state:
    st.session_state.game_state = "menu"  # menu, play, result, teacher
if "level" not in st.session_state:
    st.session_state.level = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "current_task" not in st.session_state:
    st.session_state.current_task = None
if "teacher_data" not in st.session_state:
    st.session_state.teacher_data = {
        "students": [
            {"name": "小明", "accuracy": 85, "weak_point": "不规则图形面积"},
            {"name": "小红", "accuracy": 92, "weak_point": "图形密铺"},
            {"name": "小刚", "accuracy": 78, "weak_point": "图形分类"}
        ]
    }

# -------------------------- AI核心功能模块 --------------------------
def generate_task(level):
    """根据关卡生成图形相关题目"""
    tasks = []
    if level == 1:
        # 基础图形识别
        shapes = ["正方形", "长方形", "三角形", "圆形"]
        for shape in shapes:
            tasks.append({
                "type": "identify",
                "question": f"请识别图形：这是{shape}吗？",
                "answer": shape,
                "image": draw_shape(shape)
            })
    elif level == 2:
        # 图形密铺判断
        shapes = ["三角形", "正方形", "正五边形", "平行四边形"]
        for shape in shapes:
            tasks.append({
                "type": "tessellate",
                "question": f"这个图形能单独密铺吗？",
                "answer": "能" if shape in ["三角形", "正方形", "平行四边形"] else "不能",
                "image": draw_tessellate_preview(shape)
            })
    elif level == 3:
        # 不规则图形面积拆解
        tasks.append({
            "type": "area",
            "question": "请把这个不规则图形拆成2个长方形，计算总面积（单位：厘米）",
            "answer": "20",
            "image": draw_irregular_shape()
        })
    return random.choice(tasks)

def draw_shape(shape):
    """绘制基础图形"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    if shape == "正方形":
        draw.rectangle([50,50,150,150], outline='blue', width=3)
    elif shape == "长方形":
        draw.rectangle([30,70,170,130], outline='blue', width=3)
    elif shape == "三角形":
        draw.polygon([100,30,30,170,170,170], outline='blue', width=3)
    elif shape == "圆形":
        draw.ellipse([50,50,150,150], outline='blue', width=3)
    return img

def draw_tessellate_preview(shape):
    """绘制密铺预览"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    if shape == "正方形":
        for i in range(4):
            for j in range(4):
                draw.rectangle([i*50, j*50, i*50+50, j*50+50], outline='green')
    elif shape == "三角形":
        for i in range(4):
            for j in range(4):
                draw.polygon([i*50, j*50, i*50+50, j*50, i*50+25, j*50+50], outline='green')
    elif shape == "平行四边形":
        for i in range(4):
            for j in range(4):
                draw.polygon([i*50, j*50, i*50+50, j*50, i*50+75, j*50+50, i*50+25, j*50+50], outline='green')
    elif shape == "正五边形":
        draw.polygon([100,20,170,60,145,130,55,130,30,60], outline='red')
    return img

def draw_irregular_shape():
    """绘制不规则图形（由两个长方形组成）"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    # 第一个长方形
    draw.rectangle([20,20,100,100], outline='blue', width=2)
    # 第二个长方形
    draw.rectangle([100,60,180,140], outline='blue', width=2)
    # 标注尺寸
    draw.text((60, 105), "4cm", fill='black')
    draw.text((105, 100), "5cm", fill='black')
    draw.text((60, 15), "5cm", fill='black')
    draw.text((140, 105), "4cm", fill='black')
    return img

def ai_feedback(user_answer, correct_answer, task_type):
    """AI智能反馈与讲解"""
    if task_type == "identify":
        if user_answer == correct_answer:
            return "✅ 太棒了！图形识别完全正确！正方形的四条边都相等，四个角都是直角哦~"
        else:
            return f"❌ 别灰心，再仔细看看！这个图形的特征是：{correct_answer}的边和角有什么特点呢？"
    elif task_type == "tessellate":
        if user_answer == correct_answer:
            return "✅ 正确！这个图形的内角和能被360度整除，所以可以无缝密铺！"
        else:
            return f"❌ 再想想！能密铺的图形需要满足什么条件？提示：内角和与360度的关系~"
    elif task_type == "area":
        if user_answer == correct_answer:
            return "✅ 计算正确！你成功把不规则图形拆成了两个规则图形，总面积是20平方厘米！"
        else:
            return f"❌ 差一点就对了！提示：把图形拆成两个长方形，分别计算面积再相加：(5×4)+(5×4)=20平方厘米"

def next_level():
    """升级关卡"""
    if st.session_state.level < 3:
        st.session_state.level += 1
    st.session_state.current_task = generate_task(st.session_state.level)
    st.session_state.feedback = ""

# -------------------------- 主界面 --------------------------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🎨 AI智趣图形王国</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">小学数学图形互动教学AI工具</div>', unsafe_allow_html=True)

    # 主菜单
    if st.session_state.game_state == "menu":
        st.markdown("""
        <div class="canvas-area">
            <h3>欢迎来到图形王国！</h3>
            <p>通过AI互动游戏，轻松掌握图形知识~</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 开始闯关"):
            st.session_state.game_state = "play"
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.correct_answers = 0
            st.session_state.current_task = generate_task(1)
            st.experimental_rerun()
        
        if st.button("👩‍🏫 教师后台"):
            st.session_state.game_state = "teacher"
            st.experimental_rerun()

    # 游戏界面
    elif st.session_state.game_state == "play":
        # 关卡进度
        st.markdown(f"""
        <div class="progress-bar">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>关卡 {st.session_state.level}/3</span>
                <span>得分 {st.session_state.score}</span>
            </div>
            <div class="progress-fill" style="width: {st.session_state.level/3*100}%"></div>
        </div>
        """, unsafe_allow_html=True)

        # 题目区域
        if st.session_state.current_task:
            task = st.session_state.current_task
            st.markdown(f'<div class="canvas-area"><h4>{task["question"]}</h4></div>', unsafe_allow_html=True)
            st.image(task["image"], width=200)

            # 答题输入
            if task["type"] == "identify":
                user_answer = st.selectbox("请选择答案：", ["正方形", "长方形", "三角形", "圆形"])
            elif task["type"] == "tessellate":
                user_answer = st.radio("请选择答案：", ["能", "不能"])
            elif task["type"] == "area":
                user_answer = st.number_input("请输入答案（平方厘米）：", min_value=0, step=1)

            # 提交答案
            if st.button("✅ 提交答案"):
                st.session_state.total_questions += 1
                if str(user_answer) == str(task["answer"]):
                    st.session_state.correct_answers += 1
                    st.session_state.score += 10
                st.session_state.feedback = ai_feedback(str(user_answer), str(task["answer"]), task["type"])

            # 显示反馈
            if st.session_state.feedback:
                st.markdown(f'<div class="feedback-box">{st.session_state.feedback}</div>', unsafe_allow_html=True)

            # 下一题/升级按钮
            if st.button("➡️ 下一题/升级关卡"):
                next_level()
                st.experimental_rerun()

        # 闯关结束
        if st.session_state.level > 3:
            st.session_state.game_state = "result"
            st.experimental_rerun()

    # 结果界面
    elif st.session_state.game_state == "result":
        accuracy = st.session_state.correct_answers / st.session_state.total_questions * 100 if st.session_state.total_questions > 0 else 0
        st.markdown(f"""
        <div class="canvas-area">
            <h3>🎉 闯关结束！</h3>
            <p>总题数：{st.session_state.total_questions}</p>
            <p>正确数：{st.session_state.correct_answers}</p>
            <p>正确率：{accuracy:.1f}%</p>
            <p>最终得分：{st.session_state.score}</p>
        </div>
        """, unsafe_allow_html=True)

        # AI个性化学习建议
        if accuracy < 70:
            suggestion = "建议多练习图形密铺和不规则图形面积计算，可在教师后台获取针对性练习~"
        elif accuracy < 90:
            suggestion = "基础不错！可以挑战更高难度的图形组合题，巩固薄弱环节~"
        else:
            suggestion = "太棒了！你已经是图形小能手啦，可以尝试拓展图形推理题目~"
        
        st.markdown(f'<div class="feedback-box">AI学习建议：{suggestion}</div>', unsafe_allow_html=True)

        if st.button("🔄 重新闯关"):
            st.session_state.game_state = "menu"
            st.experimental_rerun()

    # 教师后台界面
    elif st.session_state.game_state == "teacher":
        st.markdown('<div class="teacher-panel"><h3>👩‍🏫 教师学情分析后台</h3></div>', unsafe_allow_html=True)
        st.write("班级学生学情数据：")
        for student in st.session_state.teacher_data["students"]:
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background: #e6f7ff; border-radius: 8px;">
                <p><strong>{student['name']}</strong></p>
                <p>正确率：{student['accuracy']}%</p>
                <p>薄弱点：{student['weak_point']}</p>
            </div>
            """)
        
        if st.button("📄 导出学情报告"):
            st.success("学情报告已生成！可下载用于教学分析~")
        
        if st.button("🔙 返回主菜单"):
            st.session_state.game_state = "menu"
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)
