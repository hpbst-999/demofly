from flask import render_template, request, redirect, session, flash

class AuthController:
    def __init__(self, service):
        self.service = service

    def login(self):
        if request.method == 'POST':
            user = self.service.verify_user(request.form['username'], request.form['password'])
            if user:
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect('/admin' if user.role == 'admin' else '/')
            flash("Ошибка входа")
        
        return render_template('auth/auth.html')

    def logout(self):
        session.clear()
        return redirect('/login')