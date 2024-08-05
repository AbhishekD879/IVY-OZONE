from random import choice
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.navigation
@pytest.mark.adhoc_suite
@pytest.mark.trending_bets
@pytest.mark.mobile_only
@vtest
class Test_C65972742_Verify_the_Display_of_popular_bets_carousel_in_Bet_Receipt_page_for_combination_of_football_and_Non_football_selection_bets(BaseBetSlipTest):
    """
    TR_ID: C65972742
    NAME: Verify the Display of popular bets carousel in Bet Receipt page for combination of football and Non football selection bets
    DESCRIPTION: This testcase is to verifies the Display of popular bets carousel in Bet Receipt page for combination of football and Non football selection bets
    PRECONDITIONS: Should have football events
    PRECONDITIONS: Should able to placebet
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def get_event_info(self, category_id):
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
            events = self.get_active_events_for_category(category_id=category_id, additional_filters=additional_filter)
            if events:
                event = events[0]
                self.__class__.event_name = normalize_name(event['event']['name'])
                self.__class__.event_id = event['event']['id']
                self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
                self._logger.info(f'*** Found event "{self.event_name}" with ID "{self.event_id}"')
            else:
                self._logger.warning(f'No active events found for category ID "{category_id}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_league
            self._logger.info(f'*** Created event "{self.event_name}" with ID "{self.event_id}"')


    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        trending_carousel_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_betslip:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)
        trending_carousel_betreceipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('active')
        if not trending_carousel_betreceipt:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(active=True)



    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_003_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any Selection
        EXPECTED: Single Selection is added to Betslip
        """
        self.get_event_info(category_id=self.ob_config.football_config.category_id)
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')
        self.__class__.selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(self.selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{self.selection}" was not found')
        bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)

    def test_004_navigate_to_any_other_sport_add_selection(self):
        """
        DESCRIPTION: Navigate to any other sport add selection
        EXPECTED: Should able to add selections to betslip
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        self.get_event_info(category_id=self.ob_config.tennis_config.category_id)
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')
        self.__class__.selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(self.selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{self.selection}" was not found')
        bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)


    def test_005_place_bet_in_betslip(self):
        """
        DESCRIPTION: Place bet in betslip
        EXPECTED: Should able to place bet and betreceipt should be loaded
        """
        self.site.open_betslip()
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False), msg=f'betslip has trending_bet carousel which shouldnt be available')
        self.place_multiple_bet(number_of_stakes=1)

    def test_006_verify_betreceipt(self):
        """
        DESCRIPTION: Verify betreceipt
        EXPECTED: Popular bets carousel should not display in bet slip section
        """
        self.assertFalse(self.site.bet_receipt.has_trending_bet_carousel(), msg=f'bet receipt has trending bet carousel which shouldnt be available')

    def test_007_verify_betreceipt_by_adding_selections_in_vice_versa_and_place_a_bet(self):
        """
        DESCRIPTION: Verify betreceipt by adding selections in Vice versa and place a bet
        EXPECTED: able to add selection1 from any sport other than football and selection2 from football
        """
        self.test_004_navigate_to_any_other_sport_add_selection()
        self.test_002_click_on_the_football_sport()
        self.test_003_click_on_any_selection()

    def test_008_enter_stake_and_place_a_double_bet(self):
        """
        DESCRIPTION: enter Stake and Place a Double bet
        EXPECTED: Able to place a bet successfully
        """
        self.site.open_betslip()
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False), msg=f'betslip has trending_bet carousel which shouldnt be available')
        self.place_multiple_bet(number_of_stakes=1)

    def test_009_verify_betreceipt(self):
        """
        DESCRIPTION: Verify betreceipt
        EXPECTED: Popular bets carousel should not display in bet slip section
        """
        self.assertFalse(self.site.bet_receipt.has_trending_bet_carousel(), msg=f'bet receipt has trending bet carousel which shouldnt be available')
