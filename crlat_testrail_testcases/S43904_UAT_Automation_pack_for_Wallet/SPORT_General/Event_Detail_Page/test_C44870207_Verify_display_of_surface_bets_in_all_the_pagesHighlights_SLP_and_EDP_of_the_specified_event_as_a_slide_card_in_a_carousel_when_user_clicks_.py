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
class Test_C44870207_Verify_display_of_surface_bets_in_all_the_pagesHighlights_SLP_and_EDP_of_the_specified_event_as_a_slide_card_in_a_carousel_when_user_clicks_on_the_odds_button_the_selection_is_added_to_the_quick_bet_bet_slip(Common):
    """
    TR_ID: C44870207
    NAME: Verify display of surface bets in all the pages(Highlights, SLP and EDP of the specified event) as a slide/card in a carousel, when user clicks on the odds button the selection is added  to the quick bet/ bet slip
    DESCRIPTION: Verify display of surface bets in all the pages(Highlights, SLP and EDP of the specified event) as a slide/card in a carousel, when user clicks on the odds button the selection is added  to the quick bet/ bet slip
    PRECONDITIONS: -There is a  Surface Bet added to the Event Details page (EDP).
    PRECONDITIONS: -Content/Was price/Icon
    PRECONDITIONS: -Display on Highlights tab
    PRECONDITIONS: -Open this EDP in Oxygen application.
    PRECONDITIONS: -CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: Home page opened
        """
        pass

    def test_002_verify_display_of_surface_bets_on_highlights_sports_landing_page_and_event_detail_page(self):
        """
        DESCRIPTION: Verify display of surface bets on highlights, Sports landing page and Event detail page
        EXPECTED: Surface bets are displayed on highlights tab, sports landing page and event detail page
        """
        pass

    def test_003_verify_the_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify the Surface Bet carousel
        EXPECTED: Carousel can be smoothly swiped to the left/right
        """
        pass

    def test_004_verify_the_surface_bet_with_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet with Content/Was price/Icon displaying
        EXPECTED: Contents, price, was price and icon are displayed
        """
        pass

    def test_005_verifies_that_expireddisableddeleted_surface_bet_is_not_shown_on_highlighs_tab_sports_landing_page_and_event_detail_page(self):
        """
        DESCRIPTION: Verifies that expired/disabled/deleted surface bet is not shown on Highlighs tab, sports landing page and Event detail page
        EXPECTED: expired/disabled/deleted surface bet are not displayed
        """
        pass

    def test_006_verify_that_suspendedfuture_surface_bet_is_shown_on_the_edp(self):
        """
        DESCRIPTION: Verify that Suspended/future Surface Bet is shown on the EDP
        EXPECTED: Suspended surface bet are greyed out
        EXPECTED: Future surface bets are displayed on EDP
        """
        pass

    def test_007_verify_live_updates_on_surface_bets(self):
        """
        DESCRIPTION: Verify Live updates on surface bets
        EXPECTED: Price updates without page refresh
        """
        pass

    def test_008_place_the_bet_using_price_button_of_the_surface_bet_from_the_quickbetbetslip_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the Quickbet/Betslip. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        pass
