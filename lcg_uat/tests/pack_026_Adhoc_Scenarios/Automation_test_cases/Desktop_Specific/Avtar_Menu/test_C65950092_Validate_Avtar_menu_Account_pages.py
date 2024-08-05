import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65950092_Validate_Avtar_menu_Account_pages(Common):
    """
    TR_ID: C65950092
    NAME: Validate Avtar menu Account pages
    DESCRIPTION: This test case is to verify the Avtar menu Account pages
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.site.login()

    def test_002_verify_avatar__icon_in_the__header(self):
        """
        DESCRIPTION: Verify avatar  icon in the  header
        EXPECTED: User should be able to see Avatar  icon should be present
        """
        avatar = wait_for_result(
            lambda: self.site.header.has_right_menu() and self.site.header.right_menu_button.is_displayed(timeout=1),
            timeout=10,
            name='Right Menu button to be displayed')
        self.assertTrue(avatar, msg="Avatar is not available")

    def test_003_click_on_avatar_menu_icon(self):
        """
        DESCRIPTION: Click on Avatar menu icon
        EXPECTED: User should able to see avatar menus
        """
        self.site.header.right_menu_button.click()

    def test_004_verify_account_page(self):
        """
        DESCRIPTION: verify Account page
        EXPECTED: page should cosnsits of
        EXPECTED: 1.My bets
        EXPECTED: 2.my account details
        EXPECTED: 3.settings
        EXPECTED: 4.Transaction history
        EXPECTED: 5.Gambling controls
        EXPECTED: 6.Help &amp;contact
        """
        right_menu_items = self.site.right_menu.section_wise_items
        account_items = right_menu_items.get("ACCOUNT").keys()
        expected_account_items = ['MYBETS', 'MYACCOUNTDETAILS', 'SETTINGS', 'TRANSACTIONHISTORY', 'GAMBLINGCONTROLS',
                                  'LOSSLIMIT&DEPOSITCAP', 'HELP&CONTACT']
        for account_item in account_items:
            self.assertIn(account_item, expected_account_items,
                          msg=f"cashier item {account_item} is not present in cashier items {expected_account_items}")
