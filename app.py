from flask import Flask,render_template,url_for,request,redirect
from flask_mysqldb import MySQL
from datetime import datetime

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='flask'

db=MySQL(app)





@app.route('/',methods=['POST','GET'])
def index():
    
    if request.method=='POST':

        
        task_content=request.form['content']
        
        

        
        try:
            
            cursor=db.connection.cursor()
            cursor.execute("INSERT INTO task (content) VALUES(%s)",(task_content,))
           
            db.connection.commit()
            cursor.close()
            return redirect('/')
        except:
            return "there was a error"

    else:
        cursor=db.connection.cursor()
        cursor.execute("SELECT * FROM task")
        tasks=cursor.fetchall()
        
        cursor.close()
        return render_template('index.html',tasks=tasks)
@app.route('/delete/<int:id>')    
def delete(id):
    
    try:
        cursor=db.connection.cursor()
        cursor.execute("DELETE from task where id=%s",(id,))
        db.connection.commit()
        cursor.close()
        return redirect('/')
    except:
        return "there was a error"
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    
    
    if request.method=='POST':
        new_content=request.form["new_content"]
        try:
            cursor=db.connection.cursor()

            cursor.execute("UPDATE task SET content= %s WHERE id= %s",(new_content,id,))
            db.connection.commit()
            return redirect('/')
        except:
            return "there was a error"
    else:
        cursor=db.connection.cursor()
        cursor.execute("SELECT * FROM task where id=%s",(id,))
        tasks=cursor.fetchone()
        
        cursor.close()
        return render_template('update.html',ids=id,old_content=tasks[1])

    

if __name__=="__main__":
    app.run(debug=True)