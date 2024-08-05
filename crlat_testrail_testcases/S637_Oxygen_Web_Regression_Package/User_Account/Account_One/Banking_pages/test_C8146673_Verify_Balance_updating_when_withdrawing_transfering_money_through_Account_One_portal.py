import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C8146673_Verify_Balance_updating_when_withdrawing_transfering_money_through_Account_One_portal(Common):
    """
    TR_ID: C8146673
    NAME: Verify 'Balance' updating when withdrawing/transfering money through 'Account One' portal
    DESCRIPTION: This test case verifies successful money withdrawing through 'Account One' portal
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile [C23061812]
    DESCRIPTION: Desktop [C23066024]
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'withdraw' and 'transfer' & 'Field Value' = [account one URL e.g. http://accountone-test.ladbrokes.com/withdraw and http://accountone-test.ladbrokes.com/transfer] are available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: 4. User has some money on balance
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Test Accounts for Payment methods: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection URLs:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/withdraw?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/withdraw?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/withdraw?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_the_right_menu__banking__withdraw_or_transfer_menu_itemdesktopclick_on_my_account__banking__withdraw_or_transfer_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > 'Banking' > 'Withdraw' or 'Transfer' menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Banking' > 'Withdraw' or 'Transfer' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Withdraw' or 'Transfer' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Withdraw' or 'Transfer' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_select_service_to_withdraw_or_transfer_to__fill_in_amount_field_with_some_figure_eg_5__tap_withdraw_or_transfer_button__accept(self):
        """
        DESCRIPTION: Select service to withdraw or transfer to > Fill in 'Amount' field with some figure (e.g., 5) > Tap 'Withdraw' or 'Transfer' button > Accept
        EXPECTED: Money has been taken from user's balance in 'Account One'
        """
        pass

    def test_003_mobiletablettap_on_close_icon_in_the_right_upper_corner_of_withdraw_or_transfer_page_on_account_one_portaldesktopclose_the_withdraw_or_transfer_account_one_portal_pop_up_by_clicking_on_x_icon_within_the_pop_up(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on 'Close' icon in the right upper corner of 'Withdraw' or 'Transfer' page (on 'Account One' portal)
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Withdraw' or 'Transfer' ('Account One' portal) pop up by clicking on 'X' icon within the pop-up
        EXPECTED: - User is redirected back to an app
        EXPECTED: - The app is refreshed > splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance has been reduced on the amount of money transferred in step 2
        """
        pass
