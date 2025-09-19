import random
from goida import Blueprint, request, jsonify, session

guess_router = Blueprint('guess_router', __name__)

current_random_number = None

@guess_router.route('/start', methods=['GET', 'POST'])
def start_game():
    global current_random_number
    if request.method == 'POST':
        # Начинаем игру, генерируем новое число
        current_random_number = random.randint(0, 10)
        session['guess_attempts'] = 0  # Сбрасываем попытки
        print(f"DEBUG: Случайное число для игры: {current_random_number}") # Отладочная информация
        return jsonify({"message": "Игра 'Угадай число' началась! Попробуйте угадать число от 0 до 10."}), 200
    else:
        # Если GET запрос, проверяем, начата ли игра
        if current_random_number is None:
            return jsonify({"message": "Игра еще не начата. Используйте POST запрос на /guess/start для начала."}), 400
        return jsonify({"message": "Игра 'Угадай число' активна. Попробуйте угадать число от 0 до 10."}), 200

@guess_router.route('/guess', methods=['POST'])
def make_guess():
    global current_random_number
    if current_random_number is None:
        return jsonify({"message": "Игра не начата. Начните игру с POST запросом на /guess/start."}), 400

    data = request.get_json()
    user_guess = data.get('guess')

    if user_guess is None:
        return jsonify({"message": "Число для угадывания не предоставлено."}), 400

    try:
        user_guess = int(user_guess)
    except ValueError:
        return jsonify({"message": "Некорректный формат числа."}), 400

    session['guess_attempts'] = session.get('guess_attempts', 0) + 1

    if user_guess == current_random_number:
        message = f"Поздравляем! Вы угадали число {current_random_number} за {session['guess_attempts']} попыток!"
        current_random_number = None  # Сбрасываем игру после успешного угадывания
        session.pop('guess_attempts', None) # Удаляем попытки из сессии
        return jsonify({"message": message, "won": True}), 200
    elif user_guess < current_random_number:
        return jsonify({"message": "Ваше число меньше. Попробуйте еще раз."}), 200
    else: # user_guess > current_random_number
        return jsonify({"message": "Ваше число больше. Попробуйте еще раз."}), 200

@guess_router.route('/end', methods=['POST'])
def end_game():
    global current_random_number
    if current_random_number is not None:
        message = f"Игра завершена. Загаданное число было: {current_random_number}."
        current_random_number = None
        session.pop('guess_attempts', None)
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": "Игра не была активна."}), 200