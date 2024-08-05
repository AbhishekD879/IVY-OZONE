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
class Test_C26711659_Header_bar_design_verification(Common):
    """
    TR_ID: C26711659
    NAME: Header bar design verification
    DESCRIPTION: Verify UI matches mock-ups
    PRECONDITIONS: Some user with balance without freebets exist in system
    PRECONDITIONS: Some user with free bets exist in system
    PRECONDITIONS: App isntalled user not logged in
    """
    keep_browser_open = True

    def test_001_launch_app(self):
        """
        DESCRIPTION: Launch app
        EXPECTED: Login button shown on header bar
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/795027)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/795026)
        """
        pass

    def test_002_navigate_to_some_sport_then_select_some_event(self):
        """
        DESCRIPTION: Navigate to some sport then select some event
        EXPECTED: Beck button appears. Header changed according to sports name
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/795030)
        EXPECTED: ![](index.php?/attachments/get/795031)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/795028)
        EXPECTED: ![](index.php?/attachments/get/795029)
        """
        pass

    def test_003_go_back_to_home_page_and_login_with_user_that_have_balance(self):
        """
        DESCRIPTION: Go back to home page and login with user that have balance
        EXPECTED: User balance is shown
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/795034)
        EXPECTED: ![](index.php?/attachments/get/795035)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/795032)
        EXPECTED: ![](index.php?/attachments/get/795033)
        """
        pass

    def test_004_log_out_and_login_with_user_that_have_freebets(self):
        """
        DESCRIPTION: Log out and login with user that have freebets
        EXPECTED: User balance is shown with freebets
        EXPECTED: ![](index.php?/attachments/get/795036)
        EXPECTED: ![](index.php?/attachments/get/795037)
        """
        pass
