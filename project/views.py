
###################################
############IMPORTS################
import datetime
from functools import wraps
from flask import Flask, flash, redirect, render_template ,request, session, url_for, Blueprint 
from forms import SpidersForm
import subprocess
import os


####################################
##########CONFIGURATIONS############
spiders_blueprint = Blueprint('spiders', __name__)

####################################
########## HELPER FUNCTIONS ########


@spiders_blueprint.route('/', methods = ['GET','POST'])
def start_spiders():
	form = SpidersForm(request.form)
	error = None	
	os.getcwd()
	if request.method == 'POST' and form.validate_on_submit:
		spider_choice =  form.spider_choice.data		
		
		path = os.getcwd()		
		os.chdir('Spiders')		
		spider_choice = spider_choice.replace("'",'')
		os.system("python main.py %s" %(spider_choice))
		os.chdir(path)
		flash('Successfully started spider: . %s' %(spider_choice))
		
		
	return render_template('tasks.html', form = form, error = error)



# @tasks_blueprint.route('/complete/<int:task_id>/')
# @login_required
# def complete(task_id):
# 	new_id = task_id
# 	task = db.session.query(Task).filter_by(task_id = new_id)
# 	if session['user_id'] == task.first().user_id or session['role'] == 'admin':		
# 		task.update({'status':"0"})
# 		db.session.commit()	
# 		flash('Task was marked as complete.')
# 		return redirect(url_for('tasks.tasks'))
# 	else:
# 		flash('You can only update tasks that belong to you.')
# 		return redirect(url_for('tasks.tasks'))


# # 
