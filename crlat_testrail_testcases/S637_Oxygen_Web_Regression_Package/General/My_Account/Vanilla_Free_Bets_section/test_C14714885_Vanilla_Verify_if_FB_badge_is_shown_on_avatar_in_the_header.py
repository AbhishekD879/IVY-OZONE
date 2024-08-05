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
class Test_C14714885_Vanilla_Verify_if_FB_badge_is_shown_on_avatar_in_the_header(Common):
    """
    TR_ID: C14714885
    NAME: [Vanilla] Verify if 'FB'-badge is shown on avatar in the header
    DESCRIPTION: This test case verifies that users are able to see on the avatar in the header if there are any FreeBets available
    DESCRIPTION: Autotests:
    DESCRIPTION: [C28946286]
    DESCRIPTION: [C38555082]
    PRECONDITIONS: - User is logged in with only 1 FreeBet available
    PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 3088)
    PRECONDITIONS: - FreeBets menu item exists if available in CMS (Right Menu) no matter if FreeBets are available to user or not
    """
    keep_browser_open = True

    def test_001_open_main_page_and_verify_the_header(self):
        """
        DESCRIPTION: Open main page and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        pass

    def test_002_use_free_bet_available_for_the_user_and_verify_the_header(self):
        """
        DESCRIPTION: Use free bet available for the user and verify the header
        EXPECTED: 'FB'-badge is not shown anymore on avatar in the header
        """
        pass

    def test_003_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_004_login_to_the_account_with_multiple_more_than_two_freebets_available_and_verify_the_header(self):
        """
        DESCRIPTION: Login to the account with multiple (more than two) FreeBets available and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        pass

    def test_005_use_one_of_the_free_bet_and_verify_the_header(self):
        """
        DESCRIPTION: Use one of the free bet and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        pass
