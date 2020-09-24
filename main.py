import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from TaskListdata import TaskListdata
from TaskBoarddata import TaskBoarddata
from datetime import datetime


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
            url = ''
            url_string = ''
            myuser=''
            user =''
            welcome = 'Welcome back'
            user= users.get_current_user()
            if user:
                template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                self.response.write(template.render())
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'
                myuser_key = ndb.Key('MyUser', user.email())
                myuser = myuser_key.get()
                if myuser == None:
                    welcome = 'Welcome to the application'
                    myuser = MyUser(id=user.email())
                    myuser.email_address=user.email()
                    myuser.put()

            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'
            template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
            }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

class boardadd(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user()
        if self.request.get('Submit'):
            taskboard=ndb.Key('TaskBoarddata',user.email()+""+self.request.get('board')).get()
            if taskboard==None:
                x=TaskBoarddata(id=user.email()+""+self.request.get('board'))
                x.taskboard_name=self.request.get('board')
                x.taskboard_owner_name=user.email()
                x.taskboard_participant.append(user.email())
                x.put()
                myuser = ndb.Key('MyUser', user.email()).get()
                myuser.i.append(user.email()+""+self.request.get('board'))
                myuser.put()
                self.redirect('/')
            else:
                self.response.write('dashboard already exits!!!!')
                self.redirect('/')
        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render())

class boarddisplay(webapp2.RequestHandler):
    def get(self):
        x=[]
        user= users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email()).get()
        myuser_key.i
        if myuser_key.i ==None:
            self.response.write('errror')
        else:
             taskboardlist=myuser_key.i
             for i in taskboardlist:
                    taskboard=ndb.Key('TaskBoarddata',i).get()
                    x.append(taskboard)
        self.response.write(self.request.get('taskboard_name'))
        template_values = {
        'x':x
        }
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))

class vi(webapp2.RequestHandler):
    def get(self):
        x=[]
        user=users.get_current_user()
        taskboard_name=self.request.get('taskboard_name')
        taskboard_owner_name=self.request.get('taskboard_owner_name')
        value_id=self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')
        myuser_key = ndb.Key('TaskBoarddata',value_id). get()
        myuser_key.task
        if myuser_key.task ==None:
            self.response.write('errror')
        else:
             taskboardlist=myuser_key.task
             for i in taskboardlist:
                    taskboard=ndb.Key('TaskListdata',i).get()
                    x.append(taskboard)
        template_values={
        'taskboard_name':taskboard_name,
        'taskboard_owner_name':taskboard_owner_name,
        'x':x
        }
        template = JINJA_ENVIRONMENT.get_template('dash.html')
        self.response.write(template.render(template_values))


