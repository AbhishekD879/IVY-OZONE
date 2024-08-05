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
class Test_C60007046_Verify_event_disappears_with_live_push_update_when_event_become_resulted(Common):
    """
    TR_ID: C60007046
    NAME: Verify event disappears with live push update when event become resulted
    DESCRIPTION: This test case verifies that Virtual Sport event disappears with live push update when event become resulted
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/16231,289,288,285,286,287,290,291?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.typeId:notEquals:3048&simpleFilter=event.typeId:notEquals:3049&simpleFilter=event.typeId:notEquals:3123&simpleFilter=event.startTime:lessThanOrEqual:2016-04-18T16:28:45Z&simpleFilter=event.startTime:greaterThan:2016-04-18T09:28:45Z&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
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

    def test_001_open_virtual_sports_page__horse_racing_virtual_sport_tab(self):
        """
        DESCRIPTION: Open Virtual Sports page > Horse Racing virtual sport tab
        EXPECTED: * The first track from CMS is displayed as default. The display order of the tracks should be as per the CMS.
        EXPECTED: * The 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS.
        """
        pass

    def test_002__wait_when_one_of_the_events_for_selected_virtual_sport_became_resultedor_make_one_of_the_events_for_selected_virtual_sport_resulted_in_ti(self):
        """
        DESCRIPTION: * Wait when one of the events for selected Virtual Sport became resulted
        DESCRIPTION: or
        DESCRIPTION: * Make one of the events for selected Virtual Sport resulted in TI
        EXPECTED: * Push update is received with result_conf = “y” parameter for this event
        EXPECTED: * Event disappears from UI
        """
        pass

    def test_003_repeat_this_test_case_for_the_following_virtual_sportsgreyhoundsfootballmotorsportscyclingspeedwaytennisgrand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: Greyhounds
        DESCRIPTION: Football,
        DESCRIPTION: Motorsports,
        DESCRIPTION: Cycling,
        DESCRIPTION: Speedway,
        DESCRIPTION: Tennis
        DESCRIPTION: Grand National
        EXPECTED: 
        """
        pass
