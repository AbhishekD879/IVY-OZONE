import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_C888171_Reflection_on_Race_Event_suspended_unsuspended(BaseRacing):
    """
    TR_ID: C888171
    VOL_ID: C9698123
    NAME: Reflection on <Race> Event suspended/unsuspended
    DESCRIPTION: This test case verifies Quick Bet reflection when <Race> event is Suspended/Unsuspended.
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: - Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: - Event should not be **Live** ( **isStarted - absent)**
    PRECONDITIONS: 3.  Event, Market, Outcome should be **Active** ( **eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A")**
    PRECONDITIONS: This test case is applied for **Mobile** application.
    """
    keep_browser_open = True
    prices = {0: '2/17'}

    def test_001_go_to_racing_edp(self):
        """
        DESCRIPTION: Go to the racing event details page
        """
        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices)
        self.__class__.eventID = event.event_id
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')

    def test_002_make_single_selection(self):
        """
        DESCRIPTION: Make single selection
        EXPECTED: Quick Bet is opened with selection added
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()

        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')

        self.device.driver.implicitly_wait(1)  # VOL-1107
        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.quick_bet.amount_form.input.value = '0.01'

    def test_003_suspend_event_in_backoffice_tool(self):
        """
        DESCRIPTION: Suspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"S"**
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True)

    def test_004_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: 'Your Event has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: Stake box, E/W option & Price are disabled
        EXPECTED: 'LOGIN & PLACE BET' button and 'Add to Betslip' button are disabled
        """
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        self.device.driver.implicitly_wait(0)  # VOL-1107

        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.selection.content.odds_dropdown.is_enabled(
            timeout=5, expected_result=False), msg='Odds dropdown is not greyed out')
        self.assertFalse(self.site.quick_bet_panel.selection.content.each_way_checkbox.input.is_enabled(
            timeout=5, expected_result=False), msg='Each Way checkbox is not greyed out')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_005_unsuspend_event_in_backoffice(self):
        """
        DESCRIPTION: Unsuspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"A"**
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True, displayed=True)

    def test_006_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: Message is removed
        EXPECTED: Stake box & Price are enabled
        EXPECTED: 'Bet Now' button and 'Add to Betslip' button are enabled
        """
        message = self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=False)
        self.assertFalse(message, msg='Notification Message was not removed')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(timeout=3),
                        msg='Add to Betslip button is disabled')
        self.assertTrue(self.site.quick_bet_panel.selection.content.odds_dropdown.is_enabled(),
                        msg='Odds dropdown is not enabled')
        self.assertTrue(self.site.quick_bet_panel.selection.content.each_way_checkbox.input.is_enabled(),
                        msg='Each Way checkbox is not enabled')
