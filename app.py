from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Необходим для защиты формы

db = SQLAlchemy(app)

# Модель для хранения записей
class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

# Форма для ввода записи
class GuestbookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])

# Главная страница с поиском
@app.route('/')
def index():
    search_query = request.args.get('search')
    if search_query:
        entries = GuestbookEntry.query.filter(
            GuestbookEntry.name.contains(search_query) |
            GuestbookEntry.message.contains(search_query)
        ).all()
    else:
        entries = GuestbookEntry.query.all()

    form = GuestbookForm()
    return render_template('index.html', entries=entries, form=form)

# Обработчик добавления записи
@app.route('/sign', methods=['POST'])
def sign_guestbook():
    form = GuestbookForm()
    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data
        new_entry = GuestbookEntry(name=name, message=message)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'errors': form.errors}), 400

# Обработчик удаления записи
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = GuestbookEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
