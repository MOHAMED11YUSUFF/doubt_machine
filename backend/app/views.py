from django.shortcuts import render
from db_connect import get_connection
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from datetime import datetime
import psycopg2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
import pytz

conn = get_connection()
india_tz = pytz.timezone("Asia/Kolkata")



@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "message": "Only POST method allowed"
        })

    try:
        data = json.loads(request.body)

        gmail = data.get("email")
        password = data.get("password")

        if not gmail or not password:
            return JsonResponse({
                "status": False,
                "message": "gmail and password required"
            })

        cur = conn.cursor()

        query = """
            SELECT password
            FROM user_db
            WHERE gmail = %s
        """

        cur.execute(query, (gmail,))
        user = cur.fetchone()

        if user is None:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            })

        stored_password = user[0]

        # verify hashed password
        if check_password(password, stored_password):
            return JsonResponse({
                "status": True,
                "message": "Login successful"
            })

        return JsonResponse({
            "status": False,
            "message": "Invalid password"
        })

    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": str(e)
        })

def create_admin(request):
    try:
        cur = conn.cursor()

        # =========================================================
        # CREATE TABLES
        # =========================================================

        cur.execute("""
        CREATE TABLE IF NOT EXISTS company_db (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            is_blocked BOOLEAN DEFAULT FALSE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by VARCHAR(255),
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_by VARCHAR(255)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS access_db (
            access_id SERIAL PRIMARY KEY,
            access_name VARCHAR(255) UNIQUE NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by VARCHAR(255),
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_by VARCHAR(255)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS role_db (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            is_blocked BOOLEAN DEFAULT FALSE,
            access_id INTEGER REFERENCES access_db(access_id),
            is_admin BOOLEAN DEFAULT FALSE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by VARCHAR(255),
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_by VARCHAR(255)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_db (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            company_id INTEGER REFERENCES company_db(id),
            role_id INTEGER REFERENCES role_db(id),
            gmail VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by VARCHAR(255),
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_by VARCHAR(255)
        );
        """)

        conn.commit()

        # =========================================================
        # CREATE COMPANY (ONLY IF NOT EXISTS)
        # =========================================================

        cur.execute("""
        SELECT id FROM company_db
        WHERE name = %s
        """, ("smy tech",))

        company = cur.fetchone()

        if company:
            company_id = company[0]
        else:
            cur.execute("""
            INSERT INTO company_db (
                name,
                is_blocked,
                created_by,
                modified_by
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """, (
                "smy tech",
                False,
                "system",
                "system"
            ))

            company_id = cur.fetchone()[0]

        conn.commit()

        # =========================================================
        # CREATE ACCESS (ONLY IF NOT EXISTS)
        # =========================================================

        cur.execute("""
        SELECT access_id FROM access_db
        WHERE access_name = %s
        """, ("ALL_ACCESS",))

        access = cur.fetchone()

        if access:
            access_id = access[0]
        else:
            cur.execute("""
            INSERT INTO access_db (
                access_name,
                created_by,
                modified_by
            )
            VALUES (%s, %s, %s)
            RETURNING access_id
            """, (
                "ALL_ACCESS",
                "system",
                "system"
            ))

            access_id = cur.fetchone()[0]

        conn.commit()

        # =========================================================
        # CREATE ROLE (ONLY IF NOT EXISTS)
        # =========================================================

        cur.execute("""
        SELECT id FROM role_db
        WHERE name = %s
        """, ("ADMIN",))

        role = cur.fetchone()

        if role:
            role_id = role[0]
        else:
            cur.execute("""
            INSERT INTO role_db (
                name,
                is_blocked,
                access_id,
                is_admin,
                created_by,
                modified_by
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (
                "ADMIN",
                False,
                access_id,
                True,
                "system",
                "system"
            ))

            role_id = cur.fetchone()[0]

        conn.commit()

        # =========================================================
        # CREATE ADMIN USER (ONLY IF NOT EXISTS)
        # =========================================================

        cur.execute("""
        SELECT id FROM user_db
        WHERE gmail = %s
        """, ("mdyusuffprsnl@gmail.com",))

        user = cur.fetchone()

        if not user:

            hashed_password = make_password("yusuff@smy11486")

            cur.execute("""
            INSERT INTO user_db (
                name,
                company_id,
                role_id,
                gmail,
                password,
                created_by,
                modified_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                "yusuff",
                company_id,
                role_id,
                "mdyusuffprsnl@gmail.com",
                hashed_password,
                "system",
                "system"
            ))

        conn.commit()

        cur.close()

        return HttpResponse("Database initialized successfully!")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def create_yusuff(request):
    try:

        # Connect as postgres superuser
        conn = psycopg2.connect(
            host="localhost",
            database="doubt_machine",
            user="postgres",
            password="yusuff"
        )

        cur = conn.cursor()

        # =====================================================
        # GRANT DATABASE ACCESS
        # =====================================================

        cur.execute("""
            GRANT ALL PRIVILEGES
            ON DATABASE doubt_machine
            TO yusuff;
        """)

        # =====================================================
        # GRANT SCHEMA ACCESS
        # =====================================================

        cur.execute("""
            GRANT ALL
            ON SCHEMA public
            TO yusuff;
        """)

        # =====================================================
        # CHANGE OWNER
        # =====================================================

        cur.execute("""
            ALTER SCHEMA public
            OWNER TO yusuff;
        """)

        # =====================================================
        # ALLOW TABLE CREATION
        # =====================================================

        cur.execute("""
            ALTER USER yusuff
            CREATEDB;
        """)

        conn.commit()

        cur.close()
        conn.close()

        return HttpResponse("Permissions granted successfully!")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def about(request):
    return HttpResponse("About Page")

def contact(request):
    return HttpResponse("Contact Page")