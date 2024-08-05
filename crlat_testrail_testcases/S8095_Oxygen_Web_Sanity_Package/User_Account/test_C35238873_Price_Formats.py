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
class Test_C35238873_Price_Formats(Common):
    """
    TR_ID: C35238873
    NAME: Price Formats
    DESCRIPTION: This test case verifies price format across the application according to selected option Decimal or Fractional
    DESCRIPTION: AUTOMATED [C48912787]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_click_on_user_account_icon_on_header__settings__betting_setting(self):
        """
        DESCRIPTION: Click on [User account] icon on Header > Settings > Betting Setting
        EXPECTED: Preference page is opened.
        EXPECTED: ![](index.php?/attachments/get/13795457)
        """
        pass

    def test_003_select_decimal(self):
        """
        DESCRIPTION: Select "Decimal"
        EXPECTED: 
        """
        pass

    def test_004_navigate_through_the_application_and_make_sure_prices_are_displayed_according_to_selected_format(self):
        """
        DESCRIPTION: Navigate through the application and make sure prices are displayed according to selected format
        EXPECTED: Prices are displayed according to selected format on:
        EXPECTED: - Homepage
        EXPECTED: - Sports/Races Landing pages
        EXPECTED: - Sport/Races Details pages
        EXPECTED: - Betslip
        EXPECTED: - Cash Out
        EXPECTED: - Bet History
        EXPECTED: - Horse Race -> BetFilter-> Bet Filter Results
        EXPECTED: - etc
        """
        pass

    def test_005_repeat_step_2_and_select_fractional(self):
        """
        DESCRIPTION: Repeat step 2 and select "Fractional"
        EXPECTED: 
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: Results are the same
        """
        pass
