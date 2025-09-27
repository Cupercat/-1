from fastapi import fastapi
from routers.login_router import login_router
from routers.guess_router import guess_router
from routers.bank_router import bank_router

app = fastapi(__name__)

# Регистрация роутеров
app.register_blueprint(login_router, url_prefix='/login')
app.register_blueprint(guess_router, url_prefix='/guess')
app.register_blueprint(bank_router, url_prefix='/bank')

if __name__ == '__main__':

    app.run(debug=True)
