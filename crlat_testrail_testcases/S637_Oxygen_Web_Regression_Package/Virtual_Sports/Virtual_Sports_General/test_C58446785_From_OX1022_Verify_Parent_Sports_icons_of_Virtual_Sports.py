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
class Test_C58446785_From_OX1022_Verify_Parent_Sports_icons_of_Virtual_Sports(Common):
    """
    TR_ID: C58446785
    NAME: From [OX102.2] Verify Parent Sports icons of Virtual Sports
    DESCRIPTION: This test case verifies the icons for all Virtual sport types
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
    PRECONDITIONS: Darts class id 26615
    PRECONDITIONS: Boxing class id 26614
    PRECONDITIONS: Grand National class id 26604
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: - 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS
        EXPECTED: - First configured on CMS sport displayed on the page load
        EXPECTED: - When Parent Sport has on Child Sports configured on CMS, icon should not appear in header
        EXPECTED: - Virtuals Sports/Parent Sports header displayed according to designs:
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa
        """
        pass

    def test_002_check_header_scrolling(self):
        """
        DESCRIPTION: Check header scrolling
        EXPECTED: Header should be scrollable to fit all the sports
        """
        pass

    def test_003_verify_virtual_horse_racing_icon_in_the_sports_carousel(self):
        """
        DESCRIPTION: Verify 'Virtual Horse Racing' icon in the Sports carousel
        EXPECTED: Horse racing icon is displayed in the Sports carousel
        """
        pass

    def test_004_choose_another_sport_from_virtuals_sportsparent_sports_header(self):
        """
        DESCRIPTION: Choose another sport from Virtuals Sports/Parent Sports header
        EXPECTED: - User is redirected to other Parent sports page
        EXPECTED: - First Child Sport opened
        EXPECTED: - Events/Markets related to that sport displayed
        """
        pass

    def test_005_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
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
