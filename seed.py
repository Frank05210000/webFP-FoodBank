from app import app
from extensions import db
from models import Shop, Food, User
from datetime import datetime, timedelta

def seed_data():
    with app.app_context():
        # 清空現有資料
        db.drop_all()
        db.create_all()
        
        print("正在建立假資料...")

        # 建立基本帳號
        user = User(name="示範用戶", email="user@example.com", phone="0912-345-678", role="user")
        user.set_password("password")
        shop_owner1 = User(name="店長A", email="shop1@example.com", phone="02-1234-5678", role="shop")
        shop_owner1.set_password("password")
        shop_owner2 = User(name="店長B", email="shop2@example.com", phone="02-8765-4321", role="shop")
        shop_owner2.set_password("password")
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("admin123")
        db.session.add_all([user, shop_owner1, shop_owner2, admin])
        db.session.commit()

        # 建立商家
        shop1 = Shop(
            name="快樂超市 - 信義店",
            owner=shop_owner1,
            manager_email="shop1@example.com",
            phone="02-1234-5678",
            address="台北市信義區信義路五段7號",
            latitude=25.0330,
            longitude=121.5654, # 台北 101 附近
            opening_time=datetime.strptime("09:00", "%H:%M").time(),
            closing_time=datetime.strptime("22:00", "%H:%M").time(),
            rating=4.5
        )

        shop2 = Shop(
            name="愛心麵包坊",
            owner=shop_owner2,
            manager_email="shop2@example.com",
            phone="02-8765-4321",
            address="台北市信義區松高路11號",
            latitude=25.0390,
            longitude=121.5660, # 信義誠品附近
            opening_time=datetime.strptime("10:00", "%H:%M").time(),
            closing_time=datetime.strptime("20:00", "%H:%M").time(),
            rating=4.8
        )

        shop3 = Shop(
            name="全家便利商店 - 復興店",
            manager_email="shop3@example.com",
            phone="02-2222-3333",
            address="台北市大安區忠孝東路三段300號",
            latitude=25.0410,
            longitude=121.5430, # SOGO 復興館附近
            opening_time=datetime.strptime("00:00", "%H:%M").time(),
            closing_time=datetime.strptime("23:59", "%H:%M").time(),
            rating=4.2
        )

        db.session.add_all([shop1, shop2, shop3])
        db.session.commit()

        # 建立食物
        foods = [
            Food(
                shop_id=shop1.id,
                name="即期吐司",
                category="麵包",
                quantity=12,
                expiry_time=datetime.now() + timedelta(days=1),
                description="白吐司一條，保存期限至明日",
                photo_url="https://placehold.co/300x200?text=Toast"
            ),
            Food(
                shop_id=shop1.id,
                name="有機蔬菜包",
                category="生鮮",
                quantity=8,
                expiry_time=datetime.now() + timedelta(days=2),
                description="當季蔬菜組合",
                photo_url="https://placehold.co/300x200?text=Veggies"
            ),
            Food(
                shop_id=shop1.id,
                name="水果禮盒",
                category="水果",
                quantity=6,
                expiry_time=datetime.now() + timedelta(days=3),
                description="當季水果禮盒",
                photo_url="https://placehold.co/300x200?text=Fruit"
            ),
            Food(
                shop_id=shop2.id,
                name="綜合麵包袋",
                category="麵包",
                quantity=10,
                expiry_time=datetime.now() + timedelta(hours=8),
                description="今日現烤麵包福袋",
                photo_url="https://placehold.co/300x200?text=Bread"
            ),
            Food(
                shop_id=shop2.id,
                name="沙拉盒",
                category="輕食",
                quantity=5,
                expiry_time=datetime.now() + timedelta(hours=10),
                description="清爽沙拉組合",
                photo_url="https://placehold.co/300x200?text=Salad"
            ),
            Food(
                shop_id=shop3.id,
                name="御飯糰",
                category="便當",
                quantity=15,
                expiry_time=datetime.now() + timedelta(hours=6),
                description="鮪魚口味御飯糰",
                photo_url="https://placehold.co/300x200?text=RiceBall"
            ),
            Food(
                shop_id=shop3.id,
                name="熟食便當",
                category="便當",
                quantity=7,
                expiry_time=datetime.now() + timedelta(hours=5),
                description="便利商店熱食便當",
                photo_url="https://placehold.co/300x200?text=Bento"
            )
        ]

        db.session.add_all(foods)
        db.session.commit()

        print("假資料建立完成！")

if __name__ == "__main__":
    seed_data()
