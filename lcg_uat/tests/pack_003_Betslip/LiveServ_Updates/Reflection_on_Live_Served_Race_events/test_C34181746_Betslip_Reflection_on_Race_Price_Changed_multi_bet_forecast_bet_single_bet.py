import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot on work on prod/beta as it is involving price changing
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C34181746_Betslip_Reflection_on_Race_Price_Changed_multi_bet_forecast_bet_single_bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C34181746
    NAME: Betslip Reflection on <Race>  Price Changed (multi bet-forecast bet +single b et)
    DESCRIPTION: This test case verifies Betslip reflection on HR Price Change with forecast and single E/W bets.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: *   Event should not be **Live** (**isStarted - absent)**
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    PRECONDITIONS: ![](index.php?/attachments/get/10750319)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and login
        """
        self.site.login()
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices,
                                                          forecast_available=True)
        event_start_time = event_params.event_date_time
        start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
        event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
        self.__class__.event_id = event_params.event_id
        self.__class__.selection_ids = list(event_params.selection_ids.values())
        self._logger.info(
            f'*** Created Horse Racing Forecast/Tricast event "{event_name}" with id "{self.event_id}"')

    def test_001_load_invictus_applicationtap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Load Invictus application.
        DESCRIPTION: Tap <Race> icon from the sports ribbon.
        EXPECTED: <Race> Landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_003_add_forecast_bet_to_betslip_or_bet_with_multiple_outcomes(self):
        """
        DESCRIPTION: Add Forecast Bet to BetSlip or Bet with multiple outcomes.
        EXPECTED: Betslip counter is increased
        """
        self.expected_betslip_counter_value = 0
        event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        event_tab_content.market_tabs_list.open_tab('FORECAST')
        self.__class__.expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True)
        self.verify_betslip_counter_change(expected_value=1)

    def test_004_add_single_bet_to_betslip_it_should_be_the_first_id_from_legpart_in_forecast_bet_see_preconditions(self):
        """
        DESCRIPTION: Add single Bet to BetSlip (it should be the first ID from legPart in forecast Bet, see preconditions).
        EXPECTED: Betslip counter is increased.
        """
        self.expected_betslip_counter_value = 2
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.verify_betslip_counter_change(expected_value=2)

    def test_005_open_betslip_and_check_ew_checkbox_for_the_single_bet(self):
        """
        DESCRIPTION: Open 'Betslip' and check E/W checkbox for the single bet.
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        stake = list(singles_section.values())[1]
        stake.each_way_checkbox.click()
        self.assertTrue(stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.__class__.old_odds = stake.odds

    def test_006_open_ti_backofficetrigger_the_following_situation_for_this_eventchange_price_for_single_betand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self, new_price='1/5'):
        """
        DESCRIPTION: Open ti backoffice.
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: Change price for single Bet.
        DESCRIPTION: And at the same time have Betslip page opened to watch for updates
        EXPECTED: - New Odds prices are displayed
        EXPECTED: - Forecast Bet is displayed
        """
        self.ob_config.change_price(selection_id=self.selection_ids[0], price=new_price)
        if self.brand == 'ladbrokes':
            self.device.refresh_page()
            self.site.wait_splash_to_hide(5)
            self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        _, stake = list(singles_section.items())[1]
        new_odds = stake.odds
        self.assertNotEqual(new_odds, self.old_odds, msg=f'Actual odd "{new_odds}" is not same as'
                                                         f'Expected odd:"{self.old_odds}"')
        _, stake = list(singles_section.items())[0]

        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), self.expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{self.expected_selection_name}"')

        self.assertTrue(stake, msg=f'Stake "{self.expected_selection_name}" was not found')
        self.assertEqual(stake.market_name, vec.betslip.FORECAST,
                         msg=f'Market name "{stake.market_name}" '
                             f'is not the same as expected "{vec.betslip.FORECAST}"')

    def test_007_place_a_bets_from_the_betslip_go_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Place a bets from the betslip. Go to the Open Bets tab.
        EXPECTED: All bets placed are displayed
        """
        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_008_repeat_steps_2_6_try_different_options_of_price_changing_for_a_single_bet_increasingdecreasing_value(self):
        """
        DESCRIPTION: Repeat steps 2-6. Try different options of price changing for a single bet (increasing/decreasing value).
        EXPECTED: - New Odds prices are displayed
        EXPECTED: - Forecast Bet is displayed
        """
        self.test_001_load_invictus_applicationtap_race_icon_from_the_sports_ribbon()
        self.test_002_go_to_the_event_details_page()
        self.test_003_add_forecast_bet_to_betslip_or_bet_with_multiple_outcomes()
        self.test_004_add_single_bet_to_betslip_it_should_be_the_first_id_from_legpart_in_forecast_bet_see_preconditions()
        self.test_005_open_betslip_and_check_ew_checkbox_for_the_single_bet()
        self.test_006_open_ti_backofficetrigger_the_following_situation_for_this_eventchange_price_for_single_betand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(new_price='1/4')

    def test_009_place_bets_from_the_betslip_go_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Place bets from the betslip. Go to the Open Bets tab.
        EXPECTED: Forecast Bet is placed and displayed.
        EXPECTED: All bets placed are displayed.
        """
        self.test_007_place_a_bets_from_the_betslip_go_to_the_open_bets_tab()

    def test_010_repeat_steps_2_4open_ti_backofficechange_price_for_single_betplace_bets_from_betslip_without_checking_ew_checkbox(self):
        """
        DESCRIPTION: Repeat steps 2-4.
        DESCRIPTION: Open ti backoffice.
        DESCRIPTION: Change price for single Bet.
        DESCRIPTION: Place bets from betslip without checking E/W checkbox.
        EXPECTED: Forecast Bet is placed and displayed.
        EXPECTED: All bets placed are displayed.
        """
        self.test_001_load_invictus_applicationtap_race_icon_from_the_sports_ribbon()
        self.test_002_go_to_the_event_details_page()
        self.test_003_add_forecast_bet_to_betslip_or_bet_with_multiple_outcomes()
        self.test_004_add_single_bet_to_betslip_it_should_be_the_first_id_from_legpart_in_forecast_bet_see_preconditions()
        self.test_006_open_ti_backofficetrigger_the_following_situation_for_this_eventchange_price_for_single_betand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(new_price='1/1')
        self.test_007_place_a_bets_from_the_betslip_go_to_the_open_bets_tab()
