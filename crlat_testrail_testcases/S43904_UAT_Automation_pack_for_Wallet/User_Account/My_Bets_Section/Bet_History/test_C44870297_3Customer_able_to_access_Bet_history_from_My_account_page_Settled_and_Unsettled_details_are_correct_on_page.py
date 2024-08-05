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
class Test_C44870297_3Customer_able_to_access_Bet_history_from_My_account_page_Settled_and_Unsettled_details_are_correct_on_page(Common):
    """
    TR_ID: C44870297
    NAME: "3.Customer able to access Bet history from My account page Settled and Unsettled details are correct on page"
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in.
    PRECONDITIONS: Uses must have placed bets (single, double, each way and accumulator)
    """
    keep_browser_open = True

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch test App/Site
        EXPECTED: User successfully Launches test App/Site
        """
        pass

    def test_002_user_shall_login_with__valid_credentials(self):
        """
        DESCRIPTION: User shall Login with  valid credentials
        EXPECTED: User successfully logs in with valid credentials
        """
        pass

    def test_003_verify_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: Cashout/Open bets/Settled bets/Shop bets
        EXPECTED: All bet tabs must be displayed with the right details
        """
        pass

    def test_004_verify_bet_history_via_my_account_overlay___for_all_types_of_bets___single_multiple_ew_cashed_out_bets_hr_etc(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay - for all types of bets - single, multiple, E/W, cashed out bets, HR etc
        EXPECTED: User must be able to open Bet History via My Account
        EXPECTED: All bets must be displayed with the right details
        EXPECTED: for all types of bets
        EXPECTED: - single, multiple, E/W, cashed out bets, HR etc
        """
        pass

    def test_005_verify_bet_history_via_my_account_overlay___for_all_types_of_bets___settled(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay - for all types of bets - settled
        EXPECTED: All bets must be displayed with the right details
        """
        pass

    def test_006_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days_from_bet_history_via_my_account_overlay(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days from Bet History via My Account overlay
        EXPECTED: Date Picker Today, Last 7 days and Last 30 days must be functional and working as per design implementation
        """
        pass
