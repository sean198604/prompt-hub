import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────
DB_PATH = os.environ.get("DB_PATH", "/app/data/db.sqlite3")
CATEGORIES = ["图像-生图", "图像-修图", "调研", "通用", "开发信", "需求"]
EDIT_PASSWORD = "2026"

app = FastAPI(title="企业提示词库 Prompt Hub")

# 模板目录
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
INDEX_HTML  = os.path.join(TEMPLATE_DIR, "index.html")

# ──────────────────────────────────────────────
# 数据库
# ──────────────────────────────────────────────
def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            content   TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            likes     INTEGER NOT NULL DEFAULT 0,
            created_at TEXT   NOT NULL
        )
    """)
    # 点赞记录表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS like_records (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ip        TEXT    NOT NULL,
            prompt_id INTEGER NOT NULL,
            prompt_title TEXT NOT NULL DEFAULT '',
            category   TEXT   NOT NULL DEFAULT '',
            liked_at  TEXT    NOT NULL,
            UNIQUE(ip, prompt_id)
        )
    """)
    cur = conn.execute("SELECT COUNT(*) as cnt FROM prompts")
    if cur.fetchone()["cnt"] == 0:
        samples = [
            ("产品概念图生成", "请生成一张风格简洁的产品概念图，背景为纯白色，主体为工业设计感的产品，光线柔和，色调冷白，适合用于官网展示。", "图像-生图", 15),
            ("人物写真背景替换", "将图片背景替换为现代简约办公室环境，保持主体人物比例和光线方向不变，背景虚化 f/2.8 效果，整体色调偏暖。", "图像-修图", 9),
            ("展会产品宣传图", "生成一张适合外贸展会的产品宣传图，产品置于中央，背景为深蓝色渐变，添加英文标题文字，风格专业大气。", "图像-生图", 7),
            ("竞品深度调研", "请帮我全面调研以下竞品：[竞品名称]。需要包含：核心功能对比、定价策略、用户评价摘要、市场定位差异、近半年重大更新。输出为结构化表格。", "调研", 22),
            ("行业报告速读", "以下是一份行业报告，请提取：①核心数据（3-5个关键数字）②主要结论（3条）③对我司的影响（2条）④可行动建议（2条）。报告内容：[粘贴此处]", "调研", 18),
            ("商务邮件润色", "请将以下英文邮件润色为正式商务风格，保持原意不变，语气专业友好，适合发给海外客户。原文：[粘贴此处]", "通用", 13),
            ("产品描述生成", "根据以下产品参数，生成一段适合 Amazon/独立站的英文产品描述，300字以内，突出卖点，包含关键词自然嵌入。参数：[粘贴此处]", "通用", 11),
            ("需求：批量导出提示词", "希望系统支持将所有提示词导出为 Excel 或 CSV 文件，方便团队离线使用和存档管理。", "需求", 28),
            ("需求：提示词标签功能", "希望每条提示词可以打多个自定义标签（如：高频、重要、待优化），方便按标签检索和管理。", "需求", 19),
        ]
        for title, content, category, likes in samples:
            conn.execute(
                "INSERT INTO prompts (title, content, category, likes, created_at) VALUES (?,?,?,?,?)",
                (title, content, category, likes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
    conn.commit()
    conn.close()

init_db()

# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

# ──────────────────────────────────────────────
# API
# ──────────────────────────────────────────────

@app.get("/api/prompts")
def list_prompts(category: Optional[str] = None):
    conn = get_conn()
    if category and category != "全部":
        rows = conn.execute(
            "SELECT * FROM prompts WHERE category=? ORDER BY likes DESC, id DESC",
            (category,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM prompts ORDER BY likes DESC, id DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/demands")
def list_demands():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM prompts WHERE category='需求' ORDER BY likes DESC, id DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/prompts")
def create_prompt(
    title: str    = Form(...),
    content: str  = Form(...),
    category: str = Form(...)
):
    if category not in CATEGORIES:
        raise HTTPException(status_code=400, detail="无效分类")
    if not title.strip() or not content.strip():
        raise HTTPException(status_code=400, detail="标题和内容不能为空")

    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO prompts (title, content, category, likes, created_at) VALUES (?,?,?,0,?)",
        (title.strip(), content.strip(), category, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    new_id = cur.lastrowid
    row = conn.execute("SELECT * FROM prompts WHERE id=?", (new_id,)).fetchone()
    conn.close()
    return dict(row)


@app.put("/api/prompts/{prompt_id}")
def update_prompt(
    request: Request,
    prompt_id: int,
    title: str    = Form(...),
    content: str  = Form(...),
    category: str = Form(...),
    password: str = Form(...)
):
    # 验证密码
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")

    conn = get_conn()
    row = conn.execute("SELECT id FROM prompts WHERE id=?", (prompt_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="提示词不存在")

    if category not in CATEGORIES:
        conn.close()
        raise HTTPException(status_code=400, detail="无效分类")

    conn.execute(
        "UPDATE prompts SET title=?, content=?, category=? WHERE id=?",
        (title.strip(), content.strip(), category, prompt_id)
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM prompts WHERE id=?", (prompt_id,)).fetchone()
    conn.close()
    return dict(updated)


@app.post("/api/prompts/{prompt_id}/like")
def like_prompt(request: Request, prompt_id: int):
    ip = get_client_ip(request)
    conn = get_conn()

    # 检查今日是否已点赞
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    existing = conn.execute(
        "SELECT id FROM like_records WHERE ip=? AND prompt_id=? AND liked_at>=?",
        (ip, prompt_id, today_start)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(status_code=429, detail="一天之内一次哟")

    row = conn.execute("SELECT * FROM prompts WHERE id=?", (prompt_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="提示词不存在")

    # 记录点赞（包含标题和分类）
    try:
        conn.execute(
            "INSERT INTO like_records (ip, prompt_id, prompt_title, category, liked_at) VALUES (?,?,?,?,?)",
            (ip, prompt_id, row["title"], row["category"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    except sqlite3.IntegrityError:
        pass  # 已存在记录

    conn.execute("UPDATE prompts SET likes = likes + 1 WHERE id=?", (prompt_id,))
    conn.commit()
    updated = conn.execute("SELECT * FROM prompts WHERE id=?", (prompt_id,)).fetchone()
    conn.close()
    return dict(updated)


@app.delete("/api/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, password: Optional[str] = None):
    # 验证密码
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    conn = get_conn()
    row = conn.execute("SELECT id FROM prompts WHERE id=?", (prompt_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="提示词不存在")
    conn.execute("DELETE FROM prompts WHERE id=?", (prompt_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


# ──────────────────────────────────────────────
# 页面
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(INDEX_HTML, media_type="text/html; charset=utf-8")

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# ──────────────────────────────────────────────
# 后台管理页面
# ──────────────────────────────────────────────
ADMIN_HTML = os.path.join(TEMPLATE_DIR, "admin.html")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    return FileResponse(ADMIN_HTML, media_type="text/html; charset=utf-8")

@app.get("/api/admin/stats")
def admin_stats(password: Optional[str] = None):
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) as cnt FROM prompts").fetchone()["cnt"]
    total_likes = conn.execute("SELECT SUM(likes) as s FROM prompts").fetchone()["s"] or 0
    demands = conn.execute("SELECT COUNT(*) as cnt FROM prompts WHERE category='需求'").fetchone()["cnt"]
    by_cat = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM prompts GROUP BY category ORDER BY cnt DESC"
    ).fetchall()
    conn.close()
    return {"total": total, "total_likes": total_likes, "demands": demands, "by_cat": [dict(r) for r in by_cat]}

@app.get("/api/admin/like-records")
def get_like_records(password: Optional[str] = None):
    """获取所有点赞记录"""
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    conn = get_conn()
    rows = conn.execute("""
        SELECT lr.*, p.title as prompt_title, p.category
        FROM like_records lr
        JOIN prompts p ON lr.prompt_id = p.id
        ORDER BY lr.liked_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/admin/reset-likes")
def reset_likes(password: Optional[str] = None):
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    conn = get_conn()
    conn.execute("UPDATE prompts SET likes=0")
    conn.execute("DELETE FROM like_records")
    conn.commit()
    conn.close()
    return {"ok": True}

@app.post("/api/admin/clear-all")
def clear_all(password: Optional[str] = None):
    if password != EDIT_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    conn = get_conn()
    conn.execute("DELETE FROM prompts")
    conn.execute("DELETE FROM like_records")
    conn.commit()
    conn.close()
    return {"ok": True}
