import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C66017363_Verify_virtual_sport_entry_point_from_sport_page(Common):
    """
    TR_ID: C66017363
    NAME: Verify virtual sport entry point from sport page.
    DESCRIPTION: Virtual sport entry banners should be displayed in sport landing pages.
    PRECONDITIONS: Virtual sport entry banners should be configured for sports in CMS.
    PRECONDITIONS: i.e. CMS&gt;Sports&gt;Football&gt; Matches tab&gt; under virtual sport entry point section
    PRECONDITIONS: enable 'Banner enabled' check box
    PRECONDITIONS: enter data under below fields
    PRECONDITIONS: Desktop Banner Id
    PRECONDITIONS: Mobile Banner Id
    PRECONDITIONS: CTA Button Label
    PRECONDITIONS: Redirection URL
    PRECONDITIONS: Banner Position
    PRECONDITIONS: Similarly configure data under competition tab.
    PRECONDITIONS: Configure data for other sports as well like Tennis, Basketball etc.
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_navigate_to_football_sport_page(self):
        """
        DESCRIPTION: Launch the application and navigate to football sport page
        EXPECTED: Navigation should be successful and data should be loaded under matches tab. By default user will be under today sub tab
        """
        pass

    def test_000_verify_the_presence_of_virtual_football_sport_entry_banner(self):
        """
        DESCRIPTION: Verify the presence of virtual football sport entry banner
        EXPECTED: Virtual sport entry banner should be displayed. Position of the banner should match with the configured value in CMS.
        EXPECTED: Ex- If position set as 5 in CMS, then after 5 competitions banner should be displayed.
        """
        pass

    def test_000_navigate_to_tomorrow_sub_tab_and_validate_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Tomorrow sub tab and validate the presence of virtual sport banner
        EXPECTED: Virtual sport entry banner should be displayed. Position of the banner should match with the configured value in CMS.
        """
        pass

    def test_000_navigate_to_future_sub_tab_and_validate_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Future sub tab and validate the presence of virtual sport banner
        EXPECTED: Virtual sport entry banner should be displayed. Position of the banner should match with the configured value in CMS.
        """
        pass

    def test_000_navigate_to_competition_tab_and_validate_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Competition tab and validate the presence of virtual sport banner
        EXPECTED: Virtual sport entry banner should be displayed. Position of the banner should match with the configured value in CMS.
        """
        pass

    def test_000_click_on_virtual_sport_banner_and_validate_the_navigation(self):
        """
        DESCRIPTION: Click on virtual sport banner and validate the navigation
        EXPECTED: Should navigate to configured url in CMS i.e. virtual football sport.
        """
        pass

    def test_000_similarly_repeat_the_above_steps_for_other_sports_like_tennis_basketball_and_horse_racing_etc(self):
        """
        DESCRIPTION: Similarly repeat the above steps for other sports like tennis, basketball and horse racing etc.
        EXPECTED: Result should be same as mentioned above
        """
        pass
