import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# 1. 증강 설정
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    fill_mode='constant',
    cval=0
)

base_path = "digit_data"

# 2. [수정] 범위를 range(1, 5)에서 range(0, 10)으로 변경
# 0부터 9까지 모든 폴더를 훑도록 합니다.
for digit in range(10):
    folder_path = os.path.join(base_path, str(digit))

    # 해당 폴더가 있는지 체크 (방어 코드)
    if not os.path.exists(folder_path):
        continue

    # 'aug_'가 붙지 않은 원본 파일만 골라냅니다.
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.png') and not f.startswith('aug_')]

    print(f"[{digit}]번 폴더 증강 중... 원본: {len(file_list)}장")

    for file_name in file_list:
        img_path = os.path.join(folder_path, file_name)
        img = load_img(img_path, color_mode='grayscale', target_size=(28, 28)) # 크기 고정 추가
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        i = 0
        # 3. [선택] 원본 20장이니 5장보다는 10~15장 정도로 늘리는 걸 추천합니다.
        # i >= 10으로 바꾸면 숫자당 총 200장 이상의 데이터를 확보할 수 있습니다.
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=folder_path,
                                  save_prefix=f"aug_{digit}",
                                  save_format='png'):
            i += 1
            if i >= 10: break # 1장당 10장 생성 (총 220장 내외)

print("모든 데이터 증강 완료!")
