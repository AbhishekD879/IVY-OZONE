import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60004607_Verify_the_CSS_styles_for_Market_description(Common):
    """
    TR_ID: C60004607
    NAME: Verify the CSS styles for Market description
    DESCRIPTION: Verify the CSS styles for Market description displayed in EDP for both Horse Racing & Grey Hounds
    PRECONDITIONS: 1. Horse racing & Greyhound racing events & markets should be available.
    PRECONDITIONS: 2.Market Descriptions should be configured and enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_003_click_on_any_race_which_has_the_market_templates_available_for_which_description_are_added_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description are added in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_004_validate_css(self):
        """
        DESCRIPTION: Validate CSS
        EXPECTED: CSS styles should be as per Zeplin designs
        """
        pass

    def test_005_navigate_to_grey_hounds_and_repeat_3__4_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 3 & 4 Steps
        EXPECTED: CSS styles should be as per Zeplin designs
        """
        pass
