from src.db import get_connection
from datetime import datetime

def safe_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val[:10], "%Y-%m-%d").date()
    except:
        return None

def transform():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, raw_data FROM raw_permits")
    rows = cur.fetchall()

    for raw_id, raw in rows:

        permit_id = raw.get("job__")
        issue_date = safe_date(raw.get("dobrundate"))
        address = f"{raw.get('house__','')} {raw.get('street_name','')}".strip()
        borough = raw.get("borough")
        job_type = raw.get("job_type")
        building_type = raw.get("bldg_type")
        work_type = raw.get("work_type")
        zip_code = raw.get("zip_code")
        latitude = raw.get("gis_latitude")
        neighborhood = raw.get("gis_nta_name")

        cur.execute("""
            INSERT INTO staging_permits
            (permit_id, issue_date, address, borough, job_type,
            building_type, work_type, zip_code, latitude, neighborhood, raw_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (permit_id) DO NOTHING
        """, (
            permit_id, issue_date, address, borough, job_type,
            building_type, work_type, zip_code, latitude, neighborhood, raw_id
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Staging load complete")

if __name__ == "__main__":
    transform()