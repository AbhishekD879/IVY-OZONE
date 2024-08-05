import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.mobile_only
@vtest
class Test_C10922797_Reflection_of_undisplayed_Event_Market_Outcome_when_selection_is_added_to_Quick_Bet(BaseRacing):
    """
    TR_ID: C10922797
    VOL_ID: C14408222
    NAME: Reflection of undisplayed Event/Market/Outcome when selection is added to Quick Bet
    DESCRIPTION: This test case verifies reflection of undisplayed Event/Market/Outcome when selection is added to Quick Bet
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: .Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: .XXXXXXX - event id
    PRECONDITIONS: .LL - language (e.g. en, ukr)
    PRECONDITIONS: * To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: * Updates are received in Remote Betslip microservice: Development tool > Network > WS > remotebetslip/?EIO=3&transport=websocket > Messages section
    """
    keep_browser_open = True

    def check_quick_bet_section(self, expected_message):
        result = self.site.quick_bet_panel.wait_for_quick_bet_info_panel()
        self.assertTrue(result, msg='Suspend message was not shown')

        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(
            self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=5, expected_result=False),
            msg='Stake box is not disabled')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Event creation in OB
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id
        self.__class__.selectionID = list(event.selection_ids.values())[0]

    def test_001_add_one_selection_to_the_quick_bet(self):
        """
        DESCRIPTION: Add one selection to the Quick Bet
        EXPECTED: Quick Bet is opened with added selection
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.add_selection_to_quick_bet()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.site.quick_bet_panel.selection.content.amount_form.input.value = '0.10'

    def test_002_undisplay_eventmarketselection_in_backoffice_tool(self):
        """
        DESCRIPTION: Undisplay Event/Market/Selection in Backoffice tool
        EXPECTED: Changes are saved
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True)

    def test_003_check_quick_bet_when_eventmarketoutcome_is_undisplayed(self):
        """
        DESCRIPTION: Check Quick Bet when Event/Market/Outcome is undisplayed
        EXPECTED: * Message is shown the event has been suspended 'Sorry, the event/market/selection has been suspended' is shown
        EXPECTED: * Stake box & Price are disabled
        EXPECTED: * 'ADD TO BETSLIP' and 'LOGIN & PLACE BET'/'PLACE BET' buttons are disabled
        """
        self.check_quick_bet_section(expected_message=vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended)

    def test_004_display_eventmarketselection_in_backoffice_tool(self):
        """
        DESCRIPTION: Display Event/Market/Selection in Backoffice tool
        EXPECTED: Changes are saved
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_005_check_quick_bet_when_eventmarketoutcome_is_displayed_again(self):
        """
        DESCRIPTION: Check Quick Bet when Event/Market/Outcome is displayed again
        EXPECTED: * No warning message is displayed
        EXPECTED: * 'ADD TO BETSLIP' and 'LOGIN & PLACE BET'/'PLACE BET' buttons are enabled
        """
        message = self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=False)
        self.assertFalse(message, msg='Notification Message was not removed')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(timeout=3),
                        msg='Add to Betslip button is disabled')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(timeout=3),
                        msg='LOGIN & PLACE BET button is not disabled')

    def test_006_check_market_suspention(self):
        """
        DESCRIPTION: Suspend market
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=True)
        self.check_quick_bet_section(expected_message=vec.quickbet.BET_PLACEMENT_ERRORS.market_suspended)
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.test_005_check_quick_bet_when_eventmarketoutcome_is_displayed_again()

    def test_007_check_selection_suspention(self):
        """
        DESCRIPTION: Suspend selection
        """
        self.ob_config.change_selection_state(selection_id=self.selectionID, active=True)
        self.check_quick_bet_section(expected_message=vec.quickbet.BET_PLACEMENT_ERRORS.outcome_suspended)
        self.ob_config.change_selection_state(selection_id=self.selectionID, displayed=True, active=True)
        self.test_005_check_quick_bet_when_eventmarketoutcome_is_displayed_again()
