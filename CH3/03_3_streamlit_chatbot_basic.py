from google import genai
from google.genai import types
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

with st.sidebar:
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = st.text_input("Gemini API Key", type="password")
    
    if st.button("대화 내용 초기화"):
        st.session_state.messages = []
        st.rerun()

# 메시지가 없으면 "무엇을 도와드릴까요?"라는 메시지를 초기 응답으로 설정하도록 딕셔너리 형태로 지정
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

if "client" not in st.session_state:
    if GOOGLE_API_KEY:
        # 여기서 client를 생성해서 session_state에 딱 등록합니다.
        st.session_state.client = genai.Client(api_key=GOOGLE_API_KEY)
    else:
        st.warning("API 키가 필요합니다. .env 파일을 확인하거나 사이드바에 입력해주세요.")
        st.stop() # 키가 없으면 여기서 실행 중단!


st.title("Chat Bot")


# st.session_state : streamlit에서 사용자의 세션 상태를 관리하는 기능(history 저장?)
# st.session_state.messages : 대화 내용 유지, 대화 목록 확인



# 대화 내용 표시
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
# chat_input : 사용자가 채팅 입력
if prompt := st.chat_input("Gemini에게 물어보기"):
    # user 메시지 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    # chat_message: 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 출력
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 6. Gemini 스트리밍 호출
        try:
            # 과거 대화 기록
            history = [
                types.Content(
                    role="user" if m["role"] == "user" else "model",
                    parts=[{"text": m["content"]}] 
                ) for m in st.session_state.messages[:-1] # 마지막 질문 제외한 과거 기록
            ]
            
            # 응답 생성
            response = st.session_state.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7
                ),
                history=history # 이전 대화 맥락 전달
            )
          
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # 7. AI 응답 기록 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")