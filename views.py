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
    return render_template('index.html', list=computer_type_list, type='box_type')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type')
def box_type(country_id, company_id, computer_type_id):
    box_type_list = BoxFormat.query.all()
    return render_template('index.html', list=box_type_list, type='year')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year')
def year(country_id, company_id, computer_type_id, box_type_id):
    year_list = Computer.query.with_entities(Computer.year).distinct()
    return render_template('no_id.html', list=year_list, type='computer')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer')
def computer(country_id, company_id, computer_type_id, year, box_type_id):
    computer_list = Computer.query.filter_by(year=year, company_id=company_id, box_format_id=box_type_id, computer_type_id=computer_type_id)
    return render_template('index.html', list=computer_list, type='detail_place')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer/<int:computer>/detail_place')
def detail_place(country_id, company_id, computer_type_id, year, computer, box_type_id):
    detail_place_list = Detail.query.filter_by(computer_id=computer).join(DetailPlace).with_entities(
        DetailPlace.id, DetailPlace.title).distinct()
    return render_template('index.html', list=detail_place_list, type='detail')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer/<int:computer>/detail_place/<int:detail_pl>/detail')
def detail(country_id, company_id, computer_type_id, year, computer, detail_pl, box_type_id):
    detail_list = Detail.query.filter_by(computer_id=computer, detail_place_id=detail_pl)
    return render_template('index.html', list=detail_list, type='')


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
