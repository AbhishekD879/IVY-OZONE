import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C29170_Configuration_of_What_is_Cash_Out_pop_up(Common):
    """
    TR_ID: C29170
    NAME: Configuration of 'What is Cash Out?'  pop-up
    DESCRIPTION: This test case verifies the configuration of the 'What is Cash Out?' pop-up on 'Cash out' page
    PRECONDITIONS: * CMS endpoints can be checked here: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: * To view 'What is Cash Out?' pop-up setup go to CMS -> Static Blocks -> 'What is Cash Out EN' static block
    PRECONDITIONS: * To check CMS response open Dev Tools -> Network tab -> XHR option -> set 'cms' filter -> choose request to 'what-is-cash-out-en-us' static block
    PRECONDITIONS: * Load Oxygen application
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: Design of 'What is Cash Out?' pop-up:
    PRECONDITIONS: ![](index.php?/attachments/get/2690277)
    """
    keep_browser_open = True

    def test_001_open_my_bets_page(self):
        """
        DESCRIPTION: Open 'My Bets' page
        EXPECTED: 'My Bets' page is opened
        """
        pass

    def test_002_tap_cash_out_tab_and_verifywhats_cashout_option(self):
        """
        DESCRIPTION: Tap 'Cash Out' tab and verify 'What's Cashout?' option
        EXPECTED: 'What's Cashout?' option consists of:
        EXPECTED: * Question mark icon
        EXPECTED: * 'What's Cashout?'link
        """
        pass

    def test_003_tap_whats_cashout_link(self):
        """
        DESCRIPTION: Tap 'What's Cashout?' link
        EXPECTED: Pop-up appears with the next elements:
        EXPECTED: * 'What's Cashout?' hardcoded title and 'X' button
        EXPECTED: * CMS-configurable text
        """
        pass

    def test_004_verify_cms_configurable_text(self):
        """
        DESCRIPTION: Verify CMS-configurable text
        EXPECTED: CMS-configurable text corresponds to **htmlMarkup** parameter from GET **static-block/what-is-cash-out-en-us** response from CMS
        EXPECTED: ![](index.php?/attachments/get/2723647)
        """
        pass

    def test_005_go_cms_static_blocks_what_is_cash_out_make_any_changesconfigurations_and_save_them(self):
        """
        DESCRIPTION: Go CMS->Static Blocks->What is Cash Out, make any changes/configurations and save them
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_006_repeat_steps_1_4(self):
        """
        DESCRIPTION: Repeat steps №1-4
        EXPECTED: All changes are displayed
        """
        pass
