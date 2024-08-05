import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28798_Verify_event_name_displaying(Common):
    """
    TR_ID: C28798
    NAME: Verify event name displaying
    DESCRIPTION: This test case verifies how event name which is obtained from the Site Server will be shown on the Invictus application
    PRECONDITIONS: 1) On the Invictus application for <Race> sports, event names on Site Server response contains two parts: 'event time' + 'event name'.
    PRECONDITIONS: But event time is shown in the UTC format. That's why it was decided to remove time part as user can be in a different time zones.
    PRECONDITIONS: 2) Retrieve a list of Event IDs for specific range of time:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXX?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T**00:00:00**Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T**00:00:00**Z
    PRECONDITIONS: *   *XX - Category ID (**Sport** ID)*
    PRECONDITIONS: *   *XXX -  is a comma separated list of Class ID's*
    PRECONDITIONS: *   *YYYY1-MM1-DD1 - is the lower date bound*
    PRECONDITIONS: *   *YYYY2-MM2-DD2 - is the higher date bound*
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id = 21
    PRECONDITIONS: Greyhound category id = 19
    """
    keep_browser_open = True

    def test_001_open_site_server(self):
        """
        DESCRIPTION: Open Site Server
        EXPECTED: Site Server is opened
        """
        pass

    def test_002_find_an_event_for_todays_day_which_is_satisfied_all_requirements_to_be_shown_in_the_invictus_application(self):
        """
        DESCRIPTION: Find an event for today's day which is satisfied all requirements to be shown in the Invictus application
        EXPECTED: Event is shown
        """
        pass

    def test_003_look_at_the_event_name(self):
        """
        DESCRIPTION: Look at the event name
        EXPECTED: *  Event name corresponds to the **'name' **attribute on event level
        EXPECTED: *  Event name consists of two parts in the response:
        EXPECTED: "time" + "event name" (e.g. 2:45 Saint - cloud)
        """
        pass

    def test_004_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_005_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_006_go_to_the_event_details_page_from_the_step_2(self):
        """
        DESCRIPTION: Go to the event details page from the step #2
        EXPECTED: Event details page is opened
        """
        pass

    def test_007_look_at_the_event_name(self):
        """
        DESCRIPTION: Look at the event name
        EXPECTED: *  Event type  "event name" (e.g. Saint - cloud) is shown in subheader
        EXPECTED: *  Event time "time" (e.g. 14:45) is shown on the ribbon time
        EXPECTED: *  Event name corresponds to the **'name'** attribute
        EXPECTED: *  No matter what user timezone is the race local time is shown near the event name (as come from the Site Server)
        """
        pass
