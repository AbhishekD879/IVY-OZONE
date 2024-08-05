import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C16394902_Vanilla_Verify_My_account_menu(Common):
    """
    TR_ID: C16394902
    NAME: [Vanilla] Verify "My account" menu
    DESCRIPTION: This TC verifies the "My account" menu
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
       PRECONDITIONS: 1. Load the app
       PRECONDITIONS: 2. Log in as a non VIP user
       """
        self.site.login()

    def test_001_click_the_my_account_element_top_menu_bardesktop__tablet(self):
        """
        DESCRIPTION: Click the "My account" element (top menu bar)
        DESCRIPTION: *Desktop / Tablet:*
        DESCRIPTION: ![](index.php?/attachments/get/114837491)
        DESCRIPTION: *Mobile:*
        DESCRIPTION: ![](index.php?/attachments/get/10014148)
        EXPECTED: 1. My account ?menu opens
        EXPECTED: 2. Menu should contain options (options may differ - Portal config):
        EXPECTED: - Cashier
        EXPECTED: - Offers
        EXPECTED: - History
        EXPECTED: - Inbox
        EXPECTED: - Connect
        EXPECTED: - Settings
        EXPECTED: - Gambling Controls
        EXPECTED: - Help & Contact
        EXPECTED: - Log out
        EXPECTED: and green [DEPOSIT] button at the bottom.
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg="Right Menu Failed To Open")
        right_menu_items = list(self.site.right_menu.get_items().keys())
        self.assertCountEqual(right_menu_items, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU,
                              msg=f'Actual items: "{right_menu_items}"is not same as '
                                  f'Expected items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        self.assertTrue(self.site.right_menu.deposit_button.is_displayed, msg="Deposit Button is not displayed at the "
                                                                              "botton")
        deposit_color = self.site.right_menu.deposit_button.value_of_css_property('background-color')
        self.assertEquals(deposit_color, vec.colors.DEPOSIT_BUTTON_COLOR,
                          msg=f'Actual items: "{deposit_color}"is not same as '
                              f'Expected items: "{vec.colors.DEPOSIT_BUTTON_COLOR}"')
