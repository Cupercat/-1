from fastapi import Blueprint, request, jsonify, session

login_router = Blueprint('login_router', __name__)

# Простой пароль для примера
CORRECT_PASSWORD = "123"

@login_router.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    password = data.get('password')

    if not password:
        return jsonify({"message": "Пароль не предоставлен"}), 400

    if password == CORRECT_PASSWORD:
        # В реальном приложении здесь была бы более сложная аутентификация
        session['authenticated'] = True
        return jsonify({"message": "Аутентификация успешна!", "next_step": "/guess/start"}), 200
    else:
        # Если пароль неверный, перенаправляем на угадай число
        return jsonify({"message": "Неверный пароль. Попробуйте угадать число!", "next_step": "/guess/start"}), 401

# Дополнительный роут для проверки статуса аутентификации (для примера)
@login_router.route('/status', methods=['GET'])
def auth_status():

    return jsonify({"authenticated": session.get('authenticated', False)})
