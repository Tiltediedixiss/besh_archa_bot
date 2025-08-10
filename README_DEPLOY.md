## Deployment (24/7)

Recommended VPS: Hetzner CX11 (1 vCPU, 2 GB RAM) or DigitalOcean s-1vcpu-2gb. This setup comfortably handles ~200 concurrent users.

### Option 1: Docker Compose
1. Copy `env.example` to `.env` and set values:
   - `BOT_TOKEN=...`
   - `ADMIN_ID=2092094721`
2. Build and run:
```
docker compose up -d --build
```
3. Logs:
```
docker compose logs -f
```
4. Data persistence: volumes map `./data`, `./reports`, `./feedback_day4.csv` into the container.

### Option 2: systemd (no Docker)
1. On server:
```
sudo apt update && sudo apt install -y python3-venv git
sudo useradd -r -m -d /opt/besh_archa_bot bot || true
sudo su - bot
cd /opt/besh_archa_bot
# clone or copy project here
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
```
2. Create `.env` in project root with `BOT_TOKEN` and `ADMIN_ID`.
3. Install service (as root):
```
sudo cp deploy/besh_archa_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable besh_archa_bot
sudo systemctl start besh_archa_bot
sudo journalctl -u besh_archa_bot -f
```

### Notes
- Run a single bot process (JSON storage is not multi-writer safe). For scaling, migrate to DB (SQLite/Postgres) or add file locks.
- Consider Redis storage for FSM if you need state across restarts.
- Keep `data/`, `reports/`, and `feedback_day4.csv` backed up.
- Store secrets in `.env` and never commit it.
