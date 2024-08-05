import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64597392_Verify_that_the_user_should_be_able_to_select_dates_for_various_months_and_years_using_the_calendar_provided_for_the_From_and_To_grids(Common):
    """
    TR_ID: C64597392
    NAME: Verify that the user should be able to select dates for various months and years  using the calendar provided for the From and To grids.
    DESCRIPTION: Verify that the user should be able to select dates for various months and years  using the calendar provided for the From and To grids.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Cashout tab.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_cashout_tabtabletdesktop_my_bets_section__gt_cashout_tab(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Cashout tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Cashout tab'.
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the Cashout tab.
        """
        pass

    def test_002_select_different_months_from_the_calendar_grids_provided(self):
        """
        DESCRIPTION: Select different months from the calendar grids provided.
        EXPECTED: User should be able to select various months in the From and To calendar grids.
        """
        pass

    def test_003_select_the_various_years_which_are_available_in_the_calendar_grids(self):
        """
        DESCRIPTION: Select the various years which are available in the calendar grids.
        EXPECTED: User should be able to select any year and respective dates in the From and To calendar grids.
        """
        pass

    def test_004_select_or_tap_any_date_in_the_from_and_to_calendar_grids(self):
        """
        DESCRIPTION: Select or tap any date in the From and To calendar grids.
        EXPECTED: When user selects or taps a date in the From or To calendar grid the calendar should close.
        """
        pass
