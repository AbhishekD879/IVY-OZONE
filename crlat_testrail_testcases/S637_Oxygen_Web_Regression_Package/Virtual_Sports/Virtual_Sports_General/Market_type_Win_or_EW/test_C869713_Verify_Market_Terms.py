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
class Test_C869713_Verify_Market_Terms(Common):
    """
    TR_ID: C869713
    NAME: Verify Market Terms
    DESCRIPTION: This test case verifies market terms in the 'Win or E/W' section.
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: List of relevant class id's:
    PRECONDITIONS: Horse Racing class id 285
    PRECONDITIONS: Greyhounds class id 286
    PRECONDITIONS: Football class id 287
    PRECONDITIONS: Motorsports class id 288
    PRECONDITIONS: Cycling class id 290
    PRECONDITIONS: Tennis class id 291
    PRECONDITIONS: Grand National class id 26604
    """
    keep_browser_open = True

    def test_001_open_virtual_sports_homepage(self):
        """
        DESCRIPTION: Open 'Virtual Sports' homepage
        EXPECTED: 
        """
        pass

    def test_002_go_to_virtual_horse_racing_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Horse Racing' sport page
        EXPECTED: 
        """
        pass

    def test_003_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to 'Win or E/W' section
        EXPECTED: 
        """
        pass

    def test_004_verify_termspresence(self):
        """
        DESCRIPTION: Verify 'Terms' presence
        EXPECTED: Terms are shown below the 'Win or E/W' section
        """
        pass

    def test_005_verify_terms_format(self):
        """
        DESCRIPTION: Verify 'Terms' format
        EXPECTED: Terms are shown in 'Each-way X/Y the odds a plase 1,2...' format
        """
        pass

    def test_006_verify_data_in_the_terms(self):
        """
        DESCRIPTION: Verify data in the 'Terms'
        EXPECTED: 'Terms' correspond to the SiteServer response ("eachWayFactorNum/eachWayFactorDen" and "eachWayPlaces" attributes)
        """
        pass

    def test_007_repeat_steps_4_5_and_check_terms_for_several_events_of_that_category(self):
        """
        DESCRIPTION: Repeat steps №4-5 and check 'Terms' for several events of that category
        EXPECTED: 'Terms' are shown properly for the each event
        """
        pass

    def test_008_repeat_this_test_case_for_the_following_virtual_sports_horse_racing_greyhounds_cycling_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Horse Racing
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Cycling
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
