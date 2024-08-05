import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869711_Verify_Price_Odds(Common):
    """
    TR_ID: C869711
    NAME: Verify Price/Odds
    DESCRIPTION: This test case verifies data of price/odds buttons.
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: List of relevant class id's:
    PRECONDITIONS: Horse Racing class id 285
    PRECONDITIONS: Greyhounds class id 286
    PRECONDITIONS: Football class id 287
    PRECONDITIONS: Motorsports class id 288
    PRECONDITIONS: Speedway class id 289
    PRECONDITIONS: Cycling class id 290
    PRECONDITIONS: Tennis class id 291
    PRECONDITIONS: Grand National class id 26604
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to 'Win or E/W' section
        EXPECTED: 
        """
        pass

    def test_002_verify_data_of_priceodds_for_the_next_event_for_all_selections(self):
        """
        DESCRIPTION: Verify data of 'Price/Odds' for the next event for all selections
        EXPECTED: 'Price/Odds' corresponds to the priceNum/priceDen
        """
        pass

    def test_003_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Price/odds corresponds to the priceNum/priceDen for verified events
        """
        pass

    def test_004_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
