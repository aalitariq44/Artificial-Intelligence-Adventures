import google.generativeai as genai
import logging
import random

class StoryGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.player_stats = {
            'health': 100,
            'reputation': 50,
            'wisdom': 0
        }

        self.decision_impacts = {
            'brave': {'health': -10, 'reputation': 15, 'points': 20},
            'cautious': {'health': 5, 'reputation': 5, 'points': 10},
            'clever': {'health': 0, 'reputation': 10, 'points': 15},
            'aggressive': {'health': -15, 'reputation': -5, 'points': 25}
        }

        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            raise Exception("فشل في تهيئة النموذج")

        self.story_types = {
            'survival': ['نجاة من كارثة', 'بقاء في صحراء', 'هروب من خطر'],
            'horror': ['منزل مسكون', 'مواجهة وحش', 'ظاهرة غامضة'],
            'adventure': ['بحث عن كنز', 'مغامرة في الغابة', 'اكتشاف سر قديم'],
            'crime': ['حل لغز', 'مطاردة مجرم', 'كشف مؤامرة'],
            'scifi': ['رحلة فضائية', 'مواجهة روبوتات', 'سفر عبر الزمن']
        }

    def _evaluate_decision(self, user_input):
        input_lower = user_input.lower()
        if 'هجوم' in input_lower or 'قتال' in input_lower:
            return 'aggressive'
        elif 'حكمة' in input_lower or 'تفكير' in input_lower:
            return 'clever'
        elif 'حذر' in input_lower or 'تراجع' in input_lower:
            return 'cautious'
        else:
            return 'brave'

    def _get_random_scenario(self):
        genre = random.choice(list(self.story_types.keys()))
        scenario = random.choice(self.story_types[genre])
        return genre, scenario

    def generate_initial_story(self):
        genre, scenario = self._get_random_scenario()

        prompt = f"""
        اكتب بداية قصيرة ومثيرة حول {scenario}.
        - اكتب فقرة قصيرة (2-3 جمل) تضع القارئ في موقف حرج
        - قدم خيارين واضحين للقارئ
        - اجعل كل خيار له عواقب محتملة مختلفة
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating initial story: {str(e)}")
            raise Exception("فشل في توليد القصة الأولية")

    def continue_story(self, story_context, user_input):
        decision_type = self._evaluate_decision(user_input)
        impacts = self.decision_impacts[decision_type]

        for stat, change in impacts.items():
            if stat in self.player_stats:
                self.player_stats[stat] = max(0, min(100, self.player_stats[stat] + change))

        context = "\n".join(story_context[-2:])  # نحتفظ فقط بآخر جزئين من السياق

        prompt = f"""
        آخر جزء من القصة:
        {context}

        قرار اللاعب:
        {user_input}

        اكتب استجابة قصيرة (2-3 جمل) تصف نتيجة القرار.
        قدم خيارين جديدين واضحين.
        الصحة: {self.player_stats['health']}
        السمعة: {self.player_stats['reputation']}
        """

        try:
            response = self.model.generate_content(prompt)
            return {
                'text': response.text,
                'points': impacts['points'],
                'stats': self.player_stats
            }
        except Exception as e:
            logging.error(f"Error continuing story: {str(e)}")
            raise Exception("فشل في توليد الجزء التالي من القصة")