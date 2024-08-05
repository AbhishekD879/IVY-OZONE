import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.football
@pytest.mark.event_details
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C141198_Suspending_Event_Selections(BaseSportTest):
    """
    TR_ID: C141198
    NAME: Verify displaying of suspended selection on <Sport> Event Details page when it is added to the betslip
    """
    league = tests.settings.football_autotest_league
    outputprice = None
    expected_prices = {}
    expected_betslip_counter_value = 1
    betslip_counter = None
    keep_browser_open = True

    def test_001_add_event(self):
        """
        DESCRIPTION: Add 'Football' event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        self.__class__.event_name = self.team1 + ' v ' + event_params.team2

    def test_002_open_event_details_page(self):
        """
        DESCRIPTION: Open 'Event Details' page
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails', timeout=5)

    def test_003_verify_prices_not_suspended(self):
        """
        DESCRIPTION: Verify that output prices values are not suspended
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg='*** Can not find MATCH RESULT section')
        outcomes = section.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Match result output prices were not found on Event Details page')
        for outcome_name, outcome in outcomes.items():
            self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{self.team1}"')
            self.expected_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'*** Outcome name is: {outcome_name}, output price is: {outcome.output_price}')

    def test_004_add_selection(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        DESCRIPTION: Verify that selection is added to Bet Slip
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg='Match result section is not found')
        prices = section.outcomes.items_as_ordered_dict
        self.assertTrue(prices, 'No one bet price was found')
        self.__class__.outputprice = list(prices.values())[0].output_price
        list(prices.values())[0].bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_005_suspend_price_and_verify(self):
        """
        DESCRIPTION: Suspend price and verify price is  suspended on 'Event Details' page when it is added to the betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=False)

        actual_prices = {}
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg='*** Can not find MATCH RESULT section')
        outcomes = section.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Match result output prices were not found on Event Details page')

        for outcome_name, outcome in outcomes.items():
            actual_prices.update({outcome_name: outcome.output_price})
            if outcome_name == self.team1:
                self.assertFalse(outcome.bet_button.is_enabled(timeout=15, expected_result=False),
                                 msg=f'Price is not suspended for "{self.team1}"')
        self.assertEqual(actual_prices, self.expected_prices,
                         msg=f'Actual price "{actual_prices}" and expected "{self.expected_prices}" are not equal')

    def test_006_unsuspend_price_and_verify(self):
        """
        DESCRIPTION: Unsuspend price and verify that price is not suspended on 'Event Details' page when it is added to the betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)
        actual_prices = {}
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg='*** Can not find MATCH RESULT section')
        outcomes = section.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Match result output prices were not found on Event Details page')
        team1 = self.team1.upper() if self.brand == 'ladbrokes' else self.team1
        self.assertTrue(outcomes[team1].bet_button.is_enabled(), msg=f'Price is not active for "{self.team1}"')
        for outcome_name, outcome in outcomes.items():
            actual_prices.update({outcome_name: outcome.output_price})
        self.assertEqual(actual_prices, self.expected_prices,
                         msg=f'Actual price "{actual_prices}" and expected "{self.expected_prices}" are not equal')
