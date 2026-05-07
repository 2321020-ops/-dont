import streamlit as st
import random
import json
import os
import time

# -------------------------------
# 데이터 불러오기
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "food.json")

with open(file_path, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(
    page_title="오늘 뭐 먹지? 해결사",
    page_icon="🍽️",
    layout="centered"
)

# -------------------------------
# 스타일
# -------------------------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #ff6b6b, #ffb347);
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #ff3d3d, #ff9500);
}

.result-box {
    background: linear-gradient(135deg, #ff9966, #ff5e62);
    padding: 35px;
    border-radius: 25px;
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
    margin-top: 20px;
    box-shadow: 0px 0px 25px rgba(255,255,255,0.4);
    animation: pop 0.4s ease-in-out;
}

@keyframes pop {
    0% {transform: scale(0.7);}
    100% {transform: scale(1);}
}

.food-card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    color: white;
    font-size: 20px;
}

.info-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 제목
# -------------------------------
st.markdown("""
<h1 style='text-align:center; font-size:55px; color:white;'>
🍽️ 오늘 뭐 먹지? 해결사
</h1>
""", unsafe_allow_html=True)

# -------------------------------
# 메뉴 선택
# -------------------------------
menu = st.sidebar.selectbox(
    "기능 선택",
    [
        "상황별 음식 추천",
        "카테고리별 메뉴",
        "룰렛 (메뉴 추천)",
        "결제 룰렛 게임"
    ]
)

# -------------------------------
# 세션 상태
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = {}

# -------------------------------
# 1. 상황별 음식 추천
# -------------------------------
if menu == "상황별 음식 추천":

    st.header("🔥 상황별 음식 추천")

    st.markdown("""
    <div class='info-box'>
    ✔ 혼밥 → 혼자 먹기 좋은 메뉴<br>
    ✔ 데이트 → 분위기 좋은 음식<br>
    ✔ 친구 → 같이 먹기 좋은 메뉴<br>
    ✔ 회식 → 여러 명 추천 메뉴<br>
    ✔ 비오는날 → 국물/따뜻한 음식<br>
    ✔ 해장 → 속 풀리는 음식<br>
    ✔ 간단 → 빠르게 먹는 메뉴<br>
    ✔ 야식 → 밤에 먹기 좋은 음식
    </div>
    """, unsafe_allow_html=True)

    mood = st.selectbox(
        "현재 상황 선택",
        ["혼밥", "데이트", "친구", "회식", "비오는날", "해장", "간단", "야식"]
    )

    filtered = [f for f in food_data if mood in f["mood"]]

    if mood not in st.session_state.history:
        st.session_state.history[mood] = []

    if st.button("✨ 음식 추천 받기"):

        previous = st.session_state.history[mood]

        available = [f for f in filtered if f["name"] not in previous]

        if not available:
            st.session_state.history[mood] = []
            available = filtered

        result = random.choice(available)

        st.session_state.history[mood].append(result["name"])

        st.balloons()

        st.markdown(
            f"""
            <div class='result-box'>
            🍜 {result['name']}
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# 2. 카테고리 메뉴
# -------------------------------
elif menu == "카테고리별 메뉴":

    st.header("📚 카테고리별 메뉴")

    category = st.selectbox(
        "카테고리 선택",
        ["한식", "중식", "일식", "양식", "분식", "야식"]
    )

    filtered = [f for f in food_data if f["category"] == category]

    for f in filtered:
        st.markdown(
            f"""
            <div class='food-card'>
            🍴 {f['name']}
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# 3. 룰렛
# -------------------------------
elif menu == "룰렛 (메뉴 추천)":

    st.header("🎰 프리미엄 음식 룰렛")

    st.markdown("""
    <div class='info-box'>
    버튼을 누르면 화려한 룰렛이 시작됩니다 🎉
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎡 룰렛 돌리기"):

        placeholder = st.empty()

        for i in range(45):

            temp = random.choice(food_data)

            size = random.randint(35, 60)

            color = random.choice([
                "#ff6b6b",
                "#ffd93d",
                "#6bcB77",
                "#4d96ff",
                "#ff9f1c"
            ])

            placeholder.markdown(
                f"""
                <div style="
                    background:black;
                    border-radius:25px;
                    padding:40px;
                    text-align:center;
                    box-shadow:0 0 30px {color};
                ">
                    <h1 style="
                        color:{color};
                        font-size:{size}px;
                    ">
                    🎯 {temp['name']}
                    </h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.05)

        result = random.choice(food_data)

        st.balloons()

        placeholder.markdown(
            f"""
            <div class='result-box'>
            🎉 {result['name']} 🎉
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# 4. 결제 룰렛 게임
# -------------------------------
elif menu == "결제 룰렛 게임":

    st.header("💸 결제 룰렛 게임")

    people_input = st.text_area(
        "참가자 이름 입력 (쉼표로 구분)",
        "철수,영희,민수"
    )

    people = [p.strip() for p in people_input.split(",") if p.strip()]

    if len(people) > 0:

        pay_count = st.number_input(
            "몇 명이 결제할까요?",
            min_value=1,
            max_value=len(people),
            value=1
        )

    if st.button("🔥 결제 당첨자 뽑기"):

        if len(people) == 0:
            st.warning("참가자를 입력하세요")

        else:

            placeholder = st.empty()

            for i in range(40):

                temp = random.choice(people)

                placeholder.markdown(
                    f"""
                    <div style="
                        background:#111827;
                        border-radius:25px;
                        padding:35px;
                        text-align:center;
                        box-shadow:0 0 25px red;
                    ">
                        <h1 style="
                            color:#ff4d4d;
                            font-size:55px;
                        ">
                        💸 {temp}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(0.05)

            losers = random.sample(people, pay_count)

            st.balloons()

            placeholder.markdown(
                f"""
                <div class='result-box'>
                💥 {' , '.join(losers)}
                </div>
                """,
                unsafe_allow_html=True
            )
