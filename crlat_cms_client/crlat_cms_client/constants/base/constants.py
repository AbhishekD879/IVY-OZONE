from collections import namedtuple


class CmsConstants(object):

    # CMS static blocks uri
    CONNECT_STATIC_BLOCK_URI = 'connect-overlay-en-us'
    NO_FREEBET_STATIC_BLOCK_URI = 'no-freebets-en-us'
    PRIVATE_MARKETS_TC_STATIC_BLOCK_URI = 'private-markets-terms-and-conditions-en-us'
    WHAT_IS_CASH_OUT_STATIC_BLOCK_URI = 'what-is-cash-out-en-us'

    MINI_GAMES_TYPE_NAME = 'mini-games'

    ACCA_SUGGESTED_TYPE2_INSURANCE_OFFER = 'SuggestedType2'
    ACCA_SUGGESTED_INSURANCE_OFFER = 'Suggested'
    ACCA_ELIGIBLE_INSURANCE_OFFER = 'Eligible'

    __SPORT_TABS_INTERNAL_NAMES = namedtuple('sport_tabs_internal_ids', ('matches',
                                                                         'competitions',
                                                                         'outrights',
                                                                         'coupons',
                                                                         'in_play',
                                                                         'jackpot',
                                                                         'specials',
                                                                         'popularbets'
                                                                         ))
    SPORT_TABS_INTERNAL_NAMES = __SPORT_TABS_INTERNAL_NAMES(matches='matches',
                                                            competitions='competitions',
                                                            outrights='outrights',
                                                            coupons='coupons',
                                                            in_play='live',
                                                            jackpot='jackpot',
                                                            specials='specials',
                                                            popularbets='popularbets')
    __MODULE_RIBBON_INTERNAL_IDS = namedtuple('module_ribbon_internal_ids', ('featured',
                                                                             'next_races',
                                                                             'live_stream',
                                                                             'in_play',
                                                                             'multiples',
                                                                             'build_your_bet',
                                                                             'one_two_free'))
    MODULE_RIBBON_INTERNAL_IDS = __MODULE_RIBBON_INTERNAL_IDS(featured='tab-featured',
                                                              next_races='tab-next-races',
                                                              live_stream='tab-live-stream',
                                                              in_play='tab-in-play',
                                                              multiples='tab-multiples',
                                                              build_your_bet='tab-build-your-bet',
                                                              one_two_free='tab-1-2-free')

    __BONUS_SUPPRESSION_RISK_LEVEL = namedtuple('bonus_suppression_risk_level', ('risk_level_zero',
                                                                                 'risk_level_one',
                                                                                 'risk_level_two',
                                                                                 'risk_level_three',
                                                                                 'risk_level_four',
                                                                                 'risk_level_five',
                                                                                 'risk_level_six',
                                                                                 'risk_level_seven'))
    BONUS_SUPPRESSION_RISK_LEVEL = __BONUS_SUPPRESSION_RISK_LEVEL(risk_level_zero='0 - Bonus Suppression',
                                                                  risk_level_one= '1 - Problem Gambler Low' ,
                                                                  risk_level_two='2 - Problem Gambler  Medium',
                                                                  risk_level_three='3 - Problem Gambler High',
                                                                  risk_level_four='4 - Problem Gambler V High',
                                                                  risk_level_five='5 - At Risk Low',
                                                                  risk_level_six='6 - At Risk Medium',
                                                                  risk_level_seven='7 - At Risk High')

    __BONUS_SUPPRESSION_REASON_CODE = namedtuple('bonus_suppression_reason_code', ('reason_code_zero',
                                                                                   'reason_code_one',
                                                                                   'reason_code_two',
                                                                                   'reason_code_three',
                                                                                   'reason_code_four',
                                                                                   'reason_code_five',
                                                                                   'reason_code_six',
                                                                                   'reason_code_seven',
                                                                                   'reason_code_eight',
                                                                                   'reason_code_nine',
                                                                                   'reason_code_ten',
                                                                                   'reason_code_eleven',
                                                                                   'reason_code_twelve',
                                                                                   'reason_code_thirteen',
                                                                                   'reason_code_fourteen',
                                                                                   'reason_code_fifteen',
                                                                                   'reason_code_sixteen',
                                                                                   'reason_code_seventeen'))
    BONUS_SUPPRESSION_REASON_CODE = __BONUS_SUPPRESSION_REASON_CODE(reason_code_zero='0 - RGY User',
                                                                    reason_code_one= '1 - Difference in spend from norm' ,
                                                                    reason_code_two='2 - Frequency of play',
                                                                    reason_code_three='3 - Frequency of play increase',
                                                                    reason_code_four='4 - Deposit frequency',
                                                                    reason_code_five='5 - Declined deposits',
                                                                    reason_code_six='6 - Multiple payment methods',
                                                                    reason_code_seven='7 - Credit Cards',
                                                                    reason_code_eight='8 - Cancelled withdrawals',
                                                                    reason_code_nine='9 - Late night play',
                                                                    reason_code_ten='10 - Speed of Play',
                                                                    reason_code_eleven='11 - Chaotic Play',
                                                                    reason_code_twelve='12 - Deposit Amount',
                                                                    reason_code_thirteen='13 - Tenure*',
                                                                    reason_code_fourteen='14 - In Session TopUp*',
                                                                    reason_code_fifteen='15 - Variety of Games*',
                                                                    reason_code_sixteen='16 - Frequency of Play TOSL7D',
                                                                    reason_code_seventeen='17 - Player days')

    BETSLIP_WIDGET_NAME = 'BETSLIP'
    BETSLIP_WIDGET_NAME2 = 'BET SLIP'
    OFFERS_WIDGET_NAME = 'OFFERS'
    OFFERS_WIDGET_TYPE = 'offers'
    OFFER_MODULE_NAME = 'Offer Module: Auto test Offer Module DO NOT EDIT/DELETE'

    # Promo keys configured in CMS
    PROMO_KEY_EPR = 'ExtraPlaceRace'
    PROMO_KEY_YOUR_CALL = 'YC'
