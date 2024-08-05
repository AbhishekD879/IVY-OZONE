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
class Test_C10922797_Reflection_of_undisplayed_Event_Market_Outcome_when_selection_is_added_to_Quick_Bet(Common):
    """
    TR_ID: C10922797
    NAME: Reflection of undisplayed Event/Market/Outcome when selection is added to Quick Bet
    DESCRIPTION: This test case verifies reflection of undisplayed Event/Market/Outcome when selection is added to Quick Bet
    DESCRIPTION: AUTOTEST [C14408222]
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

    def test_001_add_one_selection_to_the_quick_bet(self):
        """
        DESCRIPTION: Add one selection to the Quick Bet
        EXPECTED: Quick Bet is opened with added selection
        """
        pass

    def test_002_undisplay_eventmarketselection_in_backoffice_tool(self):
        """
        DESCRIPTION: Undisplay Event/Market/Selection in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_003_check_quick_bet_when_eventmarketoutcome_is_undisplayed(self):
        """
        DESCRIPTION: Check Quick Bet when Event/Market/Outcome is undisplayed
        EXPECTED: * 'Your Event/Market/Selection has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * Stake box & Price are disabled
        EXPECTED: * 'ADD TO BETSLIP' and 'LOGIN & PLACE BET'/'PLACE BET' buttons are disabled
        """
        pass

    def test_004_display_eventmarketselection_in_backoffice_tool(self):
        """
        DESCRIPTION: Display Event/Market/Selection in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_005_check_quick_bet_when_eventmarketoutcome_is_displayed_again(self):
        """
        DESCRIPTION: Check Quick Bet when Event/Market/Outcome is displayed again
        EXPECTED: * No warning message is displayed
        EXPECTED: * 'ADD TO BETSLIP' and 'LOGIN & PLACE BET'/'PLACE BET' buttons are enabled
        """
        pass
