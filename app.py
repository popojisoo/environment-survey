import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(page_title="환경 위험 인식 조사", page_icon="🌱")

st.title("🌱 환경 위험 인식 조사")
st.subheader("프레이밍 효과와 음료수 캔 분리배출 문제")

st.write("같은 환경 문제라도 표현 방식에 따라 심각하게 느껴지는 정도가 달라지는지 조사합니다.")

name = st.text_input("이름을 입력해 주세요")

st.markdown("### 📌 두 가지 표현을 읽고 선택해 주세요")

st.info("A. 한 학년당 하루 평균 120개의 음료수 캔이 버려진다.")

st.warning("B. 한 학년당 한 달 동안 약 2,400개의 음료수 캔이 버려진다.")

choice = st.radio(
    "어느 표현이 더 심각하게 느껴지나요?",
    ["A", "B"]
)

score = st.slider(
    "이 표현을 본 뒤 분리배출 행동을 바꾸고 싶은 정도는?",
    1, 5, 3
)

if st.button("제출하기"):
    if not name:
        st.error("이름을 입력해 주세요.")
        st.stop()
    new_data = pd.DataFrame({
        "이름": [name],
        "더 심각하게 느껴진 표현": [choice],
        "행동 변화 의향": [score]
    })

    file_name = "responses.csv"

    if os.path.exists(file_name):
        old_data = pd.read_csv(file_name)
        data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(file_name, index=False, encoding="utf-8-sig")
    st.success("응답이 제출되었습니다. 참여해주셔서 감사합니다!")

st.markdown("---")
st.subheader("📊 현재 응답 결과")

if os.path.exists("responses.csv"):
    data = pd.read_csv("responses.csv")

    st.write("총 응답 수:", len(data))

    count_data = data["더 심각하게 느껴진 표현"].value_counts()
    st.bar_chart(count_data)

    st.write("평균 행동 변화 의향:", round(data["행동 변화 의향"].mean(), 2))
else:
    st.write("아직 응답이 없습니다.")

st.markdown("---")
st.subheader("🔒 관리자 전용 - 랜덤 추첨")

admin_pw = st.text_input("관리자 비밀번호를 입력해 주세요", type="password")

if admin_pw == "1226":
    if os.path.exists("responses.csv"):
        data = pd.read_csv("responses.csv")
        names = data["이름"].dropna().drop_duplicates().tolist()

        if len(names) < 5:
            st.warning(f"응답자가 {len(names)}명으로 5명 미만입니다. 전체 명단에서 추첨합니다.")
            draw_count = len(names)
        else:
            draw_count = 5

        if st.button("🎲 추첨하기"):
            winners = random.sample(names, draw_count)
            st.success(f"🎉 당첨자 {draw_count}명")
            for i, winner in enumerate(winners, 1):
                st.write(f"{i}. {winner}")
    else:
        st.warning("아직 응답 데이터가 없습니다.")
        st.markdown("---")
        st.markdown("#### 🗑️ 데이터 초기화")
        if st.button("전체 응답 데이터 삭제"):
            if os.path.exists("responses.csv"):
                os.remove("responses.csv")
                st.success("응답 데이터가 초기화되었습니다.")
            else:
                st.info("삭제할 데이터가 없습니다.")
elif admin_pw != "":
    st.error("비밀번호가 틀렸습니다.")