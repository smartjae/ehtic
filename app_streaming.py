# ===== app_streaming.py =====
import json
import cv2
import numpy as np
from mtcnn import MTCNN
import tensorflow as tf
import streamlit as st

# MTCNN 얼굴 검출기 초기화 (한 번만)
@st.cache_resource
def load_face_detector():
    return MTCNN()

@st.cache_resource  # 모델과 레이블 맵을 캐싱하여 앱 성능 최적화
def load_emotion_model():
    # 1) label_map.json에서 클래스 순서 불러오기
    with open("label_map.json", "r", encoding="utf-8") as f:
        label_map = json.load(f)
    # 2) 학습된 CNN 모델 로드 (.h5 포맷)
    model = tf.keras.models.load_model("fer_cnn_directory.h5")
    return label_map, model


def run_emotion_analysis():
    """
    Streamlit 페이지 내에서 실시간으로 웹캠을 통해 얼굴을 감지하고
    CNN 모델로 감정을 예측해 화면에 프레임과 확률 분포를 표시합니다.
    """
    # 모델과 레이블 로드
    label_map, model = load_emotion_model()
    # 얼굴 검출기 로드
    detector = load_face_detector()

    # 웹캠 열기 및 레이아웃: 좌3 : 우1 비율 컬럼
    cap = cv2.VideoCapture(0)
    col1, col2 = st.columns([3, 1])
    frame_placeholder = col1.empty()
    proba_placeholder = col2.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("카메라를 열 수 없습니다.")
            break

        # BGR → RGB 변환
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MTCNN으로 얼굴 검출
        detections = detector.detect_faces(rgb)
        if detections:
            # 첫 번째 얼굴만 처리
            x, y, w, h = detections[0]['box']
            # 좌표 음수 방지
            x, y = max(0, x), max(0, y)
            face = rgb[y:y+h, x:x+w]

            # 작은 얼굴 건너뛰기
            if face.size == 0 or w < 20 or h < 20:
                frame_placeholder.image(frame, channels="BGR")
                continue

            # 얼굴 전처리: 그레이스케일 → 리사이즈 → 정규화
            gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
            resized = cv2.resize(gray, (48, 48))
            x_input = resized.astype("float32") / 255.0
            x_input = np.expand_dims(x_input, axis=(0, -1))  # (1,48,48,1)

            # 예측 수행
            proba = model.predict(x_input)[0]
            proba_dict = {label_map[i]: float(proba[i]) for i in range(len(proba))}
            proba_placeholder.write(proba_dict)

            # 최고 확률 라벨, 상태 결정
            idx = int(np.argmax(proba))
            pred_label = label_map[idx]
            status = (
                "Positive" if pred_label == "Happy"
                else "Negative" if pred_label in ["Sad", "Angry", "Disgust", "Fear"]
                else "Neutral"
            )

            # 결과 텍스트 오버레이
            cv2.putText(
                frame,
                f"{status} ({pred_label})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # 영상 출력
        frame_placeholder.image(frame, channels="BGR")

    cap.release()
