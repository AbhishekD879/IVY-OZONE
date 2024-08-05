from collections import OrderedDict

import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C135478_Verify_Displaying_Of_Suspended_Selections_on_Landing(BaseSportTest):
    """
    TR_ID: C135478
    NAME:  Verify displaying of suspended selection on <Sport> Landing page when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Sport> Landing page when it is added to the betslip
    """
    keep_browser_open = True
    outputprice = None
    initial_output_prices = None
    expected_prices = None
    expected_betslip_counter_value = 1
    betslip_counter = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        self.__class__.event_name = self.team1 + ' v ' + event_params.team2
        self.__class__.league = tests.settings.football_autotest_league

    def test_001_tap_football_tab(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_verify_prices_not_suspended(self):
        """
        DESCRIPTION: Verify output prices values are not suspended
        """
        self.__class__.initial_output_prices = self.get_output_prices_values(
            self.league, event_id=self.eventID)
        self.verify_prices_not_suspended(self.initial_output_prices)

    def test_003_add_selection(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button
        """
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league)
        prices = event.get_active_prices()
        self.__class__.outputprice = list(prices.values())[0]
        self.__class__.outputprice.click()

        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_004_suspend_price_and_verify(self):
        """
        DESCRIPTION: Suspend price and verify price is suspended on Landing page when it is added to the betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=False)

        event = self.get_event_from_league(section_name=self.league, event_id=self.eventID)
        self.assertTrue(event, msg=f'Event with name "{self.event_name}" not found')

        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        actual_prices = OrderedDict()
        for selection_name, outputprice in price_buttons:
            actual_prices[selection_name] = outputprice.outcome_price_text

        self.verify_prices(actual_prices, self.initial_output_prices)
        self.assertFalse(self.outputprice.is_enabled(timeout=30, expected_result=False),
                         msg=f'Price is not suspended for "{self.team1}"')

    def test_005_unsuspend_price_and_verify(self):
        """
        DESCRIPTION: Unsuspend price and verify that price is not suspended on Landing page when it is added to the betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)

        event = self.get_event_from_league(section_name=self.league, event_id=self.eventID)
        self.assertTrue(event, msg=f'Event with name "{self.event_name}" not found')

        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        actual_prices = OrderedDict()
        for selection_name, outputprice in price_buttons:
            actual_prices[selection_name] = outputprice.outcome_price_text

        self.verify_prices(actual_prices, self.initial_output_prices)
        self.assertTrue(self.outputprice.is_enabled(timeout=5),
                        msg=f'Price is suspended for "{self.team1}"')
