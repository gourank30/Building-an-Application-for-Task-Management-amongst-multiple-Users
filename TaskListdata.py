from google.appengine.ext import ndb

class TaskListdata(ndb.Model):
    taskboard_name=  ndb.StringProperty()
    task_creater=ndb.StringProperty(repeated=False)
    task_name=ndb.StringProperty(repeated=False)
    task_allocated_user=ndb.StringProperty(repeated=False)
    task_Status=ndb.StringProperty()
    task_due_date=ndb.StringProperty()
    task_completed_date_time=ndb.StringProperty()
