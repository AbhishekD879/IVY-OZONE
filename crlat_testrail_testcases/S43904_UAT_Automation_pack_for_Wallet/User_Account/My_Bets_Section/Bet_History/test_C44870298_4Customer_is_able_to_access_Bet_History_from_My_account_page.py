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
class Test_C44870298_4Customer_is_able_to_access_Bet_History_from_My_account_page(Common):
    """
    TR_ID: C44870298
    NAME: 4.Customer is able to access Bet History from 'My account' page
    DESCRIPTION: Verify that games and lotto history displays on the front end when a user has played that relevant game
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Must place the bets
    """
    keep_browser_open = True

    def test_001_login_to_websiteapp(self):
        """
        DESCRIPTION: Login to website/App
        EXPECTED: User logged in
        """
        pass

    def test_002_place_abet_on_each_on_any_sportlottopools(self):
        """
        DESCRIPTION: Place abet on each on any sport/lotto/pools
        EXPECTED: User has placed a bet on sport/lotto/pools
        """
        pass

    def test_003_navigate_to_settled_bets_page_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Navigate to Settled bets page via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: User navigated to Settled bets where the user can see all sports/lotto/pools bets
        """
        pass

    def test_004_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days
        EXPECTED: User can see correct history for all the relevant bets placed
        """
        pass
