from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, SelectField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Optional

db = SQLAlchemy()

# Tabela de associação entre participantes e eventos
participant_event = db.Table('participant_event',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

# Tabela de associação entre participantes e encontros
participant_meeting = db.Table('participant_meeting',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
)

class Participant(db.Model):
    """Modelo para participantes."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    city = db.Column(db.String(100))
    check_in_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    events = db.relationship('Event', secondary=participant_event,
                           backref=db.backref('participants', lazy='dynamic'))
    meetings = db.relationship('Meeting', secondary=participant_meeting,
                             backref=db.backref('participants', lazy='dynamic'))

    def __repr__(self):
        return f'<Participant {self.name}>'

class Event(db.Model):
    """Modelo para eventos."""
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    meetings = db.relationship('Meeting', backref='event', lazy=True,
                             cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.theme}>'

class Meeting(db.Model):
    """Modelo para encontros."""
    __tablename__ = 'meeting'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    attendances = db.relationship('Attendance', backref='meeting', lazy=True,
                                cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Meeting {self.title}>'

class Attendance(db.Model):
    """Modelo para registro de presença em encontros."""
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    present = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Attendance meeting={self.meeting_id} participant={self.participant_id}>'

class MeetingForm(FlaskForm):
    event_id = SelectField('Evento', validators=[DataRequired()], coerce=int)
    title = StringField('Título', [DataRequired()])
    date = DateField('Data', [DataRequired()])
    time = TimeField('Hora', [DataRequired()])
    description = TextAreaField('Descrição', [Optional()])

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        from app import Event  # Import aqui para evitar importação circular
        self.event_id.choices = [(event.id, event.theme) for event in Event.query.all()]

class MeetingFormInline(FlaskForm):
    title = StringField('Título', [DataRequired()])
    date = DateField('Data', [DataRequired()])
    time = TimeField('Hora', [DataRequired()])
    description = TextAreaField('Descrição', [Optional()])

class EventForm(FlaskForm):
    theme = StringField('Tema', [DataRequired()])
    date = DateField('Data', [DataRequired()])
    description = TextAreaField('Descrição', [Optional()])
    max_participants = IntegerField('Máximo de Participantes', [DataRequired()])
    meetings = FieldList(FormField(MeetingFormInline), min_entries=1, max_entries=10)
