import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28435_Verify_Considering_of_Users_Time_Zone(Common):
    """
    TR_ID: C28435
    NAME: Verify Considering of User's Time Zone
    DESCRIPTION: This test case verifies considering of User's Time Zone.
    PRECONDITIONS: 1) For verifying specific event use link (or search in Network tab in Dev tools via next keyword "EventToOutcomeForEvent":
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - currently supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, Ukr)
    PRECONDITIONS: ---------------------------------------------------
    PRECONDITIONS: 2) Retrieve a list of Event IDs for specific range of time(or search in Network tab in Dev tools via next keyword "EventToOutcomeForClass":
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T**00:00:00**Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T**00:00:00**Z
    PRECONDITIONS: *   XX - Category ID (Sport ID)
    PRECONDITIONS: *   XXX -  is a comma-separated list of Class ID's
    PRECONDITIONS: *   YYYY1-MM1-DD1 - is the lower date bound
    PRECONDITIONS: *   YYYY2-MM2-DD2 - is the higher date bound
    PRECONDITIONS: *   X.XX - currently supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, Ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is opened by default
        """
        pass

    def test_003_verify_start_time_of_specific_event_on_the_landing_page(self):
        """
        DESCRIPTION: Verify Start Time of specific event on the Landing Page
        EXPECTED: 
        """
        pass

    def test_004_go_to_event_detailspage_of_verified_event_and_verify_start_time(self):
        """
        DESCRIPTION: Go to Event Details Page of verified event and verify Start Time
        EXPECTED: Event start Time matches with Time on the event section we navigated from
        """
        pass

    def test_005_verifystarttime_of_verified_event_in_the_response(self):
        """
        DESCRIPTION: Verify **startTime** of verified event in the response
        EXPECTED: *   Event Start Time on Site Server corresponds to UTC time zone
        EXPECTED: *   User's time zone is taken into consideration correctly on Invictus application
        """
        pass

    def test_006_retrieve_the_list_of_events_for_specific_day_using_pre_condition_2(self):
        """
        DESCRIPTION: Retrieve the list of events for specific day using Pre-condition №2
        EXPECTED: 
        """
        pass

    def test_007_in_time_range_yyyy_mm_ddt000000_set_a_time_that_is_consistent_with_users_time_zone(self):
        """
        DESCRIPTION: In time range YYYY-MM-DDT00:00:00 set a time that is consistent with user's time zone
        EXPECTED: 
        """
        pass

    def test_008_verify_number_of_retrieved_events_in_the_response(self):
        """
        DESCRIPTION: Verify number of retrieved events in the response
        EXPECTED: 
        """
        pass

    def test_009_verify_number_of_displayed_events_on_the_invictus_application_for_specific_day(self):
        """
        DESCRIPTION: Verify number of displayed events on the Invictus application for specific day
        EXPECTED: *   Number of events match with the number of events got on step №8
        EXPECTED: *   Events without outcomes are not displayed in the Invictus application
        """
        pass

    def test_010_change_users_time_zone_on_the_device(self):
        """
        DESCRIPTION: Change user's time zone on the device
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps №5-9
        EXPECTED: *   Number of events match with the number of events got on step №8
        EXPECTED: *   Events without outcomes are not displayed in the Invictus application
        """
        pass
