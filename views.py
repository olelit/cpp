from time import strptime

from flask_breadcrumbs import register_breadcrumb

from app import app, db
from forms import *
from models import *
from flask import Flask, render_template, redirect, url_for, request

PER_PAGE_COUNT = 5
page_num = 1


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
@register_breadcrumb(app, '.', 'Страна')
def countries():
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    country_list = Country.query.paginate(per_page=PER_PAGE_COUNT, page=int(page_num), error_out=False)
    return render_template('index.html', list=country_list, type='company')


@app.route('/<int:country_id>/company')
@register_breadcrumb(app, '.country_id', 'Компания')
def companies(country_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    company_list = Company.query.filter_by(id=country_id).paginate(per_page=PER_PAGE_COUNT, page=int(page_num),
                                                                   error_out=False)
    return render_template('index.html', list=company_list, type='computer_type')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type')
@register_breadcrumb(app, '.country_id.company_id', 'Тип компьютера')
def computer_type(country_id, company_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    computer_type_list = ComputerType.query.paginate(per_page=PER_PAGE_COUNT, page=int(page_num), error_out=False)
    return render_template('index.html', list=computer_type_list, type='box_type')


@app.route('/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type')
@register_breadcrumb(app, '.country_id.company_id.computer_type_id', 'Тип корпуса')
def box_type(country_id, company_id, computer_type_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    box_type_list = BoxFormat.query.paginate(per_page=PER_PAGE_COUNT, page=int(page_num), error_out=False)
    return render_template('index.html', list=box_type_list, type='year')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year')
@register_breadcrumb(app, '.country_id.company_id.computer_type_id.box_type_id', 'Год выпуска')
def year(country_id, company_id, computer_type_id, box_type_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    year_list = Computer.query.with_entities(Computer.year).distinct().paginate(per_page=PER_PAGE_COUNT, page=int(page_num),
                                                                                error_out=False)
    return render_template('no_id.html', list=year_list, type='computer')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer')
@register_breadcrumb(app, '.country_id.company_id.computer_type_id.box_type_id.year', 'Компьютеры')
def computer(country_id, company_id, computer_type_id, year, box_type_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    computer_list = Computer.query.filter_by(year=year, company_id=company_id, box_format_id=box_type_id,
                                             computer_type_id=computer_type_id).paginate(per_page=PER_PAGE_COUNT,
                                                                                         page=int(page_num), error_out=False)
    return render_template('index.html', list=computer_list, type='detail_place')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer/<int:computer>/detail_place')
@register_breadcrumb(app, '.country_id.company_id.computer_type_id.box_type_id.year.computer', 'Расположение детали')
def detail_place(country_id, company_id, computer_type_id, year, computer, box_type_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    detail_place_list = Detail.query.filter_by(computer_id=computer).join(DetailPlace).with_entities(
        DetailPlace.id, DetailPlace.title).distinct().paginate(per_page=PER_PAGE_COUNT, page=int(page_num), error_out=False)
    return render_template('index.html', list=detail_place_list, type='detail')


@app.route(
    '/<int:country_id>/company/<int:company_id>/computer_type/<int:computer_type_id>/box_type/<int:box_type_id>/year/<year>/computer/<int:computer>/detail_place/<int:detail_pl>/detail')
@register_breadcrumb(app, '.country_id.company_id.computer_type_id.box_type_id.year.computer.detail_pl', 'Деталь')
def detail(country_id, company_id, computer_type_id, year, computer, detail_pl, box_type_id):
    page_num = request.args.get("page")
    if not page_num:
        page_num = 1
    detail_list = Detail.query.filter_by(computer_id=computer, detail_place_id=detail_pl).paginate(
        per_page=PER_PAGE_COUNT, page=int(page_num), error_out=False)
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
