import sqlite3
import re
import cv2

def on_logic_clicked(): # DB확인 및 주차 안내 로직
    global current_frame, recognized_vehicle_no, model_b, last_full_frame

    # 프레임 데이터 정상적으로 들어왔는지 디버그 출력
    print(f"DEBUG: last_full_frame type: {type(last_full_frame)}")

    # 인식된 번호판이 없으면 진행 불가
    if not recognized_vehicle_no:
        window.update_message("먼저 번호판을 인식해 주세요.")
        return

    # DB에서 해당 번호판의 사용자 정보 조회
    user_data = step2_db_check(recognized_vehicle_no)
    
    if user_data:
        # 등록 차량일 경우, YOLO로 현재 주차장 빈자리 스캔
        seat_status = step3_yolo_analysis(last_full_frame, model_b)

        # 사용자 이름과 선호 구역(my_area) 데이터를 기반으로 주차 위치 결정
        final_seat = step4_logic_dicision(seat_status, user_data['name'], user_data['my_area'])

        # 최종 안내 메시지 생성 및 시각적 가이드 처리
        _, guide_msg = step5_visual_guide(last_full_frame, final_seat)
        window.update_message(f"환영합니다 {user_data['name']}님! {guide_msg}")
    else:
        # DB에 등록되지 않은 차량 처리
        window.update_message(f"미등록 차량({recognized_vehicle_no})입니다. 진입 불가.")
