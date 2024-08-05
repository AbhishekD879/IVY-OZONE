from collections import namedtuple


class FREERIDE(object):
    """
    Free ride related constants/messages
    """
    _excpeted_options_list = namedtuple('excpeted_options_list', ('top_player', 'dark_horse', 'surprise_me', 'big_strong',
                                                                  'small_nimble', 'good_chance', 'nice_price'))
    OPTIONS_LIST = _excpeted_options_list(top_player='Top player', dark_horse='Dark horse', surprise_me='Surprise me!',
                                          big_strong='Big & Strong', small_nimble='Small & Nimble',
                                          good_chance='Good Chance', nice_price='Nice Price')
