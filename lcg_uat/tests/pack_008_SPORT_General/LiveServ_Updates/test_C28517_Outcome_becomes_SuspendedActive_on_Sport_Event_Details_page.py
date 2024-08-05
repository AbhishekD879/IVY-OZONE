import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C28517_Outcome_becomes_Suspended_Active_on_Sport_Event_Details_page(BaseSportTest):
    """
    TR_ID: C28517
    NAME: Outcome becomes Suspended/Active on <Sport> Event Details page
    DESCRIPTION: This test case verifies suspension/unsuspension of outcome on <Sport> Event Details page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events.
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.selection_id = event.selection_ids[self.team1]
        self.__class__.section_name = self.expected_market_sections.match_result

    def test_001_open_sport_event_details_page(self):
        """
        DESCRIPTION: Open <Sport> Event Details page
        EXPECTED: Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_trigger_outcome_suspension(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of outcomes of any expanded market
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=False)

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds button of changed outcome is displayed immediately as greyed out and becomes disabled on <Sports> Event Details page but still displaying the price. The rest outcomes and market types are not changed.
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            self.__class__.market = markets_list.get(self.section_name.title())
        else:
            self.__class__.market = markets_list.get(self.section_name.upper())
        self.assertTrue(self.market, msg='Can not find Match Result section')
        self.__class__.outcomes = self.market.outcomes.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes are shown for Match Result market')
        # TODO: VOL-1970 - can be used verify_price_buttons_enabled() after VOL-1970 will be implemented
        for outcome_name, outcome in self.outcomes.items():
            if outcome_name.lower() == self.team1.lower():
                self.assertFalse(
                    outcome.bet_button.is_enabled(expected_result=False, timeout=15),
                    msg='Price/Odds button of "%s" outcome is not displayed as greyed out and '
                        'not becomes disabled' % outcome_name)
            else:
                self.assertTrue(
                    outcome.bet_button.is_enabled(),
                    msg='Price/Odds button of "%s" outcome is not active' % outcome_name)

    def test_004_trigger_outcome_activation(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: Price/Odds button of this outcome becomes active immediately, the rest outcomes and market types remain not changed
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=True)
        for outcome_name, outcome in self.outcomes.items():
            self.assertTrue(
                outcome.bet_button.is_enabled(timeout=15),
                msg='Price/Odds button of "%s" outcome is not active' % outcome_name)

    def test_005_verify_outcome_suspension_in_collapsed_market(self):
        """
        DESCRIPTION: Verify outcome suspension in collapsed market
        EXPECTED: If section is collapsed and outcome was suspended, then after expanding the section Price/Odds button of this outcome is shown as greyed out and disabled
        """
        self.market.collapse()
        self.assertFalse(self.market.is_expanded(), msg='Cannot collapse the section "%s"' % self.section_name)
        self.test_002_trigger_outcome_suspension()
        self.market.expand()
        self.assertTrue(self.market.is_expanded(), msg='Cannot expand the section "%s"' % self.section_name)
        self.test_003_verify_outcomes_for_the_event()
