from flask import Flask, render_template, request, jsonify, session
import os
from bedrock_text_generator import BedrockTextGenerator
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Bedrock generator
generator = BedrockTextGenerator(region='us-east-1', model_id='amazon.nova-lite-v1:0')

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['total_tokens'] = 0
        session['message_count'] = 0
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    prompt_type = data.get('prompt_type', 'general')
    custom_prompt = data.get('custom_prompt', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Apply prompt engineering based on type
    if prompt_type == 'custom' and custom_prompt:
        final_prompt = f"{custom_prompt}\n\nUser Question: {user_message}"
    else:
        prompts = {
            'general': user_message,
            'detailed': f"Please provide a detailed and comprehensive answer to: {user_message}",
            'brief': f"Please provide a brief and concise answer to: {user_message}",
            'step_by_step': f"Please provide a step-by-step explanation for: {user_message}",
            'creative': f"Please provide a creative and engaging response to: {user_message}",
            'technical': f"Please provide a technical and precise answer to: {user_message}",
            'simple': f"Please explain in simple terms suitable for students: {user_message}"
        }
        final_prompt = prompts.get(prompt_type, user_message)
    
    # Generate response
    response = generator.generate_text(final_prompt, max_tokens=1000)
    
    # Update session stats
    session['message_count'] = session.get('message_count', 0) + 1
    session['total_tokens'] = session.get('total_tokens', 0) + len(user_message.split()) + len(response.split())
    
    return jsonify({
        'response': response,
        'tokens': session['total_tokens'],
        'message_count': session['message_count']
    })

@app.route('/reset', methods=['POST'])
def reset():
    session['total_tokens'] = 0
    session['message_count'] = 0
    session['session_id'] = str(uuid.uuid4())
    return jsonify({'status': 'success', 'message': 'Session reset successfully'})

@app.route('/change_model', methods=['POST'])
def change_model():
    data = request.json
    model_id = data.get('model_id', 'amazon.nova-lite-v1:0')
    
    global generator
    generator = BedrockTextGenerator(region='us-east-1', model_id=model_id)
    
    return jsonify({'status': 'success', 'model': model_id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
