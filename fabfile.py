from fabric.api import *
import datetime, os

APPNAME = 'troebr.net'
VERSION = datetime.datetime.now().strftime('%Y%m%d_%H%M')
FILENAME = '%s_%s.tar.gz' % (APPNAME, VERSION)

APPROOT = '/home/troebr/troebr.net'
DEVROOT = os.path.dirname(os.path.abspath(__file__))

# the user to use for the remote commands
env.user = 'troebr'
# the servers where the commands are executed
env.hosts = ['new.troebr.net']
env.activate = 'source '+ os.path.join(APPROOT, 'bin/activate')
env.deploy_user = 'troebr'


def up():
    pack()
    deploy()
    restart()
    clean()

def clup():
    """Removes troebr.net/troebr."""
    pack()
    
    # Save gunicorn.pid
    
    run('rm -rf %s/troebr' % APPROOT)
    up()

def pack():
    # create a new source distribution as tarball
    with cd(DEVROOT):
        local('tar -czf dist/%s $(git ls-files)' % FILENAME, capture=False)

def deploy():
    
    # upload the source tarball to the temporary folder on the server
    with cd(DEVROOT):
        put('dist/%s' % FILENAME, '/tmp/%s' % FILENAME)
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('rm -rf /tmp/%s && mkdir /tmp/%s' % (APPNAME, APPNAME))
    with cd('/tmp/%s' % APPNAME):
        run('tar xzf /tmp/%s' % FILENAME)
        run('cp -r /tmp/%s/* %s' % (APPNAME, APPROOT))
    
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    # run('touch /var/www/%s.wsgi' % APPNAME)


def clean():
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/%s /tmp/%s' % (APPNAME, FILENAME))
    
def restart():
    """Restart gunicorn."""
    with settings(warn_only=True):    
        run('kill -HUP $(cat %s/gunicorn.pid)' % APPROOT)



# TOOLS 
def virtualenv(command):
    run(env.activate + ' && ' + command)
    
    
