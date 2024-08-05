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
class Test_C869654_Verify_Price_Odds_for_all_Tennis_market_types(Common):
    """
    TR_ID: C869654
    NAME: Verify Price/Odds for all Tennis market types
    DESCRIPTION: This test case verifies data of price/odds buttons.
    PRECONDITIONS: Get SiteServer response to verify data (Tennis class id 291):
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/291?translationLang=LL?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: Where X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *   **Match Betting **market corresponds to** **name**="|Head/Head (winner)|"**
    PRECONDITIONS: *   **Correct Score (Game)** market corresponds to name=**"|Correct Score (game)|"**
    PRECONDITIONS: *   **Total Number of Points **market corresponds to name=**"|Total Number of Points|"**
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_tennis_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Tennis' sport page
        EXPECTED: 'Virtual Tennis' sport page is opened
        """
        pass

    def test_002_go_to_correct_score_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' section
        EXPECTED: 
        """
        pass

    def test_003_verify_data_of_priceodds_for_the_next_event_for_all_selections(self):
        """
        DESCRIPTION: Verify data of 'Price/Odds' for the next event for all selections
        EXPECTED: 'Price/Odds' corresponds to the priceNum/priceDen
        """
        pass

    def test_004_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Price/odds corresponds to the priceNum/priceDen for verified events
        """
        pass

    def test_005_repeat_this_test_case_for_all_tennis_market_types_correct_score_match_betting_total_number_of_points(self):
        """
        DESCRIPTION: Repeat this test case for all Tennis market types:
        DESCRIPTION: * Correct Score
        DESCRIPTION: * Match Betting
        DESCRIPTION: * Total Number of Points
        EXPECTED: 
        """
        pass
