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
class Test_C60092523_Verify_Full_page_skeleton_to_actual_page_content_in_SLP(Common):
    """
    TR_ID: C60092523
    NAME: Verify Full page skeleton to actual page content in SLP.
    DESCRIPTION: For Sport landing pages Data should load at single cycle.All the data should be loaded as Full skeleton to actual page content.
    DESCRIPTION: Story : https://jira.egalacoral.com/browse/BMA-51663.
    DESCRIPTION: For the below Sports.
    DESCRIPTION: Football
    DESCRIPTION: Tennis
    DESCRIPTION: Darts
    DESCRIPTION: Basketball
    DESCRIPTION: Golf
    DESCRIPTION: Cricket
    DESCRIPTION: Snooker
    DESCRIPTION: Table Tennis
    DESCRIPTION: Rugby League
    DESCRIPTION: Rugby Union
    DESCRIPTION: Boxing
    DESCRIPTION: Ice Hockey
    DESCRIPTION: Am Football
    DESCRIPTION: Badminton
    DESCRIPTION: Baseball
    DESCRIPTION: Esports
    DESCRIPTION: Handball
    DESCRIPTION: Volleyball
    DESCRIPTION: Formula 1
    DESCRIPTION: UFC/MMA
    DESCRIPTION: Cycling
    DESCRIPTION: Motor Bikes
    DESCRIPTION: Motor Sports
    DESCRIPTION: Music
    DESCRIPTION: Olympics
    DESCRIPTION: Pool
    DESCRIPTION: TV Specials
    DESCRIPTION: Movies
    DESCRIPTION: Aussie Rules
    DESCRIPTION: GAA
    DESCRIPTION: Netball
    DESCRIPTION: Politics
    DESCRIPTION: Speedway
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sport_landing_page_list_of_sports_from_preconditions(self):
        """
        DESCRIPTION: Navigate to any <sport> landing page (list of sports from preconditions)
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
