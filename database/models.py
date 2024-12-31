from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, SelectField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Optional

db = SQLAlchemy()

# Tabela de associação entre participantes e eventos
participant_events = db.Table('participant_events',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

# Tabela de presenças em encontros
meeting_attendance = db.Table('meeting_attendance',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
    db.Column('attended_at', db.DateTime, server_default=db.func.now())
)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    check_in_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relacionamento many-to-many com eventos
    events = db.relationship('Event',
                           secondary=participant_events,
                           lazy='subquery',
                           backref=db.backref('participants', lazy=True))

    # Adicionar relacionamento com presenças
    attended_meetings = db.relationship('Meeting',
                                      secondary=meeting_attendance,
                                      lazy='subquery',
                                      backref=db.backref('attendees', lazy=True))

    def __repr__(self):
        return f'<Participant {self.full_name}>'

    @property
    def event_count(self):
        return len(self.events)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    theme = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_participants = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Event {self.theme} on {self.date}>'

    @property
    def participant_count(self):
        return len(self.participants)

    @property
    def is_full(self):
        return self.max_participants and len(self.participants) >= self.max_participants

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    event = db.relationship('Event', backref=db.backref('meetings', lazy=True))

    def __repr__(self):
        return f'<Meeting {self.title}>'

    @property
    def registered_count(self):
        """Retorna o número de participantes registrados para este encontro através do evento"""
        return len(self.event.participants) if self.event else 0
    
    @property
    def attendance_count(self):
        """Retorna o número de participantes que compareceram ao encontro"""
        return len(self.attendees)
    
    @property
    def attendance_percentage(self):
        """Retorna a porcentagem de presença no encontro"""
        registered = self.registered_count
        if registered == 0:
            return 0
        return (self.attendance_count / registered) * 100

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
