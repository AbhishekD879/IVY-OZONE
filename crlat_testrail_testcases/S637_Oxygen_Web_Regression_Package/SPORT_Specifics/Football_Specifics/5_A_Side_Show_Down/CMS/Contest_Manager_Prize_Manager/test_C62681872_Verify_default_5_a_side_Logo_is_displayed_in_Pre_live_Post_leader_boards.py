import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62681872_Verify_default_5_a_side_Logo_is_displayed_in_Pre_live_Post_leader_boards(Common):
    """
    TR_ID: C62681872
    NAME: Verify default 5-a-side Logo is displayed in Pre/live/Post leader boards.
    DESCRIPTION: This test cases verifies default 5-a-side Logo is displayed in Pre/live/Post leader boards.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2)  user should not placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_login_to_cms_ladbrokes_application_with_admin_access(self):
        """
        DESCRIPTION: Login to CMS Ladbrokes application with admin access
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_image_manager_and_add_5_a_side_logo_image(self):
        """
        DESCRIPTION: Navigate to Image manager and add 5-a-side logo image
        EXPECTED: user should able to navigate to image manager and able to upload 5-a-side logo
        EXPECTED: ![](index.php?/attachments/get/171308945)
        """
        pass

    def test_003_validate_5_a_side_logo_for_the_active_contest_in_fe(self):
        """
        DESCRIPTION: Validate 5-a-side logo for the active contest in FE
        EXPECTED: Uploaded 5-a-side image should display in
        EXPECTED: 1.Pre-leaderboard
        EXPECTED: ![](index.php?/attachments/get/171308980)
        EXPECTED: 2.Live Leaderboard
        EXPECTED: ![](index.php?/attachments/get/171308983)
        EXPECTED: 3.Post leaderboard
        EXPECTED: ![](index.php?/attachments/get/171308984)
        """
        pass
