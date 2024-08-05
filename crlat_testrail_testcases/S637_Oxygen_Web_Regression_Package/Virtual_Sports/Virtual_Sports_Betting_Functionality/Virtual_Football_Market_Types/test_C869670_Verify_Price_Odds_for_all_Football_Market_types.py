import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869670_Verify_Price_Odds_for_all_Football_Market_types(Common):
    """
    TR_ID: C869670
    NAME: Verify Price/Odds for all Football Market types
    DESCRIPTION: This test case verifies data of price/odds buttons.
    PRECONDITIONS: Get SiteServer response to verify data (Football class id 287):
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/287?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *   **Match Betting **market corresponds to name=**"|Win/Draw/Win|"**
    PRECONDITIONS: *   **Correct Score** market corresponds to name=**"|Correct Score|"**
    PRECONDITIONS: *   **Total Number of Goals** market corresponds to name=**"|**Total Number of Goals**|"**
    PRECONDITIONS: *   **Under/Over 2.5** market corresponds to name=**"|Under/Over 2.5|"**
    PRECONDITIONS: *   **Double Chance** market corresponds to name=**"|**Double Chance**|"**
    """
    keep_browser_open = True

    def test_001_open_virtual_sports_homepage(self):
        """
        DESCRIPTION: Open 'Virtual Sports' homepage
        EXPECTED: 
        """
        pass

    def test_002_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 
        """
        pass

    def test_003_go_to_double_chance_section(self):
        """
        DESCRIPTION: Go to 'Double Chance' section
        EXPECTED: 
        """
        pass

    def test_004_verify_data_of_priceodds_for_the_next_event_for_all_selections(self):
        """
        DESCRIPTION: Verify data of 'Price/Odds' for the next event for all selections
        EXPECTED: 'Price/Odds' corresponds to the priceNum/priceDen
        """
        pass

    def test_005_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Price/odds corresponds to the priceNum/priceDen for verified events
        """
        pass

    def test_006_repeat_this_test_case_for_all_football_market_types_double_chance_match_betting_underover_25_correct_score_total_number_of_goals(self):
        """
        DESCRIPTION: Repeat this test case for all Football Market types:
        DESCRIPTION: * Double Chance
        DESCRIPTION: * Match Betting
        DESCRIPTION: * Under/Over 2.5
        DESCRIPTION: * Correct Score
        DESCRIPTION: * Total Number of Goals
        EXPECTED: 
        """
        pass
