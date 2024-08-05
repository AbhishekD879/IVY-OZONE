import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C28511_Verify_Event_Suspended_Active(BaseSportTest):
    """
    TR_ID: C28511
    NAME: Event becomes Suspended/Active on <Sport> Event Details page
    """
    keep_browser_open = True
    event_id = None

    def test_000_add_event(self):
        """
        DESCRIPTION: Add event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id

    def test_001_suspend_event_in_TI(self):
        """
        DESCRIPTION: Suspend event in TI
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled,
        but still displaying the prices
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)

        self.__class__.market_name = self.expected_market_sections.match_result
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        outcomes = markets[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():
            price = outcome.bet_button.name
            self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=60, poll_interval=1),
                             msg='Bet button "%s" is not disabled, but was expected to be disabled' % price)
            self.assertTrue(price, msg='Bet button text is not displayed, but was expected to be displayed')

    def test_002_activate_event_in_TI(self):
        """
        DESCRIPTION: Make event Active again in TI
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        outcomes = markets[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():
            price = outcome.bet_button.name
            self.assertTrue(outcome.bet_button.is_enabled(expected_result=True, timeout=60, poll_interval=1),
                            msg='Bet button "%s" is not enabled, but was expected to be enabled' % price)
            self.assertTrue(price, msg='Bet button text is not displayed, but was expected to be displayed')
