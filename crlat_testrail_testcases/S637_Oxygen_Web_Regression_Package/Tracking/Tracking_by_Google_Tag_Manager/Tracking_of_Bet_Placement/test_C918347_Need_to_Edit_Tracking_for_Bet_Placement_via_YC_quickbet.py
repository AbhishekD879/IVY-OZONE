import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C918347_Need_to_Edit_Tracking_for_Bet_Placement_via_YC_quickbet(Common):
    """
    TR_ID: C918347
    NAME: [Need to Edit] Tracking for Bet Placement via YC quickbet
    DESCRIPTION: This test case verifies tracking for Bet Placement via YC quickbet
    DESCRIPTION: test case should be edited according to https://jira.egalacoral.com/browse/BMA-33176
    DESCRIPTION: test case example https://ladbrokescoral.testrail.com//index.php?/tests/view/14789306
    PRECONDITIONS: * There is sport event with YourCall (YC) markets available
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Attribute <<CUSTOMER BUILT>> show Yes/No,
    PRECONDITIONS: if bet type = "Build Your Bet shows 'Yes'
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_with_yc_available_and_select_yc_tab(self):
        """
        DESCRIPTION: Navigate to EDP with YC available and select YC tab
        EXPECTED: 
        """
        pass

    def test_002_trigger_successful_bet_placement_add_yc_selections_to_dashboard_proceed_to_yc_betslip_enter_valid_stake_click_place_bet(self):
        """
        DESCRIPTION: Trigger **successful** bet placement:
        DESCRIPTION: * Add YC selection(s) to Dashboard
        DESCRIPTION: * Proceed to YC betslip
        DESCRIPTION: * Enter valid stake
        DESCRIPTION: * Click 'Place bet'
        EXPECTED: 
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Following parameters are sent:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "quickbet"
        EXPECTED: * eventAction: "place bet"
        EXPECTED: * eventLabel: "success"
        EXPECTED: * betID: "<BET ID>", where <BET ID> is the same as on bet receipt
        EXPECTED: * betType: "<BET TYPE>", where BET TYPE is "Single" for one placed selection and "Multiple" for more than one placed selections
        EXPECTED: * location: "yourcall"
        EXPECTED: * 'customerBuilt' : "CUSTOMER BUILT"
        """
        pass

    def test_004_click_done_on_bet_receipt(self):
        """
        DESCRIPTION: Click 'Done' on Bet receipt
        EXPECTED: 
        """
        pass

    def test_005_trigger_unsuccessful_bet_placement_add_yc_selections_to_dashboard_proceed_to_yc_betslip_enter_stake_click_place_bet(self):
        """
        DESCRIPTION: Trigger **UNsuccessful** bet placement:
        DESCRIPTION: * Add YC selection(s) to Dashboard
        DESCRIPTION: * Proceed to YC betslip
        DESCRIPTION: * Enter stake
        DESCRIPTION: * Click 'Place bet'
        EXPECTED: 
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Following parameters are sent:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "quickbet"
        EXPECTED: * eventAction: "place bet"
        EXPECTED: * eventLabel: "failure"
        EXPECTED: * errorMessage: "<ERROR MESSAGE>", where ERROR MESSAGE is the same as received in websocket
        EXPECTED: * errorCode: "<ERROR CODE>", where ERROR CODE is the same is the same as received in websocket
        EXPECTED: * betType: "<BET TYPE>", where BET TYPE is "Single" for one placed selection and "Multiple" for more than one placed selections
        EXPECTED: * location: "yourcall"
        EXPECTED: * 'customerBuilt' : "CUSTOMER BUILT" e.g. "no" (for all non YourCall bets)
        """
        pass
