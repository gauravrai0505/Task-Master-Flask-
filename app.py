from flask import Flask, render_template,url_for,request,redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

#from werkzeug.wrappers import request

app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) #initializing database

#creating a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #reference for the ID of each entry
    content = db.Column(db.String(200), nullable=False)#text column which hold each task and 200 characters nullable is required
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #return a string everytime we create a new element
    def __repr__(self):
        return'<Task %r>' % self.id #so everytime we make a new element its going to return a task and id of that task created


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'there was issue adding your task'
   
   
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')                             
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting that task'   
        
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
            

if __name__  == "__main__":
    app.run(debug=True)