from flask import render_template, jsonify, request
import psycopg2.extras
import datetime
import re
from app.models.database import query_db, get_columns, get_default_data

pattern_num = r"^\d{13}$"
pattern_code_num = r"^[A-Z]{2}\s\d{13}$"
pattern_time = r'\d{2}:\d{2}:\d{2}'

class AdminController:

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
            ]}

    ALLOWED_TABLES = [
        "bookings", "tickets", "boarding_passes",
        "segments", "flights", "routes",
        "airports", "airplanes", "seats"
    ]

    def serialize_row_safe(self,row):

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
    
    def admin_index(self):
        return render_template("admin/newadmin.html", tables=self.entities["tables"])

    def search_columns(self, table_name):
       
        rows = get_columns(table_name)
        return [r["column_name"] for r in rows]
    

    
    def search_default_data(self):
        table_name = request.args.get('t', '').strip()
        if not table_name:
            return jsonify({"error": "table parameter is required"}), 400

        try:
            rows = get_default_data(table_name)
            if table_name == "routes" and rows:
                data = [self.serialize_row_safe(r) for r in rows]
            else:
                data = rows if rows else []

            columns = list(data[0].keys())
            return  render_template("admin/main_table.html", data=data, columns = columns)
        except Exception:
            return jsonify({"error": "Server error"}), 500

    def search_advanced_data(self):

        table_name = request.args.get("t", "").strip()
        search_query = request.args.get("q", "").strip()
        if not table_name:
            return jsonify({"error": "table parameter is required"}), 400
        if table_name not in self.ALLOWED_TABLES:
            return jsonify({"error": "table not allowed"}), 400
        
        
        try:
            if search_query:
                if re.match(pattern_num, search_query):
                    columns  =['ticket_no']  
                elif re.match(pattern_code_num, search_query):
                    columns  =['passenger_id']
                else:
                    columns = get_columns(table_name)
                rows = get_default_data(table_name,columns, search_query)
            else:
                rows = get_default_data(table_name)

            if table_name == "routes" and rows:
                data = [self.serialize_row_safe(r) for r in rows]
            else:
                data = rows if rows else []

            return jsonify({
                "table": table_name,
                "data": data
            })
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
    
