import sqlite3

# DB 정보 가져오기 (이름, 동, 선호 구역)
def step2_db_check(vehicle_no):
    conn = sqlite3.connect('parking_system.db')
    cur = conn.cursor()
    cur.execute("SELECT name, building_no, assigned_seat FROM car_info WHERE vehicle_no=?", (vehicle_no,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {'name': row[0], 'dong': row[1], 'my_area': row[2]}
    return None

# 우리 동 우선 -> 다른 동(가까운 순) -> 전체 만차 시 입장 유도
def get_parking_guide(user, seat_status):
    if user is None:
        return "외부 차량입니다. 경비실로 문의해 주세요."

    name, dong, my_area = user['name'], user['dong'], user['my_area']

    # 전체 빈자리 리스트 [주차 칸 딕셔너리를 거리순으로 정렬해야만 함]
    all_empty = [s for s, status in seat_status.items() if status == "Empty"]

    # 단지에 빈자리가 하나도 없을 때
    if not all_empty:
        return f"{name}님, 현재 전 구역 만차입니다. 우선 입차 후 통로에서 서행하며 빈자리를 기다려 주세요."

    # 우리 동(my_area) 키워드가 포함된 빈자리부터 찾기
    my_home_empty = [s for s in all_empty if str(my_area) in s]

    if my_home_empty:
        best_seat = my_home_empty[0]
        return f"{name}님 환영합니다! 거주하시는 {dong} 근처 [{best_seat}]에 주차하세요."

    # 우리 동네 자리는 없지만 다른 곳(다른 동)에 빈자리가 있을 때
    # all_empty[0]은 전체 중 가장 가까운 순서
    alt_seat = all_empty[0]
    return f"{name}님, {dong} 근처가 만차입니다. 다른 구역 중 가장 가까운 [{alt_seat}]로 안내할게요."
