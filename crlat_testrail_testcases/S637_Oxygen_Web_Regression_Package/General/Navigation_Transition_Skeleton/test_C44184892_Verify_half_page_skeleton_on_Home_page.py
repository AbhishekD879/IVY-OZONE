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
class Test_C44184892_Verify_half_page_skeleton_on_Home_page(Common):
    """
    TR_ID: C44184892
    NAME: Verify half page skeleton on Home page
    DESCRIPTION: This test case verifies the half page loading skeleton (instead of spinners) on Home Page when page content is available for top banners, but content for the tabs underneath is not yet ready.
    DESCRIPTION: Note: the following skeleton applies to Home page only (as there are separate skeletons for other pages across application)
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Story related: https://jira.egalacoral.com/browse/BMA-49852
    DESCRIPTION: Designs Ladbrokes: https://app.zeplin.io/project/5bbf1a517265930a0786d254/dashboard
    DESCRIPTION: Designs Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - The content is available only for the top half of the page
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: - No spinners are displayed
        EXPECTED: - The content is available for the top half of the page
        EXPECTED: - Generic half page loading skeleton is shown (under the tabs on home page)
        EXPECTED: ![](index.php?/attachments/get/53576224)
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

    def test_006_repeat_the_above_steps_for_different_tabs_on_the_home_page_in_playnext_racesaccasetc(self):
        """
        DESCRIPTION: Repeat the above steps for different tabs on the Home page (in-play/next races/ACCAs/etc.)
        EXPECTED: When the content is not available for the bottom part of the Home page, user sees half page loading skeleton until the whole content fully loads
        """
        pass
