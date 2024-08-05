import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
# @pytest.mark.prod - valid only for QA2 as OB is involved
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.p1
@vtest
class Test_C44870390_Verify_price_boost_feature_for_sports_and_racing_events__Verify_price_boost_sign_posting_on_the_EDP_and_landing_pages__Place_a_bet_on_price_boost_selection_and_verify_bet_receipt_and_my_bets_Configure_price_boost_through_CMS_on_sports_and_verify(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C44870390
    NAME: "Verify price boost feature for sports and racing events, - Verify price boost sign posting on the EDP and landing pages - Place a bet on price boost selection and verify bet receipt and my bets -Configure price boost through CMS on sports and verify
    DESCRIPTION: "Verify price boost feature for sports and racing events,
    DESCRIPTION: - Verify price boost sign posting on the EDP and landing pages
    DESCRIPTION: - Place a bet on price boost selection and verify bet receipt and my bets
    DESCRIPTION: -Configure price boost through CMS on sports and verify on FE"
    """
    keep_browser_open = True

    def navigate_to_Open_Bets(self):
        avatar = self.site.header.user_panel.my_account_button
        self.assertTrue(avatar.is_displayed(),
                        msg='User avatar is not displayed.')
        avatar.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened.')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        menu_items['History'].scroll_to_we()
        self.site.right_menu.click_item(item_name='HISTORY')
        self.site.right_menu.wait_item_appears(item_name='Betting History')
        self.site.right_menu.click_item(item_name='Betting History')
        self.site.wait_content_state(state_name='BetHistory')
        bet_tabs = self.site.bet_history.tabs_menu.items_as_ordered_dict
        bet_tabs['OPEN BETS'].click()
        self.site.wait_content_state(state_name='OpenBets')

    def test_000_preconditions(self):
        """
        DESCRIPTION: preconditions
        """
        football_event1 = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True, cashout=True)
        self.__class__.event1_eventID = football_event1.event_id
        self.__class__.event1_team1 = football_event1.team1
        self.__class__.event1_team2 = football_event1.team2
        football_event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event2_eventID = football_event2.event_id
        football_event3 = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True, cashout=True)
        self.__class__.event3_eventID = football_event3.event_id
        self.__class__.event3_team1 = football_event3.team1
        self.__class__.event3_team2 = football_event3.team2
        event3_selection_ids = football_event3.selection_ids
        self.__class__.event3_selection_id1 = list(event3_selection_ids.values())[0]
        racing_event1 = self.ob_config.add_UK_racing_event(number_of_runners=1, price_boost=True, market_price_boost=True, cashout=True)
        self.__class__.racing_event1_eventID = racing_event1.event_id
        start_time1_local = self.convert_time_to_local(date_time_str=racing_event1.event_date_time, ui_format_pattern='%H:%M, Today')
        self.__class__.racing_selection_ids = list(racing_event1.selection_ids.values())[0]
        self.__class__.racing_event1_short_name = f'{start_time1_local}'
        self.__class__.racing_event1_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time1_local}'
        self.__class__.racing_single_bet_event_names = [self.racing_event1_name]
        racing_event2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.racing_event2_eventID = racing_event2.event_id
        racing_event3 = self.ob_config.add_UK_racing_event(number_of_runners=1, price_boost=True, market_price_boost=True, cashout=True)
        self.__class__.racing_event3_eventID = racing_event3.event_id

    def test_001_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level
        EXPECTED: Price Boost icon is displayed on the right side of market header
        """
        self.site.wait_content_state('HOMEPAGE')
        self.device.driver.delete_all_cookies()
        self.navigate_to_edp(event_id=self.event1_eventID)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        self.__class__.market = list(markets.values())[0]
        self.assertTrue(self.market.section_header, msg='section header was not found')
        self.assertTrue(self.market.promotion_icons.has_price_boost(timeout=3),
                        msg=f'Price boost icon is not displayed on event: "{self.event1_team1}" "vs" "{self.event1_team2}" details page')
        market_width = self.market.market_section_header.size["width"]
        price_boost_icon_location = self.market.promotion_icons.price_boost.location.get('x')
        self.assertTrue(market_width / 2 < price_boost_icon_location,
                        msg='Price boost icon is not displayed on the right side of market header')

    def test_002_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level__cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level & cashout flag available
        EXPECTED: Cashout icon is present
        EXPECTED: Price Boost icon is displayed after Cashout icon
        """
        self.assertTrue(self.market.section_header.has_cash_out_mark(),
                        msg=f'Cash out label not displayed on event: "{self.event1_team1}" "vs" "{self.event1_team2}" details page')
        price_boost_coordinates = self.market.promotion_icons.price_boost.location.get('x')
        cash_out_coordinates = self.market.market_section_header.cash_out_mark.location.get('x')
        self.assertTrue(price_boost_coordinates > cash_out_coordinates,
                        msg=f'PriceBoost icon is not displayed after Cashout. PriceBosst coordinates is: '
                            f'{price_boost_coordinates}, Cashout coordinates is: {cash_out_coordinates}')

    def test_003_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: Price Boost icon remains displayed on the right side of market heade
        """
        if self.market.is_expanded:
            self.market.collapse()
        else:
            self.market.expand()
        market_width = self.market.market_section_header.size["width"]
        price_boost_icon_location = self.market.promotion_icons.price_boost.location.get('x')
        self.assertTrue(market_width / 2 < price_boost_icon_location,
                        msg='Price Boost icon is not displayed on the right side of market header')
        try:
            self.navigate_to_edp(event_id=self.racing_event3_eventID, sport_name='horse-racing', timeout=15)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RACINGEVENTDETAILS', timeout=15)
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertTrue(market.section_header, msg='section header was not found')
        self.assertTrue(market.section_header.promotion_icons.has_price_boost(timeout=3),
                        msg=f'Price boost icon is not displayed on racing event details page')
        market_width = market.section_header.size["width"]
        price_boost_icon_location = market.section_header.promotion_icons.price_boost.location.get('x')
        self.assertTrue(market_width / 2 < price_boost_icon_location,
                        msg='Price boost icon is not displayed on the right side of market header')
        self.assertTrue(market.section_header.has_cash_out_mark(),
                        msg=f'Cash out label not displayed on racing event details page')
        price_boost_coordinates = market.section_header.promotion_icons.price_boost.location.get('x')
        cash_out_coordinates = market.section_header.cash_out_label.location.get('x')
        self.assertTrue(price_boost_coordinates > cash_out_coordinates,
                        msg=f'PriceBoost icon is not displayed after Cashout. PriceBosst coordinates is: '
                            f'{price_boost_coordinates}, Cashout coordinates is: {cash_out_coordinates}')

    def test_004_navigate_to_edp_of_event_with_price_boost_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag not ticked
        EXPECTED: Price Boost icon is not displayed
        """
        self.navigate_to_edp(event_id=self.event2_eventID)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertFalse(market.promotion_icons.has_price_boost(expected_result=False),
                         msg='Price boost icon is displayed')
        try:
            self.navigate_to_edp(event_id=self.racing_event2_eventID, sport_name='horse-racing', timeout=20)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RACINGEVENTDETAILS', timeout=15)
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertFalse(market.section_header.promotion_icons.has_price_boost(expected_result=False),
                         msg='Price boost icon is displayed')

    def test_005_place_any_bet_with_price_boost_bet_and_verify_the_signposting_on_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place any bet with Price boost bet and verify the signposting on bet receipt and my bets
        EXPECTED: Bet placed successfully and the signposting is displayed
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('HOMEPAGE')
        self.site.login(close_all_banners=False)
        self.navigate_to_edp(event_id=self.event3_eventID)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        self.open_betslip_with_selections(selection_ids=self.event3_selection_id1)
        self.site.close_cookie_banner()
        self.place_and_validate_single_bet()
        self.assertTrue(self.site.bet_receipt.is_displayed(timeout=3),
                        msg='bet receipt is not displayed')
        self.assertTrue(self.site.bet_receipt.has_price_boost_label(timeout=3),
                        msg='Price boost is not displayed on bet receipt')
        self.site.bet_receipt.footer.done_button.click()
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.navigate_to_Open_Bets()
            else:
                self.site.open_my_bets_open_bets()
        else:
            self.site.open_my_bets_open_bets()
        sleep(5)  # to make sure all open bets are loaded
        event_name = '%s v %s' % (self.event3_team1, self.event3_team2)
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(event_names=event_name,
                                                                                       bet_type='SINGLE')
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg='No one bet leg was found for bet: "%s"' % bet_name)
        bet_leg = list(bet_legs.values())[0]
        self.assertTrue(bet_leg.has_promo_icon(timeout=3), msg='Price boost is not displayed on my bets')
        try:
            self.navigate_to_edp(event_id=self.racing_event1_eventID, sport_name='horse-racing', timeout=15)
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='RACINGEVENTDETAILS', timeout=15)
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertTrue(market.section_header, msg='section header was not found')
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.racing_selection_ids)
        self.place_and_validate_single_bet()
        self.assertTrue(self.site.bet_receipt.is_displayed(timeout=3),
                        msg='bet receipt is not displayed')
        self.assertTrue(self.site.bet_receipt.has_price_boost_label(timeout=3),
                        msg='Price boost is not displayed on bet receipt')
        self.site.bet_receipt.footer.done_button.click()
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.navigate_to_Open_Bets()
            else:
                self.site.open_my_bets_open_bets()
        else:
            self.site.open_my_bets_open_bets()
        sleep(5)  # to make sure all open bets are loaded
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                event_name = self.racing_event1_short_name
            else:
                event_name = self.racing_event1_name
        else:
            event_name = self.racing_event1_short_name
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(event_names=event_name,
                                                                                       bet_type='SINGLE')
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg='No one bet leg was found for bet: "%s"' % bet_name)
        bet_leg = list(bet_legs.values())[0]
        self.assertTrue(bet_leg.has_promo_icon(timeout=3), msg='Price boost is not displayed on my bets')
