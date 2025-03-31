from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import random
import os
import time
import csv
from datetime import datetime
from categories import all_categories

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production

@app.route('/register', methods=['POST'])
def register():
    session['user_data'] = {
        'name': request.form['name'],
        'age': request.form['age'],
        'profession': request.form['profession'],
        'start_time': time.time()
    }
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_data' not in session:
        return render_template('user_form.html')
  #if not is_logged_in():
  #return redirect(url_for('login'))

  # Select 4 random categories each time the index page is loaded
  selected_categories = random.sample(list(all_categories.keys()), 4)
  # Select words from these categories
  words = []
  for category in selected_categories:
    words.extend(random.sample(all_categories[category], 4))
  # Shuffle the words to mix the categories
  random.shuffle(words)

  # Initialize for a new game
  session['used_colors'] = []
  session['category_colors'] = {}
  session.pop('mistakes', None)  # Properly reset the 'mistakes' counter
  session['mistakes'] = 4
  session['already_guessed'] = []  # Initialize the already_guessed list
  session['grid'] = [words[i:i + 4] for i in range(0, 16, 4)]
  return render_template('index.html', grid=session['grid'])
  
@app.route('/submit_guess', methods=['POST'])
def submit_guess():
  data = request.get_json()
  selected_words = data.get('selectedWords', [])
  if not selected_words:
    return jsonify({'result': 'error', 'message': 'No words selected'})

  already_guessed = session.get('already_guessed', [])
  selected_words_set = frozenset(selected_words)

  if selected_words_set in map(
      frozenset, already_guessed
  ):  # Use map to ensure we compare correctly between list of lists and set
    return jsonify({
        'result': 'error',
        'message': 'Words have already been guessed!',
        'alreadyGuessed': True,
        'disableSubmit': True
    })

  first_word_category = None
  for category, words in all_categories.items():
    if selected_words[0] in words:
      first_word_category = category
      break

  if not first_word_category:
    return jsonify({
        'result': 'error',
        'message': 'First word not in any category'
    })

  all_correct = all(word in all_categories[first_word_category]
                    for word in selected_words)

  if not all_correct:
    session['mistakes'] = session.get('mistakes', 4) - 1
    already_guessed.append(selected_words)
    session['already_guessed'] = already_guessed
    return jsonify({
      'result': 'failure',
      'message': 'Try again!',
      'mistakes': session['mistakes'],
      'alreadyGuessed': False
  })
  else:
    # All words are in the same category, so handle the color assignment
    if first_word_category not in session['category_colors']:
      # Get difficulty level from categories
      difficulty_colors = {
          0: 'yellow',  # Easiest
          1: 'green',   # Medium-Easy
          2: 'blue',    # Difficult
          3: 'purple'   # Most Difficult
      }
      # Get index of category to determine difficulty (0-3)
      categories_list = list(all_categories.keys())
      difficulty_level = categories_list.index(first_word_category)
      color = difficulty_colors[difficulty_level]
      session['used_colors'].append(color)
      session['category_colors'][first_word_category] = color
  color = session['category_colors'][first_word_category]

  # Store the correct guess in the session
  already_guessed.append(selected_words_set)
  session['already_guessed'] = [list(guess) for guess in already_guessed]

  return jsonify({
      'result': 'success',
      'message': 'Yay! Category: ' + first_word_category,
      'color': color,
      'category': first_word_category,
      'words': all_categories[first_word_category],
      'alreadyGuessed': False
  })

@app.route('/complete_game', methods=['POST'])
def complete_game():
    if 'user_data' in session:
        end_time = time.time()
        duration = end_time - session['user_data']['start_time']
        
        # Save to CSV
        data = [
            session['user_data']['name'],
            session['user_data']['age'],
            session['user_data']['profession'],
            f"{duration:.2f}"
        ]
        
        with open('game_results.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if os.path.getsize('game_results.csv') == 0:
                writer.writerow(['Name', 'Age', 'Profession', 'Time (seconds)'])
            writer.writerow(data)
            
        session.pop('user_data', None)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})

if __name__ == '__main__':
  app.run(debug=True, port=5001, host='0.0.0.0')
