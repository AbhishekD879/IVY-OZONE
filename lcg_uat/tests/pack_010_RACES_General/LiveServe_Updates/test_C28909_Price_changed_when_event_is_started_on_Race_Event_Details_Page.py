import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod // cannot suspend or update price in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C28909_Price_changed_when_event_is_started_on_Race_Event_Details_Page(BaseRacing):
    """
    TR_ID: C28909
    NAME: Price changed when event is started on <Race> Event Details Page
    DESCRIPTION: Test case verifies price update on Race EDP when flag isStarted' **= 'true'  is received
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes' **= 'SP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: In order to set event **'isStarted'**= 'true' -> in TI on event level set 'is Off' attribute to 'Yes'.
    """
    keep_browser_open = True
    lp_prices = {0: '1/2',
                 1: '1/4'}

    def test_000_preconditions(self):
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1)
        self.__class__.eventID_sp, self.__class__.selection_ids_sp = \
            event_params.event_id, event_params.selection_ids

        self._logger.info(f'*** Created SP event id: {self.eventID_sp}, '
                          f'selection ids: {list(self.selection_ids_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                          lp_prices=self.lp_prices, sp=True)
        self.__class__.eventID_lp_sp, self.__class__.selection_ids_lp_sp = \
            event_params.event_id, event_params.selection_ids

        self._logger.info(f'*** Created LP-SP event id: {self.eventID_lp_sp}, '
                          f'selection ids: {list(self.selection_ids_lp_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                          lp_prices=self.lp_prices, sp=False)
        self.__class__.eventID_lp, self.__class__.selection_ids_lp = \
            event_params.event_id, event_params.selection_ids

        self._logger.info(f'*** Created LP event id: {self.eventID_lp},'
                          f'selection ids: {list(self.selection_ids_lp.values())}')
        self.__class__.eventID = self.eventID_lp
        self.__class__.selection_ids = self.selection_ids_lp

    def test_001_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> Landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing', timeout=20)

    def test_002_open_race_event_details_page_where_event_has_lp_price_type_and_it_is_not_going_to_started_now(self):
        """
        DESCRIPTION: Open <Race> event details page where event has LP price type and it is not going to started now
        EXPECTED: * Event details page is opened
        EXPECTED: * Available market tabs are present
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_003_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodesnavigate_to_application_and_observe_changes(
            self, is_off=True, eventStatusCode=False):
        """
        DESCRIPTION: In TI: Trigger the following situation for this event when the market(s) are collapsed:
        DESCRIPTION: **'isStarted' **= 'true'
        DESCRIPTION: **'eventStatusCode'='S'
        DESCRIPTION: Navigate to application and observe changes
        EXPECTED: * Corresponding 'Price/Odds' are displayed as greyed out but still display the prices when expanding the market(s).
        EXPECTED: * All 'Price/Odds' buttons become disabled for all markets associated with this event
        """
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=is_off)
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=eventStatusCode)
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        sleep(3)
        section_name, section = list(sections.items())[0]
        self.__class__.outcomes = section.items_as_ordered_dict
        for (index, (outcome_name, outcome)) in enumerate(self.outcomes.items()):
            if eventStatusCode:
                self.assertTrue(outcome.bet_button.is_enabled(),
                                msg=f'Price is suspended for "{outcome_name}"')
                self.assertTrue(outcome.bet_button.is_displayed(),
                                msg=f'Price is not displayed for "{outcome_name}"')
            else:
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False),
                                 msg=f'Price is not suspended for "{outcome_name}"')
                self.assertTrue(outcome.bet_button.is_displayed(),
                                msg=f'Price is not displayed for "{outcome_name}"')

    def test_004_collapsed_the_markets(self):
        """
        DESCRIPTION: Collapsed the market(s)
        EXPECTED:
        """
        # Step NA

    def test_005_in_ti_change_price_for_one_of_the_selections_within_the_market_tab__navigate_to_application_and_observe_changes(
            self):
        """
        DESCRIPTION: In TI: Change price for one of the selections within the market tab > Navigate to application and observe changes
        EXPECTED: * Corresponding 'Price/Odds' button is displayed the new price when expanding the market(s).
        EXPECTED: * Price/Odds' button doesn't change the color
        EXPECTED: * Previous Odds, under Price/Odds button, is updated/added respectively
        """
        selection_name, selection = list(self.outcomes.items())[0]
        expected_old_price = selection.bet_button.outcome_price_text
        expected_new_price = '7/1'
        self.ob_config.change_price(selection_id=self.selection_ids[selection_name], price=expected_new_price)

        result = wait_for_result(lambda: selection.previous_price,
                                 name='Previous price to appear',
                                 timeout=40)
        self.assertTrue(result, msg='Price update is not shown on page')
        old_price = selection.previous_price

        self.assertEqual(old_price, expected_old_price,
                         msg=f'Old price is "{old_price}" not as expected "{expected_old_price}"')
        new_price = selection.bet_button.outcome_price_text
        result = wait_for_result(lambda: selection.bet_button.outcome_price_text == new_price,
                                 name='Price to change',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'New price is "{selection.bet_button.outcome_price_text}" not as expected "{expected_new_price}"')
        self.assertEqual(new_price, expected_new_price,
                         msg=f'New price is "{new_price}" not as expected "{expected_new_price}"')

        # this step is NA for SP as it will not reflect the price as we change.

    def test_006_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodeanavigate_to_application_and_observe_changes(
            self):
        """
        DESCRIPTION: In TI: Trigger the following situation for this event when the market(s) are collapsed:
        DESCRIPTION: **'isStarted' **= 'true'
        DESCRIPTION: **'eventStatusCode'='A'
        DESCRIPTION: Navigate to application and observe changes
        EXPECTED: All 'Price/Odds' buttons are no more disabled, they become active for all market types when expanding the market(s).
        """
        self.test_003_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodesnavigate_to_application_and_observe_changes(is_off=True, eventStatusCode=True)

    def test_007_in_ti_change_price_for_one_of_the_selections__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections > Navigate to application and observe changes
        EXPECTED: Corresponding 'Price/Odds' button is immediately displayed new price and for a few seconds changed their color to:
        EXPECTED: * blue color if price has decreased;
        EXPECTED: * pink color if price has increased;
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        # NA as price increased or decreased color will be in few sec.

    def test_008_repeat_steps__3_9_for_the_event_where_price_type_is_splpsp_and_the_markets_are_expanded(self):
        """
        DESCRIPTION: Repeat steps # 3-9 for the event where price type is 'SP'/'LP,SP' and the market(s) are expanded
        EXPECTED:
        """
        self.eventID = self.eventID_sp
        self.selection_ids = self.selection_ids_sp
        self.test_002_open_race_event_details_page_where_event_has_lp_price_type_and_it_is_not_going_to_started_now()
        self.test_003_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodesnavigate_to_application_and_observe_changes(
            is_off=True, eventStatusCode=False)
        self.test_006_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodeanavigate_to_application_and_observe_changes()

        self.eventID = self.eventID_lp_sp
        self.selection_ids = self.selection_ids_lp_sp
        self.test_002_open_race_event_details_page_where_event_has_lp_price_type_and_it_is_not_going_to_started_now()
        self.test_003_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodesnavigate_to_application_and_observe_changes()
        self.test_005_in_ti_change_price_for_one_of_the_selections_within_the_market_tab__navigate_to_application_and_observe_changes()
        self.test_006_in_ti_trigger_the_following_situation_for_this_event_when_the_markets_are_collapsedisstarted__trueeventstatuscodeanavigate_to_application_and_observe_changes()
