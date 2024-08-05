import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C539917_Tracking_of_Horse_Racing_Streaming_Simulation(Common):
    """
    TR_ID: C539917
    NAME: Tracking of Horse Racing Streaming Simulation
    DESCRIPTION: This test case verifies tracking of Horse Racing Streaming Simulation
    PRECONDITIONS: * Test case should be run on **Mobile, Tablet, Desktop and Wrappers**
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Make sure there is mapped race visualization for tested event
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_horse_racing_icon_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on Module selector ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_go_to_the_hr_event_details_page_of_event_from_uk__ire_group_more__that_15_minutes_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Go to the HR event details page of event from 'UK & IRE' group more  that 15 minutes before the scheduled race-off time
        EXPECTED: * 'Watch Free' button is inactive by default
        """
        pass

    def test_004_tap_watch_free_button(self):
        """
        DESCRIPTION: Tap 'Watch Free' button
        EXPECTED: * Visualization video object is shown
        EXPECTED: * Pre sim visualization is launched
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: The following event with corresponding parameters is present in data layer object:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'watch pre sim',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        EXPECTED: where, parameters 'sportID', 'typeID' and 'eventID' correspond to event that pre sim was launched for
        """
        pass

    def test_006_collapse_visualization_video_object_and_repeat_steps_4_5(self):
        """
        DESCRIPTION: Collapse Visualization video object and repeat steps #4-5
        EXPECTED: The following event is NOT present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'watch pre sim',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        """
        pass

    def test_007_go_to_hr_event_details_page_of_event_from_uk__ire_group_if_it_is_5_minutes_left_before_the_race_off_time(self):
        """
        DESCRIPTION: Go to HR event details page of event from 'UK & IRE' group if it is 5 minutes left before the race off time
        EXPECTED: * The area below 'WATCH FREE' button is expanded automatically
        EXPECTED: * Visualization video object is shown
        EXPECTED: * Live sim visualization video is playing
        """
        pass

    def test_008_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: The following event with corresponding parameters is present in data layer object:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'onload',
        EXPECTED: 'eventLabel' : 'watch live sim',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        EXPECTED: where, parameters 'sportID', 'typeID' and 'eventID' correspond to event that live sim was launched for
        """
        pass

    def test_009_collapse_visualization_video_object_expand_it_again_and_repeat_step_8(self):
        """
        DESCRIPTION: Collapse Visualization video object, expand it again and repeat step #8
        EXPECTED: The following event is NOT present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'onload',
        EXPECTED: 'eventLabel' : 'watch live sim',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        """
        pass

    def test_010_log_in_and_repeat_steps_3_9(self):
        """
        DESCRIPTION: Log in and repeat steps #3-9
        EXPECTED: 
        """
        pass
