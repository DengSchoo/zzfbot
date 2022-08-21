super_user = '1425123490'
admins = ['2787614041', '1425123490']
users = ['2787614041', '1425123490']

def add_usr(userid):
    users.__add__(userid)


def warden_admin(id):
    # 判断是否是wly
    if id == super_user:
        return True
    return False

def warden_admin(id):
    # 判断是否是wly
    if id in admins:
        return True
    return False

def warden_messgae(id):
    # 判断是否是wly
    if id in lovers:
        return True
    return False