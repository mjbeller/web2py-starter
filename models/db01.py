# -*- coding: utf-8 -*-

DEBUG = True

from gluon import current

# track changes for modules
from gluon.custom_import import track_changes
track_changes(DEBUG)

# set utc as standard time for app
request.now = request.utcnow

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.14.1 or newer")

# request.requires_https()

# application configuration using private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=DEBUG)
current.myconf = myconf
myconf_env = myconf.get('environment.type')
current.myconf_env = myconf_env

# set db connection
if not request.env.web2py_runtime_gae:
    # if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get(myconf_env + 'db.uri'),
             pool_size=myconf.get(myconf_env + 'db.pool_size'),
             migrate_enabled=myconf.get(myconf_env + 'db.migrate'),
             check_reserved=['mysql', 'postgres'],  # ['all'])
             lazy_tables=True)
else:
    # connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    # store sessions and tickets there
    session.connect(request, response, db=db)
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

# choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# static assets folder versioning
# response.static_version = '0.0.0'

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db, host_names=myconf.get(myconf_env + 'host.name'))
service = Service()
plugins = PluginManager()

# define custom auth fields (before creating auth tables)
auth.settings.extra_fields['auth_user'] = [
    Field(
        'bookmarks', length=4096,
        # filter_in = lambda bm_obj: repr(bm_obj),  # could be str()
        # filter_out = lambda bm_str: eval(bm_str) if bm_str else {},  # could be ast.literal_eval
        represent=(lambda v, r: BEAUTIFY(eval(v)) if v else None),
        readable=False, writable=False,
        default={}
    )
]

# create all tables needed by auth
auth.define_tables(username=True, signature=True)

# add auth formatting, validation, and representation
db.auth_user._format = '%(first_name)s %(last_name)s (%(id)s)'  # defaults to '%(username)'

# configure email
mail = auth.settings.mailer
mail.settings.server = myconf.get(myconf_env + 'smtp.server')
mail.settings.sender = myconf.get(myconf_env + 'smtp.sender')
mail.settings.login = myconf.get(myconf_env + 'smtp.login')
mail.settings.tls = myconf.get(myconf_env + 'smtp.tls') or False
mail.settings.ssl = myconf.get(myconf_env + 'smtp.ssl') or False

# configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False  # defaults to True
auth.settings.expiration = 60 * 60 * 24  # seconds

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# add db, auth, mail to current for access from modules
current.db = db
current.auth = auth
current.mail = mail
