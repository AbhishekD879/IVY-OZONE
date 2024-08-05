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
class Test_C45122599_Verify_Skeleton_on_Tablet(Common):
    """
    TR_ID: C45122599
    NAME: Verify Skeleton on Tablet
    DESCRIPTION: This test case verifies loading skeleton on Tablet.
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Story related: https://jira.egalacoral.com/browse/BMA-49851
    DESCRIPTION: Designs Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5dfcbcee94044a995f85211b
    DESCRIPTION: Designs Coral:
    DESCRIPTION: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    PRECONDITIONS: -Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: - The home page content is not yet available
        EXPECTED: - No spinner is displayed
        EXPECTED: - User sees skeletons only on the main content (and not over the betslip widget)
        """
        pass

    def test_002_navigate_to_some_other_pages_in_the_app_and_return_back_to_home_page(self):
        """
        DESCRIPTION: Navigate to some other pages in the app and return back to home page
        EXPECTED: - The home page content is not yet available
        EXPECTED: - No spinner is displayed
        EXPECTED: - User sees skeletons only on the left-hand column (and not over the betslip)
        """
        pass

    def test_003_check_the_skeleton_appearance(self):
        """
        DESCRIPTION: Check the skeleton appearance
        EXPECTED: - Skeleton appears for few seconds (till content becomes available)
        EXPECTED: - Skeleton does not jump up and down and appears smoothly
        EXPECTED: - There is no extra space/area below/beneath the skeleton
        """
        pass

    def test_004_check_the_skeleton_animation_while_page_skeleton_is_displayed_to_the_user(self):
        """
        DESCRIPTION: Check the skeleton animation while page skeleton is displayed to the user
        EXPECTED: User sees shimmering animation when viewing loading skeletons. Please see details in attachment
        """
        pass

    def test_005_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        """
        pass

    def test_006_repeat_steps_2_and_3(self):
        """
        DESCRIPTION: Repeat steps 2 and 3
        EXPECTED: - User sees shimmering animation when viewing loading skeletons
        EXPECTED: - When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        """
        pass
