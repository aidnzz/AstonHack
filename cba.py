import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv
import json

class CBA:
    def __init__(self):
        # Load the API key from environment variables
        load_dotenv()
        genai.configure(api_key="AIzaSyB44phXD347QuPfNXKM9Gsz6tVjcIrISIQ")
        
        # Set up the Gemini model for chat
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Start a chat with initial context about being helpful for all project sizes
        self.chat = self.model.start_chat(history=[])
        
        # Define the chatbot's personality and approach
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
        
        # Send the initial context to Gemini
        self.chat.send_message(self.context)

    def get_project_basics(self) -> Dict:
        """
        Gathers essential project information through simple questions.
        Keeps the conversation friendly and approachable.
        """
        print("Let's start with some basics of the basics:")
        
        # Gather key project details with simple questions
        project_info = {}
        
        print("\n\nWhat would you like to do for your community? Tell me about your project idea:")
        project_info['description'] = input("> ")
        
        print("\nDo you have a specific amount of money you can use for this project?")
        print("(It's okay if you don't know exactly - you can give a rough estimate or range)")
        project_info['budget'] = input("> ")
        
        print("\nWhen would you like to do this project? For example: next month, over the summer, etc.")
        project_info['timeline'] = input("> ")
        
        print("\nWho will help you with this project? For example: friends, neighbors, volunteers, etc.")
        project_info['helpers'] = input("> ")
        
        return project_info

    def get_budget_advice(self, project_info: Dict) -> str:
        """
        Generates simple, practical budget advice tailored to the project size.
        """
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
        Avoid overwhelming them with too much information.
        """
        
        try:
            response = self.chat.send_message(prompt).text
            return response
        except Exception as e:
            return "I'm having trouble right now. Could you try asking me again?"

    def get_response(self, user_message: str) -> str:
        """
        Processes user messages and returns helpful responses.
        """
        try:
            # Guide Gemini to give appropriately scaled advice
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
            return response
        except Exception as e:
            return "I'm having trouble understanding. Could you try asking that in a different way?"

    def run(self):
        """
        Runs the main chatbot conversation loop.
        Keeps the interaction simple and friendly.
        """
        print("Welcome! I'm here to help you plan your community project budget.")
        print("I can help with projects of any size - big or small!")
        
        try:
            # Start by gathering basic project information
            project_info = self.get_project_basics()
            
            # Provide initial budget advice
            print("\nThanks for sharing! Let me help you think through this...\n")
            initial_advice = self.get_budget_advice(project_info)
            print("\n" + initial_advice)
            
            # Continue conversation
            print("\nWhat questions do you have about planning your budget? I'm happy to help!")
            
            while True:
                user_input = input("> ")
                
                if user_input.lower() in ['bye', 'exit', 'quit', 'thank you', 'thanks']:
                    print("\nGood luck with your project! \nP.S remeber you're doing great work for your community!")
                    break
                
                response = self.get_response(user_input)
                print("\n" + response)
                
        except Exception as e:
            print("Sorry, I ran into a problem. Please try starting our conversation again.")

if __name__ == "__main__":
    # Create and run the budget bot
    bot = CBA()
    bot.run()