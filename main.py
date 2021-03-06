from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import fix_path
from gaesessions import SessionMiddleware
from LazyControllerLoader import url_list
import settings

class Warmup(webapp.RequestHandler):
    """This handler warms up the instance (imports modules, etc.)."""
    def get(self):
        pass

url_mappings = [
    ('/',                     'controllers.Home.Home'),

    # user pages
    ('/anonymous_login',      'controllers.AnonLogin.AnonLogin'),
    ('/logout',               'controllers.Logout.Logout'),
    ('/rpx_response',         'controllers.RPX.RPX'),
    ('/profile/update',       'controllers.UserProfileEdit.UserProfileEdit'),
    ('/tracker',              'controllers.UserProfile.UserProfile'),
    ('/track/specific_ad',    'controllers.TrackAd.TrackAd'),

    # search pages
    ('/new',                  'controllers.SearchNew.SearchNew'),
    ('/delete',               'controllers.SearchDelete.SearchDelete'),
    ('/search/rename',        'controllers.SearchRename.SearchRename'),
    ('/view',                 'controllers.SearchView.SearchView'),

    # ajax pages
    ('/ajax/is_feed_ready',   'controllers.ajax.IsFeedReady.IsFeedReady'),
    ('/ajax/comment/(\d+)',   'controllers.ajax.Comment.Comment'),
    ('/ajax/(un)?hide/(\d+)', 'controllers.ajax.Hide.Hide'),
    ('/ajax/rate/(\d+)/(\d+)', 'controllers.ajax.Rate.Rate'),

    # simple pages
    ('/(contact)',            'controllers.DirectToTemplate.DirectToTemplate'),
    ('/(faq)',                'controllers.DirectToTemplate.DirectToTemplate'),
    ('/(legal)',              'controllers.DirectToTemplate.DirectToTemplate'),
    ('/(privacy)',            'controllers.DirectToTemplate.DirectToTemplate'),
    ('/_ah/warmup',           'main.Warmup'),

    # tasks (admin-only URLs: protected by app.yaml)
    ('/task/update_feed',     'controllers.task.UpdateFeed.UpdateFeed'),

    # send everything else to the page not found handler
    ('/.*',           'controllers.PageNotFound.PageNotFound'),
    ]
COOKIE_KEY = '\xff\xbbL\x10/\xd2\x89\xd9\x1b0H]w\xc4\xca\x9e8\x1ch\xe4.\xf3\x9acU.\xe9\xc4\xd6\xf9\x155o\x9bCR\xef\x18\xca\x0e\x0f\xaf\x16<c\xc1\xc3\xf0(\xcc\xef\x91\xfbA\x9f\xc2\xd7r \xca\xb18\xce\xdd'
app = webapp.WSGIApplication(url_list(url_mappings), debug=settings.DEBUG)
app = SessionMiddleware(app, COOKIE_KEY)

if settings.USE_APP_STATS:
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)

def main():
    fix_path.fix_sys_path()
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
