# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Backend (asset-server/)
cd asset-server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000   # Start API server
python -m app.scripts.seed                                    # Reset DB + seed demo data
pip install -r requirements.txt                               # Install dependencies

# Frontend (asset-web/)
cd asset-web
npm run dev                                                   # Start dev server (port 3000)
npm run build                                                 # Production build

# Database migrations (manual, no Alembic versions exist)
# Use scripts in asset-server/: run_add_*.py
python run_add_fields.py
```

## Architecture

### Backend (FastAPI + SQLAlchemy 2.0)

Layered: **API → Service → Repository → Model**

- `app/api/v1/` — Route handlers. Each file = one resource prefix (assets, users, categories, borrow, change, auth, reports, qrcode)
- `app/services/` — Business logic. `asset_service.py` is the largest file
- `app/repositories/` — Data access (BaseRepository with generic CRUD)
- `app/models/` — SQLAlchemy ORM models (User, Asset, Category, AssetRecord, AssetBorrowRecord, AssetChangeRecord)
- `app/schemas/` — Pydantic models. `AssetBase` → `AssetCreate` / `AssetInDB`. `AssetUpdate` is standalone
- `app/api/deps.py` — `SessionDep`, `get_current_active_user`, `require_admin`

Tables are created via `Base.metadata.create_all()` at startup (`main.py:44`). Alembic is initialized but has **no migration versions**.

### Frontend (Vue 3 + Element Plus + Pinia)

- 3 main pages: Dashboard (`/dashboard`), Category Management (`/categories`), User Management (`/users`)
- Category page is the **device management hub** — search, CRUD, borrow, return, change all happen here
- Shared dialogs: `BorrowDialog.vue`, `ChangeDialog.vue`, `AssetTimeline.vue`
- Scan pages (`/scan`, `/scan/result/:id`) are standalone (no sidebar), used for mobile QR workflow
- Global styles in `App.vue` (border-radius 12px, card shadows)

### API Response Format

```json
{ "code": 200, "message": "success", "data": {} }
```

Axios response interceptor checks `data.code !== 200` and shows error messages. On 401, clears token and redirects to `/login`.

## Key Design Decisions

### Asset Status (actual, not README)

The system uses **3 statuses**: `normal` (在库), `borrowed` (已借出), `scrapped` (已报废). The README mentions 6 statuses but those are NOT implemented.

Status map in `asset_service.py`:
```python
ASSET_STATUS_MAP = { "normal": "在库", "borrowed": "已借出", "scrapped": "已报废" }
```

Default sort: `CASE status WHEN 'normal' THEN 1 WHEN 'borrowed' THEN 2 WHEN 'scrapped' THEN 3 END, created_at DESC`

### Department Field

The `assets` table has `department VARCHAR(100)` column (added mid-project via `run_add_dept.py`). It is an **Asset model field**, used in display and change tracking. Do NOT try to create a separate Department model/table.

### Router Order (critical gotcha)

FastAPI matches routes in registration order. `GET /assets/export` **MUST** be registered before `GET /assets/{asset_id}`, otherwise `"export"` matches `{asset_id}` and causes a 422 (int parse error).

### QR Code

QR codes contain `http://<local-ip>:3000/scan/result/{id}`. The IP is hardcoded in `qrcode_service.py` — update it when the network changes. QR code images are served from `/uploads/qrcode/` via Starlette StaticFiles mount in `main.py`.

### User-Owner Naming

The Asset model uses `user_id` (not `owner_id`). The frontend displays "负责人". The field stores a user ID; `owner_name` is injected at query time via User table join in `asset_service.py`. Schema (`AssetBase`) does NOT include `owner_name` — it's added to the response dict manually.

### DB Migration Pattern

No Alembic migrations. SQL changes are applied via `run_*.py` scripts in `asset-server/` that execute raw SQL through pymysql. SQL files live in `docs/`.

## Additional Tables (Round 2)

- `asset_borrow_record` — tracks borrow/return events (borrower, dates, status)
- `asset_change_record` — tracks field changes (change_type: owner/dept/location/category, old_value, new_value)

Both are queried in the asset timeline (`AssetTimeline.vue`) and dashboard recent activities.

## Important Patterns

- Frontend form for add/edit devices: shared reactive `deviceForm`, `isDeviceEdit` flag, `resetDeviceForm()` on close
- Category tags + status buttons + search dropdown share the **same state source** (`searchForm.status`, `activeCategory`)
- Dialog components (Borrow, Change) use `v-model` for visibility and emit `success` for parent refresh
- The `AssetInDB` schema uses `from_attributes = True` to map ORM objects; `created_at`/`updated_at` were added later
- `userStore.user.role === 'admin'` controls admin-only UI visibility (no route-level guard on frontend)
