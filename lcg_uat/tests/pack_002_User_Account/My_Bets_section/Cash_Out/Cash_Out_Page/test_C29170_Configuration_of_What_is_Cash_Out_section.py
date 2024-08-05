import pytest

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_hl
@pytest.mark.crl_prod
@pytest.mark.cms
@pytest.mark.cash_out
@pytest.mark.static_block
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29170_Configuration_of_What_is_Cash_Out_section(Common):
    """
    TR_ID: C29170
    NAME: Configuration of What is Cash Out section
    DESCRIPTION: This test case verifies configuration of 'What is Cash Out?' section
    PRECONDITIONS: User is logged in
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    """
    keep_browser_open = True
    dialog = None
    whats_cashout_dialog = vec.dialogs.DIALOG_MANAGER_WHATS_CASHOUT
    is_enabled = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if not cls.is_enabled and tests.settings.cms_env != 'prd0':
            cms = cls.get_cms_config()
            cms.enable_static_block(uri=cms.constants.WHAT_IS_CASH_OUT_STATIC_BLOCK_URI, enable=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CMS settings ans set cookies
        """
        self.__class__.is_enabled = self.cms_config.is_static_block_enabled(uri=self.cms_config.constants.WHAT_IS_CASH_OUT_STATIC_BLOCK_URI)
        if not self.is_enabled:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.enable_static_block(uri=self.cms_config.constants.WHAT_IS_CASH_OUT_STATIC_BLOCK_URI)
            else:
                raise CmsClientException(f'Static block with uri "{self.cms_config.constants.WHAT_IS_CASH_OUT_STATIC_BLOCK_URI}" is disabled, '
                                         f'cannot execute the test on prod endpoints')
        static_block = self.cms_config.get_static_block(uri=self.cms_config.constants.WHAT_IS_CASH_OUT_STATIC_BLOCK_URI)
        self.__class__.cms_static_block_description = cleanhtml(static_block['htmlMarkup']).strip().replace('\r\n', '\n')

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        """
        self.site.login(async_close_dialogs=False)

    def test_002_open_my_bets_page(self):
        """
        DESCRIPTION: Open 'My Bets' page
        EXPECTED: 'My Bets' page is opened
        """
        self.site.open_my_bets_cashout()

    def test_003_tap_cash_out_tab_and_verify_whats_cashout_link(self):
        """
        DESCRIPTION: Tap 'Cash Out' tab and verify 'What's Cashout?' link
        EXPECTED: 'What's Cashout?' pop-up is opened
        """
        self.site.cashout.tab_content.accordions_list.header.what_is_cashout.click()
        self.__class__.dialog = self.site.wait_for_dialog(self.whats_cashout_dialog)
        self.assertTrue(self.dialog, msg=f'{self.whats_cashout_dialog}" dialog is not shown')

    def test_004_verify_content_of_whats_cashout_pop_up(self):
        """
        DESCRIPTION: Verify content of 'What's Cashout?' pop-up
        EXPECTED: Content of 'What's Cashout?' pop-up corresponds to the html text set up in CMS->Static Blocks->What is Cash Out
        """
        dialog_description = self.dialog.description
        self.cms_static_block_description = self.cms_static_block_description.replace("run. ", "run.")
        self.assertEqual(dialog_description, self.cms_static_block_description,
                         msg='Actual description on pop-up \n"%s"\n is not the same as on CMS: \n"%s"'
                         % (dialog_description, self.cms_static_block_description))

    def test_005_click_on_x_button_on_whats_cashout_pop_up(self):
        """
        DESCRIPTION: Click on 'X' button on 'What's Cashout?' pop-up
        EXPECTED: 'What's Cashout?' pop-up is closed
        """
        self.dialog.close_dialog()
        self.dialog.wait_dialog_closed()
        dialog = self.site.wait_for_dialog(self.whats_cashout_dialog, timeout=1)
        self.assertFalse(dialog, msg=f'"{self.whats_cashout_dialog}" dialog still shown after clicking on "X" button')
