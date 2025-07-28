import streamlit as st
from datetime import datetime

# ——— Page config & title ———
st.set_page_config(layout='wide', page_title='ethicapp')
st.title('Ethics Is Good for Us')

# ——— Sidebar menu header & 버튼 추가 ———
st.sidebar.subheader('Menu …')
# 학생 데이터 불러오기 버튼
load_data = st.sidebar.button('학생데이터 가져오기')
# (여러 페이지를 원할 경우, st.sidebar.radio나 selectbox로 확장 가능)

# ——— Main layout: two columns (4:1) ———
left_col, right_col = st.columns([4, 1])

with left_col:
    # 파일에서 데이터를 불러오도록 요청받은 경우
    if load_data:
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                data = f.read()
            st.subheader('저장된 학생 데이터')
            st.text_area('', data, height=300)
        except FileNotFoundError:
            st.error('저장된 데이터 파일(data.txt)을 찾을 수 없습니다.')
        except Exception as e:
            st.error(f'데이터 불러오는 중 오류 발생: {e}')
    else:
        st.subheader('Content')
        # 유튜브 영상 임베드
        st.video('https://www.youtube.com/watch?v=XyEOEBsa8I4')

        # 학생 개인 생각 기록 및 제출 기능
        thoughts = st.text_area('학생 개인 생각을 기록하세요:', height=150)
        if st.button('제출'):
            if thoughts.strip():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                entry = f'[{timestamp}] {thoughts}\n'
                try:
                    with open('data.txt', 'a', encoding='utf-8') as f:
                        f.write(entry)
                    st.success('생각이 성공적으로 제출되었습니다!')
                except Exception as e:
                    st.error(f'제출 중 오류 발생: {e}')
            else:
                st.warning('생각을 입력한 후 제출해주세요.')

with right_col:
    st.subheader('Tips & Help')
    st.markdown(
        '''
- 💡 **Tip 1:** 윤리적 딜레마가 발생할 수 있는 상황을 미리 상상해 보세요.  
- 💡 **Tip 2:** AI가 내린 판단을 그대로 믿기보다, 항상 비판적으로 검토하세요.  
- ❓ **Help:** 문제가 있을 땈 사이드바의 ‘문의하기’ 버튼을 눌러주세요.
        '''
    )
