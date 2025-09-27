from fastapi import Blueprint, request, jsonify

bank_router = Blueprint('bank_router', __name__)

# Массив для хранения банковских счетов
bank_accounts = [100, 200, 0]

@bank_router.route('/', methods=['POST'])
def add_account():
    """
    POST /bank/
    Добавляет новый счет в массив.
    """
    new_balance = 0
    bank_accounts.append(new_balance)
    return jsonify({"message": f"Новый счет успешно добавлен. ID: {len(bank_accounts) - 1}, Баланс: {new_balance}"}), 201

@bank_router.route('/<int:account_id>', methods=['GET'])
def get_balance(account_id):
    """
    GET /bank/<id>
    Получает баланс счета по его ID.
    """
    if 0 <= account_id < len(bank_accounts):
        return jsonify({"account_id": account_id, "balance": bank_accounts[account_id]}), 200
    else:
        return jsonify({"message": f"Счет с ID {account_id} не найден."}), 404

@bank_router.route('/<int:account_id>', methods=['PUT'])
def update_balance(account_id):
    """
    PUT /bank/<id>
    Изменяет баланс счета.
    Ожидает JSON с ключом 'balance_change' (int).
    """
    data = request.get_json()
    balance_change = data.get('balance_change')

    if balance_change is None:
        return jsonify({"message": "Параметр 'balance_change' (int) не предоставлен."}), 400

    try:
        balance_change = int(balance_change)
    except ValueError:
        return jsonify({"message": "Некорректный формат 'balance_change'. Должно быть целым числом."}), 400

    if 0 <= account_id < len(bank_accounts):
        bank_accounts[account_id] += balance_change
        return jsonify({
            "message": f"Баланс счета ID {account_id} изменен.",
            "account_id": account_id,
            "new_balance": bank_accounts[account_id]
        }), 200
    else:
        return jsonify({"message": f"Счет с ID {account_id} не найден."}), 404

@bank_router.route('/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """
    DELETE /bank/<id>
    Удаляет счет по его ID.
    """
    if 0 <= account_id < len(bank_accounts):
        deleted_balance = bank_accounts.pop(account_id)
        return jsonify({
            "message": f"Счет с ID {account_id} успешно удален.",
            "deleted_balance": deleted_balance
        }), 200
    else:
        return jsonify({"message": f"Счет с ID {account_id} не найден."}), 404

@bank_router.route('/', methods=['GET'])
def get_all_accounts():
    """
    GET /bank/
    Получает список всех счетов и их балансов.
    """
    return jsonify({
        "accounts": [{"id": i, "balance": balance} for i, balance in enumerate(bank_accounts)]

    }), 200
