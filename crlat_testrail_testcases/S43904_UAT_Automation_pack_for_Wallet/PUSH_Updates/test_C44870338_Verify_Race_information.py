import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870338_Verify_Race_information(Common):
    """
    TR_ID: C44870338
    NAME: Verify  Race information
    DESCRIPTION: Verify that Race information is updated in any page through the site
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    """
    keep_browser_open = True

    def test_001_navigate_to_home_page___next_racesverify_that_races_are_updated_by_pushverify__race_card_information_event_name_and_timeverify_the_event_is_dropped_off_by_push_after_the_event_has_startedfinished(self):
        """
        DESCRIPTION: Navigate to Home Page - Next Races
        DESCRIPTION: Verify that Races are updated by push
        DESCRIPTION: Verify  Race Card information: event name and time
        DESCRIPTION: Verify the event is dropped off by Push (after the event has started/finished)
        EXPECTED: In Home page - Next Races, the event info is updated by push
        """
        pass

    def test_002_navigate_to_horse_racing___meetingsverify_that_event_status_is_updated_by_push_result_race_live_race_offverify_that_events_dont_drop_offverify_the_event_is_dropped_off_by_push_after_the_event_has_startedfinished(self):
        """
        DESCRIPTION: Navigate to Horse Racing - Meetings
        DESCRIPTION: Verify that event status is updated by push (Result, Race live, Race off)
        DESCRIPTION: Verify that events don't drop off
        DESCRIPTION: Verify the event is dropped off by Push (after the event has started/finished)
        EXPECTED: In HR page - Meetings the event info is updated by push
        """
        pass

    def test_003_navigate_to_horse_racing___next_racesverify_that_races_are_listed_in_chronological_order_and_info_is_updated_by_pushverify__race_card_information_event_name_and_time(self):
        """
        DESCRIPTION: Navigate to Horse Racing - Next Races
        DESCRIPTION: Verify that Races are listed in chronological order and info is updated by push
        DESCRIPTION: Verify  Race Card information: event name and time
        EXPECTED: In HR page - Next Races, the event info is updated by push
        """
        pass

    def test_004_navigate_to_horse_racing___edp_and_verify_that_race_info_is_updated_by_pushverify_that_the_event_name_and_time_are_displayedverify_that_data_update__or_the_event_is_suspended_by_push(self):
        """
        DESCRIPTION: Navigate to Horse Racing - EDP and verify that Race info is updated by push:
        DESCRIPTION: Verify that the event name and time are displayed
        DESCRIPTION: Verify that data update  or the event is suspended by push
        EXPECTED: In HR page - EDP the event info is updated by push
        """
        pass
