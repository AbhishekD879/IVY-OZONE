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
class Test_C44870181_Verifies_back_button_functionality_navigating_between_tabs_on_Racecard_HR_Sports_landing_page_(Common):
    """
    TR_ID: C44870181
    NAME: "Verifies back button functionality navigating between tabs on Racecard ,HR ,Sports landing page "
    DESCRIPTION: 
    PRECONDITIONS: BETA Application is loaded
    PRECONDITIONS: User is on Home page
    """
    keep_browser_open = True

    def test_001_tap_on_horse_racing_from_sports_ribbon_on_mobile__tablet(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' from Sports ribbon on mobile / Tablet
        EXPECTED: Horse Racing Landing page is loaded with Meeting tab opened by default
        """
        pass

    def test_002_tap_on__back_button_on_the_header(self):
        """
        DESCRIPTION: tap on '< Back' button on the header
        EXPECTED: User is navigated back to the Home Page
        """
        pass

    def test_003_tap_on_horse_racing_from_header_menu_on_desktop(self):
        """
        DESCRIPTION: Tap on 'HORSE RACING' from header menu on Desktop
        EXPECTED: Horse Racing Landing page is loaded with Meeting tab opened by default
        """
        pass

    def test_004_click_on____chvron_on_the_sub_header(self):
        """
        DESCRIPTION: click on ' < ' chvron on the sub header
        EXPECTED: User is navigated back to the Home Page
        """
        pass

    def test_005_repeat_steps_1_4_for_other_racing_events(self):
        """
        DESCRIPTION: Repeat steps 1-4 for other Racing events
        EXPECTED: 
        """
        pass

    def test_006_tap_on_football_from_sports_ribbon_on_mobile__tablet(self):
        """
        DESCRIPTION: Tap on Football from Sports ribbon on mobile / Tablet
        EXPECTED: Football sports Landing page is loaded with Matches tab expanded by default
        """
        pass

    def test_007_click_on__back_button_on_the_header(self):
        """
        DESCRIPTION: Click on '< Back' button on the header
        EXPECTED: User is navigated back to the Home Page
        """
        pass

    def test_008_tap_on_football_from_header_menu_on_desktop(self):
        """
        DESCRIPTION: Tap on 'FOOTBALL' from header menu on Desktop
        EXPECTED: Football Sports Landing Page is loaded with Matches tab opened by default
        """
        pass

    def test_009_click_on____chvron_on_the_sub_header(self):
        """
        DESCRIPTION: click on ' < ' chvron on the sub header
        EXPECTED: User is navigated back to the Home Page
        """
        pass
