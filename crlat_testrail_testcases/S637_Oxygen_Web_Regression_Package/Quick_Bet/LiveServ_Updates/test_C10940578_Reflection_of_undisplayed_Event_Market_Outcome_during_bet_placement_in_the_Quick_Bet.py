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
class Test_C10940578_Reflection_of_undisplayed_Event_Market_Outcome_during_bet_placement_in_the_Quick_Bet(Common):
    """
    TR_ID: C10940578
    NAME: Reflection of undisplayed Event/Market/Outcome during bet placement in the Quick Bet
    DESCRIPTION: This test case verifies reflection of undisplayed Event/Market/Outcome during bet placement in the Quick Bet
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Log in app
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
        EXPECTED: Quick Bet is opened with the added selection
        """
        pass

    def test_002_enter_the_value_in_stake_field(self):
        """
        DESCRIPTION: Enter the value in 'Stake' field
        EXPECTED: 'Stake' field is populated with the entered value
        """
        pass

    def test_003_tap_place_bet_button_and_at_the_same_timeundisplay_eventmarketselection_in_backoffice_toolnotetapping_place_bet_should_be_done_a_little_bit_sooner_than_undisplaying(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button and at the same time
        DESCRIPTION: undisplay Event/Market/Selection in Backoffice tool
        DESCRIPTION: *Note:*
        DESCRIPTION: Tapping 'PLACE BET' should be done a little bit sooner than undisplaying
        EXPECTED: * Spinner is displayed on 'PLACE BET' icon while bet placement is in process
        EXPECTED: * 'Your the Event/Market/Selection has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * Stake box & Price are disabled
        EXPECTED: * 'ADD TO BETSLIP' and 'LOGIN & PLACE BET'/'PLACE BET' buttons are disabled
        EXPECTED: * displayed: "N" attribute is received for Event/Market/Selection from remotebetslip MS
        EXPECTED: -
        EXPECTED: In case of Event/Market undisplay(suspension) first message shown will be regarding the 'selection' suspension, followed by a message about suspension of certain entity(market/event) that was suspended.
        """
        pass

    def test_004_verify_if_bet_placement_was_successful(self):
        """
        DESCRIPTION: Verify if bet placement was successful
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #2
        EXPECTED: * Bet Receipt is displayed with bet ID number
        """
        pass
