import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569603_Verify_that_Remove_button_is_displayed_and_on_clicking_Remove_option_Confirmation_pop_up_is_displayed(Common):
    """
    TR_ID: C64569603
    NAME: Verify that Remove button is displayed and on clicking Remove option Confirmation pop-up is displayed
    DESCRIPTION: 
    PRECONDITIONS: 1: User should have access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_byb_gt_byb_markets(self):
        """
        DESCRIPTION: Navigate to BYB &gt; BYB Markets
        EXPECTED: Verify that User is able to view Create BuildYourMarket button
        EXPECTED: Table Headers
        EXPECTED: 1: Market Title
        EXPECTED: 2: Market Group Name
        EXPECTED: 3: Market Grouping
        EXPECTED: 4: Incident Grouping
        EXPECTED: 5: Market Type
        EXPECTED: 6: Popular Market
        EXPECTED: 7: Market Description
        EXPECTED: 8: Remove
        EXPECTED: 9: Edit
        """
        pass

    def test_003_navigate_to_any_of_the_market_created_and_check_the_remove_button_available(self):
        """
        DESCRIPTION: Navigate to any of the market created and check the remove button available
        EXPECTED: * Click on Remove button
        EXPECTED: * Remove BuildYourBet Market pop screen will display with Yes/No
        EXPECTED: ![](index.php?/attachments/get/241d288c-985d-477b-a494-a6b787365fc7)
        """
        pass

    def test_004_validate_remove_completed_pop_up_appears_when_click_on_yes(self):
        """
        DESCRIPTION: Validate Remove Completed pop up appears when click on yes
        EXPECTED: * Remove Pop up with Ok button
        EXPECTED: * Cick on Ok
        EXPECTED: ![](index.php?/attachments/get/563b0218-b29d-4ef5-8935-037cada32163)
        """
        pass
