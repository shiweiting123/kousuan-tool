<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
    <title>AI口算错题本·100以内加减法</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "微软雅黑", sans-serif;
        }
        body {
            background: linear-gradient(145deg, #f9f0d4 0%, #f4e5c1 100%);
            min-height: 100vh;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: #fffef7;
            border-radius: 36px;
            box-shadow: 0 20px 40px rgba(100,70,20,0.15);
            border: 1px solid #e9d6a7;
            padding: 20px;
            text-align: center;
        }
        h1 {
            font-size: 1.4rem;
            color: #b45f2b;
            margin-bottom: 6px;
        }
        .user-info {
            background: #fef5e6;
            padding: 8px;
            border-radius: 16px;
            margin-bottom: 10px;
            font-size: 0.85rem;
            display: flex;
            gap: 6px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .user-info input {
            padding: 4px 6px;
            border: 1px solid #ebca8c;
            border-radius: 8px;
            outline: none;
            width: 100px;
            text-align: center;
        }
        .level-group {
            margin-bottom: 10px;
        }
        .level-btn {
            border: none;
            padding: 5px 10px;
            border-radius: 16px;
            margin: 0 3px;
            font-size: 0.8rem;
            background: #f0e2ca;
            color: #666;
            cursor: pointer;
        }
        .level-btn.active {
            background: #b45f2b;
            color: white;
        }
        .diagnose-card {
            background: #fef5e6;
            border-radius: 16px;
            padding: 10px;
            margin-bottom: 12px;
            font-size: 0.85rem;
            color: #8b3c1c;
        }
        .weak-tag {
            background: #e86c3a;
            color: #fff;
            padding: 3px 10px;
            border-radius: 12px;
            margin: 3px;
            display: inline-block;
            font-size: 0.75rem;
        }
        .q-card {
            background: #fef5e6;
            border-radius: 24px;
            padding: 20px 10px;
            margin: 10px 0;
        }
        .q-text {
            font-size: 2.6rem;
            color: #8b3c1c;
            font-weight: bold;
            margin: 10px 0;
        }
        #answerInput {
            width: 130px;
            font-size: 1.5rem;
            text-align: center;
            padding: 8px;
            border-radius: 16px;
            border: 2px solid #ebca8c;
            outline: none;
            margin-bottom: 10px;
        }
        button {
            border: none;
            color: #fff;
            font-size: 0.9rem;
            font-weight: bold;
            padding: 8px 14px;
            margin: 4px;
            border-radius: 20px;
            cursor: pointer;
        }
        .gen-btn { background: #2f6b47; }
        .check-btn { background: #b47c48; }
        .next-btn { background: #4e79a7; }
        .error-btn { background: #d9534f; }
        .reset-btn { background: #6c757d; }
        button:disabled {
            background: #aaa !important;
            cursor: not-allowed;
        }
        .feedback {
            border-radius: 16px;
            padding: 10px;
            margin: 10px 0;
            font-size: 0.95rem;
            font-weight: bold;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .correct-feedback { background: #e2f3e2; color: #1f6d2b; }
        .wrong-feedback { background: #ffe6e6; color: #b13e3e; }
        .score-wrap {
            background: #f0e2ca;
            border-radius: 16px;
            padding: 10px;
            margin-top: 8px;
        }
        .score-row {
            display: flex;
            justify-content: space-around;
            font-size: 0.8rem;
            flex-wrap: wrap;
            gap: 6px;
        }
        .item { display: flex; gap: 3px; align-items: center; }
        .badge {
            background: #dfc089;
            padding: 3px 6px;
            border-radius: 12px;
            font-weight: bold;
            color: #423019;
        }
        .medal {
            margin-top: 8px;
            font-size: 0.85rem;
            color: #b45f2b;
            font-weight: bold;
        }
        .info-panel {
            background: #fff8e8;
            padding: 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            text-align: left;
            line-height: 1.5;
            margin-top: 10px;
            display: none;
        }
        .questions-list {
            background: #fff8e8;
            border-radius: 16px;
            padding: 12px;
            margin: 10px 0;
            text-align: left;
            font-size: 1rem;
            line-height: 1.8;
            display: none;
        }
        .question-item {
            margin: 6px 0;
            padding: 4px 8px;
            background: #fef5e6;
            border-radius: 8px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>📚 AI口算错题本</h1>
    <div class="user-info">
        <input id="userName" placeholder="姓名">
        <input id="userClass" placeholder="班级">
    </div>
    <div class="level-group">
        <button class="level-btn active" data-level="base">基础</button>
        <button class="level-btn" data-level="mid">进阶</button>
        <button class="level-btn" data-level="hard">困难</button>
    </div>
    <button class="gen-btn" id="generateBtn">📝 一键出10道题</button>
    <div class="diagnose-card">
        <div>AI薄弱诊断：<span id="weakTip">暂无错题</span></div>
        <div id="weakTags"></div>
    </div>
    <div class="questions-list" id="questionsList"></div>
    <div class="q-card">
        <div class="q-text" id="qText">5 + 3 = ?</div>
        <input type="number" id="answerInput" placeholder="得数">
        <div>
            <button class="check-btn" id="checkBtn">✅ 核对</button>
            <button class="next-btn" id="nextBtn" disabled>➡️ 下一题</button>
            <button class="error-btn" id="errorBtn">📖 错题重做</button>
            <button class="reset-btn" id="resetBtn">🔄 重置数据</button>
        </div>
    </div>
    <div id="feedbackArea" class="feedback">💡 认真计算，细心答题</div>
    <div class="score-wrap">
        <div class="score-row">
            <div class="item"><span class="badge">总题</span><span id="totalCount">0</span></div>
            <div class="item"><span class="badge">做对</span><span id="rightCount">0</span></div>
            <div class="item"><span class="badge">错题</span><span id="errorCount">0</span></div>
            <div class="item"><span class="badge">正确率</span><span id="accuracy">0</span>%</div>
        </div>
        <div class="medal" id="medalText">💪 加油挑战勋章</div>
    </div>
    <button class="info-btn" id="showInfo">📄 作品说明</button>
    <div class="info-panel" id="infoPanel">
        <strong>作品名称：</strong>AI口算错题本（100以内加减法智能诊断系统）<br>
        <strong>AI功能：</strong>智能出题、自动判分、错题本、薄弱点诊断、学情统计<br>
        <strong>适用场景：</strong>小学生数学口算练习、智能辅导<br>
        <strong>技术：</strong>HTML+JavaScript+本地存储+AI统计算法<br>
        <strong>创新点：</strong>免安装、轻量化、自适应难度、精准定位薄弱题型
    </div>
</div>
<script>
    let qObj = {a:0,b:0,opt:"+",ans:0,kind:""};
    let totalCount = 0;
    let rightCount = 0;
    let isAnswered = false;
    let errorList = JSON.parse(localStorage.getItem('mathErrorList')) || [];
    let isRedoMode = false;
    let currentLevel = "base";
    let questionQueue = [];
    let currentIndex = 0;
    const el = (id) => document.getElementById(id);

    // 题型分类：不进位加法、进位加法、不退位减法、退位减法
    function getKind(a,b,opt){
        if(opt === '+'){
            if(a%10 + b%10 >=10) return 'carry_add';
            else return 'normal_add';
        }else{
            if(a%10 < b%10) return 'carry_sub';
            else return 'normal_sub';
        }
    }

    const kindMap = {
        normal_add: {text:'不进位加法', color:'#e65100'},
        carry_add: {text:'进位加法', color:'#d83a34'},
        normal_sub: {text:'不退位减法', color:'#0a79a2'},
        carry_sub: {text:'退位减法', color:'#7e4bb2'}
    };

    document.querySelectorAll(".level-btn").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".level-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentLevel = btn.dataset.level;
            createQ();
        }
    });

    el("generateBtn").onclick = () => {
        questionQueue = [];
        for(let i=0; i<10; i++){
            questionQueue.push(generateSingleQuestion());
        }
        currentIndex = 0;
        showCurrentQuestion();
        renderQuestionsList();
        el("questionsList").style.display = "block";
        el("feedbackArea").innerText = "✅ 已生成10道题，开始练习！";
        el("feedbackArea").className = "feedback correct-feedback";
    };

    function generateSingleQuestion(){
        let a,b,ans,opt;
        if (currentLevel === "base") {
            opt = Math.random()>.5 ? '+' : '-';
            if(opt === '+'){
                do {
                    a = Math.floor(Math.random()*10)+1;
                    b = Math.floor(Math.random()*10)+1;
                    ans = a+b;
                } while(ans>20);
            }else{
                do {
                    a = Math.floor(Math.random()*15)+5;
                    b = Math.floor(Math.random()*10)+1;
                    ans = a-b;
                } while(ans<0);
            }
        } else if (currentLevel === "mid") {
            opt = Math.random()>.5 ? '+' : '-';
            if(opt === '+'){
                a = Math.floor(Math.random()*25)+10;
                b = Math.floor(Math.random()*25)+5;
                ans = a+b;
            }else{
                a = Math.floor(Math.random()*35)+15;
                b = Math.floor(Math.random()*25)+5;
                ans = a-b;
            }
            if(ans<0) return generateSingleQuestion();
        } else {
            opt = Math.random()>.5 ? '+' : '-';
            if(opt === '+'){
                do {
                    a = Math.floor(Math.random()*40)+30;
                    b = Math.floor(Math.random()*40)+20;
                    ans = a+b;
                } while(ans>100);
            }else{
                do {
                    a = Math.floor(Math.random()*50)+50;
                    b = Math.floor(Math.random()*45)+10;
                    ans = a-b;
                } while(ans<0);
            }
        }
        let kind = getKind(a,b,opt);
        return { a, b, opt, ans, kind };
    }

    function showCurrentQuestion(){
        if(currentIndex >= questionQueue.length){
            el("feedbackArea").innerText = "🎉 10道题全部完成！";
            el("feedbackArea").className = "feedback correct-feedback";
            el("checkBtn").disabled = true;
            el("nextBtn").disabled = true;
            return;
        }
        qObj = questionQueue[currentIndex];
        el("qText").innerText = `${qObj.a} ${qObj.opt} ${qObj.b} = ?`;
        isAnswered = false;
        el("checkBtn").disabled = false;
        el("nextBtn").disabled = true;
        el("answerInput").value = "";
    }

    function renderQuestionsList(){
        let html = "<strong>📋 本次10道题：</strong><br>";
        questionQueue.forEach((q, i) => {
            let cls = i === currentIndex ? "style='background:#f6d392;'" : "";
            html += `<div class="question-item" ${cls}>${i+1}. ${q.a} ${q.opt} ${q.b} = ?</div>`;
        });
        el("questionsList").innerHTML = html;
    }

    function createQ() {
        isAnswered = false;
        isRedoMode = false;
        el("checkBtn").disabled = false;
        el("nextBtn").disabled = true;
        el("answerInput").value = "";
        el("feedbackArea").innerText = "💡 认真计算，细心答题";
        el("feedbackArea").className = "feedback";
        el("errorBtn").style.display = "inline-block";
        qObj = generateSingleQuestion();
        el("qText").innerText = `${qObj.a} ${qObj.opt} ${qObj.b} = ?`;
    }

    function getRandomErrorQ(){
        return errorList.length ? errorList[Math.floor(Math.random()*errorList.length)] : null;
    }

    function addError(){
        let exist = errorList.some(i=>
            i.a===qObj.a && i.b===qObj.b && i.opt===qObj.opt
        );
        if(!exist) {
            errorList.push({...qObj});
            localStorage.setItem('mathErrorList',JSON.stringify(errorList));
        }
    }

    function removeError(){
        errorList = errorList.filter(i=>
            !(i.a===qObj.a && i.b===qObj.b && i.opt===qObj.opt)
        );
        localStorage.setItem('mathErrorList',JSON.stringify(errorList));
    }

    // ========== 核心修改：精准4类错题诊断 ==========
    function diagnoseWeak(){
        el("errorCount").innerText = errorList.length;
        if(errorList.length === 0){
            el("weakTip").innerText = "暂无错题，太棒啦！";
            el("weakTags").innerHTML = "";
            return;
        }

        let count = {
            normal_add:0, carry_add:0, normal_sub:0, carry_sub:0
        };
        errorList.forEach(q => count[q.kind]++);

        el("weakTip").innerText = `共${errorList.length}道错题`;
        let tags = '';
        for(let k in count){
            if(count[k]>0){
                tags += `<span class="weak-tag" style="background:${kindMap[k].color}">
                    ${kindMap[k].text}：错${count[k]}道
                </span>`;
            }
        }
        el("weakTags").innerHTML = tags;
    }

    function updateMedal(){
        let acc = totalCount>0 ? Math.round(rightCount/totalCount*100) : 0;
        let text;
        if(acc>=95) text="🏅 口算小天才";
        else if(acc>=80) text="🥇 口算小达人";
        else if(acc>=60) text="🥈 继续努力";
        else text="💪 加油练习";
        el("medalText").innerText = text;
    }

    function updateScore(){
        el("totalCount").innerText = totalCount;
        el("rightCount").innerText = rightCount;
        let acc = totalCount===0 ? 0 : Math.round(rightCount/totalCount*100);
        el("accuracy").innerText = acc;
        diagnoseWeak();
        updateMedal();
    }

    function checkAnswer(){
        if(isAnswered) return;
        let user = parseInt(el("answerInput").value.trim());
        if(isNaN(user)){
            el("feedbackArea").innerText="⚠️ 请输入数字";
            el("feedbackArea").className="feedback wrong-feedback";
            return;
        }
        isAnswered = true;
        el("checkBtn").disabled = true;
        el("nextBtn").disabled = false;
        totalCount++;

        if(user === qObj.ans){
            rightCount++;
            if(isRedoMode){
                removeError();
                el("feedbackArea").innerText="🎉 做对！已移出错题本";
            }else{
                el("feedbackArea").innerText="🎉 回答正确！";
            }
            el("feedbackArea").className="feedback correct-feedback";
        }else{
            el("feedbackArea").innerText=`❌ 正确答案：${qObj.ans}`;
            el("feedbackArea").className="feedback wrong-feedback";
            if(!isRedoMode) addError();
        }
        updateScore();
    }

    el("nextBtn").onclick = () => {
        if(isRedoMode){
            redoError();
            el("answerInput").focus();
            return;
        }
        if(questionQueue.length > 0){
            currentIndex++;
            showCurrentQuestion();
            renderQuestionsList();
        }else{
            createQ();
        }
        el("answerInput").focus();
    };

    function redoError(){
        if(errorList.length === 0){
            el("feedbackArea").innerText="✅ 错题全部订正完成！";
            el("feedbackArea").className="feedback correct-feedback";
            el("checkBtn").disabled = true;
            el("nextBtn").disabled = true;
            return;
        }
        isAnswered = false;
        isRedoMode = true;
        el("checkBtn").disabled = false;
        el("nextBtn").disabled = true;
        el("answerInput").value = "";
        el("feedbackArea").innerText = "📖 错题专项练习";
        el("errorBtn").style.display = "none";
        let err = getRandomErrorQ();
        if(err){
            qObj = err;
            el("qText").innerText = `${err.a} ${err.opt} ${err.b} = ?`;
        }
    }

    function resetAll(){
        if(!confirm("确定清空所有数据？")) return;
        totalCount = 0;
        rightCount = 0;
        errorList = [];
        questionQueue = [];
        currentIndex = 0;
        localStorage.removeItem("mathErrorList");
        updateScore();
        createQ();
        el("questionsList").style.display = "none";
    }

    el("showInfo").onclick = () => {
        let p = el("infoPanel");
        p.style.display = p.style.display === "block" ? "none" : "block";
    };

    el("checkBtn").onclick = checkAnswer;
    el("errorBtn").onclick = redoError;
    el("resetBtn").onclick = resetAll;
    el("answerInput").addEventListener("keydown",e=>{
        if(e.key === "Enter" && !isAnswered) checkAnswer();
    });

    createQ();
    updateScore();
</script>
</body>
</html>
