from time import strptime

from app import app, db
from forms import *
from models import *
from flask import Flask, render_template, redirect, url_for, request


@app.context_processor
def create_forms():
    return {'company_form': [
        CountryForm(),
        CompanyForm(),
        ComputerTypeForm(),
        ComputerForm(),
        BoxFormatForm(),
        DetailPlaceForm(),
        DetailForm()
    ]}


@app.route('/')
def countries():
    country_list = Country.query.all()
    return render_template('index.html', list=country_list, type='company')


@app.route('/<int:country_id>/company')
def companies(country_id):
    company_list = Company.query.filter_by(id=country_id)
    return render_template('index.html', list=company_list, type='computer_type')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type')
def computer_type(country_id, company_id):
    computer_type_list = ComputerType.query.all()
    return render_template('index.html', list=computer_type_list, type='year')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/year')
def year(country_id,company_id, computer_type_id):
    year_list = Computer.query.with_entities(Computer.year).distinct()
    print(year_list)
    return render_template('years.html', list=year_list, type='computer')


@app.route('/form/save', methods=['POST'])
def save():
    query = request.form
    id_model = query['form_id']
    title = query['title']
    elem = None

    if id_model == 'country_modal':
        elem = Country(title=title)
    if id_model == 'company_modal':
        elem = Company(title=title, country_id=query['country'])
    if id_model == 'computer_type_modal':
        elem = ComputerType(title=title)
    if id_model == 'computer_modal':
        elem = Computer(title=title, year=query['year'], computer_type_id=query['computer_type'],
                        company_id=query['company'], box_format_id=query['box_format'])
    if id_model == 'box_format_modal':
        elem = BoxFormat(title=title)
    if id_model == 'detail_place_modal':
        elem = DetailPlace(title=title)
    if id_model == 'detail_modal':
        elem = Detail(title=title, detail_place_id=query['detail_place'], computer_id=query['computer'])

    db.session.add(elem)
    db.session.commit()
    return redirect(url_for("countries"))
