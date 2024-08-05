import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28436_to_update_Verify_tabs_order_on_the_Sport_Landing_Page(Common):
    """
    TR_ID: C28436
    NAME: (to update) Verify tabs order on the <Sport> Landing Page
    DESCRIPTION: (to update) What conditions need to be met for 'Jackpot''Specials' and 'Player Bets' to be displayed in Football sport category page?
    DESCRIPTION: This test case verifies tabs order on the <Sport> Landing Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
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
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
        EXPECTED: <Sports> Landing Page is opened
        """
        pass

    def test_003_verify_tabs_order_for_sport(self):
        """
        DESCRIPTION: Verify tabs order for 'Sport'
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches' (the corresponding label for this tab is listed in the preconditions for every sport)
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        """
        pass

    def test_004_navigate_between_tabs(self):
        """
        DESCRIPTION: Navigate between tabs
        EXPECTED: *   The content of the corresponding tab is shown
        EXPECTED: *   Navigation is carried out smoothly
        """
        pass

    def test_005_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to <Football> Landing page
        EXPECTED: <Football> Landing Page is opened
        """
        pass

    def test_006_verify_tabs_order_for_football(self):
        """
        DESCRIPTION: Verify tabs order for 'Football'
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches'
        EXPECTED: - 'Competitions'
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        EXPECTED: - 'Jackpot'
        EXPECTED: - 'Specials'
        EXPECTED: - 'Player Bets
        """
        pass

    def test_007_navigate_between_tabs(self):
        """
        DESCRIPTION: Navigate between tabs
        EXPECTED: *   The content of the corresponding tab is shown
        EXPECTED: *   Navigation is carried out smoothly
        """
        pass
