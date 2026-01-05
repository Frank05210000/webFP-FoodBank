# 食物銀行預訂系統

一個使用 Flask + PostgreSQL 構建的食物銀行預訂平台，讓民眾預訂即期物資、商家管理上架與訂單，並提供管理者後台監控全站資訊。

## 研究動機
在台灣，從大型超市到便利商店，每天都有大量食物因為即將或剛過保存期限而被丟棄。研究估計每年浪費高達 360～380 萬噸，若將這些廚餘裝進桶子堆疊起來，高度可以超過一萬三千五百座台北 101。大量本來可以被好好吃完的食物，最後卻成為垃圾。

另一方面，全國仍有約 26 萬戶低收入及中低收入家庭，在日常三餐上面臨壓力，更需要穩定而有尊嚴的食物援助。如果能把這些仍在安全食用期限內的食物，透過完善的管理系統從超商、量販店或一般家庭媒合給有需要的人，就能同時減少食物浪費並支援弱勢族群。這也是本次專題的目標：打造一個好用的「食物銀行網站」，協助整合捐贈端與受贈端資訊，讓資源被更有效率地分配。

## 功能概要
- 民眾：註冊/登入、查看地圖暨附近據點、進入商家頁面加入購物車、結帳預訂、查看訂單紀錄與帳號管理。
- 商家：申請帳號、上架/編輯/刪除物資、查看訂單並標記為完成或取消。
- 管理者：儀表板統計、查看最新訂單、刪除商家與一般用戶、可介入取消訂單。
- 多語系：內建英文/中文介面，可於導覽列切換語言（預設英文）。

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

## Testing
本專案包含兩層自動化測試，透過 `pytest` 執行：

- **Unit Test**：驗證 `Shop.available_quantity` 只會計算啟用且有庫存的品項。
- **Integration Test**：模擬完整預訂流程（登入 → 加入購物車 → 結帳），並檢查是否產生訂單與扣減庫存。

執行方式：
```bash
source venv/bin/activate
pytest
```

## 開發建議
- 修改資料模型後，執行 `flask --app app.py db migrate` 產生遷移，再 `db upgrade` 套用。
- 新增更多商家/物資可直接編輯 `seed.py`，重新執行載入。
- 尚未整合自動化測試，可依需求加入 pytest。歡迎針對 UI/流程再做優化或國際化。
