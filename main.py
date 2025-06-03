from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, text
from typing import Optional
from fastapi import Query

app = FastAPI()

# database connection
engine = create_engine('postgresql://postgres:*****@localhost/SOC')

@app.get("/")
def read_home():
    return FileResponse("static/home.html")

@app.get("/logs")
def get_logs(
    is_malicious: Optional[int] = Query(None),
    protocol: Optional[str] = Query(None)
):
    query = "SELECT * FROM network_logs"
    filters = []

    if is_malicious is not None:
        filters.append(f"is_malicious = {is_malicious}")

    if protocol:
        filters.append(f"UPPER(protocol) = '{protocol.upper()}'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY timestamp DESC LIMIT 100"

    with engine.connect() as conn:
        result = conn.execute(text(query)).mappings().all()
        return list(result)
