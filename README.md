# 食物銀行預訂系統

一個使用 Flask + PostgreSQL 構建的食物銀行預訂平台，讓民眾預訂即期物資、商家管理上架與訂單，並提供管理者後台監控全站資訊。

## 功能概要
- 民眾：註冊/登入、查看地圖暨附近據點、進入商家頁面加入購物車、結帳預訂、查看訂單紀錄與帳號管理。
- 商家：申請帳號、上架/編輯/刪除物資、查看訂單並標記為完成或取消。
- 管理者：儀表板統計、查看最新訂單、刪除商家與一般用戶、可介入取消訂單。

## 架構
- **後端**：Flask、Flask-Login、Flask-Migrate、SQLAlchemy
- **資料庫**：PostgreSQL（可透過 `DATABASE_URL` 切換）
- **前端**：Bootstrap 5 + Leaflet.js + 原生 JS/CSS

## 目錄結構
```
├── app.py                # Flask 入口與路由
├── config.py             # Config (Postgres/Secret)
├── extensions.py         # db/migrate 初始化
├── models.py             # SQLAlchemy 模型
├── seed.py               # 假資料產生器
├── requirements.txt      # 相依套件
├── migrations/           # Alembic 遷移紀錄
├── templates/            # Jinja2 模板 (頁面)
├── static/
│   ├── css/style.css     # 自訂樣式
│   └── js/script.js      # Leaflet/互動腳本
├── ref/                  # 參考範例檔案
├── food_bank_spec.md     # 需求規格
├── SETUP.md              # 安裝與啟動指南
└── README.md             # 專案介紹 (本檔)
```

## 快速開始
請參考 [SETUP.md](./SETUP.md) 完成環境建置、資料庫初始化與假資料載入。

啟動後於 `http://localhost:5001/` 體驗：
- 民眾帳號：`user@example.com` / `password`
- 商家帳號：`shop1@example.com` / `password`
- 管理員：`admin@example.com` / `admin123`

## 開發建議
- 修改資料模型後，執行 `flask --app app.py db migrate` 產生遷移，再 `db upgrade` 套用。
- 新增更多商家/物資可直接編輯 `seed.py`，重新執行載入。
- 尚未整合自動化測試，可依需求加入 pytest。歡迎針對 UI/流程再做優化或國際化。
