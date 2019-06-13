""" from flask_table import Table, Col, LinkCol
 
class Results(Table):
    user_id = Col('Id', show=False)
    user_Name = Col('Name')
    user_Email = Col('Email')
    user_PhoneNumber = Col('Phone Number')
    TicketFrom = Col('From')
    TicketTo = Col('To')
    TicketTime = Col('Time')
    TicketDate = Col('Date')
    Tickets = Col('Tickets')
    TicketPrice = Col('Price')
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='user_id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'))"""
