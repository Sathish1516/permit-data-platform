import json
from src.db import get_connection
from datetime import datetime

def is_valid(permit_id, issue_date,borough, latitude):
    if not permit_id:
        return False , "missing_permit_id"
    if not issue_date:
        return False , "invalid_issue_date"
    if not borough:
        return False , "missing_borough"
    try:
        if latitude:
            float(latitude)
    except:
        return False , "invalid_latitude"
    return True, None

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

    # last processed id
    cur.execute("SELECT last_raw_id FROM pipeline_state ORDER BY id DESC LIMIT 1")
    last_processed_id = cur.fetchone()[0]

    cur.execute("""
        SELECT id, raw_data
        FROM raw_permits
        WHERE id > %s
        ORDER BY id
    """, (last_processed_id,))
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

        valid, reason = is_valid(permit_id, issue_date, borough, latitude)
        if not valid:
            cur.execute("""
                        INSERT INTO rejected_permits (raw_id, reason,raw_data)
                        VALUES (%s, %s, %s)
                    """, (raw_id, reason, json.dumps(raw)))
            continue

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

    # update checkpoint ONLY after success
    if rows:
        max_id = rows[-1][0]   # last row because ORDER BY id
        cur.execute("UPDATE pipeline_state SET last_raw_id = %s", (max_id,))

    conn.commit()
    cur.close()
    conn.close()

    print("Staging load complete")

if __name__ == "__main__":
    transform()