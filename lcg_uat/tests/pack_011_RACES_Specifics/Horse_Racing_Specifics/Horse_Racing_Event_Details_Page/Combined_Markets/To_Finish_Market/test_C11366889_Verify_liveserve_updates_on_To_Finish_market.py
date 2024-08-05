import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Can't trigger price change on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.liveserv_updates
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.slow
@vtest
class Test_C11366889_Verify_liveserve_updates_on_To_Finish_market(BaseRacing):
    """
    TR_ID: C11366889
    NAME: Verify liveserve updates on 'To Finish' market
    DESCRIPTION: This test case verifies liveserve updates on 'To Finish' market
    PRECONDITIONS: 1) Horse Racing events with To Finish '2ND / 3RD / 4TH' markets (templateMarketName='To Finish Second', templateMarketName="To Finish Third", templateMarketName="To Finish Fourth") are available
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: 3) To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [
        ('to_finish_second',),
        ('to_finish_third',),
        ('to_finish_fourth',)
    ]
    expected_runners_order = ['3', '2', '1']
    prices = {0: '1/3',
              1: '1/3',
              2: '1/3'}

    @staticmethod
    def get_price(decimal=False):
        return '1.33' if decimal else '1/3'

    @staticmethod
    def get_bigger_price(decimal=False):
        return '1.50' if decimal else '1/2'

    @staticmethod
    def get_lower_price(decimal=False):
        return '1.25' if decimal else '1/4'

    def test_000_preconditions(self, login=True):
        """
        DESCRIPTION: Create test event and login
        """
        event_params = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=3, sp=False,
                                                          lp_prices=self.prices)
        self.__class__.eventID = event_params.event_id
        self.__class__.marketID = self.ob_config.market_ids['to_finish_second']
        self.__class__.selection_ids = event_params.selection_ids

        if login:
            self.site.login()

    def test_001_navigate_to_edp_and_open_to_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'To Finish' market tab
        EXPECTED: 'To Finish' market tab is opened
        """
        self.__class__.tab_name = vec.racing.TO_FINISH_MARKET_NAME
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found')
        self.assertIn(self.tab_name, market_tabs.keys(),
                      msg=f'"{self.tab_name}" tab was not found in the tabs list "{market_tabs.keys()}"')

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)

    def test_002_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions(self, decimal=False):
        """
        DESCRIPTION: In TI: Change price for one of the selections with enabled liveServe updates (see Preconditions)
        """
        self.__class__.selection_name_1, self.__class__.selection_id_1 = list(self.selection_ids['to_finish_second'].items())[2]
        self.__class__.selection_name_2, self.__class__.selection_id_2 = list(self.selection_ids['to_finish_second'].items())[0]

        self.ob_config.change_price(selection_id=self.selection_id_1, price=self.get_price(decimal))
        self.ob_config.change_price(selection_id=self.selection_id_2, price=self.get_price(decimal))

        self.ob_config.change_price(selection_id=self.selection_id_1, price=self.get_lower_price(decimal))
        self.ob_config.change_price(selection_id=self.selection_id_2, price=self.get_bigger_price(decimal))

    def test_003_in_application_observe_changes_on_the_to_finish_market_tab(self, decimal=False, range=3):
        """
        DESCRIPTION: In application: observe changes on the 'To Finish' market tab
        EXPECTED: - Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * pink color if price has increased
        EXPECTED: - Previous Odds, under Price/Odds button, are updated/added respectively
        """
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets_list, msg='No markets found')
        self.assertIn(self.tab_name, event_markets_list,
                      msg=f'"{self.tab_name}" market was not found in "{event_markets_list.keys()}"')

        self.__class__.event_market = event_markets_list[self.tab_name]

        outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')

        self.__class__.outcome_bigger_price = outcomes.get(self.selection_name_2)
        outcome_lower_price = outcomes.get(self.selection_name_1)
        result = wait_for_result(lambda: self.outcome_bigger_price.output_price == self.get_bigger_price(decimal),
                                 poll_interval=2, timeout=45,
                                 name='Waiting price update')

        self.assertTrue(result, msg=f'Price for "{self.selection_name_2}" outcome was not updated')
        self.assertEqual(self.outcome_bigger_price.previous_price[:range], self.get_price(decimal),
                         msg=f'Previous price "{self.outcome_bigger_price.previous_price}" '
                             f'is not the same as expected "{self.get_price(decimal)}" '
                             f'for "{self.selection_name_2}" outcome')

        self.assertEqual(outcome_lower_price.output_price, self.get_lower_price(decimal),
                         msg=f'Price was not updated for "{self.selection_name_1}" outcome')
        self.assertEqual(outcome_lower_price.previous_price[:range], self.get_price(decimal),
                         msg=f'Previous price "{outcome_lower_price.previous_price}" '
                             f'is not the same as expected "{self.get_price(decimal)}" '
                             f'for "{self.selection_name_1}" outcome')

        self.__class__.outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')

        runner_numbers = []
        for outcome_name, outcome in self.outcomes.items():
            runner_numbers.append(outcome.runner_number)

        self.assertEqual(runner_numbers, self.expected_runners_order,
                         msg=f'Runners order "{runner_numbers}" is not the same '
                             f'as expected "{self.expected_runners_order}"')

    def test_004_in_ti_suspend_market(self):
        """
        DESCRIPTION: In TI: Suspend market
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)

    def test_005_in_application_observe_changes_on_the_to_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'To Finish' market tab
        EXPECTED: All Price/Odds buttons under specific market column are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        """
        self.assertFalse(self.outcome_bigger_price.bet_button.is_enabled(timeout=20, expected_result=False),
                         msg=f'Bet button of "{self.selection_name_2}" outcome was not disabled')

        outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')

        for outcome_name, outcome in outcomes.items():
            self.assertFalse(outcome.bet_button.is_enabled(expected_result=False),
                             msg=f'Bet button is not disabled for "{outcome_name}"')
            self.assertTrue(outcome.output_price, msg=f'Price was not shown for "{outcome_name}"')

    def test_006_in_ti_suspend_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions(self):
        """
        DESCRIPTION: In TI: Suspend one of the selections with enabled liveServe updates (see Preconditions)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.assertTrue(self.outcome_bigger_price.bet_button.is_enabled(timeout=20),
                        msg=f'Bet button of "{self.selection_name_2}" outcome was not enabled')

        self.ob_config.change_selection_state(selection_id=self.selection_id_1, displayed=True)

    def test_007_in_application_observe_changes_on_the_to_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'To Finish' market tab
        EXPECTED: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled
        EXPECTED: The rest outcomes and market tabs are not changed
        """
        outcomes = self.event_market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')
        suspended_outcome = outcomes.get(self.selection_name_1)

        self.assertFalse(suspended_outcome.bet_button.is_enabled(expected_result=False, timeout=20),
                         msg=f'Suspended outcome "{self.selection_name_1}" was not disabled')

        runner_numbers = []
        for outcome_name, outcome in outcomes.items():
            runner_numbers.append(outcome.runner_number)
            self.assertTrue(outcome.output_price, msg=f'Price is not shown for {outcome_name} outcome')
            if outcome_name != self.selection_name_1:
                self.assertTrue(outcome.bet_button.is_enabled(),
                                msg=f'Bet button for outcome {outcome_name} was disabled')

        self.assertEqual(runner_numbers, self.expected_runners_order,
                         msg=f'Runners order "{runner_numbers}" is not the same '
                             f'as expected "{self.expected_runners_order}"')

        self.ob_config.change_selection_state(selection_id=self.selection_id_1, displayed=True, active=True)

    def test_008_in_ti_undisplay_all_to_finish_markets(self):
        """
        DESCRIPTION: In TI: Undisplay all 'To Finish' markets
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.ob_config.market_ids['to_finish_second'], active=True)
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.ob_config.market_ids['to_finish_third'], active=True)
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.ob_config.market_ids['to_finish_fourth'], active=True)

    def test_009_in_application_observe_changes_on_the_to_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'To Finish' market tab
        EXPECTED: 'To Finish' collection tab is available and is empty
        """
        result = self.site.racing_event_details.tab_content.event_markets_list \
            .has_market_outcomes(expected_result=False, timeout=3, tab_name=self.tab_name)

        self.assertFalse(result, msg='Outcomes are still present on the tab')

        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertIn(self.tab_name, event_markets_list.keys(),
                      msg=f'"{self.tab_name}" market was not found')

    def test_010_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'To Finish' collection tab disappears
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets_list, msg='No markets found')
        self.assertNotIn(self.tab_name, event_markets_list,
                         msg=f'"{self.tab_name}" market was found')

    def test_011_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_1___10(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 10
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

        self.test_000_preconditions(login=False)
        self.test_001_navigate_to_edp_and_open_to_finish_market_tab()
        self.test_002_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions(decimal=True)
        self.test_003_in_application_observe_changes_on_the_to_finish_market_tab(decimal=True, range=4)
        self.test_004_in_ti_suspend_market()
        self.test_005_in_application_observe_changes_on_the_to_finish_market_tab()
        self.test_006_in_ti_suspend_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions()
        self.test_007_in_application_observe_changes_on_the_to_finish_market_tab()
        self.test_008_in_ti_undisplay_all_to_finish_markets()
        self.test_009_in_application_observe_changes_on_the_to_finish_market_tab()
        self.test_010_refresh_the_page()
