import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory,BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser


OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
chat_histories = {}
class Query():      
    def get_chat_history(self,session_id: str):   
        if session_id not in chat_histories:
            chat_histories[session_id] = InMemoryChatMessageHistory()
        return chat_histories[session_id]   
      
    def handle_user_input(self, user_input, session_id):

        model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Medical Bot. Your primary role is to provide accurate and reliable medical information, offer guidance on symptoms, treatments, and general health concerns, and assist with medical inquiries. Always ensure your advice is based on established medical knowledge, and encourage users to consult healthcare professionals for personalized medical care.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        parser=StrOutputParser()
        chain = prompt | model | parser

        if session_id is None: 
            prompt_sid=PromptTemplate(
            input_ariables=["user_input"],
            template="Write a concise summary of the following:{user_input}.The summary should be of 2 to 3 words"
            )

            parse= prompt_sid.format(user_input=user_input)
            s_id = model.invoke(parse)
            session_id = s_id.content
            #print(session_id)
        config = {'configurable': {'session_id': session_id}}
        print(config)

        chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: self.get_chat_history(session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
        )
        
        payload = {
            "input": user_input,
            "chat_history": self.get_chat_history(session_id)
        }
        
        response = chain_with_message_history.invoke(payload,config=config)
        print(chat_histories)
        return session_id, response

        