from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

from infobox import InfoBox

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess stringhard to guess string'
bootstrap = Bootstrap(app)
todayText = InfoBox()
day_history = todayText.dayInHistory
translate = todayText.baiduTrans
textInbox = day_history


class NameForm(FlaskForm):
    textArea = TextAreaField('历史上的今天', render_kw={'cols': 30, 'rows': 4},
                             validators=[DataRequired()])
    submit = SubmitField('翻译并播放')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    global textInbox
    if form.validate_on_submit():
        textInbox = form.textArea.data
        flash(translate(textInbox))
        session['textArea'] = textInbox
        return redirect(url_for('index'))
    form.textArea.data = textInbox
    return render_template('index.html', form=form, textArea=textInbox)
