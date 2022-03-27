from app import app
from .models import VotesModel,CandidateModel, UserModel,db
from flask import redirect, render_template, flash,url_for,request
from flask_login import login_required, current_user,logout_user
from flask_cors import cross_origin
import string
import json
import random

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/profile")
@login_required
def profile():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    voter = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    return render_template("profile.html",name=current_user.name,prez=prez,vice=vice,voter=voter)

@app.route("/profile", methods=["POST"])
def post_vote():
    president = request.form.get('president')
    vicepresident = request.form.get('vice-president')

    voted = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    if not voted:
        voter = VotesModel(roll_num=current_user.roll_num,voter_id=current_user.id,post_1=int(president),post_2=int(vicepresident))
        db.session.add(voter)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))
    

@app.route("/candidate")
def candidate():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    return render_template("candidate.html",prez=prez,vice=vice)

@app.route("/candidate_register")
@login_required
def candidate_register():
    if current_user.admin !=1:
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("candidate_register.html")

@app.route("/candidate_register", methods=["POST"])
def candidate_post():
    roll_num = request.form.get('roll_num')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    batch = request.form.get('batch')
    course = request.form.get('course')
    department = request.form.get('department')
    post = request.form.get('post')
    pic_path = request.form.get('pic_path')
    agenda = request.form.get('agenda')
    
    roll_no = UserModel.query.filter_by(roll_num =roll_num).first()
    cand = CandidateModel.query.filter_by(roll_num = roll_num).first()

    error = False

    if not 10000000 <= int(roll_no) < 99999999:
        flash('Roll Number is not valid. Should be 8 digits.','error')
        error = True

    if cand:
        flash('Candidate has already been registered.','error')
        return redirect(url_for('candidate_register'))
    
    if not set(first_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True
    
    if not set(last_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True

    if not first_name and not last_name:
        flash('Name cannot be left blank.','error')
        error = True

    if not batch and not course and not department:
        flash('Please fill in all the details. Batch, Course and Department information is neccessary.','error')
        error = True
    
    if error:
        return redirect(url_for('candidate_register'))
    else:
        candidate = CandidateModel(roll_num=roll_num, first_name=first_name,last_name=last_name,batch=batch,course=course,department=department,post=post,pic_path=pic_path,agenda=agenda)
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate successfully registered.','success')
        return redirect(url_for('candidate_register'))

@app.route("/live_result")
def live_result():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.roll_num).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.roll_num).count()
        data1.append(vote)
 
    return render_template('graph.html',labels=labels,data=data,labels1=labels1,data1=data1)


@app.route("/vote/count")
@cross_origin()
def voteCount():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.roll_num).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.roll_num).count()
        data1.append(vote)

    output = {"data": data,
            "labels": labels,
            "data1": data1,
            "labels1": labels1}
    response = app.response_class(
        response=json.dumps(output),
        status=200,
        mimetype='application/json'
    )
    return response
