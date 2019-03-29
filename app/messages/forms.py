from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l

class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[DataRequired(),
                                                      Length(min=0, max=140)])
    submit = SubmitField(_l('Send'))


class MessageReplyForm(FlaskForm):
    reply = TextAreaField(_l('Reply'), validators=[DataRequired(),
                                                   Length(min=0, max=140)])
    send = SubmitField(_l('Send'))
