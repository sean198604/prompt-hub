<p align="center"><img src="assets/readme-cover.png" alt="Prompt Hub project cover" width="100%" /></p>

# 企业提示词库 · Prompt Hub

## 目录结构
```
prompt-hub/
├── app.py              # 后端 + 前端（FastAPI，HTML 内嵌）
├── requirements.txt    # Python 依赖
├── Dockerfile          # 镜像构建
└── docker-compose.yml  # 容器编排（含 volume 持久化）
```

## 快速启动
```bash
cd C:\Users\Administrator\Documents\Github\prompt-hub
docker compose up -d --build
```

## 访问地址
- 局域网：http://192.168.1.246:7000/
- 本机：http://localhost:7000/

## 运维操作

### 更新代码
```bash
cd C:\Users\Administrator\Documents\Github\prompt-hub
# 修改 app.py 后执行：
docker compose build --no-cache
docker compose up -d
```

### 备份数据库
```bash
docker run --rm -v prompt_hub_data:/data -v C:\backup:/backup alpine cp /data/db.sqlite3 /backup/db_backup.sqlite3
```

### 恢复数据库
```bash
docker compose down
docker run --rm -v prompt_hub_data:/data -v C:\backup:/backup alpine cp /backup/db_backup.sqlite3 /data/db.sqlite3
docker compose up -d
```

### 重启服务
```bash
docker compose restart prompt-hub
```

### 查看日志
```bash
docker logs -f prompt-hub
```

### 停止服务
```bash
docker compose down
```
