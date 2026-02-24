from flask import Blueprint, render_template, jsonify,request
from db import query_db
import psycopg2.extras
import datetime
import re

def serialize_row_safe(row):
    result = {}
    for key, value in row.items():
        if value is None:
            result[key] = None
        elif isinstance(value, psycopg2.extras.Range):
            result[key] = f"[{value.lower},{value.upper})"
        elif isinstance(value, (datetime.time, datetime.datetime)):
            result[key] = value.isoformat()
        elif isinstance(value, datetime.timedelta):
            total_seconds = int(value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            result[key] = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            result[key] = value
    return result

def get_columns(table_name):
    sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
        AND data_type IN ('text', 'character varying', 'character', 'integer')
    """
    rows = query_db(sql, (table_name,))
    return [r["column_name"] for r in rows]

pattern_num = r"^\d{13}$"
pattern_code_num = r"^[A-Z]{2}\s\d{13}$"
pattern_time = r'\d{2}:\d{2}:\d{2}'

admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates"
)
@admin_bp.route("/admin")
def admin_index():
    return render_template("/admin.html")

entities = {
    "tables": [
      {"name": "bookings"},
      {"name": "tickets"},
      {"name": "boarding_passes"},
      {"name": "segments"},
      {"name": "flights"},
      {"name": "routes"},
      {"name": "airports"},
      {"name": "airplanes"},
      {"name": "seats"}
    ]
}
ALLOWED_TABLES = [
    "bookings", "tickets", "boarding_passes",
    "segments", "flights", "routes",
    "airports", "airplanes", "seats"
]

@admin_bp.route("/api/admin/entity")
def admin_entity():
    return jsonify(entities)

@admin_bp.route("/api/admin/table")
def get_table_data():
    table_name = request.args.get('t', '').strip()
    if not table_name:
        return jsonify({"error": "table parameter is required"}), 400
    sql = f"SELECT * FROM {table_name} LIMIT 100;"

    try:
        rows = query_db(sql)
        if table_name == "routes" and rows:
            data = [serialize_row_safe(r) for r in rows]
        else:
            data = rows if rows else []

        return jsonify({
            "table": table_name,
            "data": data
        })

    except Exception:
        return jsonify({"error": "Server error"}), 500
    
    
@admin_bp.route("/api/admin/search")
def get_search_data():
    table_name = request.args.get("t", "").strip()
    search_query = request.args.get("q", "").strip()
    if not table_name:
        return jsonify({"error": "table parameter is required"}), 400
    if table_name not in ALLOWED_TABLES:
        return jsonify({"error": "table not allowed"}), 400
    
    
    try:
        if search_query:
            if re.match(pattern_num, search_query):
              columns  =['ticket_no']  
            elif re.match(pattern_code_num, search_query):
                columns  =['passenger_id']
            else:
                columns = get_columns(table_name)
            where_clause = " OR ".join([f"{col}::text ILIKE %s" for col in columns])
            sql = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 100;"
            params = [f"{search_query}%"] * len(columns)
        else:
            sql = f"SELECT * FROM {table_name} LIMIT 100;"
            params = []

        rows = query_db(sql, params)
        if table_name == "routes" and rows:
            data = [serialize_row_safe(r) for r in rows]
        else:
            data = rows if rows else []

        return jsonify({
            "table": table_name,
            "data": data
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 500
    


@admin_bp.route("/api/admin/delete", methods=["DELETE"])
def delete_row():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Пустой запрос"}), 400
    table_name = data.get("table")
    row_data = data.get("row")
    if table_name not in ALLOWED_TABLES:
        return jsonify({"error": "table not allowed"}), 400
    if not row_data or not isinstance(row_data, dict):
        return jsonify({"error": "Данные строки не предоставлены"}), 400
    conditions = []
    params = []
    for col, val in row_data.items():
        if isinstance(val, str):
            if re.search(pattern_time, val) or "[" in val or "{" in val or "," in val:
                continue
            else:
                conditions.append(f"{col} = %s")
                params.append(val)
        else:
            continue

    if not conditions:
        return jsonify({
            "error": "Не найдено подходящих полей (текст/числа) для удаления записи"
        }), 400
    where_clause = " AND ".join(conditions)
    sql = f"DELETE FROM {table_name} WHERE {where_clause}"
    try:
        query_db(sql, tuple(params))
        return jsonify({"success": True, "message": "Запись удалена"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Внутренняя ошибка сервера при удалении"}), 500