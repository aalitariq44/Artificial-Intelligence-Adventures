import google.generativeai as genai
import logging

class StoryGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_initial_story(self):
        prompt = """
        أنت كاتب قصص تفاعلي. قم بكتابة بداية قصة مثيرة باللغة العربية (حوالي 3-4 جمل).
        يجب أن تنتهي القصة بخيار أو سؤال للقارئ ليقرر ما سيحدث بعد ذلك.
        اجعل القصة مشوقة ومثيرة للاهتمام.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating initial story: {str(e)}")
            raise Exception("فشل في توليد القصة الأولية")

    def continue_story(self, story_context, user_input):
        context = "\n".join(story_context)
        
        prompt = f"""
        سياق القصة حتى الآن:
        {context}

        رد المستخدم:
        {user_input}

        استمر في القصة بناءً على رد المستخدم (3-4 جمل).
        انتهِ دائماً بسؤال أو خيار للمستخدم ليقرر ما سيحدث بعد ذلك.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error continuing story: {str(e)}")
            raise Exception("فشل في توليد الجزء التالي من القصة")
