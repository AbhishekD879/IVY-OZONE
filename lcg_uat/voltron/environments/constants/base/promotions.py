from collections import namedtuple


class Promotions(object):
    """
    src/app/lazy-modules/locale/translations/en-US/promotions.lang.ts
    """
    PROMOTIONS = 'Promotions'
    MORE = 'More'
    OK = 'Ok'
    MORE_INFORMATION = 'More information'
    NO_PROMOTIONS_FOUND = 'No active Promotions at the moment'
    NO_PROMO = 'Promotion is expired or unavailable'
    TABS_ALL = 'All'.upper()
    TABS_RETAIL = 'Shop Exclusive'.upper()
    TERMS_AND_CONDITIONS_LABEL = 'Terms and Conditions'

    _footer_text = namedtuple('footer_text', ['part_1', 'part_2'])
    _footer_text_part_1 = 'Click here'
    _footer_text_part_2 = 'for more information about this offer'
    FOOTER_TEXT = _footer_text(part_1=_footer_text_part_1,
                               part_2=_footer_text_part_2)
    FOOTER_MORE = 'More Info'
    BET_NOW = 'bet now'
    UNASSIGNED_GROUP = 'More from Coral'
