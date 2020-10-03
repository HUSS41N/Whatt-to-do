import os
from flask import Flask,render_template,session,flash,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

###########################################

###################form####################
class ToDo(FlaskForm):
    add = StringField('ADD A TODO',validators=[DataRequired()])
    submit = SubmitField('ADD')


###########################################

###################DATABAE#################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
class TodoList(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    todo = db.Column(db.Text)

    def __init__(self,todo):
        self.todo = todo
   
    def __repr__(self):
        return f'{self.todo} '

###########################################

##################VIEWS####################

@app.route('/',methods=['GET','POST'])
def index():
    form = ToDo()
    if form.validate_on_submit():
        todo = TodoList(todo = form.add.data)
        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('index'))
    list_todo = TodoList.query.all()
    
 
    return render_template('index.html',form=form,list_todo=list_todo)

@app.route('/<int:todos_id>/delete',methods=['GET','POST'])
def delete(todos_id):
    deletetodo = TodoList.query.get_or_404(todos_id)
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)