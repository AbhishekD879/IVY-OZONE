import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C871647_Verify_tabs_scrolling_on_Sports_Landing_page_for_Desktop(Common):
    """
    TR_ID: C871647
    NAME: Verify tabs scrolling on <Sports> Landing page for Desktop
    DESCRIPTION: This test case verifies tabs scrolling on <Sports> Landing page for Desktop
    PRECONDITIONS: Make sure data is available for all tabs
    PRECONDITIONS: The correct labels for "Matches" tab for every Sport are listed in the table below:
    PRECONDITIONS: |||:Sport|: Correct Label for "Matches" tab
    PRECONDITIONS: || American Football | Matches
    PRECONDITIONS: || Aussie Rules | Matches
    PRECONDITIONS: || Badminton | Matches
    PRECONDITIONS: || Baseball | Matches
    PRECONDITIONS: || Basketball | Matches
    PRECONDITIONS: || Bowls | Matches
    PRECONDITIONS: || Boxing | Fights
    PRECONDITIONS: || Cricket | Matches
    PRECONDITIONS: || Cycling | Events
    PRECONDITIONS: || Darts | Matches
    PRECONDITIONS: || Eurovision | Events
    PRECONDITIONS: || Football | Matches
    PRECONDITIONS: || Formula 1 | Events
    PRECONDITIONS: || Gaelic Football | Matches
    PRECONDITIONS: || Golf | Events
    PRECONDITIONS: || Handball | Matches
    PRECONDITIONS: || Hockey | Matches
    PRECONDITIONS: || Hurling | Matches
    PRECONDITIONS: || Ice Hockey | Matches
    PRECONDITIONS: || Motor Bikes | Events
    PRECONDITIONS: || Motor Sports | Events
    PRECONDITIONS: || Movies | Events
    PRECONDITIONS: || Politics | Events
    PRECONDITIONS: || Pool | Matches
    PRECONDITIONS: || Rugby League | Matches
    PRECONDITIONS: || Rugby Union | Matches
    PRECONDITIONS: || Snooker | Matches
    PRECONDITIONS: || Speedway | Events
    PRECONDITIONS: || Tennis | Matches
    PRECONDITIONS: || TV Specials | Events
    PRECONDITIONS: || UFC/MMA | Fights
    PRECONDITIONS: || Volleyball | Matches
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: Sports Landing Page is opened
        """
        pass

    def test_003_verify_tabs_displaying_on_sports_landing_page(self):
        """
        DESCRIPTION: Verify tabs displaying on Sports Landing page
        EXPECTED: The following tabs are displayed on Sports Landing page:
        EXPECTED: * 'In-Play'
        EXPECTED: * 'Matches' (the corresponding label for this tab is listed in the preconditions for every sport)
        EXPECTED: * 'Coupons'
        EXPECTED: * 'Outrights'
        """
        pass

    def test_004_scroll_tabs_to_the_right_and_left(self):
        """
        DESCRIPTION: Scroll tabs to the right and left
        EXPECTED: Navigation arrows appear for scrolling tabs by clicking on these arrows
        """
        pass

    def test_005_resize_page_to_1025px_for_example_and_scroll_tabs_to_the_right_and_left(self):
        """
        DESCRIPTION: Resize page to 1025px for example and scroll tabs to the right and left
        EXPECTED: Navigation arrows appear for scrolling tabs by clicking on these arrows
        """
        pass

    def test_006_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_007_verify_tabs_displaying_on_football_landing_page(self):
        """
        DESCRIPTION: Verify tabs displaying on Football Landing page
        EXPECTED: The following tabs are displayed on Football Landing page:
        EXPECTED: * 'In-Play'
        EXPECTED: * 'Matches'
        EXPECTED: * 'Competitions'
        EXPECTED: * 'Coupons'
        EXPECTED: * 'Outrights'
        EXPECTED: * 'Jackpot'
        EXPECTED: * 'Specials'
        EXPECTED: * 'Player Bets
        """
        pass

    def test_008_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps 4-5
        EXPECTED: Navigation arrows appear for scrolling tabs by clicking on these arrows
        """
        pass
