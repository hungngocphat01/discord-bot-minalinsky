import json 
from BasicDefinitions import session, Base
from sqlalchemy import create_engine, update
from Logging import *

def query_settings(field: str):
    Settings = Base.classes.settings
    try:
        settings_value = session.query(Settings).filter(Settings.field == field).one()
    except:
        session.rollback()
        raise
    return settings_value.value

def is_admin(role_id) -> bool:
    return (role_id in query_settings("admin_role_ids"))

def mark_as_notified(day, month):
    Events = Base.classes.events 
    try:
        for c in session.query(Events).filter(Events.day == day, Events.month == month):
            c.notified = True
            log("Notified=true")
        session.commit()
    except:
        session.rollback()
        raise