import google.generativeai as genai
import logging
import random

class StoryGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            raise Exception("فشل في تهيئة النموذج")

        self.story_types = {
            'survival': [
                'الهروب من السجن',
                'النجاة من تحطم طائرة',
                'البقاء في جزيرة مهجورة',
                'مواجهة كارثة طبيعية'
            ],
            'horror': [
                'منزل مسكون',
                'مستشفى مهجور',
                'غابة ملعونة',
                'مدينة الأشباح'
            ],
            'adventure': [
                'السفر عبر الزمن',
                'مواجهة تنين',
                'البحث عن كنز مفقود',
                'استكشاف حضارة قديمة'
            ],
            'crime': [
                'تحقيق غامض',
                'الهروب من الشرطة',
                'سرقة متحف',
                'كشف مؤامرة'
            ],
            'scifi': [
                'ذكاء اصطناعي متمرد',
                'اختراق أنظمة مستقبلية',
                'غزو فضائي',
                'استعمار كوكب جديد'
            ]
        }

    def _get_random_scenario(self):
        genre = random.choice(list(self.story_types.keys()))
        scenario = random.choice(self.story_types[genre])
        return genre, scenario

    def generate_initial_story(self):
        genre, scenario = self._get_random_scenario()

        prompt = f"""
        أنت كاتب قصص تفاعلي ماهر. اكتب بداية قصة مثيرة باللغة العربية تدور حول {scenario}.

        إرشادات مهمة:
        - اكتب 3-4 جمل قوية تضع القارئ مباشرة في قلب الأحداث
        - اجعل البداية مشوقة ومفاجئة
        - صف المشاعر والأجواء بتفاصيل حية
        - اطرح خيارات مثيرة للاهتمام في النهاية
        - ضع القارئ في موقف يتطلب قراراً مصيرياً

        انتهِ القصة بسؤال أو خيارات واضحة للقارئ ليقرر ما سيحدث بعد ذلك.
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

        إرشادات استكمال القصة:
        - استجب لقرار المستخدم بطريقة تؤثر على مسار القصة
        - أضف تحديات وتعقيدات جديدة غير متوقعة
        - اجعل القرارات تؤدي إلى نتائج مهمة
        - حافظ على التشويق والإثارة في كل منعطف
        - اكتب 3-4 جمل تصف ما يحدث نتيجة لقرار المستخدم

        انتهِ دائماً بخيارات جديدة أو سؤال يضع المستخدم أمام قرار مصيري آخر.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error continuing story: {str(e)}")
            raise Exception("فشل في توليد الجزء التالي من القصة")