from google.appengine.ext import ndb

class TaskBoarddata(ndb.Model):
    taskboard_owner_name=ndb.StringProperty(repeated=False)
    taskboard_name=  ndb.StringProperty(repeated=False)
    taskboard_participant=ndb.StringProperty(repeated=True)
    task=ndb.StringProperty(repeated=True)
