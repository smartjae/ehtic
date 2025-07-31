import streamlit as st
from datetime import datetime
from PIL import Image
from app_streaming import run_emotion_analysis
import streamlit.components.v1 as components
import pandas as pd
import re

# ——— Page config & title ———
st.set_page_config(layout='wide', page_title='ethicapp')
st.title('감정을 읽는 기계')

# ——— Sidebar navigation menu ———
st.sidebar.subheader('Menu …')
page = st.sidebar.radio(
    '',
    ['Home','감정 분석 AI','감정 분석 AI의 작동원리', '학생응답 결과']
)

# ——— Main layout: two columns (4:1) ———
left_col, right_col = st.columns([4, 1])

if page == 'Home':
    with left_col:
        st.subheader('Content')
        st.video('https://youtu.be/5GN2dIu5fg4')

        # — 첫 번째 질문 —
        st.markdown(
            "<p style='font-size:18px; font-weight:bold;'>1️⃣ 기계가 사람의 감정을 인식할 수 있다면, 어떤 상황에서 도움이 될 수 있을까요?</p>",
            unsafe_allow_html=True
        )
        answer1 = st.text_area('학생들의 생각을 적어주세요:', key='answer1', height=120)

        # — 두 번째 질문 —
        st.markdown(
            "<p style='font-size:18px; font-weight:bold;'>2️⃣ 기계가 감정을 읽을 수 있다고 생각하나요?</p>",
            unsafe_allow_html=True
        )
        answer2 = st.text_area('학생들의 생각을 적어주세요:', key='answer2', height=120)

        if st.button('제출'):
            if not answer1.strip() or not answer2.strip():
                st.warning('두 질문에 모두 답변한 후 제출해주세요.')
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                entry = f'[{timestamp}] {answer1} | {answer2}\n'
                with open('data.txt', 'a', encoding='utf-8') as f:
                    f.write(entry)
                st.success('생각이 성공적으로 제출되었습니다!')

    with right_col:
        st.subheader('Tips & Help')
        st.markdown(
            '''
- 💡 **Tip 1:** 윤리적 딜레마가 발생할 수 있는 상황을 미리 상상해 보세요.  
- 💡 **Tip 2:** AI가 내린 판단을 그대로 믿기보다, 항상 비판적으로 검토하세요.  
            '''
        )





elif page == '감정 분석 AI':
    # 먼저 오른쪽에 사용법을 보여줍니다.
    with right_col:
        st.subheader('How to use')
        st.markdown(
            '''
- 웹캠을 통해 실시간으로 얼굴을 감지하고 감정을 예측합니다.  
- 브라우저에서 카메라 권한을 허용해 주세요.  
- 여러 가지 표정으로 테스트해 보세요.
            '''
        )

     # 왼쪽: 시작/중단 버튼 및 분석, 피드백 폼
    with left_col:
        btn1, btn2 = st.columns(2)
        if btn1.button('Start Emotion Analysis'):
            st.session_state['emotion_running'] = True
        if btn2.button('Stop Emotion Analysis'):
            st.session_state['emotion_running'] = False

        # 감정 분석 실행 또는 정지
        if st.session_state.get('emotion_running'):
            run_emotion_analysis()

        st.subheader('감정 분석 결과')
        student_name = st.text_input('학번')
        incorrect = st.text_area('잘못 인식된 감정', height=100)
        reason = st.text_area('이유', height=100)
        if st.button('제출'):
            if student_name.strip() and incorrect.strip() and reason.strip():
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                entry = f'[{ts}] Student: {student_name} | Incorrect Analysis: {incorrect} | Reason: {reason}\n'
                try:
                    with open('analyze.txt', 'a', encoding='utf-8') as f:
                        f.write(entry)
                    st.success('Feedback submitted!')
                except Exception as e:
                    st.error(f'Error saving feedback: {e}')
            else:
                st.warning('모든 필드를 입력한 후 제출해주세요.')













   


elif page == '학생응답 결과':
    with left_col:
        st.subheader('학생 응답 결과')

        # data.txt 파싱해서 표로 보여주기
        try:
            rows = []
            with open('data.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'\[(.*?)\]\s*(.*?)\s*\|\s*(.*)', line)
                    if m:
                        rows.append({
                            '제출 시각': m.group(1),
                            '질문 1 응답': m.group(2),
                            '질문 2 응답': m.group(3)
                        })
            if rows:
                df = pd.DataFrame(rows)
                st.table(df)
            else:
                st.info('아직 제출된 응답이 없습니다.')
        except FileNotFoundError:
            st.error('data.txt 파일을 찾을 수 없습니다.')
        except Exception as e:
            st.error(f'응답 결과를 불러오는 중 오류가 발생했습니다: {e}')

        # 기존 analyze.txt 테이블 표시 (필요 시 그대로 유지)
        st.subheader('Emotional Analysis Results')
        try:
            analysis_rows = []
            with open('analyze.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 3:
                        name = parts[0].split('Student:')[-1].strip()
                        incorrect = parts[1].split('Incorrect Analysis:')[-1].strip()
                        reason = parts[2].split('Reason:')[-1].strip()
                        analysis_rows.append({
                            '학번': name,
                            '잘못 인식된 감정': incorrect,
                            '이유': reason
                        })
            if analysis_rows:
                df2 = pd.DataFrame(analysis_rows)
                st.table(df2)
            else:
                st.info('analyze.txt에 기록된 데이터가 없습니다.')
        except FileNotFoundError:
            st.warning('analyze.txt 파일이 없습니다.')
        except Exception as e:
            st.error(f'analyze.txt 불러오기 중 오류 발생: {e}')

    with right_col:
        st.write('')  # 필요에 따라 도움말 추가







elif page == '감정 분석 AI의 작동원리':
    # 왼쪽 컬럼: 설명
    with left_col:
        st.markdown('### 🧠 감정 분석 AI의 작동 원리')
        st.markdown(
            '''
1. **입력 데이터 수집**  
   - 얼굴 이미지나 영상 스트림이 입력으로 들어옵니다.

2. **얼굴 감지 (Face Detection)**  
   - 이미지에서 얼굴 영역을 찾아냅니다. (예: MediaPipe 사용)

3. **얼굴 특징 추출 (Feature Extraction)**  
   - 눈, 코, 입 등 3D 특징점을 추출하여 표정 변화를 인식합니다.

4. **데이터 전처리 (Preprocessing)**  
   - 이미지 크기 조정, 흑백 변환, 정규화를 통해 AI가 학습하기 좋은 형태로 만듭니다.

5. **감정 분류 모델 입력 (Model Inference)**  
   - CNN 기반 모델에 이미지를 입력하고, 감정 확률을 예측합니다.

6. **감정 선택 (Prediction Result)**  
   - 가장 높은 확률의 감정을 최종 결과로 출력합니다.

7. **시각화 및 출력**  
   - 예측된 감정을 텍스트, 이모지, 차트 등으로 시각화합니다.
            '''
        )

    # 오른쪽 컬럼: 버튼
    
    with right_col:
            # 소제목: 폰트 크기 조절
        st.markdown(
            "<p style='font-size:25px; font-weight:bold; margin-bottom:8px;'>AI 모델 개발 도구</p>",
            unsafe_allow_html=True
        )

        if st.button('➡️ Teachable Machine'):
            components.html(
                """
                <script>
                    window.open('https://teachablemachine.withgoogle.com/train', '_blank')
                </script>
                """,
                height=0  # 보이지 않게 삽입
            )
        if st.button('➡️ Colab'):
            components.html(
                """
                <script>
                    window.open('https://colab.google/', '_blank')
                </script>
                """,
                height=0
            )







