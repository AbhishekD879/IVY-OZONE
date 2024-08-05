import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C2988342_Verify_successful_depositing_through_Account_One_portal(Common):
    """
    TR_ID: C2988342
    NAME: Verify successful depositing through 'Account One' portal
    DESCRIPTION: This test case verifies updating user balance in an app after successful depositing from 'Account One' portal
    PRECONDITIONS: 1. In CMS > System Configuration > Structure: 'Account One' section with 'Field Name' = 'deposit' & 'Field Value' = [account one url e.g. http://accountone-test.ladbrokes.com/deposit] is available
    PRECONDITIONS: 2. Roxanne app is loaded
    PRECONDITIONS: 3. User is logged into an app
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Test Accounts for Payment methods: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: - Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/deposit?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_mobiletablettap_on_the_right_menu__banking__deposit_menu_itemdesktopclick_on_my_account__banking__deposit_menu_item(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap on the 'Right Menu' > 'Banking' > 'Deposit' menu item
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click on 'My Account' > 'Banking' > 'Deposit' menu item
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: User is redirected to 'Account One' portal > 'Deposit' page
        EXPECTED: **Desktop**
        EXPECTED: 'Account One' portal > 'Deposit' page is opened in a separate pop up over the browser tab with 'Roxanne' site
        """
        pass

    def test_002_in_account_one_add_any_payment_method_eg_netellerpaypalcredit_cards_etc(self):
        """
        DESCRIPTION: In 'Account One': Add any Payment Method e.g. Neteller/Paypal/Credit Cards etc
        EXPECTED: Payment method is added
        """
        pass

    def test_003_in_account_one_deposit_any_amount_through_an_added_payment_method(self):
        """
        DESCRIPTION: In 'Account One': Deposit any amount through an added Payment Method
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: - Deposit has been successful
        EXPECTED: - "Your deposit of X was successful"(where X is an amount that was deposited by the User) message is displayed
        EXPECTED: - "This page will be closed after Y seconds"(where Y is a countdown that starts from 3) message is displayed
        EXPECTED: **Desktop:**
        EXPECTED: - Deposit has been successful
        EXPECTED: - Money has been added to user's balance in 'Account One'
        """
        pass

    def test_004_desktopclose_the_deposit_account_one_portal_pop_up_by_clicking_on_x_icon_within_the_pop_up(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Close the 'Deposit' ('Account One' portal) pop up by clicking on 'X' icon within the pop up
        EXPECTED: **Desktop:**
        EXPECTED: - User is redirected back to an
        EXPECTED: - The app is refreshed & splash screen is displayed
        EXPECTED: - User is landed on the page from which he was redirected
        EXPECTED: - Balance has been updated with deposited amount in step #3
        """
        pass

    def test_005_repeat_steps_134(self):
        """
        DESCRIPTION: Repeat steps #1,3,4
        EXPECTED: 
        """
        pass