class dashboard(webapp2.RequestHandler):
    def get(self):

        action=self.request.get('task')
        action1 =self.request.get('invite')
        user=users.get_current_user()

        if action :
            x=ndb.Key('TaskListdata',self.request.get('taskboard_name')+""+self.request.get('task_name')).get()
            if x==None:
                if self.request.get('task_Status')=='':
                    b=False
                else:
                    b=self.request.get('task_Status')
                action=self.request.get('task')
                user=users.get_current_user()
                x=TaskListdata(id=self.request.get('taskboard_name')+""+self.request.get('task_name'))
                x.taskboard_name=self.request.get('taskboard_name')
                x.task_creater=user.email()
                x.task_Status=str(b)
                if self.request.get('task_Status')=='True':
                    x.task_completed_date_time=now.strftime("%d/%m/%Y %H:%M:%S")
                x.task_allocated_user=self.request.get('task_allocated_user')
                x.task_name=self.request.get('task_name')
                x.task_due_date=self.request.get('task_due_date')
                x.put()
                o=user.email()+""+self.request.get('taskboard_name')
                mytask = ndb.Key('TaskBoarddata', self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')).get()
                mytask.task.append(self.request.get('taskboard_name')+""+self.request.get('task_name'))
                mytask.put()
                self.redirect('/')
            else:
                self.response.write('task already present in task boad')
                self.redirect('/')


        elif action1=="invite":
            self.response.write('action1')
            admin=self.request.get('taskboard_owner_name')
            self.response.write(self.request.get('taskboard_owner_name'))
            if admin==user.email():
                myuser_key = ndb.Key('MyUser', self.request.get('user'))
                myuser = myuser_key.get()
                if myuser == None:
                    myuser = MyUser(id=self.request.get('user'))
                    myuser.email_address=self.request.get('user')
                    myuser.i.append(user.email()+""+self.request.get('taskboard_name'))
                    myuser.put()
                    mytask = ndb.Key('TaskBoarddata',user.email()+""+self.request.get('taskboard_name') ).get()
                    mytask.taskboard_participant.append(self.request.get('user'))
                    mytask.put()
                    self.redirect('/')
                else:
                    myuser = ndb.Key('MyUser', self.request.get('user')).get()
                    myuser.i.append(user.email()+""+self.request.get('board'))
                    myuser.put()
                    mytask = ndb.Key('TaskBoarddata',user.email()+""+self.request.get('taskboard_name') ).get()
                    mytask.taskboard_participant.append(self.request.get('user'))
                    mytask.put()
                    self.redirect('/')
            else:
                self.response.write('Please Contact Admin To add participant.')
                self.redirect('/')

        template_values = {
        'taskboard_name':self.request.get('taskboard_name'),
        'taskboard_owner_name':self.request.get('taskboard_owner_name'),
        'list':list,
        'task_Status':self.request.get('task_Status')
        }
        template = JINJA_ENVIRONMENT.get_template('dash.html')
        self.response.write(template.render(template_values))

class stat(webapp2.RequestHandler):
    def get(self):
        now =datetime.now()
        mytask = ndb.Key('TaskListdata', self.request.get('taskboard_name')+""+self.request.get('task_name')).get()
        if mytask.task_Status=='False':
            mytask.task_Status='True'
            mytask.task_completed_date_time=now.strftime("%d/%m/%Y %H:%M:%S")
            mytask.put()
            self.redirect('/')
        else:
            self.response.write('allready Completed!! TRY TO DELETE!!')
            self.redirect('/')
        template_values = {
        'taskboard_name':self.request.get('taskboard_name'),
        'taskboard_owner_name':self.request.get('taskboard_owner_name')
        }
        template = JINJA_ENVIRONMENT.get_template('dash.html')
        self.response.write(template.render(template_values))

class delet(webapp2.RequestHandler):
    def get(self):
        x=self.request.get('taskboard_name')+""+self.request.get('task_name')
        mytask = ndb.Key('TaskListdata', self.request.get('taskboard_name')+""+self.request.get('task_name')).get()
        mytask.key.delete()
        myboard= ndb.Key('TaskBoarddata', self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')).get()
        myboard.task.remove(x)
        myboard.put()
        self.redirect('/')
        template_values = {
        'taskboard_name':self.request.get('taskboard_name'),
        'taskboard_owner_name':self.request.get('taskboard_owner_name')
        }
        template = JINJA_ENVIRONMENT.get_template('dash.html')
        self.response.write(template.render(template_values))
class edittask(webapp2.RequestHandler):
    def get(self):
        taskboard_name=self.request.get('taskboard_name')
        task_name=self.request.get('task_name')
        taskboard_owner_name=self.request.get('taskboard_owner_name')
        myboard= ndb.Key('TaskListdata', self.request.get('taskboard_name')+""+self.request.get('task_name')).get()
        if self.request.get('edit'):
            now =datetime.now()
            x=TaskListdata(id=self.request.get('taskboard_name')+""+self.request.get('task_name'))
            x.taskboard_name=self.request.get('taskboard_name')
            x.task_creater=self.request.get('task_creater')
            x.task_Status=self.request.get('task_Status')
            x.task_allocated_user=self.request.get('task_allocated_user')
            x.task_name=self.request.get('task_name')
            if self.request.get('task_completed_date_time')=='':
                if self.request.get('task_Status')=='True':
                    x.task_completed_date_time=now.strftime("%d/%m/%Y %H:%M:%S")
            else:
                x.task_completed_date_time=self.request.get('task_completed_date_time')
            x.task_due_date=self.request.get('task_due_date')

            x.put()
            self.redirect('/')

        elif self.request.get('cancle'):
            self.redirect('/')

        template_values = {
        'myboard':myboard,
        'taskboard_name':self.request.get('taskboard_name'),
        'taskboard_owner_name':self.request.get('taskboard_owner_name'),
        'task_name':self.request.get('task_name')
        }
        template = JINJA_ENVIRONMENT.get_template('taskedit.html')
        self.response.write(template.render(template_values))


class modifyboard(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        taskboard_name=self.request.get('taskboard_name')
        taskboard_owner_name=self.request.get('taskboard_owner_name')
        myboard= ndb.Key('TaskBoarddata', self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')).get()

        if self.request.get('Modify'):
            if taskboard_name==self.request.get('taskboard_name1'):
                edit= TaskBoarddata(id= self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name'))
                myboard= ndb.Key('TaskBoarddata', self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')).get()

                self.response.write(myboard)
                for i in myboard.task:
                    mytask = ndb.Key('TaskListdata', i).get()
                    if mytask.task_allocated_user==self.request.get('use'):
                        mytask.task_allocated_user==''
                        mytask.put()

                edit.taskboard_name=self.request.get('taskboard_name')
                if self.request.get('use')!='':
                    y=[]
                    if self.request.get('use') in y:
                        edit.taskboard_participant.remove(self.request.get('use'))
                edit.put()

                if self.request.get('use')!='':
                    x=[]
                    id=self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')
                    myuser = ndb.Key('MyUser', self.request.get('use')).get()
                    x=myuser.i
                    if id in x:
                        myuser.i.remove(self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name'))
                    else:
                        self.response.write('User was not in the board')
                    myuser.put()
                    self.redirect('/')
            elif self.request.get('taskboard_name1')!=taskboard_name:
                myboard= ndb.Key('TaskBoarddata', self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')).get()
                edit= TaskBoarddata(id= self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name1'))


                self.response.write(myboard)
                for i in myboard.task:
                    mytask = ndb.Key('TaskListdata', i).get()
                    if mytask.task_allocated_user==self.request.get('use'):
                        mytask.task_allocated_user==''
                        mytask.put()

                edit.taskboard_name=self.request.get('taskboard_name1')
                if self.request.get('use')!='':
                    y=[]
                    if self.request.get('use') in y:
                        edit.taskboard_participant.remove(self.request.get('use'))
                edit.put()

                if self.request.get('use')!='':
                    x=[]
                    id=self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name')
                    myuser = ndb.Key('MyUser', self.request.get('use')).get()
                    x=myuser.i
                    if id in x:
                        myuser.i.append(self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name1'))
                        myuser.i.remove(self.request.get('taskboard_owner_name')+""+self.request.get('taskboard_name'))
                    else:
                        self.response.write('User was not in the board')
                    myuser.put()
                myboard.key.delete()
                myboard.put()
                self.redirect('/')

        elif self.request.get('Cancle'):
            self.redirect('/')
        template_values = {
        'myboard':myboard,
        'taskboard_name':self.request.get('taskboard_name'),
        'taskboard_owner_name':self.request.get('taskboard_owner_name')
        }
        template = JINJA_ENVIRONMENT.get_template('boardedit.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([ ('/', MainPage),('/modifyboard',modifyboard),('/edittask',edittask),('/delet',delet),('/stat',stat),('/boardadd',boardadd),('/boarddisplay',boarddisplay),('/dashboard',dashboard),('/vi',vi)], debug=True)
