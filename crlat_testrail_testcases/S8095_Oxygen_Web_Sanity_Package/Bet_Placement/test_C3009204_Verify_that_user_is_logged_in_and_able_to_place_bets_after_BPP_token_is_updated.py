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
class Test_C3009204_Verify_that_user_is_logged_in_and_able_to_place_bets_after_BPP_token_is_updated(Common):
    """
    TR_ID: C3009204
    NAME: Verify that user is logged in and able to place bets after BPP token is updated
    DESCRIPTION: AUTOTEST: [C49357447]
    DESCRIPTION: This test case verifies that user is logged in and able to place bets/cashout after BPP token is updated
    DESCRIPTION: **Automation note - this test has to be updated - invalidateSession request does not present anymore starting from OX 106**
    PRECONDITIONS: 1. Application is launched
    PRECONDITIONS: 2. User is logged in to application
    PRECONDITIONS: 3. Trigger situation when BPP token is wrong or expired:
    PRECONDITIONS: * Open Postman
    PRECONDITIONS: * Send DELETE request to correct BPP from **user** request > 'Preview' with actual **Headers** for request:
    PRECONDITIONS: https://{domain}/Proxy/auth/invalidateSession
    PRECONDITIONS: **token** key - with current BPP token value
    PRECONDITIONS: **username** key - with currently logged in user's login
    PRECONDITIONS: where **{domain}** may be
    PRECONDITIONS: * https://bpp-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com - Ladbrokes TST2
    PRECONDITIONS: * https://hl-bpp.ladbrokes.com - Ladbrokes HL
    PRECONDITIONS: * https://bp-hl.coral.co.uk - Coral BETA
    PRECONDITIONS: **etc.**
    PRECONDITIONS: e.g. ![](index.php?/attachments/get/28190)
    PRECONDITIONS: Request returns **204 No Content** status code
    """
    keep_browser_open = True

    def test_001_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in_after_passing_preconditions(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in (after passing Preconditions)
        EXPECTED: * User is still logged in to application
        EXPECTED: * User has BPP token value assigned (Check in **OX.USER** parameter in Dev Tools -> Application -> Local Storage)
        """
        pass

    def test_002_add_selection_to_the_betslip_where_cash_out_is_available_and_place_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip (where cash out is available) and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003__go_to_open_bets___cash_out_section_make_fullpartial_cash_out(self):
        """
        DESCRIPTION: * Go to Open Bets - Cash out section.
        DESCRIPTION: * Make full/partial Cash out
        EXPECTED: Cash out process is successfully done
        """
        pass

    def test_004_in_dev_tools___application___local_storage_select_app_urlfor_oxuser_parameter_change_bpptoken_value_and_save_changesin_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In Dev Tools -> Application -> Local Storage select app url
        DESCRIPTION: For OX.USER parameter change bppToken: value and save changes
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: * User is still logged in to application
        EXPECTED: * User has BPP token value assigned (could be checked in **OX.USER** parameter in Dev Tools -> Application -> Local Storage)
        """
        pass

    def test_005_add_selection_to_the_betslip_where_cash_out_is_available_and_place_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip (where cash out is available) and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_006__go_to_open_bets___cash_out_section_make_fullpartial_cash_out(self):
        """
        DESCRIPTION: * Go to Open Bets - Cash out section.
        DESCRIPTION: * Make full/partial Cash out
        EXPECTED: Cash out process is successfully done
        """
        pass
