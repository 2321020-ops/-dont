# -------------------------------
# 1. 상황별 추천
# -------------------------------
if menu == "상황별 음식 추천":
    st.header("상황별 음식 추천")

    st.info("""
추천 기준:
- 혼밥: 혼자 먹기 좋은 음식
- 데이트: 분위기 있는 음식
- 친구: 같이 먹기 좋은 메뉴
- 회식: 여러 명이 먹기 좋은 음식
- 비오는날: 국물/따뜻한 음식
- 해장: 속 풀리는 음식
- 간단: 빠르게 먹기 좋은 음식
- 야식: 밤에 먹기 좋은 음식
""")

    mood = st.selectbox("현재 상황 선택", [
        "혼밥", "데이트", "친구", "회식", "비오는날", "해장", "간단", "야식"
    ])

    if st.button("추천 받기"):
        filtered = [f for f in food_data if mood in f["mood"]]

        if filtered:
            result = random.choice(filtered)
            st.success(f"👉 오늘은 **{result['name']}** 어때?")
        else:
            st.warning("추천 가능한 메뉴가 없어요 😢")


# -------------------------------
# 2. 카테고리 메뉴 보기
# -------------------------------
elif menu == "카테고리별 메뉴":
    st.header("카테고리별 메뉴")

    category = st.selectbox("카테고리 선택", [
        "한식", "중식", "일식", "양식", "분식", "야식"
    ])

    filtered = [f for f in food_data if f["category"] == category]

    for f in filtered:
        st.write(f"🍴 {f['name']}")


# -------------------------------
# 3. 메뉴 룰렛
# -------------------------------
elif menu == "룰렛 (메뉴 추천)":
    import time

    st.header("🎡 메뉴 룰렛")

    if st.button("룰렛 돌리기!"):
        placeholder = st.empty()

        for _ in range(15):
            temp = random.choice(food_data)
            placeholder.markdown(f"🎯 **{temp['name']}**")
            time.sleep(0.1)

        result = random.choice(food_data)
        placeholder.success(f"🎉 오늘 메뉴는 → **{result['name']}**")


# -------------------------------
# 4. 결제 룰렛 게임
# -------------------------------
elif menu == "결제 룰렛 게임":
    st.header("💸 결제 룰렛 게임")

    people_input = st.text_input("참가자 이름 (쉼표로 구분)", "철수,영희,민수")

    if st.button("누가 쏠까? 😈"):
        people = [p.strip() for p in people_input.split(",") if p.strip()]

        if len(people) < 2:
            st.warning("최소 2명 필요!")
        elif len(people) > 10:
            st.warning("최대 10명까지 가능!")
        else:
            loser = random.choice(people)
            st.error(f"💥 오늘 결제는 → **{loser}** 😈")
