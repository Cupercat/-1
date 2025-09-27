from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class BankAccount(BaseModel):
    username: str
    balance: float = 0.0

accounts_db: Dict[str, BankAccount] = {}

@app.post("/accounts", response_model=BankAccount)
def create_account(username: str):
    """
    Создает новый банковский аккаунт.
    """
    if username in accounts_db:
        raise HTTPException(status_code=400, detail="Аккаунт с таким username уже существует.")
    new_account = BankAccount(username=username, balance=0.0)
    accounts_db[username] = new_account
    return new_account

@app.get("/accounts/{username}", response_model=BankAccount)
def get_account(username: str):
    """
    Получает данные о конкретном банковском аккаунте.
    """
    account = accounts_db.get(username)
    if not account:
        raise HTTPException(status_code=404, detail="Аккаунт не найден.")
    return account

@app.put("/accounts/{username}")
def update_balance(username: str, bal: float):
    """
    Изменяет баланс банковского аккаунта, прибавляя указанную сумму.
    """
    account = accounts_db.get(username)
    if not account:
        raise HTTPException(status_code=404, detail="Аккаунт не найден.")
    account.balance += bal
    accounts_db[username] = account  # Обновляем в "базе данных"
    return {"message": f"Баланс аккаунта '{username}' изменен. Новый баланс: {account.balance}"}

@app.delete("/accounts/{username}")
def delete_account(username: str):
    """
    Удаляет банковский аккаунт.
    """
    if username not in accounts_db:
        raise HTTPException(status_code=404, detail="Аккаунт не найден.")
    del accounts_db[username]
    return {"message": f"Аккаунт '{username}' успешно удален."}
