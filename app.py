from flask import Flask, session,redirect,render_template,url_for,request,flash
import data_manager
import data


app=Flask(__name__)
app.secret_key='secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        if data_manager.check_login(email,password):
            session['email']=request.form.get('email')
            session['password']=request.form.get('password')
            session['index']=0
            session[' correct_answer']=0
            return redirect('/')
        else:
            flash( "Wrong password")
            return redirect('/')
    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
        session.pop('email')
        session.pop('password')
        return redirect(url_for('index'))

@app.route('/test', methods=['GET','POST'])
def test():
    test=data.questions
    list_questions=[]
    for i in test:
        list_questions.append(i)
    number_of_questions = len(test)
    if request.method=='POST':
        answer=request.form.get('answer')
        if answer=='True':
            session[' correct_answer']+=1
    if  session['index'] ==number_of_questions:
        return redirect('/result')
    current_question=list_questions[session['index']]
    current_answer= test[list_questions[session['index']]]
    session['index'] +=1
    return render_template('/test.html',current_question=current_question,number_of_questions=number_of_questions, test=test,list_questions=list_questions,current_answer=current_answer)

@app.route('/result')
def result():
    if 'email' in session:
        if 'password' in session:
            return render_template('result.html')
        else:
            return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,
            port=5000)



