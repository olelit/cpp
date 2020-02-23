from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired

from app import db
from models import Country, DetailPlace, BoxFormat, Computer, ComputerType, Company


class CountryForm(FlaskForm):
    name = "Cтрана"
    id = "country_modal"

    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Add company')


class CompanyForm(FlaskForm):
    name = "Компания"
    id = "company_modal"

    title = StringField('title', validators=[DataRequired()])
    country = SelectField('Country', choices=[(x.id, x.title) for x in Country.query.all()], coerce=int,
                          validators=[DataRequired()])
    submit = SubmitField('Add company')


class ComputerTypeForm(FlaskForm):
    name = "Тип компьютера"
    id = "computer_type_modal"

    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ComputerForm(FlaskForm):
    name = "Компьютер"
    id = "computer_modal"
    computer_type = SelectField('Тип компьютера',
                                choices=[(x.id, x.title) for x in db.session.query(ComputerType).all()], coerce=int,
                                validators=[DataRequired()])

    box_format = SelectField('Формат корпуса',
                                choices=[(x.id, x.title) for x in db.session.query(BoxFormat).all()], coerce=int,
                                validators=[DataRequired()])

    company = SelectField('Формат корпуса',
                                choices=[(x.id, x.title) for x in db.session.query(Company).all()], coerce=int,
                                validators=[DataRequired()])

    title = StringField('title', validators=[DataRequired()])
    year = DateField('Дата выпуска', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class BoxFormatForm(FlaskForm):
    name = "Формат корпуса"
    id = "box_format_modal"

    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DetailPlaceForm(FlaskForm):
    name = "Расположение детали"
    id = "detail_place_modal"

    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DetailForm(FlaskForm):
    name = "Деталь"
    id = "detail_modal"

    title = StringField('title', validators=[DataRequired()])
    detail_place = SelectField('DetailPlace', choices=[(x.id, x.title) for x in db.session.query(DetailPlace).all()],
                               coerce=int,
                               validators=[DataRequired()])
    computer = SelectField('Компьютер',
                                choices=[(x.id, x.title) for x in db.session.query(Computer).all()], coerce=int,
                                validators=[DataRequired()])
    submit = SubmitField('Добавить')
