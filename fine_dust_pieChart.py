import matplotlib.pyplot as plt

data = {"KOR": 52, "FOR\n": 48}
kor = {"Factories": 38, "Construction\n Boats": 16, "Powerplants": 15, "Disel cars": 11, "etc": 20}

# "kor" 딕셔너리의 값을 비율에 맞게 "data" 딕셔너리에 넣기
for key, value in kor.items():
    data[key] = (value * data["KOR"]) / 100

# "KOR" 값을 삭제
del data["KOR"]

# 파이 차트 생성
plt.figure(figsize=(5, 5))
pie = plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=0.7)
plt.axis('equal')  # 원형 차트로 설정

# 라벨의 글꼴 설정
for label in pie[1]:
    label.set(fontsize=10)

# 백분율의 글꼴 설정
for pct in pie[2]:
    pct.set(fontsize=12)

# 차트에 제목 추가
plt.title("Air Pollution Reasons")

# 파이 차트를 이미지 파일로 저장
plt.savefig("pie_chart.png")

# 파이 차트 출력
plt.show()
