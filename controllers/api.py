# Here go your api methods.
@auth.requires_login()
def edit():
    """
    - "/edit/3" it offers a form to edit a checklist.
    'edit' is the controller (this function)
    '3' is request.args[0]
    """

    q = ((db.checklist.user_email == auth.user.email) &
        (db.checklist.id == request.vars.id))
    CurrentPost=db(q).select().first()
    CurrentPost.update_record(title = request.vars.title , memo = request.vars.memo)
    #redirect(URL('default', 'index'))
    return "ok"
