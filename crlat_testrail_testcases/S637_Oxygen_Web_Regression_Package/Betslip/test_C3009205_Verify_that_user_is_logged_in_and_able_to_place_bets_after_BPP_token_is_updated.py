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
class Test_C3009205_Verify_that_user_is_logged_in_and_able_to_place_bets_after_BPP_token_is_updated(Common):
    """
    TR_ID: C3009205
    NAME: Verify that user is logged in and able to place bets after BPP token is updated
    DESCRIPTION: AUTOTEST: [C9698693]
    DESCRIPTION: This test case verifies that user is logged in and able to place bets after BPP token is updated
    PRECONDITIONS: Application is launched
    PRECONDITIONS: User is logged in to application and has placed bets with available cash out
    """
    keep_browser_open = True

    def test_001_1_in_dev_tools___application___local_storage_select_app_url(self):
        """
        DESCRIPTION: 1. In Dev Tools -> Application -> Local Storage select app url
        EXPECTED: 
        """
        pass

    def test_002_for_oxuser_parameter_change_bpptoken_value_and_save_changes(self):
        """
        DESCRIPTION: For OX.USER parameter change bppToken": value and save changes
        EXPECTED: 
        """
        pass

    def test_003_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: * 401 Unauthorized returned from BP Proxy -> after which new request is made in order to return valid token
        EXPECTED: * User is still logged in to application
        """
        pass

    def test_004_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added and displayed in the Betslip
        """
        pass

    def test_005_place_bet_for_the_selection(self):
        """
        DESCRIPTION: Place bet for the selection
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_006_go_to_open_bets___cashout_sectionmake_fullpartial_cashout(self):
        """
        DESCRIPTION: Go to Open Bets - Cashout section.
        DESCRIPTION: Make full/partial cashout
        EXPECTED: Cashout process is successfully done
        """
        pass
