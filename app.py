from flask import Flask, render_template, request, redirect, url_for,Response,session
import emailsend
import pose
import os
secret_key = os.urandom(24)
choice=1
emailID=""
performed=False
app = Flask(__name__)
app.secret_key = secret_key
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'emailID' in session and 'choice' in session:
        return redirect(url_for("emailing"))
    if request.method == "POST":
        emailID = request.form["email"]
        choice = request.form["option"]
        session['emailID'] = emailID
        session['choice'] = choice
        return redirect(url_for("video"))
    return render_template('index.html')
    
@app.route('/video')
def video():
        return Response(pose.capture(session['choice']),mimetype='multipart/x-mixed-replace;boundary=frame')
@app.route('/emailing')
def emailing():
        if 'emailID' in session and 'choice' in session:
            emailID = session['emailID']
            msg = pose.msg
            emailsend.send_mail("Fitness Corner Participant", emailID, msg)
            session.pop('emailID', None)
            session.pop('choice', None)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
if __name__ == '__main__':
    app.run(debug=True)
 