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
class Test_C869708_Verify_List_of_Market_Types(Common):
    """
    TR_ID: C869708
    NAME: Verify List of Market Types
    DESCRIPTION: This test case verifies the list of market types sections available for Virtual Horse Racing
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
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sportsopen_some_of_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        DESCRIPTION: Open some of Virtual Sports
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: The next event is displayed
        """
        pass

    def test_002_verify_the_list_of_market_type_sections_for_verified_event(self):
        """
        DESCRIPTION: Verify the list of market type sections for verified event
        EXPECTED: The list of market types corresponds to the list in SiteServer response
        """
        pass

    def test_003_repeat_steps_1_2_for_few_events(self):
        """
        DESCRIPTION: Repeat steps 1-2 for few events
        EXPECTED: The list of market types corresponds to the list in the Site Server response
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
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
