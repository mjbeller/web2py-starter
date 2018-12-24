'''
### in-common controller functions
###Insert notification trigger functions here

# these functions should return a dictionary, Eg.:
        # return dict(
        #     title='Invalid Filter Label(s) - '+str(survey.title.title()) + ' Survey ',
        #     message=message,
        #     message_type = 'warning',
        #     controller = 'filter_labels',
        #     function = 'list',
        #     survey_id = survey.id)
'''

# These functions are found in the db00_helpers.py file due to being needed for survey list view

### END in-common controller functions

def index():
    redirect(URL(request.controller, 'list'))

@auth.requires_login()
def list():
    num_notifications = len(all_notifications)
    notifications = all_notifications


    response.view_title = '%s %s %s' % (
        request.controller.replace('_', ' ').title(),
        ' |',
        request.function.replace('_', ' ').title(),
    )

    message_types = []
    for note in notifications:
        message_types.append(note['message_type'])

    return locals()

def menu():
    # notification check functions

    return dict(
        num_notifications = len(all_notifications),
        notifications = all_notifications
        )
