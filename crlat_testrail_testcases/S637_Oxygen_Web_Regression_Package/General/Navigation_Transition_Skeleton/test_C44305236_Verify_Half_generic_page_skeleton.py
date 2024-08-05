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
class Test_C44305236_Verify_Half_generic_page_skeleton(Common):
    """
    TR_ID: C44305236
    NAME: Verify Half generic page skeleton
    DESCRIPTION: This test case verifies the half page loading skeleton when page content is available for top banners, but content for the tabs underneath is not ready (eg. sport landing page).
    DESCRIPTION: !!! Note: the 'generic half page' skeleton is a skeleton which applies for other pages across the application, like:
    DESCRIPTION: * EDPs
    DESCRIPTION: * In play pages
    DESCRIPTION: * My Bets (+ tabs)
    DESCRIPTION: * Betslip opening
    DESCRIPTION: * Loading Bet Receipt
    DESCRIPTION: * Editing ‘My ACCA’ and saving changes
    DESCRIPTION: * Landing pages sub tabs
    DESCRIPTION: * Logging out (i.e redirect to home page after user is logged out)
    DESCRIPTION: * Virtuals
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Story related: https://jira.egalacoral.com/browse/BMA-49852
    DESCRIPTION: Designs Ladbrokes: https://app.zeplin.io/project/5bbf1a517265930a0786d254/dashboard
    DESCRIPTION: Designs Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sport_landing_page_or_any_other_from_the_list_from_preconditions(self):
        """
        DESCRIPTION: Navigate to any <sport> landing page (or any other from the list from preconditions)
        EXPECTED: - No spinners are displayed
        EXPECTED: - The content is available just for the top half of the page
        EXPECTED: - Generic half page loading skeleton is shown for the bottom half of the page (under the tabs on landing page or under the banner)
        EXPECTED: Lad: https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5e07e5b8114ed41d02bbbb22
        EXPECTED: Coral:https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e061c8e55374899d0ea243f
        """
        pass

    def test_002_check_the_skeleton_appearance(self):
        """
        DESCRIPTION: Check the skeleton appearance
        EXPECTED: - Skeleton appears for few seconds (till content becomes available)
        EXPECTED: - Skeleton does not jump up and down and appears smoothly
        EXPECTED: - There is no extra space/area below/beneath the skeleton
        """
        pass

    def test_003_check_the_skeleton_animation(self):
        """
        DESCRIPTION: Check the skeleton animation
        EXPECTED: User sees shimmering animation while viewing half loading skeleton
        """
        pass

    def test_004_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available for the bottom half of the page user sees a smooth transition from the loading skeleton to the full page
        """
        pass

    def test_005_check_the_content_of_the_page_after_skeleton_disappears(self):
        """
        DESCRIPTION: Check the content of the page after skeleton disappears
        EXPECTED: - All content is available and displayed
        EXPECTED: - No additional spinners are displayed on the page (including content inside the automatically expanded accordions)
        """
        pass

    def test_006_repeat_the_above_steps_for_different_tabs_on_sport_landing_page(self):
        """
        DESCRIPTION: Repeat the above steps for different tabs on <sport> landing page
        EXPECTED: 
        """
        pass
