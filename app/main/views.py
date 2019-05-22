from flask import render_template, redirect, url_for, flash, session, current_app
from flask_login import login_required, current_user
from . import main, forms
from app import db
from app.models import Item, Order
from valve.source import a2s


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/items')
def items_list():
    items = Item.query.all()
    return render_template('items.html', items=items)


@main.route('/item/<int:item_id>')
def item(item_id=0):
    session['buy_item'] = item_id
    data = Item.query.get_or_404(item_id)
    return render_template('item.html', item=data)


@main.route('/info-server')
def info_server():
    try:
        app = current_app
        server = a2s.ServerQuerier((app.config['SERVER_IP'], app.config['SERVER_PORT']))
        players = server.get_players()
        info = server.get_info()
        rules = server.get_rules()
        info.connect = '{}:{}'.format(server.host, rules['rules']['HOSTPORT'])
    except a2s.NoResponseError:
        players = {}
        info = {}
        rules = {}

    return render_template('info_server.html', players=players, info=info, rules=rules)


@main.route('/white-list')
def white_list():
    return render_template('white_list.html')


@main.route('/order', methods=['POST', 'GET'])
@login_required
def order():
    form = forms.BuyForm()
    item_id = session.get('buy_item')
    data = Item.query.get_or_404(item_id)
    if form.validate_on_submit():

        order = Order(item_id=item_id, login=form.login.data, steam_id=form.steam_id.data, sum=data.price)
        db.session.add(order)
        db.session.commit()
        flash('Все ок, заказ на товар <b>%s</b> оформлен ' % data.title)
        return redirect(url_for('main.item', item_id=item_id))
    return render_template('form_order.html', form=form, item=data, user=current_user)


@main.route('/news')
def news_list():
    return render_template('news.html')
