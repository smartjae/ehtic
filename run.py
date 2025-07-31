import streamlit as st
from datetime import datetime
from PIL import Image
from app_streaming import run_emotion_analysis
import streamlit.components.v1 as components

# ——— Page config & title ———
st.set_page_config(layout='wide', page_title='ethicapp')
st.title('감정을 읽는 기계')

# ——— Sidebar navigation menu ———
st.sidebar.subheader('Menu …')
page = st.sidebar.radio(
    '',
    ['Home','감정 분석 AI','감정 분석 AI의 작동원리', '학생 응답']
)

# ——— Main layout: two columns (4:1) ———
left_col, right_col = st.columns([4, 1])

if page == 'Home':
    with left_col:
        st.subheader('Content')
        st.video('https://youtu.be/5GN2dIu5fg4') #https://youtu.be/CShXWACuGp8?si=ANvHKLLaTQq6jU00    https://www.youtube.com/watch?v=lkT6qg55kpE


        # 폰트 크기를 키워서 안내 문구 출력
        st.markdown(
            """
            <p style='font-size:20px; font-weight:bold;'>기계가 감정을 읽을 수 있다고 생각하나요?</p>
            """,
            unsafe_allow_html=True
        )
        thoughts = st.text_area('학생 개인 생각을 기록하세요:', height=150)
        if st.button('제출'):
            if thoughts.strip():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                entry = f'[{timestamp}] {thoughts}\n'
                with open('data.txt', 'a', encoding='utf-8') as f:
                    f.write(some_data)
    with left_col:
        st.subheader('Stored Student Data')
        # data.txt 내용 표시
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            st.text_area('', content, height=300)
        except FileNotFoundError:
            st.error('data.txt 파일이 없습니다.')
        except Exception as e:
            st.error(f'data.txt 불러오기 중 오류 발생: {e}')

        # analyze.txt 데이터를 테이블로 표시
        st.subheader('Emotional Analysis Results')
        try:
            import pandas as pd
            rows = []
            with open('analyze.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    # Expected format: [timestamp] Student: name | Incorrect Analysis: incorrect | Reason: reason
                    try:
                        parts = line.strip().split('|')
                        name = parts[0].split('Student:')[1].strip()
                        incorrect = parts[1].split('Incorrect Analysis:')[1].strip()
                        reason = parts[2].split('Reason:')[1].strip()
                        rows.append({'학번': name, '잘못 인식된 감정': incorrect, '이유': reason})
                    except Exception:
                        continue
            if rows:
                df = pd.DataFrame(rows)
                st.table(df)
            else:
                st.info('analyze.txt에 기록된 데이터가 없습니다.')
        except FileNotFoundError:
            st.warning('analyze.txt 파일이 없습니다.')
        except Exception as e:
            st.error(f'analyze.txt 불러오기 중 오류 발생: {e}')

    with right_col:
        st.write('')







elif page == '감정 분석 AI의 작동원리':
    # 왼쪽 컬럼: 설명
    with left_col:
        st.markdown('### 🤖 감정 분석 AI의 작동 원리')
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





elif page == 'Help':
    with left_col:
        st.subheader('Tips & Help')
        st.markdown(
            '''
- 💡 **Tip 1:** 윤리적 딜레마가 발생할 수 있는 상황을 미리 상상해 보세요.  
- 💡 **Tip 2:** AI가 내린 판단을 그대로 믿기보다, 항상 비판적으로 검토하세요.  
            '''
        )
    with right_col:
        st.write('')  # 비어 있는 영역
