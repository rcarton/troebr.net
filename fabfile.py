from fabric.api import *

# the user to use for the remote commands
env.user = 'troebr'
# the servers where the commands are executed
env.hosts = ['new.troebr.net']

APPNAME = 'troebr.net'

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % APPNAME)
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/%s' % APPNAME)
    with cd('/tmp/%s' % APPNAME):
        run('tar xzf /tmp/%s.tar.gz' % APPNAME)
        # now setup the package with our virtual environment's
        # python interpreter
        run('/home/troebr/%s/bin/python setup.py install' % APPNAME)
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/%s /tmp/%s.tar.gz' % (APPNAME, APPNAME))
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/%s.wsgi' % APPNAME)
