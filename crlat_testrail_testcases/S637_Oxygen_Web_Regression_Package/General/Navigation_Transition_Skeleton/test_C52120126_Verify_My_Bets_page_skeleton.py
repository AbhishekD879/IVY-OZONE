import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C52120126_Verify_My_Bets_page_skeleton(Common):
    """
    TR_ID: C52120126
    NAME: Verify My Bets page skeleton
    DESCRIPTION: This test case verifies the loading skeleton (instead of spinners) for My Bets pages.
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Designs Ladbrokes: https://app.zeplin.io/project/5bbf1a517265930a0786d254/dashboard
    DESCRIPTION: Designs Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - User is logged in and has few bets placed already.
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_page_open_bets(self):
        """
        DESCRIPTION: Navigate to 'My Bets' page (Open Bets)
        EXPECTED: - Open Bets is displayed by default with loading skeleton below the 'Open Bets' -> 'Sports' tabs
        EXPECTED: ![](index.php?/attachments/get/74407603)
        """
        pass

    def test_002_check_the_skeleton_appearance(self):
        """
        DESCRIPTION: Check the skeleton appearance
        EXPECTED: - Skeleton does not jump up and down and appears smoothly
        EXPECTED: - There is no extra space/area below/beneath the skeleton
        EXPECTED: - No additional spinners are displayed on the page
        """
        pass

    def test_003_check_the_skeleton_animation(self):
        """
        DESCRIPTION: Check the skeleton animation
        EXPECTED: User sees shimmering animation while viewing half loading skeleton (file attached)
        """
        pass

    def test_004_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: - There is a smooth transition from the skeleton to page content
        EXPECTED: - All content is available and displayed
        """
        pass

    def test_005_switch_between_tabs_and_sub_tabs_in_my_bets_section(self):
        """
        DESCRIPTION: Switch between tabs and sub tabs in 'My Bets' section
        EXPECTED: - Same skeleton is displayed with animation and smooth transition to page content when it becomes available
        """
        pass

    def test_006_select_dates_in_a_date_picker_settle_bets_tab_and_trigger_bets_search(self):
        """
        DESCRIPTION: Select dates in a date picker (Settle Bets tab) and trigger bets search
        EXPECTED: - Same skeleton is displayed with animation and smooth transition to page content when it becomes available
        """
        pass
