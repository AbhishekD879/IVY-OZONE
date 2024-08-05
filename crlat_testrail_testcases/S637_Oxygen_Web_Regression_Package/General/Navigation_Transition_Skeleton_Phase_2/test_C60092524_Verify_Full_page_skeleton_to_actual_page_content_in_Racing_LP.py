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
class Test_C60092524_Verify_Full_page_skeleton_to_actual_page_content_in_Racing_LP(Common):
    """
    TR_ID: C60092524
    NAME: Verify Full page skeleton to actual page content in Racing LP.
    DESCRIPTION: For Racing landing pages Data should load at single cycle.All the data should be loaded as Full skeleton to actual page content.
    DESCRIPTION: Story : https://jira.egalacoral.com/browse/BMA-51663.
    DESCRIPTION: - Horse racing & Greyhound racing.
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_race_landing_page_horse_racing_and_greyhounds(self):
        """
        DESCRIPTION: Navigate to any <Race> landing page (Horse Racing and greyhounds)
        EXPECTED: - Content is not yet available
        EXPECTED: - No spinner is displayed on the page
        EXPECTED: - User sees full generic page loading skeleton
        EXPECTED: Eg.
        EXPECTED: ![](index.php?/attachments/get/122292718)
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

    def test_003_check_the_skeleton_animation_while_page_skeleton_is_displayed_to_the_user(self):
        """
        DESCRIPTION: Check the skeleton animation while page skeleton is displayed to the user
        EXPECTED: User sees shimmering animation when viewing loading skeletons
        """
        pass

    def test_004_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content.
        EXPECTED: Note : The transition is seen from full skeleton to actual page content where all the data in the page loads at once.
        """
        pass

    def test_005_check_the_content_of_the_page_after_skeleton_disappears(self):
        """
        DESCRIPTION: Check the content of the page after skeleton disappears
        EXPECTED: - All content is available and displayed
        EXPECTED: - No additional spinners are displayed on the page
        """
        pass
