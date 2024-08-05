import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C10922798_Reflection_of_undisplayed_Event_Market_Outcome_during_adding_selection_to_the_Quick_Bet(Common):
    """
    TR_ID: C10922798
    NAME: Reflection of undisplayed Event/Market/Outcome during adding selection to the Quick Bet
    DESCRIPTION: This test case verifies reflection of undisplayed Event/Market/Outcome during adding selection to the Quick Bet
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
    PRECONDITIONS: * To check logs please use Kibana tool: https://confluence.egalacoral.com/display/SPI/Symphony+Infrastructure+creds
    """
    keep_browser_open = True

    def test_001_undisplay_eventmarketselection_in_backoffice_tool_and_at_the_same_time_add_selection_to_the_quick_betnoteundisplaying_should_be_triggered_a_little_bit_sooner_than_selection_is_added_to_quick_bet(self):
        """
        DESCRIPTION: Undisplay Event/Market/Selection in Backoffice tool and at the same time add selection to the Quick Bet
        DESCRIPTION: *Note:*
        DESCRIPTION: Undisplaying should be triggered a little bit sooner than selection is added to Quick Bet
        EXPECTED: * Quick Bet is opened
        EXPECTED: * 'Selection is no longer available' message is displayed in the Quick Bet
        EXPECTED: * "EVENT_NOT_FOUND" code is received '31002' response from remotebetslip MS
        """
        pass

    def test_002__add_any_sport__race_selection_to_quick_bet_enter_value_in_stake_field_and_select_ew_option_if_available_tap_bet_now_button(self):
        """
        DESCRIPTION: * Add any <Sport> / <Race> selection to Quick bet
        DESCRIPTION: * Enter value in 'Stake' field and select 'E/W' option (if available)
        DESCRIPTION: * Tap 'BET NOW' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_trigger_situation_when_event_market_selection_becomes_undisplayed_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger situation when event/ market/ selection becomes undisplayed in Openbet TI tool
        EXPECTED: * Event/ market/ selection is undispalyed
        EXPECTED: * Bet Receipt stays opened with the same data
        """
        pass

    def test_004_tap_reuse_selection_button(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION' button
        EXPECTED: * Quick Bet is opened
        EXPECTED: * 'Selection is no longer available' message is displayed on white background
        EXPECTED: * 'ADD TO BETSLIP' and 'PLACE BET' buttons are disabled
        """
        pass

    def test_005_verify_kibana_logs(self):
        """
        DESCRIPTION: Verify Kibana logs
        EXPECTED: **[WARN ]** or **[Info]** type is being tracked for the selection e.g.:
        EXPECTED: [WARN ] [s:739415b4-ba98-42a3-a1dc-4656fb9e7b3c] c.c.oxygen.middleware.ms.quickbet.impl.FixedBetsOperations - Event was undisplayed RegularPlaceBetResponse{data=Data{receipt=null, error=RegularPlaceBetResponse.Error(code=EVENT_NOT_FOUND, description=Error reading outcome data. Data not found. OutcomeIds - [979037758], subErrorCode=null, handicap=null, price=null, stake=null, maxStake=null)}}
        """
        pass

    def test_006_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Quick Bet is not displayed anymore
        """
        pass
