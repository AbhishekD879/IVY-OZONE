import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C43884990_Verify_displaying_of_Highlights_carousel_on_the_Homepage(Common):
    """
    TR_ID: C43884990
    NAME: Verify displaying of  'Highlights' carousel on the Homepage
    DESCRIPTION: This test case verifies displaying of  'Highlights' carousel on the Homepage
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) 'Highlights' carousel module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: 2) You should have 2 active 'Highlights' carousels with active events in CMS > Sports Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - 1st Highlights Carousel should be configured by TypeID
    PRECONDITIONS: - 2nd Highlight Carousel is configured by EvenIDs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "HighlightCarouselModule" an choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32857095)
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Verify 'Highlights' carousel displaying
        EXPECTED: * Highlights Carousel module is displayed according to order in CMS > Sports Pages > Homepage
        EXPECTED: * 'Highlights' header with title configured in CMS and 'See All' link that navigates to the appropriate Competitions Details page
        EXPECTED: * All cards of available events are displayed in the carousel (based on set number of events in CMS for carousel configured by TypeID)
        """
        pass

    def test_002_verify_cards_elements_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards elements in 'Highlights' carousel
        EXPECTED: Cards in 'Highlights' carousels contain the following elements:
        EXPECTED: * Event's start date and time at the top left corner (if the event starts today there is "Today" instead of date and time) or 'Live'/'Sets' label for the Live events
        EXPECTED: * 'Watch' label at the top left corner
        EXPECTED: * '>' arrow at the top right corner (Ladbrokes only)
        EXPECTED: * 2 teams/players under start date
        EXPECTED: * Team Kits are displayed before teams/players if available
        EXPECTED: * 'Price/Odds' buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        """
        pass

    def test_003_select_any_other_tab_on_the_homepage_eg_in_play_coupons_next_races_build_your_bet_etcverify_displaying_of_highlights_carousel_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the Homepage (e.g. In-Play, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of 'Highlights' carousel on other tabs.
        EXPECTED: * Configured 'Highlights' carousel is displayed only on the 'Featured' tab
        EXPECTED: * 'Highlights' carousel container is NOT displayed on other 'Homepage' tabs
        EXPECTED: * Configured 'Highlights' carousel is NOT displayed on other 'Homepage' tabs
        """
        pass

    def test_004_go_to_any_sports_page_eg_football_tennis_and_observe_the_highlights_carouselverify_displaying_of_homepage_configured_highlights_carousel_on_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports page (e.g. Football, Tennis) and observe the 'Highlights' carousel.
        DESCRIPTION: Verify displaying of Homepage configured 'Highlights' carousel on any Sports landing page.
        EXPECTED: * Configured 'Highlights' carousel for Homepage is NOT displayed on other Sports pages
        EXPECTED: * Only 'Highlights' carousel that is configured for Sports landing page is shown (if there are some)
        EXPECTED: * 'Highlights' carousel is NOT displayed If no 'Highlights' carousel is configured for Sports pages.
        """
        pass

    def test_005_go_to_cms___sports_pages___homepage___highlights_carouselset_an_activeinactive_flag_for_the_configured_highlights_carousel_for_the_homepage_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> Homepage -> 'Highlights Carousel'.
        DESCRIPTION: Set an "Active"/"Inactive" flag for the configured 'Highlights' carousel for the Homepage to 'Inactive'.
        EXPECTED: 
        """
        pass

    def test_006_go_to_the_appnavigate_to_the_featured_tab_on_the_homepageverify_that_highlights_carousel_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to the app.
        DESCRIPTION: Navigate to the 'Featured' tab on the Homepage.
        DESCRIPTION: Verify that 'Highlights' carousel is no longer displayed.
        EXPECTED: 'Highlights' carousel container is NOT displayed.
        EXPECTED: 'Highlights' carousel is no longer displayed.
        """
        pass
