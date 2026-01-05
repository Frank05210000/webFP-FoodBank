from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config
from extensions import db, migrate
from models import User, Shop, Food, Order, OrderItem

app = Flask(__name__)
app.config.from_object(Config)

# 初始化擴充套件
db.init_app(app)
migrate.init_app(app, db)

# 登入管理
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def user_is(role):
    return current_user.is_authenticated and current_user.role == role

def shop_required():
    return current_user.is_authenticated and current_user.role == 'shop'

def _get_cart():
    return session.get('cart', {})

def _save_cart(cart):
    session['cart'] = cart
    session.modified = True

def _restock_order(order):
    for item in order.items.all():
        if item.food:
            item.food.quantity = (item.food.quantity or 0) + item.quantity

def _delete_order(order):
    for item in order.items.all():
        db.session.delete(item)
    db.session.delete(order)

def _delete_shop(shop):
    for order in shop.orders.all():
        _delete_order(order)
    for food in shop.foods.all():
        db.session.delete(food)
    db.session.delete(shop)

@app.route('/')
def index():
    shops = Shop.query.all()
    return render_template('index.html', shops=shops)

# --- 認證流程 ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('此 Email 已註冊', 'warning')
            return redirect(url_for('register'))
        user = User(name=name, email=email, phone=phone, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('註冊成功，歡迎加入！', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/register/shop', methods=['GET', 'POST'])
def register_shop():
    if request.method == 'POST':
        owner_name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        shop_name = request.form.get('shop_name')
        address = request.form.get('address')
        opening_time = request.form.get('opening_time')
        closing_time = request.form.get('closing_time')
        latitude = request.form.get('latitude') or None
        longitude = request.form.get('longitude') or None

        if User.query.filter_by(email=email).first():
            flash('此 Email 已註冊', 'warning')
            return redirect(url_for('register_shop'))

        user = User(name=owner_name, email=email, phone=phone, role='shop')
        user.set_password(password)
        shop = Shop(
            name=shop_name,
            manager_email=email,
            phone=phone,
            address=address,
            opening_time=datetime.strptime(opening_time, '%H:%M').time() if opening_time else None,
            closing_time=datetime.strptime(closing_time, '%H:%M').time() if closing_time else None,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            owner=user
        )
        db.session.add(user)
        db.session.add(shop)
        db.session.commit()
        login_user(user)
        flash('商家註冊成功，開始上架物資吧！', 'success')
        return redirect(url_for('shop_dashboard'))
    return render_template('register_shop.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('登入成功', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('帳號或密碼錯誤', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('index'))

# --- 民眾端 ---
@app.route('/shops/<int:shop_id>')
def shop_detail(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    foods = Food.query.filter_by(shop_id=shop_id, is_active=True).all()
    return render_template('shop_detail.html', shop=shop, foods=foods)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    food_id = int(request.form.get('food_id'))
    quantity = int(request.form.get('quantity', 1))
    food = Food.query.get_or_404(food_id)
    cart = _get_cart()

    # 確保購物車僅包含同一商家
    existing_shop = cart.get('shop_id')
    if existing_shop and existing_shop != food.shop_id:
        flash('購物車已包含其他商家的品項，請先結帳或清空。', 'warning')
        return redirect(url_for('shop_detail', shop_id=food.shop_id))

    items = cart.get('items', {})
    current_qty = items.get(str(food_id), 0)
    items[str(food_id)] = min(food.quantity, current_qty + quantity)
    cart['items'] = items
    cart['shop_id'] = food.shop_id
    _save_cart(cart)
    flash(f'{food.name} 已加入購物車', 'success')
    return redirect(url_for('shop_detail', shop_id=food.shop_id))

@app.route('/cart/remove/<int:food_id>', methods=['POST'])
def remove_from_cart(food_id):
    cart = _get_cart()
    items = cart.get('items', {})
    if str(food_id) in items:
        items.pop(str(food_id))
    cart['items'] = items
    if not items:
        cart.clear()
    _save_cart(cart)
    flash('已移除品項', 'info')
    return redirect(url_for('checkout'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = _get_cart()
    items = cart.get('items', {})
    if not items:
        flash('購物車是空的', 'info')
        return redirect(url_for('index'))

    foods = Food.query.filter(Food.id.in_(map(int, items.keys()))).all()
    food_map = {food.id: food for food in foods}
    shop = Shop.query.get(cart.get('shop_id'))

    if request.method == 'POST':
        pickup_time_str = request.form.get('pickup_time')
        if not pickup_time_str:
            flash('請選擇取貨時間', 'warning')
            return redirect(url_for('checkout'))

        pickup_dt = datetime.combine(date.today(), datetime.strptime(pickup_time_str, '%H:%M').time())
        now = datetime.now()
        if pickup_dt <= now:
            flash('取貨時間需晚於現在', 'warning')
            return redirect(url_for('checkout'))
        if shop and shop.closing_time and pickup_dt.time() > shop.closing_time:
            flash('取貨時間不可超過營業時間', 'warning')
            return redirect(url_for('checkout'))

        order = Order(user_id=current_user.id, shop_id=shop.id, pickup_time=pickup_dt, status='pending')
        db.session.add(order)

        for fid_str, qty in items.items():
            food = food_map.get(int(fid_str))
            if not food:
                continue
            qty_to_book = min(food.quantity, int(qty))
            food.quantity = max(0, food.quantity - qty_to_book)
            order_item = OrderItem(order=order, food_id=food.id, quantity=qty_to_book)
            db.session.add(order_item)
        db.session.commit()
        session.pop('cart', None)
        flash('預訂成功！', 'success')
        return redirect(url_for('order_success', order_id=order.id))

    return render_template('checkout.html', items=items, foods=food_map, shop=shop)

@app.route('/orders/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not user_is('admin'):
        flash('無權查看此訂單', 'danger')
        return redirect(url_for('index'))
    return render_template('order_success.html', order=order)

@app.route('/orders')
@login_required
def orders():
    all_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=all_orders)

@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    user_is_order_owner = order.user_id == current_user.id
    user_is_shop_owner = shop_required() and current_user.shop and current_user.shop.id == order.shop_id
    if not (user_is_order_owner or user_is_shop_owner or user_is('admin')):
        abort(403)
    if order.status == 'completed':
        flash('已完成的訂單無法取消', 'warning')
        return redirect(request.referrer or url_for('orders'))
    if order.status != 'cancelled':
        _restock_order(order)
        order.status = 'cancelled'
        order.completed_at = None
        db.session.commit()
        flash('訂單已取消', 'info')
    else:
        flash('訂單已取消', 'info')
    return redirect(request.referrer or url_for('orders'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        db.session.commit()
        flash('帳號已更新', 'success')
        return redirect(url_for('account'))
    return render_template('account.html')

# --- 商家後台 ---
@app.route('/shop/dashboard')
@login_required
def shop_dashboard():
    if not shop_required():
        flash('只有商家可以存取', 'danger')
        return redirect(url_for('index'))
    shop = current_user.shop
    foods = shop.foods.order_by(Food.created_at.desc()).all() if shop else []
    pending_orders = shop.orders.order_by(Order.created_at.desc()).all() if shop else []
    return render_template('shop_dashboard.html', shop=shop, foods=foods, orders=pending_orders)

@app.route('/shop/foods/new', methods=['GET', 'POST'])
@login_required
def new_food():
    if not shop_required():
        flash('只有商家可以存取', 'danger')
        return redirect(url_for('index'))
    shop = current_user.shop
    if request.method == 'POST':
        food = Food(
            shop_id=shop.id,
            name=request.form.get('name'),
            category=request.form.get('category'),
            quantity=int(request.form.get('quantity') or 0),
            expiry_time=datetime.strptime(request.form.get('expiry_time'), '%Y-%m-%d') if request.form.get('expiry_time') else None,
            photo_url=request.form.get('photo_url'),
            description=request.form.get('description'),
            is_active=True
        )
        db.session.add(food)
        db.session.commit()
        flash('已新增物資', 'success')
        return redirect(url_for('shop_dashboard'))
    return render_template('food_form.html', action='create')

@app.route('/shop/foods/<int:food_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_food(food_id):
    if not shop_required():
        flash('只有商家可以存取', 'danger')
        return redirect(url_for('index'))
    food = Food.query.get_or_404(food_id)
    if request.method == 'POST':
        food.name = request.form.get('name')
        food.category = request.form.get('category')
        food.quantity = int(request.form.get('quantity') or 0)
        food.expiry_time = datetime.strptime(request.form.get('expiry_time'), '%Y-%m-%d') if request.form.get('expiry_time') else None
        food.photo_url = request.form.get('photo_url')
        food.description = request.form.get('description')
        food.is_active = request.form.get('is_active') == 'true'
        db.session.commit()
        flash('已更新物資', 'success')
        return redirect(url_for('shop_dashboard'))
    return render_template('food_form.html', action='edit', food=food)

@app.route('/shop/foods/<int:food_id>/delete', methods=['POST'])
@login_required
def delete_food(food_id):
    if not shop_required():
        flash('只有商家可以存取', 'danger')
        return redirect(url_for('index'))
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('已刪除物資', 'info')
    return redirect(url_for('shop_dashboard'))

@app.route('/shop/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not shop_required():
        flash('只有商家可以存取', 'danger')
        return redirect(url_for('index'))
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status not in ['pending', 'completed', 'cancelled']:
        flash('無效的狀態', 'warning')
        return redirect(url_for('shop_dashboard'))
    if order.status == 'cancelled' and status != 'cancelled':
        flash('已取消的訂單無法更改狀態', 'warning')
        return redirect(url_for('shop_dashboard'))
    if status == 'cancelled' and order.status != 'cancelled':
        _restock_order(order)
    order.status = status
    if status == 'completed':
        order.completed_at = datetime.utcnow()
    else:
        order.completed_at = None
    db.session.commit()
    flash('訂單狀態已更新', 'success')
    return redirect(url_for('shop_dashboard'))

# --- 後台管理 ---
@app.route('/admin')
@login_required
def admin_dashboard():
    if not user_is('admin'):
        flash('只有管理者可以存取', 'danger')
        return redirect(url_for('index'))
    shops = Shop.query.all()
    users = User.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(20).all()
    stats = {
        'total_orders': Order.query.count(),
        'total_users': User.query.filter_by(role='user').count(),
        'total_shops': Shop.query.count()
    }
    return render_template('admin_dashboard.html', shops=shops, users=users, orders=orders, stats=stats)

@app.route('/admin/shops/<int:shop_id>/delete', methods=['POST'])
@login_required
def delete_shop(shop_id):
    if not user_is('admin'):
        abort(403)
    shop = Shop.query.get_or_404(shop_id)
    _delete_shop(shop)
    db.session.commit()
    flash('商家已刪除', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not user_is('admin'):
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id or user.role == 'admin':
        flash('無法刪除管理者帳號', 'warning')
        return redirect(url_for('admin_dashboard'))
    for order in user.orders.all():
        _delete_order(order)
    if user.shop:
        _delete_shop(user.shop)
    db.session.delete(user)
    db.session.commit()
    flash('用戶已刪除', 'info')
    return redirect(url_for('admin_dashboard'))

# 建立資料庫表格的 CLI 指令 (方便開發使用)
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
