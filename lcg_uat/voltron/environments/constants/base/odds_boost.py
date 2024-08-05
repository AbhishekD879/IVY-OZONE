from collections import namedtuple


class OddsBoost(object):
    """
    src/app/lazy-modules/locale/translations/en-US/oddsBoost.lang.ts
    """
    _tokens_info_dialog = namedtuple('tokens_info_dialog', ['title', 'available1', 'available2', 'boost', 'boosts',
                                                            'terms', 'show_more', 'ok_thanks'])
    _tokens_info_dialog_title = 'Odds Boost'
    _tokens_info_dialog_available1 = 'You have '
    _tokens_info_dialog_available2 = ' odds %1 available'
    _tokens_info_dialog_boost = 'boost'
    _tokens_info_dialog_boosts = 'boosts'
    _tokens_info_dialog_terms = '18+. Terms Apply'
    _tokens_info_dialog_show_more = 'Show more'
    _tokens_info_dialog_ok_thanks = 'Ok, thanks'
    TOKENS_INFO_DIALOG = _tokens_info_dialog(title=_tokens_info_dialog_title,
                                             available1=_tokens_info_dialog_available1,
                                             available2=_tokens_info_dialog_available2,
                                             boost=_tokens_info_dialog_boost,
                                             boosts=_tokens_info_dialog_boosts,
                                             terms=_tokens_info_dialog_terms,
                                             show_more=_tokens_info_dialog_show_more,
                                             ok_thanks=_tokens_info_dialog_ok_thanks)

    _info_dialog = namedtuple('info_dialog', ['title', 'text', 'odds_boost_unavailable'])
    _info_dialog_title = 'Odds Boost'
    _info_dialog_text = 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to £50.00 total stake.'
    _info_dialog_odds_boost_unavailable = 'Odds Boost is unavailable for this selection'
    INFO_DIALOG = _info_dialog(title=_info_dialog_title,
                               text=_info_dialog_text,
                               odds_boost_unavailable=_info_dialog_odds_boost_unavailable)

    _betslip_header = namedtuple('betslip_header', ['title', 'subtitle'])
    _betslip_header_title = 'Odds Boost'
    _betslip_header_subtitle = 'Tap to boost your betslip.'
    BETSLIP_HEADER = _betslip_header(title=_betslip_header_title,
                                     subtitle=_betslip_header_subtitle)

    _boost_button = namedtuple('boost_button', ['enabled', 'disabled', 'reboost'])
    _boost_button_enabled = 'BOOSTED'
    _boost_button_disabled = 'BOOST'
    _boost_button_reboost = 'RE-BOOST'
    BOOST_BUTTON = _boost_button(enabled=_boost_button_enabled,
                                 disabled=_boost_button_disabled,
                                 reboost=_boost_button_reboost)

    _page = namedtuple('page', ['title', 'today_odds_boosts', 'available_now', 'upcoming_boosts',
                                'available_now_section_title', 'terms_and_conditions_section_title', 'boost_up_to',
                                'boost_use_by', 'boost_valid_from', 'no_boosts_message', 'next_boost_available'])
    _page_title = 'Odds Boost'
    _page_today_odds_boosts = 'Today\'s Odds Boosts'
    _page_available_now = 'Available now'
    _page_upcoming_boosts = 'UPCOMING BOOSTS'
    _page_available_now_section_title = 'BOOSTS AVAILABLE NOW'
    _page_terms_and_conditions_section_title = 'TERMS & CONDITIONS'
    _page_boost_up_to = 'Boost Up To:'
    _page_boost_use_by = 'Use By:'
    _page_boost_valid_from = 'Valid From:'
    _page_no_boosts_message = 'Look out for boosts appearing here for upcoming events!'
    _page_next_boost_available = 'Next boost available:'

    PAGE = _page(title=_page_title,
                 today_odds_boosts=_page_today_odds_boosts,
                 available_now=_page_available_now,
                 upcoming_boosts=_page_upcoming_boosts,
                 available_now_section_title=_page_available_now_section_title,
                 terms_and_conditions_section_title=_page_terms_and_conditions_section_title,
                 boost_up_to=_page_boost_up_to,
                 boost_use_by=_page_boost_use_by,
                 boost_valid_from=_page_boost_valid_from,
                 no_boosts_message=_page_no_boosts_message,
                 next_boost_available=_page_next_boost_available)

    _betslip_dialog = namedtuple('betslip_dialog', ['no_thanks', 'yes_please', 'ok_thanks', 'continue_with_freebet',
                                                    'cancel_boost_price_message', 'cant_boost_message', 'odds_boost_unavailable',
                                                    'unavailable_message', 'ok'])
    _betslip_dialog_no_thanks = 'No, thanks'
    _betslip_dialog_yes_please = 'Yes, please'
    _betslip_dialog_ok_thanks = 'Ok, thanks'
    _betslip_dialog_continue_with_freebet = 'Continue with Free Bet?'
    _betslip_dialog_odds_boost_unavailable = 'Odds Boost Unavailable'
    _betslip_dialog_odds_boost_unavailable_message = 'Odds Boost is unavailable for SP selections'
    _betslip_dialog_ok = 'Ok'
    _betslip_dialog_cancel_boost_price_message = 'Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?'
    _betslip_dialog_cant_boost_message = 'Unfortunately you can\'t boost your odds while using a Free Bet. Please de-select your Free Bet to boost your odds.'
    BETSLIP_DIALOG = _betslip_dialog(no_thanks=_betslip_dialog_no_thanks,
                                     yes_please=_betslip_dialog_yes_please,
                                     ok_thanks=_betslip_dialog_ok_thanks,
                                     continue_with_freebet=_betslip_dialog_continue_with_freebet,
                                     cancel_boost_price_message=_betslip_dialog_cancel_boost_price_message,
                                     cant_boost_message=_betslip_dialog_cant_boost_message,
                                     odds_boost_unavailable=_betslip_dialog_odds_boost_unavailable,
                                     unavailable_message=_betslip_dialog_odds_boost_unavailable_message,
                                     ok=_betslip_dialog_ok)

    _max_stake_exceeded = namedtuple('max_stake_exceeded', ['title', 'text'])
    _max_stake_exceeded_title = 'Max Stake Exceeded'
    _max_stake_exceeded_text = 'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake. You can boost up to £50.00 total stake.'
    MAX_STAKE_EXCEEDED = _max_stake_exceeded(title=_max_stake_exceeded_title,
                                             text=_max_stake_exceeded_text)

    AVAIALABLE_ODD_BOOST = 'You Have 1 Odds Boost Available'
    DONT_SHOW_AGAIN = 'Don\'t show this again'
