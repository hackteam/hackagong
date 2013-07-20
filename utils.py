import bottle
from config import BASE_URL_PATH

def web_session_exists():
    ''' Return whether there is a web session active (from Beaker middleware).
        This is carefully structured not to triggered the creation of a session.
        TODO: FIX. CURRENTLY DOES NOT WORK.
    '''
    return 'beaker.session' in bottle.request.environ


def web_session():
    ''' Get web session (from Beaker middleware), creating a new one if necessary '''
    return bottle.request.environ.get('beaker.session')


def existing_web_session():
    ''' Get only an existing web session (from Beaker middleware) or None '''
    # TODO: Fix up sessions so that they don't get created unless needed
    if web_session_exists():
        return web_session()
    else:
        return None

def delete_web_session():
    session = bottle.request.environ['beaker.session']
    if session:
        session.delete()
        return True


def redirect(url=''):
    bottle.redirect(BASE_URL_PATH + url)
