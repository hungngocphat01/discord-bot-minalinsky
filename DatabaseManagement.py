import json 
# Database libraries
import os
import pandas as pd
from Logging import log
from BasicDefinitions import Base, session
from tabulate import tabulate

#############  Utility functions  #############
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

def legacy_query_execute(sql: str):
    if not session.is_active:
        log("Database session is not active")
        return None 
    
    # Execute sql
    try:
        resultproxy = session.execute(sql)
        return [x._asdict() for x in resultproxy]
    except:
        session.rollback()
        raise 

def tabular_format(lst: list):
    df = pd.DataFrame(lst)
    return tabulate(df, headers="keys")