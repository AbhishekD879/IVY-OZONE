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
class Test_C14835386_Verify_Cancel_Offer_pop_up(Common):
    """
    TR_ID: C14835386
    NAME: Verify 'Cancel Offer?' pop-up
    DESCRIPTION: This test case verifies 'Cancel Offer?' pop-up appears during cancelling the bet offer from a trader triggered by overask functionality
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

    def test_003_trigger_stake_modification_by_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: 'Cancel' and 'Place a bet' buttons are present and enabled
        """
        pass

    def test_005_click__tap_cancel_button(self):
        """
        DESCRIPTION: Click / tap 'Cancel' button
        EXPECTED: * 'Cancel Offer?' pop up with a message 'Moving away from this screen will cancel your offer. Are you sure you want to go ahead?' and 'No, Return' and 'Cancel Offer' buttons, pop-up appears on the grey background
        EXPECTED: ![](index.php?/attachments/get/31093) ![](index.php?/attachments/get/31097)
        """
        pass
