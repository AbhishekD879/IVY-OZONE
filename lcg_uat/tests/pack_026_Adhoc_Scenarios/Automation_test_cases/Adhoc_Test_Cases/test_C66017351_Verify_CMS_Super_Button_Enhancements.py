import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66017351_Verify_CMS_Super_Button_Enhancements(Common):
    """
    TR_ID: C66017351
    NAME: Verify CMS Super Button Enhancements
    DESCRIPTION: Verify CMS Super Button Enhancements
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: CMS Link--https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: user : ozoneqa@coral.co.uk   Password:Admin
    PRECONDITIONS: 2) Configuration for Super button below
    PRECONDITIONS: i) CMS->Sports pages->Super buttons ->Click on '+ Create Super Button'  will open new page
    PRECONDITIONS: below fields need to be updated-
    PRECONDITIONS: -Enable Active Checkbox
    PRECONDITIONS: -CTA Alignment like Center or Right alignment
    PRECONDITIONS: -Center Aligned CTA Title
    PRECONDITIONS: -Center Aligned Description
    PRECONDITIONS: -Destination URL Ex: https://sports.coral.co.uk/sport/basketball
    PRECONDITIONS: -Show on Home Tabs Ex: Featured, next races
    PRECONDITIONS: -Show on Sports Ex: Football
    PRECONDITIONS: -Show on Big Competitions Ex: Premier League
    PRECONDITIONS: -Select validity start and end date
    PRECONDITIONS: -Themes Like Theme1, Theme2 etc
    PRECONDITIONS: -Select radiobutton either Segment or Universal
    PRECONDITIONS: -Save Changes
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_navigate_to_home_pagehighlightsfeatured(self):
        """
        DESCRIPTION: Launch the application and navigate to Home page(Highlights/Featured)
        EXPECTED: Application should be launched successfully And home page should be loaded
        """
        pass

    def test_000_verify_display_super_button_on_home_page(self):
        """
        DESCRIPTION: Verify display Super button on home page
        EXPECTED: Super button should be displayed.
        EXPECTED: Theme and alignment should be displayed as per CMS configuration
        EXPECTED: Super button content like title, description should be displayed.
        """
        pass

    def test_000_verify_super_button_title_and_description_are_clickable(self):
        """
        DESCRIPTION: Verify Super button title and description are clickable
        EXPECTED: Super button title should be clickable and navigated to respective destination URL as per CMS configuration.
        EXPECTED: Super button description should not be clickable and navigated to respective destination URL
        """
        pass

    def test_000_verify_super_button_display_in_respective_sportstabs_and_big_competition(self):
        """
        DESCRIPTION: Verify super button display in respective sports/Tabs and Big competition
        EXPECTED: Super button should be displayed to respective Sport page and big competition as per CMS configuration
        """
        pass

    def test_000_verify_super_button_is_not_displayed_if_its_deactivated_in_the_cms(self):
        """
        DESCRIPTION: Verify Super Button is not displayed if it's deactivated in the CMS
        EXPECTED: Super button should not be displayed in front end.
        """
        pass

    def test_000_verify_super_button_display_for_segmented_and_rgy_user(self):
        """
        DESCRIPTION: Verify Super button display for Segmented and RGY user
        EXPECTED: Super button should be displayed for RGY (If not restricted) and segmented user
        """
        pass

    def test_000_repeat_above_steps_1_6_in_login_state(self):
        """
        DESCRIPTION: Repeat above steps 1-6 in Login state.
        EXPECTED: The results should be as above.
        """
        pass
