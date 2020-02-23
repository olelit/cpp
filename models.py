from app import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    companies = db.relationship('Company', backref='country')

    def __repr__(self):
        return '<Country %r>' % self.title


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'),
                           nullable=False)
    computers = db.relationship('Computer', backref='company')

    def __repr__(self):
        return '<Company %r>' % self.title


class ComputerType(db.Model):  # ноутбук, настольный...
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    computers = db.relationship('Computer', backref='computer_type')

    def __repr__(self):
        return '<Computer Type %r>' % self.title


class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    computer_type_id = db.Column(db.Integer, db.ForeignKey('computer_type.id'),
                                 nullable=False)
    box_format_id = db.Column(db.Integer, db.ForeignKey('box_format.id'),
                            nullable=False)

    details = db.relationship('Detail', backref='computer_detail')

    year = db.Column(db.Integer)

    def __repr__(self):
        return '<Computer %r>' % self.title


class BoxFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    computers = db.relationship('Computer', backref='computer_type_box')

    def __repr__(self):
        return '<Box Format %r>' % self.title


class DetailPlace(db.Model):  # распаяна на плате, внешняя...
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    details = db.relationship('Detail', backref='detail_place')

    def __repr__(self):
        return '<Detail Type %r>' % self.title


class Detail(db.Model):  # деталь (видеокарта, процессор)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    detail_place_id = db.Column(db.Integer, db.ForeignKey('detail_place.id'),
                                nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'),
                                nullable=False)


    def __repr__(self):
        return '<Detail %r>' % self.title
