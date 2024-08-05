import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C48473989_Verify_page_Skeleton_display_when_content_of_the_page_loads(Common):
    """
    TR_ID: C48473989
    NAME: Verify page Skeleton display when content of the page loads
    DESCRIPTION: This test case verifies loading skeleton (instead of spinners) across the app when page content is in the process of loading.
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: Designs Ladbrokes: https://app.zeplin.io/project/5bbf1a517265930a0786d254/dashboard
    DESCRIPTION: Designs Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/dashboard
    DESCRIPTION: Skeleton animation: see attachment
    DESCRIPTION: Full generic skeleton areas include:
    DESCRIPTION: - Landing pages (no content for top section + selected tab)
    DESCRIPTION: - EDPs ( no content for top section + selected tab)
    DESCRIPTION: - Promotions pages
    DESCRIPTION: - Virtuals  ( no content for top section + selected tab)
    DESCRIPTION: Half generic skeleton areas include:
    DESCRIPTION: - EDPs
    DESCRIPTION: - In play pages
    DESCRIPTION: - My Bets (+ tabs)
    DESCRIPTION: - Betslip opening
    DESCRIPTION: - Loading Bet Receipt
    DESCRIPTION: - Editing ‘My ACCA’ and saving changes
    DESCRIPTION: - Landing pages sub tabs
    DESCRIPTION: - Logging out (i.e redirect to home page after user is logged out)
    DESCRIPTION: - Virtuals
    DESCRIPTION: Banners areas include :
    DESCRIPTION: - Home page
    DESCRIPTION: - Sport Landing pages
    DESCRIPTION: - Race Landing pages
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Use slow network connection to see skeleton for longer time.
    """
    keep_browser_open = True

    def test_001_launch_the_app_and_wait_till_splash_screen_disappears(self):
        """
        DESCRIPTION: Launch the app and wait till splash screen disappears
        EXPECTED: - User sees half home page skeleton underneath the home page tabs (instead of spinners) as the content still loads
        EXPECTED: - User sees shimmering animation while viewing half loading skeleton (see attachment)
        EXPECTED: Lad:https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5e07e5b8114ed41d02bbbb22
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e061c8e55374899d0ea243f
        """
        pass

    def test_002_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: - User sees a smooth transition from the loading skeleton to the full page
        EXPECTED: - No more additional spinners on the page (including content inside the automatically expanded accordions)
        """
        pass

    def test_003_navigate_through_the_tabs_on_the_home_page(self):
        """
        DESCRIPTION: Navigate through the tabs on the Home page
        EXPECTED: - Each time user switches between tabs the skeleton is displayed until all content becomes available
        """
        pass

    def test_004_navigate_to_any_sport_landing_page_or_any_other_from_the_full_page_skeleton_areas_in_precondition(self):
        """
        DESCRIPTION: Navigate to any sport landing page (or any other from the 'Full page skeleton areas' in precondition)
        EXPECTED: - Content is not yet available
        EXPECTED: - No spinner is displayed on the page
        EXPECTED: - User sees full generic page loading skeleton (for the whole page)
        EXPECTED: - User sees shimmering animation while viewing loading skeleton (see attachment)
        EXPECTED: - When the content becomes available the smooth transition takes place from the skeleton to page content
        EXPECTED: Lad:https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5df9084597449919cc69f633
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e061688e26f6c988bf024b5
        """
        pass

    def test_005_navigate_between_tabs_on_any_sport_landing_page_or_any_other_page_from_the_half_page_skeleton_areas_in_precondition(self):
        """
        DESCRIPTION: Navigate between tabs on any sport landing page (or any other page from the 'Half page skeleton areas' in precondition)
        EXPECTED: - No spinners are displayed
        EXPECTED: - The content is available just for the top half of the page
        EXPECTED: - User sees Generic half page loading skeleton for the bottom half of the page
        EXPECTED: - User sees shimmering animation while viewing loading skeleton (see attachment)
        EXPECTED: - When the content becomes available the smooth transition takes place from the skeleton to page content
        EXPECTED: Lad:https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5e07e5b8114ed41d02bbbb22
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e061c8e55374899d0ea243f
        """
        pass

    def test_006_not_yet_implemented_expand_any_accordion_on_the_sport_landing_page_or_any_other_page(self):
        """
        DESCRIPTION: (Not yet implemented) Expand any accordion on the sport landing page (or any other page)
        EXPECTED: - Content loads inside the accordion
        EXPECTED: - No spinner is displayed inside the accordion
        EXPECTED: - User sees mini loading skeleton (just inside the accordion area)
        EXPECTED: - When the content becomes available the smooth transition takes place from the skeleton to accordion content
        EXPECTED: Lad: https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5e1c832345d97eab1166cc3c
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e1c8d4af38ae1bf8e1d6337
        """
        pass

    def test_007_navigate_to_edp_page_with_scoreboards(self):
        """
        DESCRIPTION: Navigate to EDP page with Scoreboards
        EXPECTED: - User sees a loading full skeleton page instead of missing content.
        EXPECTED: - When all content became available (except Scoreboard)user sees the Scoreboard loading skeleton
        EXPECTED: - Shimmering animation takes place when viewing loading skeletons
        EXPECTED: - When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        EXPECTED: Lad: https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5e05d0daeaf0a497d3fe5af4
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e0213edbc188b183386a6f3
        """
        pass

    def test_008_navigate_to_page_with_banners(self):
        """
        DESCRIPTION: Navigate to page with Banners
        EXPECTED: - User sees a loading full skeleton page instead of missing content
        EXPECTED: - When all content became available (except banners)user will see the banner loading skeleton
        EXPECTED: - User sees shimmering animation when viewing loading skeletons
        EXPECTED: - When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        EXPECTED: Lad:https://app.zeplin.io/project/5bbf1a517265930a0786d254/screen/5dfcdb4008d4ea15f31942d3
        EXPECTED: Coral: https://app.zeplin.io/project/5d664fe012736e9b6c042c13/screen/5e02146a517a3eaf17d3983f
        """
        pass
