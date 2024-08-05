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
class Test_C2493541_Cancelling_split_bets_linked_parts_traders_offer(Common):
    """
    TR_ID: C2493541
    NAME: Cancelling split bets & linked parts trader's offer
    DESCRIPTION: This test case verifies bet split and linking within Overask functionality
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip > Open Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection__tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection > Tap 'Bet Now' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_003_in_ti_trigger__bet_split_for_several_parts__link_some_of_split_bets__stakeoddsprice_type_modification_submit_changes(self):
        """
        DESCRIPTION: In TI trigger:
        DESCRIPTION: - Bet Split for several parts
        DESCRIPTION: - Link some of split bets
        DESCRIPTION: - Stake/Odds/Price Type modification
        DESCRIPTION: > Submit changes
        EXPECTED: 
        """
        pass

    def test_004_in_app_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: In app: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *  The bet parts are linked with 'link' symbol
        EXPECTED: *   'Accept & Bet' and 'Cancel' buttons are displayed
        EXPECTED: *   Bets are selected by default and 'Accept & Bet' button is enabled
        EXPECTED: **From OX 99**
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *   Parent selection doesn't have a Remove button
        EXPECTED: *   Remove button displays only on the child selection
        EXPECTED: *   Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: New Design!
        EXPECTED: ![](index.php?/attachments/get/33780) ![](index.php?/attachments/get/33781)
        """
        pass

    def test_005_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: *   Bets are not placed
        EXPECTED: *   Selection added in step 1 is displayed in Betslip
        EXPECTED: **From OX 99**
        EXPECTED: * 'Cancel Offer?' pop up with a message 'Moving away from this screen will cancel your offer. Are you sure you want to go ahead?' and 'No, Return' and 'Cancel Offer' buttons, pop-up appears on the grey background
        EXPECTED: ![](index.php?/attachments/get/31093)
        """
        pass

    def test_006_from_ox_99click__tap_cancel_offer_button(self):
        """
        DESCRIPTION: **From OX 99**
        DESCRIPTION: Click / tap 'Cancel Offer' button
        EXPECTED: **From OX 99**
        EXPECTED: *  Betslip closes
        EXPECTED: *  Selection is NOT present in the betslip
        EXPECTED: *  User stays on the prev page
        """
        pass

    def test_007_repeat_steps_1_5do_not_link_split_bets_in_step_3(self):
        """
        DESCRIPTION: Repeat steps 1-5
        DESCRIPTION: (do not link split bets in step 3)
        EXPECTED: *   Bets are not placed
        EXPECTED: *   Selection added in step 1 is displayed in Betslip
        """
        pass
