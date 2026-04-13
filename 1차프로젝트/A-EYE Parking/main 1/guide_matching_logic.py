import sqlite3

# 데이터베이스에서 차량 소유주 정보 조회
def step2_db_check(vehicle_no):
    conn = sqlite3.connect('parking_system.db')
    cur = conn.cursor()
    
    # 번호판(vehicle_no)을 기준으로 이름, 동, 선호 구역 조회
    cur.execute("SELECT name, building_no, assigned_seat FROM car_info WHERE vehicle_no=?", (vehicle_no,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        # 다음 단계(Step 3, 4)에서 사용할 수 있게 딕셔너리로 묶어서 반환
        return {
            'name': row[0],
            'dong': row[1],
            'my_area': row[2]  # 이 정보가 4단계에서 '우리 동 근처'를 찾는 기준이 됨
        }
    return None

# [Bridge] 2번에서 가져온 유저 정보와 3번의 YOLO 상태를 결합하는 함수
def bridge_user_to_system(user_data, seat_status):
    if user_data is None:
        return "외부 차량입니다. 경비실로 연결합니다."

    return user_data, seat_status
