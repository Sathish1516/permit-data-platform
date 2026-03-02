from src.db import get_connection

def build_summary():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM permits_monthly_summary")

    cur.execute("""
        INSERT INTO permits_monthly_summary (borough ,year, month, permit_count)
        SELECT 
                borough, 
                EXTRACT(YEAR FROM issue_date) AS year, 
                EXTRACT(MONTH FROM issue_date) AS month, 
                COUNT(*) AS permit_count
                FROM staging_permits
                WHERE issue_date IS NOT NULL
                GROUP BY borough, year, month
                """)
    conn.commit()
    cur.close()
    conn.close()    

    print("Monthly summary built")

if __name__ == "__main__":
    build_summary()