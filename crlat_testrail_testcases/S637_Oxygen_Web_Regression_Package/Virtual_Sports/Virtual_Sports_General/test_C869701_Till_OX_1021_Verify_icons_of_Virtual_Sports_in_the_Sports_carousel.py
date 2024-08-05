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
class Test_C869701_Till_OX_1021_Verify_icons_of_Virtual_Sports_in_the_Sports_carousel(Common):
    """
    TR_ID: C869701
    NAME: (Till OX 102.1) Verify icons of Virtual Sports in the Sports carousel
    DESCRIPTION: This test case verifies the icons for all Virtual sport types
    DESCRIPTION: **Case is Outdated after BMA-46326, replaced with:** https://ladbrokescoral.testrail.com//index.php?/cases/view/58446785
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
        EXPECTED: 'Virtual Horse Racing' page is opened by default
        """
        pass

    def test_002_verify_virtual_horse_racing_icon_in_the_sports_carousel(self):
        """
        DESCRIPTION: Verify 'Virtual Horse Racing' icon in the Sports carousel
        EXPECTED: Horse racing icon is displayed in the Sports carousel
        """
        pass

    def test_003_while_being_on_any_other_virtual_sport_page_tap_on_virtual_horse_racing_sport_icon(self):
        """
        DESCRIPTION: While being on any other virtual sport page, tap on 'Virtual Horse Racing' sport icon
        EXPECTED: - Icon is hyperlinked
        EXPECTED: - User is redirected to sport page
        """
        pass

    def test_004_check_timer_above_the_horse_racing_icon_in_the_carousel(self):
        """
        DESCRIPTION: Check timer above the horse racing icon in the carousel
        EXPECTED: - Horse Racing timer is present
        EXPECTED: - Timer format is mm:ss
        EXPECTED: - Timer shows when the next horse racing virtual event will start
        """
        pass

    def test_005_check_timer_correctness(self):
        """
        DESCRIPTION: Check timer correctness
        EXPECTED: Timer value is displayed according to the actual time when the next event will start (see SiteServer response)
        """
        pass

    def test_006_check_the_horse_racing_icon_when_event_is_livebroadcasting(self):
        """
        DESCRIPTION: Check the horse racing icon when event is live/broadcasting
        EXPECTED: A red label with 'Live' text is displayed above the icon instead of the timer
        """
        pass

    def test_007_check_livelabel(self):
        """
        DESCRIPTION: Check 'Live' label
        EXPECTED: 'Live' label and the live event stop being shown simultaneously
        """
        pass

    def test_008_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
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
