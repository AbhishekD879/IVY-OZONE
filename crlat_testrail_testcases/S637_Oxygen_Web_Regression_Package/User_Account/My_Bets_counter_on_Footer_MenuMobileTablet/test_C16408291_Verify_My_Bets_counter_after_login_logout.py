import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C16408291_Verify_My_Bets_counter_after_login_logout(Common):
    """
    TR_ID: C16408291
    NAME: Verify My Bets counter after login/logout
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after login/logout
    DESCRIPTION: AUTOTEST [C29431476]
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure to have at least 2 users with different number of open bets and one user with no bets placed
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - To verify correct number of my bets check response of 'count?' XHR request
    PRECONDITIONS: ( e.g.https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountHistory/count?fromDate=2018-09-25%2015%3A28%3A08&toDate=2019-09-26%2000%3A00%3A00&group=BET&pagingBlockSize=20&settled=N)
    """
    keep_browser_open = True

    def test_001_login_with_user_who_has_placed_bets(self):
        """
        DESCRIPTION: Login with user who has placed bets
        EXPECTED: User is successfully logged in
        """
        pass

    def test_002_verify_my_bets_counter_on_footer_menu(self):
        """
        DESCRIPTION: Verify My bets counter on Footer menu
        EXPECTED: My bets counter is displaying a number of open bets available for user
        """
        pass

    def test_003_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My bets counter is not displayed anymore
        """
        pass

    def test_004_repeat_step__1_2_for_another_user(self):
        """
        DESCRIPTION: Repeat step # 1-2 for another user
        EXPECTED: My bets counter is showing corresponding number of bets
        """
        pass

    def test_005_valid_for_coral_only_expire_user_session_and_check_my_bets_counter_on_footer_menuladbrokescoral_log_out(self):
        """
        DESCRIPTION: [Valid for Coral only] expire user session and check My bets counter on Footer menu
        DESCRIPTION: [Ladbrokes/Coral] Log out
        EXPECTED: User is logged out
        EXPECTED: My bets counter is not displayed anymore
        """
        pass

    def test_006__log_in_with_user_who_has_no_open_bets_verify_my_bets_counter_on_footer_menu(self):
        """
        DESCRIPTION: * Log in with user who has no open bets
        DESCRIPTION: * Verify My bets counter on Footer menu
        EXPECTED: * My bets counter icon is not displayed
        EXPECTED: * '0' is NOT displayed on My Bets counter icon
        """
        pass
