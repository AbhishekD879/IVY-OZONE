import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2988035_Highlights_Carousel__cards_UI_elements_on_different_sports(Common):
    """
    TR_ID: C2988035
    NAME: Highlights Carousel - cards UI elements on different sports
    DESCRIPTION: This test case verifies UI cards elements displaying for different sports
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 3 active Highlights Carousels with active events from appropriate sport: 1) 1st Highlights Carousel for Football configured in CMS > Sport Pages > Sport Categories > Football; 2) 2nd Highlights Carousel for Badminton configured in CMS > Sport Pages > Sport Categories > Golf; 3) 3rd Highlights Carousel for Volleyball configured in CMS > Sport Pages > Sport Categories > Boxing
    PRECONDITIONS: - "Display In-Play" option should be enabled in Highlights Carousels
    PRECONDITIONS: - For each sport above you should have: 1) prematch event without stream mapped; 2) prematch event with stream mapped; 3) live event without stream mapped; 4) live event with stream mapped
    PRECONDITIONS: - All events should have active market from |Match Betting| market template with selections
    PRECONDITIONS: - You should be on a landing page of the sports with configured Highlights Carousels: 1) For Football on "Matches" tab; 2) For Golf on "Events" tab; 3) For Boxing on "Fights" tab
    """
    keep_browser_open = True

    def test_001_verify_cards_elements_in_highlights_carousels_on_landing_pages_for_football_golf_and_boxing(self):
        """
        DESCRIPTION: Verify cards elements in Highlights Carousels on landing pages for Football, Golf and Boxing
        EXPECTED: Prematch event without stream mapped:
        EXPECTED: - Event's start date and time at the top left corner (if event starts today there is "Today" instead of date and time)
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Prematch event with stream mapped:
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner (if event starts today there is "Today" instead of date and time)
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Live event without stream mapped:
        EXPECTED: - "Live" label at the top left corner
        EXPECTED: - Event's time in live/set/round
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under "Live" label
        EXPECTED: - Correct scores against teams/players (For Badminton 2 columns G and P with scores)
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Live event with stream mapped:
        EXPECTED: - "Watch Live" label at the top left corner
        EXPECTED: - Event's time in live/set/round
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under "Watch Live" label
        EXPECTED: - Correct scores against teams/players (For Badminton 2 columns G and P with scores
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        """
        pass
