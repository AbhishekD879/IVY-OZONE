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
class Test_C14835385_TO_EDITVerify_Cancel_and_Place_bet_buttons(Common):
    """
    TR_ID: C14835385
    NAME: [TO-EDIT]Verify Cancel and Place bet buttons
    DESCRIPTION: This test case verifies Cancel and Place bet buttons appear during bet offer from a trader triggered by overask functionality
    DESCRIPTION: ![](index.php?/attachments/get/31089)    ![](index.php?/attachments/get/31088)
    DESCRIPTION: Step 5 needs to be edited according to latest changes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: 7. The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002__add_selection_and_go_betslip_singles_section_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(self):
        """
        DESCRIPTION: * Add selection and go Betslip, 'Singles' section
        DESCRIPTION: * Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        pass

    def test_003_trigger_stake_modification_by_trader_in_openbet_system_in_openbet_system(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader in OpenBet system in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * Selection is displayed
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons are enabled
        EXPECTED: NEW design:
        EXPECTED: ![](index.php?/attachments/get/33507) ![](index.php?/attachments/get/33508)
        """
        pass

    def test_005_uncheck_checkbox_with_max_bet_offerfrom_ox_99checkbox_is_removed(self):
        """
        DESCRIPTION: Uncheck checkbox with max bet offer
        DESCRIPTION: **From OX 99**
        DESCRIPTION: Checkbox is removed
        EXPECTED: * 'Cancel' and 'Place a bet' buttons are present and disabled
        EXPECTED: * Message: "You're not accepting this Trade Offer" is displayed on the grey background below the unchecked selection
        """
        pass
