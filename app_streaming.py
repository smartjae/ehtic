# ===== app_streaming.py =====
import json
import cv2
import numpy as np
from mtcnn import MTCNN
import tensorflow as tf
import streamlit as st
from PIL import Image

# MTCNN 얼굴 검출기 초기화 (한 번만 캐싱)
@st.cache_resource
def load_face_detector():
    return MTCNN()

# 감정분석 모델 로드 (한 번만 캐싱)
@st.cache_resource
def load_emotion_model():
    with open("label_map.json", "r", encoding="utf-8") as f:
        label_map = json.load(f)
    model = tf.keras.models.load_model("fer_cnn_directory.h5")
    return label_map, model


def run_emotion_analysis():
    """
    웹앱에서 스트리밍 웹캠 대신 카메라 사진 입력으로 
    얼굴을 감지하고 감정을 예측합니다.
    """
    st.subheader("Emotion Analysis (Camera Input)")

    # 모델과 얼굴 검출기 준비
    label_map, model = load_emotion_model()
    detector = load_face_detector()

    # Streamlit 카메라 입력 위젯
    camera_img = st.camera_input("카메라로 얼굴 사진 찍기")
    if camera_img is None:
        st.info("카메라 버튼을 눌러 얼굴을 촬영하세요.")
        return

    # PIL 이미지 → NumPy 배열 (RGB)
    frame = Image.open(camera_img).convert("RGB")
    rgb = np.array(frame)

    # MTCNN 얼굴 감지
    detections = detector.detect_faces(rgb)
    if not detections:
        st.warning("얼굴이 감지되지 않았습니다. 다시 시도해 주세요.")
        return

    # 첫 번째 얼굴 영역
    x, y, w, h = detections[0]['box']
    x, y = max(0, x), max(0, y)
    face = rgb[y:y+h, x:x+w]

    # 얼굴 전처리 (그레이스케일 → 리사이즈 → 정규화)
    gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray, (48, 48))
    x_input = resized.astype("float32") / 255.0
    x_input = np.expand_dims(x_input, axis=(0, -1))  # (1,48,48,1)

    # 감정 예측
    proba = model.predict(x_input)[0]
    proba_dict = {label_map[i]: float(proba[i]) for i in range(len(proba))}

    # 결과 표시
    st.image(frame, caption="Captured Image", use_container_width=True)
    st.write("**Prediction Probabilities:**", proba_dict)

    idx = int(np.argmax(proba))
    pred_label = label_map[idx]
    status = (
        "Positive" if pred_label == "Happy" 
        else "Negative" if pred_label in ["Sad", "Angry", "Disgust", "Fear"] 
        else "Neutral"
    )
    st.success(f"Prediction: {status} ({pred_label})")
