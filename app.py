import os
import logging
from flask import Flask, render_template, request, jsonify, session
from story_generator import StoryGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Initialize story generator with API key from environment
gemini_api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyD8qDZjChLT7CwQ1Lj9auydy3QcQnPjaTg")
story_generator = StoryGenerator(api_key=gemini_api_key)

@app.route('/')
def index():
    # Clear any existing game session
    session.clear()
    return render_template('game.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    try:
        # Initialize session variables
        session['points'] = 0
        session['choices_made'] = 0
        
        # Generate initial story
        initial_story = story_generator.generate_initial_story()

        # Store story context in session
        session['story_context'] = [initial_story]

        return jsonify({
            'success': True,
            'story': initial_story
        })
    except Exception as e:
        logger.error(f"Error starting game: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'عذراً، حدث خطأ أثناء بدء اللعبة. يرجى المحاولة مرة أخرى.'
        }), 500

@app.route('/continue-story', methods=['POST'])
def continue_story():
    try:
        user_input = request.json.get('userInput')

        if not user_input:
            return jsonify({
                'success': False,
                'error': 'الرجاء إدخال نص'
            }), 400

        # Get story context from session
        story_context = session.get('story_context', [])

        # Generate next part of the story
        next_part = story_generator.continue_story(story_context, user_input)

        # Update story context
        story_context.append(user_input)
        story_context.append(next_part)
        session['story_context'] = story_context

        return jsonify({
            'success': True,
            'story': next_part
        })
    except Exception as e:
        logger.error(f"Error continuing story: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'عذراً، حدث خطأ أثناء توليد القصة. يرجى المحاولة مرة أخرى.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)