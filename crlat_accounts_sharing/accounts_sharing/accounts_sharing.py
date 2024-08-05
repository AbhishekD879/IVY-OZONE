import json
import sys
from datetime import datetime

import web


with open('resources/cms_users/cms_users.json') as cms_infile,\
        open('resources/ob_users/bma.json') as ob_bma,\
        open('resources/ob_users/ladbrokes.json') as ob_ladbrokes,\
        \
        open('resources/site_users/bma/prod.json') as site_bma_prod,\
        open('resources/site_users/bma/stg2.json') as site_bma_stg2,\
        open('resources/site_users/bma/tst2.json') as site_bma_tst2, \
        \
        open('resources/site_users/ladbrokes/prod.json') as site_ladbrokes_prod, \
        open('resources/site_users/ladbrokes/stg2.json') as site_ladbrokes_stg2, \
        open('resources/site_users/ladbrokes/tst2.json') as site_ladbrokes_tst2,\
        \
        open('resources/ios_users/bma/prod.json') as ios_bma_prod,\
        open('resources/ios_users/bma/stg2.json') as ios_bma_stg2,\
        open('resources/ios_users/bma/tst2.json') as ios_bma_tst2, \
        \
        open('resources/ios_users/ladbrokes/prod.json') as ios_ladbrokes_prod, \
        open('resources/ios_users/ladbrokes/stg2.json') as ios_ladbrokes_stg2, \
        open('resources/ios_users/ladbrokes/tst2.json') as ios_ladbrokes_tst2:

    cms_config = json.load(cms_infile)
    ob_bma_config = json.load(ob_bma)
    ob_ladbrokes_config = json.load(ob_ladbrokes)
    # BMA
    site_bma_prod_config = json.load(site_bma_prod)
    site_bma_stg2_config = json.load(site_bma_stg2)
    site_bma_tst2_config = json.load(site_bma_tst2)
    # Ladbrokes
    site_ladbrokes_prod_config = json.load(site_ladbrokes_prod)
    site_ladbrokes_stg2_config = json.load(site_ladbrokes_stg2)
    site_ladbrokes_tst2_config = json.load(site_ladbrokes_tst2)
    # iOS BMA
    ios_bma_prod_config = json.load(ios_bma_prod)
    ios_bma_stg2_config = json.load(ios_bma_stg2)
    ios_bma_tst2_config = json.load(ios_bma_tst2)
    # iOS Ladbrokes
    ios_ladbrokes_prod_config = json.load(ios_ladbrokes_prod)
    ios_ladbrokes_stg2_config = json.load(ios_ladbrokes_stg2)
    ios_ladbrokes_tst2_config = json.load(ios_ladbrokes_tst2)

urls = (
    '/get_site_user/([a-zA-Z0-9_]+)/([a-zA-Z0-9]+)/(.*)', 'get_site_user',
    '/get_ios_user/([a-zA-Z0-9_]+)/([a-zA-Z0-9]+)/(.*)', 'get_ios_user',
    '/get_ob_user/([a-zA-Z0-9]+)/(.*)', 'get_ob_user',
    '/get_cms_user/(.*)', 'get_cms_user',
    '/health', 'health',
    '/', 'index'
)

bma_config = {
    'site':
        {
            'prod': site_bma_prod_config,
            'stg2': site_bma_stg2_config,
            'tst2': site_bma_tst2_config,
        },
    'ios':
        {
            'prod': ios_bma_prod_config,
            'stg2': ios_bma_stg2_config,
            'tst2': ios_bma_tst2_config,
        }
}

ladbrokes_config = {
    'site':
        {
            'prod': site_ladbrokes_prod_config,
            'stg2': site_ladbrokes_stg2_config,
            'tst2': site_ladbrokes_tst2_config,
        },
    'ios':
        {
            'prod': ios_ladbrokes_prod_config,
            'stg2': ios_ladbrokes_stg2_config,
            'tst2': ios_ladbrokes_tst2_config,
        }
}


