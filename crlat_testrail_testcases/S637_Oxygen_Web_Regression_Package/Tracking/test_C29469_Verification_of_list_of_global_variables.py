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
class Test_C29469_Verification_of_list_of_global_variables(Common):
    """
    TR_ID: C29469
    NAME: Verification of list of global variables
    DESCRIPTION: This Test Case verifies attributes about a user who uses the app.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6472 Add list of global variables that can be retrieved by 3rd party software (e.g. GTM and Evergage)
    DESCRIPTION: BMA-9994 enable SignUpDeliveryPlatofrm as a global object
    PRECONDITIONS: 1. Launch Invictus app
    PRECONDITIONS: 2. Open Console
    """
    keep_browser_open = True

    def test_001_in_console_window_type_windowbmadata_press_enter_button_and_open_displayed_object(self):
        """
        DESCRIPTION: In Console window type 'window.bmadata', press Enter button and open displayed Object
        EXPECTED: Following tags are displayed:
        EXPECTED: *   bma: true - default value
        EXPECTED: *   currency: "GPB" - default value
        EXPECTED: *   depositAmount: null
        EXPECTED: *   depositType: null
        EXPECTED: *   email: null
        EXPECTED: *   firstName: null
        EXPECTED: *   lastName: null
        EXPECTED: *   loggedIn: false
        EXPECTED: *   playerId: null
        EXPECTED: *   postCode: null
        EXPECTED: *   profileId: null
        EXPECTED: *   username: null
        EXPECTED: *   vipLevel: null
        """
        pass

    def test_002_log_in_to_the_app_with_user_who_has_gpbusdeurkr_currency_and_repeat_step_1(self):
        """
        DESCRIPTION: Log in to the app with user who has GPB/USD/EUR/Kr currency and repeat step #1
        EXPECTED: Following tags are displayed:
        EXPECTED: *   bma: true
        EXPECTED: *   currency: "GPB" or "USD" or "EUR" or "Kr" appropriately to the user's account
        EXPECTED: *   depositAmount: null
        EXPECTED: *   depostType: null
        EXPECTED: *   email: "user's email" - should be taken from IMS
        EXPECTED: *   firstName: "user's First Name" - should be taken from IMS
        EXPECTED: *   lastName: "user's Last Name" - should be taken from IMS
        EXPECTED: *   loggedIn: true
        EXPECTED: *   playerId: "XXXXXXXX", where XXXXXXXX - user's id taken from IMS
        EXPECTED: *   postCode: "user's post code" - should be taken from IMS
        EXPECTED: *   profileId: <STRING> or null if user has no profile ID
        EXPECTED: *
        EXPECTED: signUpDeliveryPlatform:"HTML5 - BMA" or ''BMANATIVE'
        EXPECTED: *   username: "user's name" - should be taken from IMS
        EXPECTED: *   vipLevel: "X", where X - VIP Level for the user's IMS account (e.g. 1, 2, 3, 10, 11, 12 )
        """
        pass

    def test_003_navigate_to_deposit_page_and_deposit_any_amount_via_registered_cardspaypalneteller_and_repeat_step_1(self):
        """
        DESCRIPTION: Navigate to Deposit page and deposit any amount via Registered Cards/PayPal/Neteller and repeat step #1
        EXPECTED: Following tags should be changed:
        EXPECTED: *   depositAmount: XX, where XX - amount that user deposited
        EXPECTED: *   depositType: "registered" / "paypal" / "neteller" - appropriately to the depositing type
        """
        pass

    def test_004_log_out_from_the_app_and_repeat_step_1(self):
        """
        DESCRIPTION: Log out from the app and repeat step #1
        EXPECTED: The same tags as in Expected result to the first step should be displayed.
        """
        pass
