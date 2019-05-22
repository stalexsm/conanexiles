from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class BuyForm(FlaskForm):
    login = StringField('Ник', render_kw={"placeholder": "Введите ник как в игре"}, validators=[DataRequired(), Length(0, 99)])
    steam_id = StringField('Идентификатор steam', render_kw={"placeholder": "steam_id"}, validators=[Length(0, 64)])
    submit = SubmitField('Заказать')
