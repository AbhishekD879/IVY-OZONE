import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2553354_Verify_setting_Marketing_preferences_for_Upgraded_user(Common):
    """
    TR_ID: C2553354
    NAME: Verify setting Marketing preferences for Upgraded user
    DESCRIPTION: This test case verify setting Marketing preferences (after in-shop user successful upgrade) for new Multi Channel user
    PRECONDITIONS: 1. Load Sport Book
    PRECONDITIONS: 2. Log in with In-Shop user
    PRECONDITIONS: The way to open upgrade dialog:
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in as an in-shop user
    PRECONDITIONS: OR
    PRECONDITIONS: Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: Open MY ACCOUNT menu
    PRECONDITIONS: Select CONNECT
    PRECONDITIONS: Select UPGRADE
    PRECONDITIONS: OR
    PRECONDITIONS: Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: Select DEPOSIT from header / Open MY ACCOUNT and select DEPOSIT / Open MY ACCOUNT, select CASHIER and DEPOSIT / Open MY ACCOUNT, select CASHIER and WITHDRAW
    PRECONDITIONS: Device
    """
    keep_browser_open = True

    def test_001__fill_all_required_fields_on_page_1_and_2(self):
        """
        DESCRIPTION: * Fill all required fields on page 1 and 2
        EXPECTED: -
        """
        pass

    def test_002__select_all_contact_preferences_on_page_3_click_the_create_account_button(self):
        """
        DESCRIPTION: * Select all contact preferences on page 3
        DESCRIPTION: * Click the CREATE ACCOUNT button
        EXPECTED: -
        """
        pass

    def test_003_log_in_using_username_and_password(self):
        """
        DESCRIPTION: Log in using username and password
        EXPECTED: -
        """
        pass

    def test_004_go_to_my_account__settings__marketing_preferences(self):
        """
        DESCRIPTION: Go to My account > Settings > Marketing preferences
        EXPECTED: Preferences selected in step 2 are correctly reflected on Communication Preferences page
        """
        pass
