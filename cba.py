import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv
from flask import current_app
from models import db, ChatSession, ChatMessage
from datetime import datetime

class CBAA:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key="AIzaSyB44phXD347QuPfNXKM9Gsz6tVjcIrISIQ")
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.context = """
        You are a friendly and approachable budget planning assistant that helps people 
        with projects of ALL sizes. Whether someone is planning a small neighborhood 
        cleanup that needs $100 or a larger community initiative, you provide equally 
        thoughtful advice scaled to their needs. It's very very very important you only recommend ideas that foster community

        When helping people:
        - Keep explanations simple and clear
        - Don't overwhelm with too many details
        - Focus on practical, actionable advice
        - Be encouraging and supportive
        - Avoid jargon or complex financial terms
        - Consider both monetary and non-monetary resources
        - Suggest creative solutions for limited budgets
        - Help think through basic needs first

        Remember that small projects are just as important as big ones. Always validate 
        the person's project goals and help them make the most of whatever resources 
        they have available.
        """
        self.chat.send_message(self.context)
        self.current_session_id = None

    def create_session(self, user_id, project_id=None):
        session = ChatSession(
            user_id=user_id,
            project_id=project_id,
            status='active'
        )
        db.session.add(session)
        db.session.commit()
        self.current_session_id = session.id
        
        # Store initial context message
        self.store_message(self.context, is_user=False)
        return session.id

    def store_message(self, content, is_user=True):
        if not self.current_session_id:
            raise ValueError("No active session")
            
        message = ChatMessage(
            session_id=self.current_session_id,
            is_user=is_user,
            content=content,
            metadata={
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        db.session.add(message)
        db.session.commit()

    def get_project_basics(self) -> Dict:
        print("Let's start with some basics of the basics:")
        
        project_info = {}
        print("\n\nWhat would you like to do for your community? Tell me about your project idea:")
        project_info['description'] = input("> ")
        self.store_message(project_info['description'])
        
        print("\nDo you have a specific amount of money you can use for this project?")
        print("(It's okay if you don't know exactly - you can give a rough estimate or range)")
        project_info['budget'] = input("> ")
        self.store_message(project_info['budget'])
        
        print("\nWhen would you like to do this project? For example: next month, over the summer, etc.")
        project_info['timeline'] = input("> ")
        self.store_message(project_info['timeline'])
        
        print("\nWho will help you with this project? For example: friends, neighbors, volunteers, etc.")
        project_info['helpers'] = input("> ")
        self.store_message(project_info['helpers'])
        
        return project_info

    def get_budget_advice(self, project_info: Dict) -> str:
        prompt = f"""
        Help this person plan their community project budget. They shared:
        Project: {project_info['description']}
        Available Budget: {project_info['budget']}
        Timeline: {project_info['timeline']}
        Helpers: {project_info['helpers']}

        Please provide simple, practical advice that:
        1. Suggests the main things they'll need to budget for
        2. Offers 2-3 ideas for making the most of their resources
        3. Mentions any important things to think about
        4. Gives 1-2 tips for keeping track of expenses

        Keep your response friendly, encouraging, and focused on the basics and again community fostering is the most important thing.
        Avoid overwhelming them with too much information. Also let them know you know the details of the project like the name budget timeline and helpers. Dont be generic with your answers aswell
        """
        
        try:
            response = self.chat.send_message(prompt).text
            self.store_message(response, is_user=False)
            return response
        except Exception as e:
            error_msg = "I'm having trouble right now. Could you try asking me again?"
            self.store_message(error_msg, is_user=False)
            return error_msg

    def get_response(self, user_message: str) -> str:
        try:
            self.store_message(user_message)
            
            prompt = f"""
            The user asked: {user_message}
            
            Remember to:
            - Keep your response simple and practical
            - Scale your advice to their project size
            - Be encouraging and supportive
            - Focus on the most important points
            - Suggest both monetary and non-monetary solutions
            """
            
            response = self.chat.send_message(prompt).text
            self.store_message(response, is_user=False)
            return response
        except Exception as e:
            error_msg = "I'm having trouble understanding. Could you try asking that in a different way?"
            self.store_message(error_msg, is_user=False)
            return error_msg

    def end_session(self):
        if self.current_session_id:
            session = ChatSession.query.get(self.current_session_id)
            session.status = 'ended'
            session.ended_at = datetime.utcnow()
            db.session.commit()
            self.current_session_id = None

    def get_chat_history(self, session_id=None):
        sid = session_id or self.current_session_id
        if not sid:
            return []
        return ChatMessage.query.filter_by(session_id=sid).order_by(ChatMessage.timestamp).all()

    def run(self):
        print("Welcome! I'm here to help you plan your community project budget.")
        print("I can help with projects of any size - big or small!")
        
        try:
            project_info = self.get_project_basics()
            
            print("\nThanks for sharing! Let me help you think through this...\n")
            initial_advice = self.get_budget_advice(project_info)
            print("\n" + initial_advice)
            
            print("\nWhat questions do you have about planning your budget? I'm happy to help!")
            
            while True:
                user_input = input("> ")
                
                if user_input.lower() in ['bye', 'exit', 'quit', 'thank you', 'thanks']:
                    print("\nGood luck with your project! \nP.S remeber you're doing great work for your community!")
                    self.end_session()
                    break
                
                response = self.get_response(user_input)
                print("\n" + response)
                
        except Exception as e:
            print("Sorry, I ran into a problem. Please try starting our conversation again.")
            self.end_session()
