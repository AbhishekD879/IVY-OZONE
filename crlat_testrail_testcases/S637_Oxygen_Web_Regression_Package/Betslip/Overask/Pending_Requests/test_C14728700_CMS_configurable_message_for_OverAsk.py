import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C14728700_CMS_configurable_message_for_OverAsk(Common):
    """
    TR_ID: C14728700
    NAME: CMS configurable message for OverAsk
    DESCRIPTION: This test case verifies CMS configurable message for OverAsk
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is more that allowed Max stake value
    PRECONDITIONS: * CMS: System Configuration-> Structure-> Overask-> text in 'title' and 'topMessage' and 'bottomMessage' is entered
    PRECONDITIONS: ![](index.php?/attachments/get/30945) ![](index.php?/attachments/get/30946)
    """
    keep_browser_open = True

    def test_001_add_selection_and_go_betslip(self):
        """
        DESCRIPTION: Add selection and go Betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_change_title_topmessage_and_bottommessage_in_cmsrepeat_step_2_3(self):
        """
        DESCRIPTION: Change title, topMessage and bottomMessage in CMS
        DESCRIPTION: Repeat step 2-3
        EXPECTED: ![](index.php?/attachments/get/31099)
        """
        pass