app = web.application(urls, globals())


class get_site_user:

    def GET(self, brand='bma', env='tst2', user_type='betplacement_user'):
        print('%s: Got request "%s" for %s/%s for %s brand'
              % (str(datetime.utcnow()), self.__class__.__name__, env, user_type, brand))
        is_ios = 'ios' in self.__class__.__name__
        config = None
        if brand == 'bma' or brand == 'vanilla':
            if is_ios:
                config = bma_config.get('ios')
            else:
                config = bma_config.get('site')
        if brand == 'ladbrokes':
            if is_ios:
                config = ladbrokes_config.get('ios')
            else:
                config = ladbrokes_config.get('site')
        if not config:
            message = 'Unknown brand "%s", expected one of "bma", "ladbrokes", "vanilla"' % brand
            print(message)
            return web.HTTPError('503 Internal error: %s' % message)
        brand_config = config.get(env)
        if not brand_config:
            message = 'Unknown backend env "%s", expected one of %s' % (env, list(config.keys()))
            print(message)
            return web.HTTPError('503 Internal error: %s' % message)
        try:
            user = brand_config[env][user_type].pop(0)
            brand_config[env][user_type].append(user)
            print('%s: Replying to request "%s" for %s/%s/%s with "%s"'
                  % (str(datetime.utcnow()), self.__class__.__name__, brand, env, user_type, user))
            return user
        except Exception:
            message = 'User group "%s" is not found for brand "%s", env "%s"' % (user_type, brand, env)
            print(message)
            return web.HTTPError('503 Internal error: %s' % message)


class get_ios_user(get_site_user):
    pass


class get_ob_user:
    def GET(self, brand='bma', env='tst2'):
        print('%s: Got request "%s" for "%s" env for "%s" brand' % (str(datetime.utcnow()), self.__class__.__name__, env, brand))
        try:
            ob_config = None
            if brand == 'bma':
                ob_config = ob_bma_config
            if brand == 'ladbrokes':
                ob_config = ob_ladbrokes_config
            if not ob_config:
                return web.HTTPError('404: Unknown brand "%s"' % brand)
            account = list(ob_config[brand][env].values())[0]
            user = account.get('name')
            password = account.get('password')
            return json.dumps({"username": user, "password": password})
        except Exception:
            message = 'Unknown BRAND: "%s" or Unknown ENVIRONMENT: "%s" or no user found for "%s"' % (brand, env, env)
            print(message)
            return web.HTTPError('503 Internal error: %s' % message)


class get_cms_user:
    def GET(self, env='dev0'):
        print('%s: Got request "%s" for %s env' % (str(datetime.utcnow()), self.__class__.__name__, env))
        try:
            account = cms_config[env]
            user = account.get('name')
            password = account.get('password')
            return json.dumps({"username": user, "password": password})
        except Exception:
            message = 'Unknown ENVIRONMENT: "%s" or no user found for "%s"' % (env, env)
            print(message)
            return web.HTTPError('503 Internal error: %s' % message)


class health:
    def GET(self):
        return '{"health": "ok"}'


class index:
    def GET(self):
        print('OK')
        urls_ = {x: '/%s' % y for x, y in zip(urls[::2], urls[1::2])}
        urls_.pop('/')
        text = '<h1>Welcome to CRLAT Account Sharing service!</h1>' \
               '<h3>Please use one of available services together  with brand, env and username</h3>%s ' % '<br>'.join(list(urls_.values()))
        text += '<h3> Examples of usages: </h3>' \
                '/get_site_user/bma/tst2/betplacement_user<br>' \
                '/get_cms_user/tst0<br>/get_ob_user/bma/tst2'
        return text


if __name__ == "__main__":
    if '443' in sys.argv:
        from cheroot.server import HTTPServer
        from cheroot.ssl.builtin import BuiltinSSLAdapter

        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate='../.cert/domain.crt',
            private_key='../.cert/domain.key')
    app.run()
