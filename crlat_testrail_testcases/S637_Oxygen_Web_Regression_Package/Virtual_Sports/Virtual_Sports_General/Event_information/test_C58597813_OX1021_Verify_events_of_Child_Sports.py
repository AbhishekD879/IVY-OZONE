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
class Test_C58597813_OX1021_Verify_events_of_Child_Sports(Common):
    """
    TR_ID: C58597813
    NAME: [OX102.1] Verify events of Child Sports
    DESCRIPTION: This test case verifies events of Child Sports
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_select_one_of_child_sports(self):
        """
        DESCRIPTION: Select one of Child sports
        EXPECTED: Number of Events displayed as per the CMS configuration 'Events number to show'
        EXPECTED: Sorted by time of the event
        """
        pass

    def test_002_when_last_event_of_child_sport_becomes_resulted_refresh_the_page(self):
        """
        DESCRIPTION: When last event of Child sport becomes resulted, refresh the page
        EXPECTED: Child sport page is NOT displayed as it doesn't have any events to be displayed
        """
        pass

    def test_003_open_event_which_becomes_undisplayedinactive_for_betting(self):
        """
        DESCRIPTION: Open event which becomes Undisplayed/Inactive for betting
        EXPECTED: User should be moved to the next event's (Race card or EDP) for the betting opportunity without page refresh
        """
        pass

    def test_004_return_back_to_virtual_sports_page(self):
        """
        DESCRIPTION: Return back to Virtual Sports Page
        EXPECTED: First sport with events sorted by the time of the events displayed
        EXPECTED: The list of Market types corresponds to the list in the Site Server response
        """
        pass

    def test_005_repeat_this_test_case_for_the_following_virtual_sportsgreyhoundsfootballmotorsportscyclingspeedwaytennisgrand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: Greyhounds
        DESCRIPTION: Football,
        DESCRIPTION: Motorsports,
        DESCRIPTION: Cycling,
        DESCRIPTION: Speedway,
        DESCRIPTION: Tennis,
        DESCRIPTION: Grand National
        EXPECTED: 
        """
        pass

    def test_006_on_desktop_onlyhover_the_mouse_on_the_odds_button(self):
        """
        DESCRIPTION: On Desktop only:
        DESCRIPTION: Hover the mouse on the odds button.
        EXPECTED: The colour of the odds button is changed as on the screenshot below:
        EXPECTED: ![](index.php?/attachments/get/106948349)
        """
        pass
