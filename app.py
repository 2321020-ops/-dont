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
# 기본 UI
# -------------------------------
st.set_page_config(page_title="오늘 뭐 먹지? 해결사", page_icon="🍽️")
st.title("🍽️ 오늘 뭐 먹지? 해결사")

menu = st.sidebar.selectbox("기능 선택", [
    "상황별 음식 추천",
    "카테고리별 메뉴",
    "룰렛 (메뉴 추천)",
    "결제 룰렛 게임"
])

# -------------------------------
# 1. 상황별 추천
# -------------------------------
if menu == "상황별 음식 추천":
    st.header("상황별 음식 추천")

    st.info("""
추천 기준:
혼밥 / 데이트 / 친구 / 회식 / 비오는날 / 해장 / 간단 / 야식
""")

    mood = st.selectbox("상황 선택", [
        "혼밥","데이트","친구","회식","비오는날","해장","간단","야식"
    ])

    filtered = [f for f in food_data if mood in f["mood"]]

    if "last" not in st.session_state:
        st.session_state.last = None

    if st.button("추천 받기"):
        choices = [f for f in filtered if f != st.session_state.last]

        if not choices:
            choices = filtered

        result = random.choice(choices)
        st.session_state.last = result

        st.success(f"👉 {result['name']} 추천!")

# -------------------------------
# 2. 카테고리
# -------------------------------
elif menu == "카테고리별 메뉴":
    st.header("카테고리별 메뉴")

    category = st.selectbox("카테고리", [
        "한식","중식","일식","양식","분식","야식"
    ])

    filtered = [f for f in food_data if f["category"] == category]

    for f in filtered:
        st.write("🍴", f["name"])

# -------------------------------
# 3. 룰렛
# -------------------------------
elif menu == "룰렛 (메뉴 추천)":
    st.header("🎡 룰렛")

    if st.button("돌리기"):
        placeholder = st.empty()

        for _ in range(30):
            temp = random.choice(food_data)
            placeholder.markdown(
                f"<h1 style='text-align:center;color:orange'>{temp['name']}</h1>",
                unsafe_allow_html=True
            )
            time.sleep(0.04)

        result = random.choice(food_data)

        st.balloons()

        placeholder.markdown(
            f"<h1 style='text-align:center;color:red'>🎉 {result['name']} 🎉</h1>",
            unsafe_allow_html=True
        )

# -------------------------------
# 4. 결제 룰렛 게임 (🔥 업그레이드)
# -------------------------------
elif menu == "결제 룰렛 게임":
    st.header("💸 결제 게임")

    people_input = st.text_input("참가자 이름 (쉼표로 구분)", "철수,영희,민수")

    people = [p.strip() for p in people_input.split(",") if p.strip()]

    if people:
        pay_count = st.number_input(
            "몇 명이 결제할까요?",
            min_value=1,
            max_value=len(people),
            value=1
        )

    if st.button("결정"):
        if len(people) < 1:
            st.warning("참가자를 입력하세요")
        else:
            pay_count = min(pay_count, len(people))

            losers = random.sample(people, pay_count)

            st.balloons()

            st.error(f"💥 결제 당첨자: {', '.join(losers)}")
            loser = random.choice(people)
            st.error(f"💥 오늘 결제는 → **{loser}** 😈")
