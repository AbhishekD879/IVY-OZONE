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
class Test_C43885002_Verify_displaying_of_Surface_Bet_module_on_the_Homepage(Common):
    """
    TR_ID: C43885002
    NAME: Verify displaying of  'Surface Bet' module on the Homepage
    DESCRIPTION: This test case verifies displaying of 'Surface Bet' module on the Homepage
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Go to CMS -> Sports Pages -> Homepage -> Surface Bet Module and configure at least 1 active 'Surface Bet' module for the Homepage
    PRECONDITIONS: 2) 'Surface Bet' module should be "Active" in CMS > Sport Pages > Homepage > Surface Bet Module
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "SurfaceBetModule" an choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32857050)
    """
    keep_browser_open = True

    def test_001_verify_surface_bet_carousel_displaying(self):
        """
        DESCRIPTION: Verify 'Surface Bet' carousel displaying
        EXPECTED: * 'Surface Bet' Carousel module is displayed according to order in CMS > Sports Pages > Homepage
        EXPECTED: * All cards of available events are displayed in the carousel
        """
        pass

    def test_002_verify_cards_elements_in_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify cards elements in 'Surface Bet' carousel
        EXPECTED: Cards in 'Surface Bet' carousels contain the following elements:
        EXPECTED: * Icon and Title (configured in CMS) at the top left corner
        EXPECTED: * Content text
        EXPECTED: * 'Price' button with correct price
        EXPECTED: * 'Was Price' information with previous price (configured in CMS) below the 'Price' button
        """
        pass

    def test_003_select_any_other_tab_on_the_homepage_eg_in_play_coupons_next_races_build_your_bet_etcverify_displaying_of_surface_bet_carousel_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the Homepage (e.g. In-Play, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of 'Surface Bet' carousel on other tabs.
        EXPECTED: * Configured 'Surface Bet' carousel is displayed only on the 'Featured' tab
        EXPECTED: * 'Surface Bet' carousel container is NOT displayed on other 'Homepage' tabs
        EXPECTED: * Configured 'Surface Bet' carousel is NOT displayed on other 'Homepage' tabs
        """
        pass

    def test_004_go_to_any_sports_page_eg_football_tennis_and_observe_the_surface_bet_carouselverify_displaying_of_homepage_configured_surface_bet_carousel_on_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports page (e.g. Football, Tennis) and observe the 'Surface Bet' carousel.
        DESCRIPTION: Verify displaying of Homepage configured 'Surface Bet' carousel on any Sports landing page.
        EXPECTED: * Configured 'Surface Bet' carousel for Homepage is NOT displayed on other Sports pages
        EXPECTED: * Only 'Surface Bet' carousel that is configured for Sports landing page is shown (if there are some)
        EXPECTED: * 'Surface Bet' carousel is NOT displayed If no 'Surface Bet' carousel is configured for Sports pages.
        """
        pass

    def test_005_go_to_cms___sports_pages___homepage___surface_betset_an_activeinactive_flag_for_the_configured_surface_bet_carousel_for_the_homepage_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> Homepage -> 'Surface Bet'.
        DESCRIPTION: Set an "Active"/"Inactive" flag for the configured 'Surface Bet' carousel for the Homepage to 'Inactive'.
        EXPECTED: 
        """
        pass

    def test_006_go_to_the_appnavigate_to_the_featured_tab_on_the_homepageverify_that_surface_bet_carousel_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to the app.
        DESCRIPTION: Navigate to the 'Featured' tab on the Homepage.
        DESCRIPTION: Verify that 'Surface Bet' carousel is no longer displayed.
        EXPECTED: 'Surface Bet' carousel container is NOT displayed.
        EXPECTED: 'Surface Bet' carousel is no longer displayed.
        """
        pass
