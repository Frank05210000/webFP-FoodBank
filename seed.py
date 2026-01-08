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
        shop_owner3 = User(name="店長C", email="shop3@example.com", phone="02-2222-3333", role="shop")
        shop_owner3.set_password("password")
        shop_owner4 = User(name="店長D", email="shop4@example.com", phone="02-2345-6789", role="shop")
        shop_owner4.set_password("password")
        shop_owner5 = User(name="店長E", email="shop5@example.com", phone="02-5566-7788", role="shop")
        shop_owner5.set_password("password")
        shop_owner6 = User(name="店長F", email="shop6@example.com", phone="02-9876-5432", role="shop")
        shop_owner6.set_password("password")
        shop_owner7 = User(name="店長G", email="shop7@example.com", phone="02-6677-8899", role="shop")
        shop_owner7.set_password("password")
        shop_owner8 = User(name="店長H", email="shop8@example.com", phone="02-3355-8899", role="shop")
        shop_owner8.set_password("password")
        shop_owner9 = User(name="店長I", email="shop9@example.com", phone="02-2233-9911", role="shop")
        shop_owner9.set_password("password")
        shop_owner10 = User(name="店長J", email="shop10@example.com", phone="02-1122-3344", role="shop")
        shop_owner10.set_password("password")
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("admin123")
        db.session.add_all([user, shop_owner1, shop_owner2, shop_owner3, shop_owner4, shop_owner5, shop_owner6, shop_owner7, shop_owner8, shop_owner9, shop_owner10, admin])
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
            owner=shop_owner3,
            manager_email="shop3@example.com",
            phone="02-2222-3333",
            address="台北市大安區忠孝東路三段300號",
            latitude=25.0410,
            longitude=121.5430, # SOGO 復興館附近
            opening_time=datetime.strptime("00:00", "%H:%M").time(),
            closing_time=datetime.strptime("23:59", "%H:%M").time(),
            rating=4.2
        )

        shop4 = Shop(
            name="仁愛市場 - 蔬果區",
            owner=shop_owner4,
            manager_email="shop4@example.com",
            phone="02-2345-6789",
            address="台北市中正區濟南路二段1號",
            latitude=25.0405,
            longitude=121.5340,
            opening_time=datetime.strptime("07:00", "%H:%M").time(),
            closing_time=datetime.strptime("19:00", "%H:%M").time(),
            rating=4.1
        )

        shop5 = Shop(
            name="社區食物銀行 - 大直館",
            owner=shop_owner5,
            manager_email="shop5@example.com",
            phone="02-5566-7788",
            address="台北市中山區北安路780號",
            latitude=25.0845,
            longitude=121.5491,
            opening_time=datetime.strptime("09:00", "%H:%M").time(),
            closing_time=datetime.strptime("21:00", "%H:%M").time(),
            rating=4.6
        )

        shop6 = Shop(
            name="吉祥里愛心廚房",
            owner=shop_owner6,
            manager_email="shop6@example.com",
            phone="02-9876-5432",
            address="台北市萬華區艋舺大道211號",
            latitude=25.0365,
            longitude=121.4970,
            opening_time=datetime.strptime("11:00", "%H:%M").time(),
            closing_time=datetime.strptime("20:00", "%H:%M").time(),
            rating=4.0
        )

        shop7 = Shop(
            name="幸福早餐屋",
            owner=shop_owner7,
            manager_email="shop7@example.com",
            phone="02-6677-8899",
            address="新北市板橋區文化路一段188號",
            latitude=25.0175,
            longitude=121.4650,
            opening_time=datetime.strptime("06:00", "%H:%M").time(),
            closing_time=datetime.strptime("13:00", "%H:%M").time(),
            rating=4.4
        )

        shop8 = Shop(
            name="樂活超商 - 三重店",
            owner=shop_owner8,
            manager_email="shop8@example.com",
            phone="02-3355-8899",
            address="新北市三重區重新路四段15號",
            latitude=25.0590,
            longitude=121.4890,
            opening_time=datetime.strptime("08:00", "%H:%M").time(),
            closing_time=datetime.strptime("23:30", "%H:%M").time(),
            rating=4.3
        )

        shop9 = Shop(
            name="安心便利店 - 永和",
            owner=shop_owner9,
            manager_email="shop9@example.com",
            phone="02-2233-9911",
            address="新北市永和區中山路一段22號",
            latitude=25.0041,
            longitude=121.5168,
            opening_time=datetime.strptime("00:00", "%H:%M").time(),
            closing_time=datetime.strptime("23:59", "%H:%M").time(),
            rating=4.5
        )

        shop10 = Shop(
            name="慈恩寺食物分享點",
            owner=shop_owner10,
            manager_email="shop10@example.com",
            phone="02-1122-3344",
            address="新北市新店區北新路二段88號",
            latitude=24.9710,
            longitude=121.5380,
            opening_time=datetime.strptime("10:00", "%H:%M").time(),
            closing_time=datetime.strptime("18:00", "%H:%M").time(),
            rating=4.7
        )

        db.session.add_all([shop1, shop2, shop3, shop4, shop5, shop6, shop7, shop8, shop9, shop10])
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
                photo_url="img/food-bread.png"
            ),
            Food(
                shop_id=shop1.id,
                name="有機蔬菜包",
                category="生鮮",
                quantity=8,
                expiry_time=datetime.now() + timedelta(days=2),
                description="當季蔬菜組合",
                photo_url="img/food-veg.png"
            ),
            Food(
                shop_id=shop1.id,
                name="水果禮盒",
                category="水果",
                quantity=6,
                expiry_time=datetime.now() + timedelta(days=3),
                description="當季水果禮盒",
                photo_url="img/food-fruit.png"
            ),
            Food(
                shop_id=shop2.id,
                name="綜合麵包袋",
                category="麵包",
                quantity=10,
                expiry_time=datetime.now() + timedelta(hours=8),
                description="今日現烤麵包福袋",
                photo_url="img/food-bread.png"
            ),
            Food(
                shop_id=shop2.id,
                name="沙拉盒",
                category="輕食",
                quantity=5,
                expiry_time=datetime.now() + timedelta(hours=10),
                description="清爽沙拉組合",
                photo_url="img/food-salad.png"
            ),
            Food(
                shop_id=shop3.id,
                name="御飯糰",
                category="便當",
                quantity=15,
                expiry_time=datetime.now() + timedelta(hours=6),
                description="鮪魚口味御飯糰",
                photo_url="img/food-rice.png"
            ),
            Food(
                shop_id=shop3.id,
                name="熟食便當",
                category="便當",
                quantity=7,
                expiry_time=datetime.now() + timedelta(hours=5),
                description="便利商店熱食便當",
                photo_url="img/food-bento.png"
            ),
            Food(
                shop_id=shop4.id,
                name="綜合蔬果盒",
                category="蔬果",
                quantity=9,
                expiry_time=datetime.now() + timedelta(days=1),
                description="市場當日新鮮蔬果組合",
                photo_url="img/food-veg.png"
            ),
            Food(
                shop_id=shop5.id,
                name="營養餐包",
                category="套餐",
                quantity=11,
                expiry_time=datetime.now() + timedelta(hours=12),
                description="多種主食與配菜組合",
                photo_url="img/food-bento.png"
            ),
            Food(
                shop_id=shop6.id,
                name="熱湯與麵食",
                category="熱食",
                quantity=6,
                expiry_time=datetime.now() + timedelta(hours=4),
                description="現煮湯品搭麵食",
                photo_url="img/food-default.svg"
            ),
            Food(
                shop_id=shop7.id,
                name="即期早餐組",
                category="早餐",
                quantity=10,
                expiry_time=datetime.now() + timedelta(hours=6),
                description="三明治與飲料組合",
                photo_url="img/food-bread.png"
            ),
            Food(
                shop_id=shop8.id,
                name="鮮蔬沙拉",
                category="輕食",
                quantity=8,
                expiry_time=datetime.now() + timedelta(hours=8),
                description="大量蔬菜與水果沙拉",
                photo_url="img/food-salad.png"
            ),
            Food(
                shop_id=shop9.id,
                name="御飯糰套餐",
                category="便當",
                quantity=20,
                expiry_time=datetime.now() + timedelta(hours=10),
                description="多口味御飯糰與飲品",
                photo_url="img/food-rice.png"
            ),
            Food(
                shop_id=shop10.id,
                name="寺院供餐",
                category="熱食",
                quantity=12,
                expiry_time=datetime.now() + timedelta(hours=6),
                description="寺院烹飪的素食餐點",
                photo_url="img/food-default.svg"
            )
        ]

        db.session.add_all(foods)
        db.session.commit()

        print("假資料建立完成！")

if __name__ == "__main__":
    seed_data()
