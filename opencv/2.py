import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# --- 1. 데이터 준비  ---
base_path = "digit_data"
images = []
labels = []

for digit in range(10):
    folder_path = os.path.join(base_path, str(digit))
    if not os.path.exists(folder_path): continue

    for file_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (28, 28))
            images.append(img)
            labels.append(digit)

X = np.array(images).reshape(-1, 28, 28, 1) / 255.0
y = np.array(labels)

# --- 2. 합성곱 신경망(CNN) 모델 설계 ---
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# --- 3. 학습 설정 ---
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print(f"총 {len(images)}장의 데이터로 학습을 시작합니다.")
model.fit(X, y, epochs=50, batch_size=32)

# --- 4. 저장 ---
model.save("digit_model.h5")
print("합성곱 모델 저장 완료!")
