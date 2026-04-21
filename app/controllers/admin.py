
from flask import render_template, jsonify, request, redirect, url_for, flash
from app.services.admin_service import AdminService
from app.models.dto import Table_dto_request
from app.models.airports import AirportsDTO
from app.models.airplanes import AirplanesDTO
from app.models.flights import FlightsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.routes import RoutesDTO
class AdminController:

    def __init__(self, service: AdminService):
        self.service = service

    
    
    def admin_index(self):
        return render_template("admin/newadmin.html", current_page=1, has_next=False,)  

    def view_airports(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airports(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500

    def create_airport(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            code = request.form.get('airport_code')
            name = request.form.get('airport_name')
            city = request.form.get('city')
            country = request.form.get('country')
            coords = request.form.get('coordinates')
            tz = request.form.get('timezone')

            if not all([code,name,city,country,coords,tz]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= AirportsDTO(airport_code=code, airport_name=name, city=city, country=country, coordinates=coords, timezone=tz)
                    self.service.create_data_airport(dto=dto_record)

                    flash("Запись успешно добавлена", "success")
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))

        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airports(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_airports', page=page, q=query))
            
    def update_airport(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            selected_id = request.form.get('selected_id')
            code = request.form.get('airport_code')
            name = request.form.get('airport_name')
            city = request.form.get('city')
            country = request.form.get('country')
            coords = request.form.get('coordinates')
            tz = request.form.get('timezone')
            if not all([code,name,city,country,coords,tz]):
                    flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= AirportsDTO(airport_code=code, airport_name=name, city=city, country=country, coordinates=coords, timezone=tz)
                    self.service.update_data_airport(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))

        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airports(dto_search)
            airport_dto = self.service.get_data_airport_by_id(selected_id)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=airport_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_airports', page=page, q=query))

    def delete_airport(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_airport(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_airports', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_airports', page=page, q=query))
        
       
    def view_airplanes(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['airplanes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page,search_query=query)        
        try:
            dto_response = self.service.get_data_airplanes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def create_airplane(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            airplane_code = request.form.get('airplane_code')
            model = request.form.get('model')
            range = request.form.get('range')
            speed = request.form.get('speed')
            if not all([airplane_code,model,range,speed]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= AirplanesDTO(airplane_code=airplane_code, model=model, range=range, speed=speed)
                    self.service.create_data_airplane(dto=dto_record)

                    flash("Запись успешно добавлена", "success")
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))

        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airplanes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airplanes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_airports', page=page, q=query))

    def update_airplane(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            airplane_code = request.form.get('airplane_code')
            model = request.form.get('model')
            range = request.form.get('range')
            speed = request.form.get('speed')
            if not all([airplane_code,model,range,speed]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= AirplanesDTO(airplane_code=airplane_code, model=model, range=range, speed=speed)
                    self.service.update_data_airplane(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query)) 
    
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airplanes(dto_search)
            airplane_dto = self.service.get_data_airplane_by_id(selected_id)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=airplane_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))

    def delete_airplane(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_airplane(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_airplanes', page=page, q=query))


    def view_flights(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['flights']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_flights(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def create_flight(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            flight_id = request.form.get('flight_id')
            status = request.form.get('status')
            scheduled_departure = request.form.get('scheduled_departure')
            scheduled_arrival = request.form.get('scheduled_arrival')
            actual_departure = request.form.get('actual_departure')or None
            actual_arrival = request.form.get('actual_arrival')or None
            route_no = request.form.get('route_no')
            departure_airport = request.form.get('departure_airport')
            arrival_airport = request.form.get('arrival_airport')
            if not all([scheduled_departure,scheduled_arrival,route_no,status]):
                    flash("Ошибка: заполните необходимые поля!", "warning")
            else:
                try:
                    dto_record= FlightsDTO(flight_id=flight_id, status=status, scheduled_departure=scheduled_departure, 
                                        scheduled_arrival=scheduled_arrival,route_no=route_no,actual_departure=actual_departure,
                                        actual_arrival=actual_arrival, departure_airport=departure_airport, arrival_airport=arrival_airport)
                    self.service.create_data_flight(dto=dto_record)
                    flash("Запись успешно добавлена", "success")              
                    return redirect(url_for('admin_bp.view_flights', page=page, q=query))
                except Exception as e:
                        flash(f"Ошибка при сохранении: {e}", "danger")
                        return redirect(url_for('admin_bp.view_flights', page=page, q=query))
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['flights']
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_flights(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]
            return render_template("admin/overlay.html", 
                                   data=data, 
                                   columns = columns,  
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_flights', page=page, q=query))

    def delete_flight(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_flight(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_flights', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_flights', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_flights', page=page, q=query))

    def update_flight(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            flight_id = request.form.get('flight_id')
            status = request.form.get('status')
            scheduled_departure = request.form.get('scheduled_departure')
            scheduled_arrival = request.form.get('scheduled_arrival')
            actual_departure = request.form.get('actual_departure')or None
            actual_arrival = request.form.get('actual_arrival')or None
            route_no = request.form.get('route_no')
            departure_airport = request.form.get('departure_airport')
            arrival_airport = request.form.get('arrival_airport')
            if not all([scheduled_departure,scheduled_arrival,route_no,status]):
                    flash("Ошибка: заполните необходимые поля!", "warning")
            else:
                try:
                    dto_record= FlightsDTO(flight_id=flight_id, status=status, scheduled_departure=scheduled_departure, 
                                        scheduled_arrival=scheduled_arrival,route_no=route_no,actual_departure=actual_departure,
                                        actual_arrival=actual_arrival, departure_airport=departure_airport, arrival_airport=arrival_airport)
                    self.service.update_data_flight(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_flights', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_flights', page=page, q=query)) 
    
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['flights']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_flights(dto_search)
            flight_dto = self.service.get_data_flight_by_id(selected_id)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=flight_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_flights', page=page, q=query))

        

    def view_bookings(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['bookings']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_bookings(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
    
    def create_booking(self):
        if request.method == 'POST':
            page = request.form.get('page', '1')
            query = request.form.get('q', '')

            book_ref = request.form.get('book_ref')
            book_date = request.form.get('book_date')
            total_amount = request.form.get('total_amount')
            ticket_no = request.form.get('ticket_no')
            passenger_id = request.form.get('passenger_id')
            passenger_name = request.form.get('passenger_name')
            outbound = request.form.get('outbound') == 'true'
            flight_id = request.form.get('flight_id')
            fare_conditions = request.form.get('fare_conditions')

            if not all([book_ref, book_date, total_amount, ticket_no, passenger_id, passenger_name,  flight_id, fare_conditions]):
                    flash("Ошибка: заполните необходимые поля!", "warning")
            else:
                try:
                    dto_record= BookingsDTO(book_ref=book_ref, book_date=book_date, total_amount=total_amount, ticket_no=ticket_no,
                                            passenger_id=passenger_id, passenger_name=passenger_name, outbound=outbound,flight_id=flight_id, fare_conditions=fare_conditions)
                    self.service.create_data_booking(dto=dto_record)
                    flash("Запись успешно добавлена", "success")              
                    return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
                except Exception as e:
                        flash(f"Ошибка при сохранении: {e}", "danger")
                        return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
                
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['bookings']
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_bookings(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]
            return render_template("admin/overlay.html", 
                                   data=data, 
                                   columns = columns,  
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
        
    def update_booking(self):
        if request.method == 'POST':
            page = request.form.get('page', '1')
            query = request.form.get('q', '')

            book_ref = request.form.get('book_ref')
            book_date = request.form.get('book_date')
            total_amount = request.form.get('total_amount')
            ticket_no = request.form.get('ticket_no')
            passenger_id = request.form.get('passenger_id')
            passenger_name = request.form.get('passenger_name')
            outbound = request.form.get('outbound') == 'true'
            flight_id = request.form.get('flight_id')
            fare_conditions = request.form.get('fare_conditions')

            if not all([book_ref, book_date, total_amount, ticket_no, passenger_id, passenger_name,  flight_id, fare_conditions]):
                    flash("Ошибка: заполните необходимые поля!", "warning")
            else:
                try:
                    dto_record= BookingsDTO(book_ref=book_ref, book_date=book_date, total_amount=total_amount, ticket_no=ticket_no,
                                            passenger_id=passenger_id, passenger_name=passenger_name, outbound=outbound,flight_id=flight_id, fare_conditions=fare_conditions)
                    self.service.update_data_booking(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_bookings', page=page, q=query))  
                
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['bookings']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_bookings(dto_search)
            booking_dto = self.service.get_data_booking_by_id(selected_id)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=booking_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_bookings', page=page, q=query))

    def delete_booking(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_booking(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_bookings', page=page, q=query))
        

    def view_boarding_passes(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['boarding_passes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query, page=page)
        try:
            dto_response = self.service.get_data_boarding_passes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500

    def create_boarding_pass(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            ticket_no = request.form.get('ticket_no')
            flight_id = request.form.get('flight_id')
            seat_no = request.form.get('seat_no')
            boarding_no = request.form.get('boarding_no')
            boarding_time = request.form.get('boarding_time')
            if not all([ticket_no, flight_id, seat_no, boarding_no, boarding_time]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= Boarding_passesDTO(ticket_no=ticket_no, flight_id=flight_id, seat_no=seat_no, boarding_no=boarding_no, boarding_time=boarding_time)
                    self.service.create_data_boarding_pass(dto=dto_record)

                    flash("Запись успешно добавлена", "success")
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))
                
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['boarding_passes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_boarding_passes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))

    def update_boarding_pass(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            ticket_no = request.form.get('ticket_no')
            flight_id = request.form.get('flight_id')
            seat_no = request.form.get('seat_no')
            boarding_no = request.form.get('boarding_no')
            boarding_time = request.form.get('boarding_time')
            if not all([ticket_no, flight_id, seat_no, boarding_no, boarding_time]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= Boarding_passesDTO(ticket_no=ticket_no, flight_id=flight_id, seat_no=seat_no, boarding_no=boarding_no, boarding_time=boarding_time)
                    self.service.update_data_boarding_pass(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query)) 
                
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['boarding_passes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_boarding_passes(dto_search)
            boarding_pass_dto = self.service.get_data_boarding_pass_by_id(selected_id)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=boarding_pass_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))

    def delete_boarding_pass(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_boarding_pass(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_boarding_passes', page=page, q=query))

    def view_routes(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['routes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_routes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def create_routes(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            route_no = request.form.get('route_no')
            airplane_code = request.form.get('airplane_code')
            departure_airport = request.form.get('departure_airport')
            arrival_airport = request.form.get('arrival_airport')
            scheduled_time = request.form.get('scheduled_time')
            duration = request.form.get('duration')
            days_of_week = request.form.get('days_of_week', '')
            v_start = request.form.get('validity_start')
            v_end = request.form.get('validity_end')
            
            if not all([route_no, airplane_code, departure_airport, arrival_airport, scheduled_time, duration, v_start, v_end]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= RoutesDTO(route_no=route_no, airplane_code=airplane_code, departure_airport=departure_airport, arrival_airport=arrival_airport,
                                          scheduled_time=scheduled_time, duration=duration, days_of_week=days_of_week, v_start=v_start, v_end=v_end)
                    self.service.create_data_routes(dto=dto_record)

                    flash("Запись успешно добавлена", "success")
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))

        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['routes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_routes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            flash("Ошибка при создании записи", "danger")
            return redirect(url_for('admin_bp.view_routes', page=page, q=query))

    def update_routes(self):
        if request.method == 'POST':
            page = request.form.get('page')
            query = request.form.get('q')
            route_no = request.form.get('route_no')
            airplane_code = request.form.get('airplane_code')
            departure_airport = request.form.get('departure_airport')
            arrival_airport = request.form.get('arrival_airport')
            scheduled_time = request.form.get('scheduled_time')
            duration = request.form.get('duration')
            days_of_week = request.form.get('days_of_week', '')
            v_start = request.form.get('validity_start')
            v_end = request.form.get('validity_end')
            if not all([route_no, airplane_code, departure_airport, arrival_airport, scheduled_time, duration, v_start, v_end]):
                flash("Ошибка: заполните абсолютно все поля!", "warning")
            else:
                try:
                    dto_record= RoutesDTO(route_no=route_no, airplane_code=airplane_code, departure_airport=departure_airport, arrival_airport=arrival_airport,
                                          scheduled_time=scheduled_time, duration=duration, days_of_week=days_of_week, v_start=v_start, v_end=v_end)
                    self.service.update_data_routes(dto=dto_record)
                    flash("Запись успешно изменена", "success")
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))
                except Exception as e:
                    flash(f"Ошибка при сохранении: {e}", "danger")
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))

        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_routes(dto_search)
            routes_dto = self.service.get_data_route_by_id(selected_id)
            print(routes_dto.v_end, routes_dto.v_start)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template('admin/overlay.html', 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns,
                                   item=routes_dto)
        except Exception as e:
            print(e)
            flash("Ошибка при изменении записи", "danger")
            return redirect(url_for('admin_bp.view_routes', page=page, q=query))

    def delete_routes(self):
        if request.method == 'POST':
            selected_id = request.form.get('selected_id')
            page = request.form.get('page', '1')
            query = request.form.get('q', '')
            if selected_id:
                try:
                    self.service.delete_data_routes(selected_id)
                    flash('Запись успешно удалена','success')
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))
                except Exception as e:
                    print(e)
                    flash("Ошибка при удалении записи", "danger")
                    return redirect(url_for('admin_bp.view_routes', page=page, q=query))
            else:
                flash("Выберите запись", "danger")
                return redirect(url_for('admin_bp.view_routes', page=page, q=query))




    

