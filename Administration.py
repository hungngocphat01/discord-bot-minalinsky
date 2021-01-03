import json 

def is_admin(role_id) -> bool:
    conf = json.loads(open("configuration.json", mode="rt").read())
    admin_role_ids = conf["admin_role_ids"]

    return bool(role_id in admin_role_ids)