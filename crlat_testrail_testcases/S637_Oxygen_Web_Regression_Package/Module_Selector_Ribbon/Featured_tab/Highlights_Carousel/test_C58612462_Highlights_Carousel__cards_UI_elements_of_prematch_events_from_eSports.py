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
class Test_C58612462_Highlights_Carousel__cards_UI_elements_of_prematch_events_from_eSports(Common):
    """
    TR_ID: C58612462
    NAME: Highlights Carousel - cards UI elements of prematch events from eSports
    DESCRIPTION: This test case verifies UI cards elements displaying of prematch events from eSports
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) CMS > Sport Pages > Homepage:
    PRECONDITIONS: - 'Highlights Carousel' module should be enabled
    PRECONDITIONS: - Highlights Carousel should be created, containing prematch events from eSports
    PRECONDITIONS: 2) CMS > Sport Pages > Sport Categories >eSports:
    PRECONDITIONS: - 'Highlights Carousel' module should be enabled
    PRECONDITIONS: - Highlights Carousel should be created, containing prematch events from eSports
    PRECONDITIONS: 3) eSports prematch events should have active Primary market from |Match Result (2 way)| market template with selections
    PRECONDITIONS: 4) Event name of eSports prematch events should be in the following formats:
    PRECONDITIONS: **|Player A| - |Player B|**
    PRECONDITIONS: **|Player A|<space here>|vs|<space here>|Player B|**
    PRECONDITIONS: To verify data within Highlights carousel open DevTools > Network > WS > Featured WS:
    PRECONDITIONS: ![](index.php?/attachments/get/104612703)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to eSports landing page > Matches tab
    """
    keep_browser_open = True

    def test_001_verify_cards_elements_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards elements in Highlights Carousel
        EXPECTED: **Prematch event without stream mapped:**
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612701)
        EXPECTED: **Prematch event with stream mapped:**
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner next to "Watch" label
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612702)
        """
        pass

    def test_002__navigate_to_home_page_gt_featured_tab_verify_cards_elements_in_highlights_carousel_for_esports(self):
        """
        DESCRIPTION: * Navigate to Home page &gt; 'Featured' tab
        DESCRIPTION: * Verify cards elements in Highlights Carousel for eSports
        EXPECTED: **Prematch event without stream mapped:**
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612701)
        EXPECTED: **Prematch event with stream mapped:**
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner next to "Watch" label
        EXPECTED: - "&gt;" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612702)
        """
        pass
