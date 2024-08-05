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
class Test_C44882517_Verify_Skeleton_on_pages_with_Banners(Common):
    """
    TR_ID: C44882517
    NAME: Verify Skeleton on pages with Banners
    DESCRIPTION: This test case verifies loading skeleton for pages with banners components so that user get feedback that something is happening when opening a page.
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Banners should be available for tested pages.
    PRECONDITIONS: Banners shown on :
    PRECONDITIONS: Home page
    PRECONDITIONS: Sport Landing pages
    PRECONDITIONS: Race Landing pages
    PRECONDITIONS: To create standard banner on AEM author instance:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+create+the+banner+in+AEM+standard+library
    PRECONDITIONS: To check correct {url}:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/AEM+Dev+environment+instances
    PRECONDITIONS: Credentials for AEM author instance:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/AEM+env+endpoints
    """
    keep_browser_open = True

    def test_001_launch_the_app_and_open_page_with_bannerstrigger_the_situation_when_banner_data_and_page_content_below_banner_are_not_available(self):
        """
        DESCRIPTION: Launch the app and open page with banners.
        DESCRIPTION: Trigger the situation when Banner data and page content below Banner are not available
        EXPECTED: User should be able to see a loading full skeleton page instead of missing content.
        EXPECTED: When all content became available (except banners) user will see the banner loading skeleton.
        EXPECTED: ![](index.php?/attachments/get/53285766)
        EXPECTED: ![](index.php?/attachments/get/53285765)
        """
        pass

    def test_002_check_the_skeleton_animation_while_page_skeleton_is_displayed_to_the_user(self):
        """
        DESCRIPTION: Check the skeleton animation while page skeleton is displayed to the user
        EXPECTED: User sees shimmering animation when viewing loading skeletons
        """
        pass

    def test_003_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        """
        pass

    def test_004_repeat_steps_1_3_with_other_pages_with_banners_list_of_the_pages_in_precondition(self):
        """
        DESCRIPTION: Repeat steps 1-3 with other pages with banners (list of the pages in precondition)
        EXPECTED: 
        """
        pass
