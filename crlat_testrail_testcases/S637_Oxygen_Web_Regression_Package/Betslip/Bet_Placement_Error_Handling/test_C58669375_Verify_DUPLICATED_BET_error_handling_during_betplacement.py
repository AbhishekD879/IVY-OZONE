import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C58669375_Verify_DUPLICATED_BET_error_handling_during_betplacement(Common):
    """
    TR_ID: C58669375
    NAME: Verify DUPLICATED_BET error handling during betplacement
    DESCRIPTION: This case verified betplacement error for DUPLICATED_BET
    PRECONDITIONS: - User is logged in with positive balance
    PRECONDITIONS: - Selection(s) added to Betslip, skate field is populated
    """
    keep_browser_open = True

    def test_001___open_betslip_in_app_and_browser_devtools_network_tab__click_on_place_bet(self):
        """
        DESCRIPTION: - Open Betslip in app and browser devtools Network tab
        DESCRIPTION: - Click on Place bet
        EXPECTED: - Bet placed / receipt displayed
        EXPECTED: - placeBet request is sent (e.g. https://bpp-dub.ladbrokes.com/Proxy/v1/placeBet)
        """
        pass

    def test_002___in_devtools_network_right_click_on_placebet_request__copy_as_fetch__in_app_click_on_reuse_selection(self):
        """
        DESCRIPTION: - In devtools (Network) right click on placeBet request > copy as fetch
        DESCRIPTION: - In app click on Reuse Selection
        EXPECTED: - Same selection added to Betslip
        EXPECTED: - 'fetch' is copied to clipboard
        EXPECTED: ![](index.php?/attachments/get/105776338)
        """
        pass

    def test_003___enter_same_stake_amount_as_in_step1__in_devtools_console_paste_fetch_command(self):
        """
        DESCRIPTION: - Enter same stake amount as in step1
        DESCRIPTION: - In devtools console paste 'fetch' command
        EXPECTED: Place Bel button is active
        EXPECTED: 'fetch' command pasted into console
        EXPECTED: ![](index.php?/attachments/get/105776361)
        """
        pass

    def test_004_need_to_execute_this_step_really_fast__press_enter_button_in_devtools_consoleand_fast__click_on_place_bet_button(self):
        """
        DESCRIPTION: !Need to execute this step really fast!
        DESCRIPTION: - Press 'Enter' button in devtools console
        DESCRIPTION: AND FAST
        DESCRIPTION: - Click on Place Bet button
        EXPECTED: - In app: error popup displayed:
        EXPECTED: "Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your Open bets"
        EXPECTED: OPEN BETS displayed as LINK.
        EXPECTED: - placeBet request returned subErrorCode: "DUPLICATED_BET"
        EXPECTED: ![](index.php?/attachments/get/105776365)
        """
        pass

    def test_005_navigate_to_open_bets(self):
        """
        DESCRIPTION: Navigate to Open bets
        EXPECTED: two bets should be displayed in open bets.
        """
        pass
