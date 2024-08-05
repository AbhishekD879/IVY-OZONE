import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28535_Verify_placing_a_bet_on_Half_Time_Full_Time_market(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28535
    NAME: Verify placing a bet on 'Half Time/Full Time' market
    DESCRIPTION: This test case verifies markets data and bet placement on 'Half Time/Full Time' market
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Jira ticket: **BMA-3863
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
            PRECONDITIONS: Create a event
        """
        self.__class__.market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.half_time_full_time

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

            for event in events:
                for market in event['event']['children']:
                    if market.get('market').get('templateMarketName') == self.market_name:
                        self.__class__.eventID = market.get('market').get('eventId')
                        self.__class__.event_name = event['event']['name']
                        break
            if self.eventID is None:
                raise SiteServeException('There are no available market with Half-time/Full-time market')
        else:
            markets_params = [('half_time_full_time', {'cashout': True})]
            event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
            self.__class__.event_name = event.team1 + ' v ' + event.team2
            self.__class__.eventID = event.event_id

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.login(username=tests.settings.default_username)

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_half_timefull_time_market_section(self):
        """
        DESCRIPTION: Go to 'Half Time/Full Time' market section
        EXPECTED: *   Section is present on Event Details Page and titled 'Half Time/Full Time market section'
        EXPECTED: *   It is possible to collapse/expand section
        """
        if self.brand == 'ladbrokes':
            self.__class__.expected_market_name = 'Half Time / Full Time' if tests.settings.backend_env == 'prod' else 'Half time/ Full Time Result Market'
        else:
            self.__class__.expected_market_name = 'HALF TIME/ FULL TIME RESULT MARKET' if self.device_type == 'mobile' else 'Half Time/ Full Time Result Market'

        self.assertIn(self.expected_market_name, self.markets_list,
                      msg=f'"{self.expected_market_name}" section is not present')

        self.__class__.half_time_full_time = self.markets_list.get(self.expected_market_name)
        self.assertTrue(self.half_time_full_time,
                        msg=f'"{self.expected_market_name}" section is not found in "{self.markets_list.keys()}"')

        self.half_time_full_time.collapse()
        self.assertFalse(self.half_time_full_time.is_expanded(expected_result=False),
                         msg=f'"{self.half_time_full_time}" section is not collapsed')

        self.half_time_full_time.expand()
        self.assertTrue(self.half_time_full_time.is_expanded(),
                        msg=f'"{self.expected_market_name}" section is not expanded')

    def test_004_expandhalf_timefull_time_market_section(self):
        """
        DESCRIPTION: Expand 'Half Time/Full Time' market section
        EXPECTED: The list of available selections received from SS response are displayed within the market section
        """
        self.__class__.outcomes = self.markets_list[self.expected_market_name].outcomes.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No items found on market outcomes')

    def test_005_add_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add selection to bet slip
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted automatically
        """
        for outcome_name, outcome in self.outcomes.items():
            outcome.bet_button.click()
            self.__class__.selection_name = outcome_name
            self.__class__.odd = outcome.bet_button.outcome_price_text
            break
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel(timeout=20)
            self.site.quick_bet_panel.header.close_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_006_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   The following information is displayed in the Betslip for added selection:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on the event level)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        self.assertEqual(self.stake_name, self.selection_name,
                         msg=f'Selection "{self.selection_name}" should be present in betslip')
        self.assertEqual(len(singles_section), 1,
                         msg='Only one selection should be present in betslip')
        event_name = self.stake.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Event name "{event_name}" is not the same as expected "{self.event_name}"')

        odd = self.stake.odds
        self.assertEqual(odd, self.odd, msg=f'odd value "{odd}" is not the same as expected "{self.odd}"')

        expected_market_name = 'Half Time / Full Time' if tests.settings.backend_env == 'prod' else 'Half-Time/Full-Time'
        self.assertEqual(self.stake.market_name, expected_market_name,
                         msg=f'Market name "{self.stake.market_name}" is not the same as expected "{expected_market_name}"')

    def test_007_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        stake_name = self.stake.name
        stake_value = "0.10"

        self.__class__.stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, self.stake), stake_bet_amounts=self.stake_bet_amounts)

    def test_008_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        user_balance = self.site.header.user_balance
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
        expected_user_balance = user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=float(expected_user_balance), timeout=10)

