import streamlit as st
from src.Query import Query
import os

def main():
    st.header("Medical Chatbot")
    with st.sidebar:
        OPENAI_API_KEY = st.text_input("Enter your OPENAI_API_KEY:")
        if st.button("Enter"):
            os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
            st.session_state.api_key_provided = True
            
        if 'api_key_provided' in st.session_state and st.session_state.api_key_provided:
            if 's_id' in  st.session_state and st.session_state.s_id:
                
                st.write(st.session_state.s_id)
                

    if 'api_key_provided' in st.session_state and st.session_state.api_key_provided:
         
         user_query=st.text_input("Hello! I'm your friendly medical assistant. How can I help you today with your health concerns?")
         if st.button("submit"):
            initialization=Query()
            if 's_id' not in  st.session_state or not st.session_state.s_id: 
                s_id,response=initialization.handle_user_input(user_query,None) 
                st.session_state.s_id=s_id
                #st.write("ifcondition")
            else:
                s_id,response=initialization.handle_user_input(user_query,st.session_state.s_id)
                #st.write("elsecondition")
            st.write(response)
            #st.write(s_id)

if __name__=="__main__":
    
    main()

             
