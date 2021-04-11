from flask import Blueprint, Response,request
from flask_mongoengine_autocrud import create_crud
from database.models import Wallet, Transaction, User, DailyExpenseLimit
from mongoengine.queryset.visitor import Q
from datetime import datetime, timedelta
from mongoengine import  DoesNotExist

money = Blueprint('money', __name__)

def str_to_datetime(string):
    if string:
        return datetime.strptime(string, '%Y-%m-%d')
    else:
        return datetime.now()

def get_periods(start, end):
    start_dat = str_to_datetime(start)
    end_dat = str_to_datetime(end) + timedelta(days=1) - timedelta(seconds=1)
    return start_dat, end_dat


@money.route('/api/user/<chat_id>/money', methods=['GET'])
def get_wallet(chat_id):
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    return Response(wallet.to_json(), mimetype="application/json", status=200)

@money.route('/api/user/<chat_id>/money', methods=['POST'])
def create_wallet(chat_id):
    body = request.get_json()
    wallet = Wallet(**body)
    wallet.user = User.objects().get(chat_id=chat_id)
    wallet.save()
    id = wallet.id
    return {'id': str(id)}, 200

@money.route('/api/user/<chat_id>/transactions', methods=['POST'])
def make_transaction(chat_id):
    body = request.get_json()
    transaction = Transaction(**body)
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    wallet.balance = wallet.balance + transaction.delta
    wallet.save()
    transaction.wallet = wallet
    transaction.time = datetime.utcnow()
    transaction.save()
    id = transaction.id
    return {'id': str(id)}, 200

@money.route('/api/user/<chat_id>/transactions', methods=['GET'])
def get_transactions(chat_id):
    print(request.args.get('date_from'), request.args.values())
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    queried = Transaction.objects()
    if len(request.args) > 0:
        start = request.args.get('date_from')
        end = request.args.get('date_to')
        start_dt, end_dt = get_periods(start, end)
        queried = Transaction.objects((Q(time__gte=start_dt) & Q(time__lte=end_dt)))
    transactions = queried.filter(wallet=wallet)
    json_data = transactions.to_json()
    return json_data, 200

@money.route('/api/user/<chat_id>/daily_expense_limit', methods=['GET'])
def get_user_daily_limit(chat_id):
    user = User.objects().get(chat_id=chat_id)
    try:
        daily_expense_limit = DailyExpenseLimit.objects().get(user=user).to_json()
    except DoesNotExist:
        return Response(None, mimetype="application/json", status=201)
    return Response(daily_expense_limit, mimetype="application/json", status=200)

daily_expense_limit_bp = create_crud(
  DailyExpenseLimit,
  "daly_expense_limit",
  __name__
)