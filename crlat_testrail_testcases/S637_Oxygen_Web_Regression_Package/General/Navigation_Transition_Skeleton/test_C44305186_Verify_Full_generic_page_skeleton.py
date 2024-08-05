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
class Test_C44305186_Verify_Full_generic_page_skeleton(Common):
    """
    TR_ID: C44305186
    NAME: Verify Full generic page skeleton
    DESCRIPTION: This test case verifies the full generic page loading skeleton across application while page loads so that user gets feedback that something is happening when opening a page.
    DESCRIPTION: !!! Note: the 'generic full' skeleton is a skeleton which applies for other pages across the application, like:
    DESCRIPTION: * Landing pages (no content for top section + selected tab)
    DESCRIPTION: * EDPs ( no content for top section + selected tab)
    DESCRIPTION: * Promotions pages
    DESCRIPTION: * Virtuals  ( no content for top section + selected tab)
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Story related: https://jira.egalacoral.com/browse/BMA-49860
    DESCRIPTION: Designs Ladbrokes:https://app.zeplin.io/project/5bbf1a517265930a0786d254/dashboard
    DESCRIPTION: Designs Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sport_landing_page_or_any_other_from_the_list_in_preconditions(self):
        """
        DESCRIPTION: Navigate to any <sport> landing page (or any other from the list in preconditions)
        EXPECTED: - Content is not yet available
        EXPECTED: - No spinner is displayed on the page
        EXPECTED: - User sees full generic page loading skeleton
        EXPECTED: Eg.
        EXPECTED: ![](index.php?/attachments/get/53576229)
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
        EXPECTED: (refer to attachment)
        """
        pass

    def test_004_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        """
        pass

    def test_005_check_the_content_of_the_page_after_skeleton_disappears(self):
        """
        DESCRIPTION: Check the content of the page after skeleton disappears
        EXPECTED: - All content is available and displayed
        EXPECTED: - No additional spinners are displayed on the page (including content inside the automatically expanded accordions)
        """
        pass
