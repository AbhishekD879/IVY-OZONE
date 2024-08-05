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
class Test_C236397_Verify_Live_Serv_subscription_for_Commentary_data(Common):
    """
    TR_ID: C236397
    NAME: Verify Live Serv subscription for Commentary data
    DESCRIPTION: This test case verifies the subscription for Commentary data for Live Now event for Football and Tennis events
    PRECONDITIONS: [1] Make sure there is Football and Tennis events available which are live now and for which commentary data is available
    PRECONDITIONS: [2] Make sure that commentary data is not updated yet for events
    PRECONDITIONS: [3] For configurations of live score updates follow the link: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: [4] NOTE, commentary updates are available ONLY for **Live Now** Football and Tennis events
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_go_to_in_play_page___live_now_tab(self):
        """
        DESCRIPTION: Go to 'In Play' page -> 'Live Now' tab
        EXPECTED: 'Live Now' tab is opened
        """
        pass

    def test_003_go_to_football_sport_section_and_find_the_event(self):
        """
        DESCRIPTION: Go to Football sport section and find the event
        EXPECTED: Event is found
        """
        pass

    def test_004_load_the_amelco_inplay_client_and_find_verified_event_by_name_attribute(self):
        """
        DESCRIPTION: Load the Amelco 'inplay' client and find verified event by name attribute
        EXPECTED: Event is shown
        """
        pass

    def test_005_start_the_commentary_updates_for_this_event_start_the_clock(self):
        """
        DESCRIPTION: Start the commentary updates for this event (start the clock)
        EXPECTED: Clock is started
        """
        pass

    def test_006_go_to_front_end_do_not_refresh_the_page_and_check_commentary_data_displaying__match_time__name_of_set__initial_score_if_available(self):
        """
        DESCRIPTION: Go to front end, do not refresh the page and check commentary data displaying:
        DESCRIPTION: - match time / name of set
        DESCRIPTION: - initial score (if available)
        EXPECTED: Nothing is shown
        EXPECTED: Subscription is NOT performed
        """
        pass

    def test_007_refresh_the_page_and_check_the_event(self):
        """
        DESCRIPTION: Refresh the page and check the event
        EXPECTED: Subscription to commentary updates is done
        EXPECTED: Initial commentary data is shown
        """
        pass

    def test_008_trigger_commentary_data_update__change_score_or__change_the_event_period(self):
        """
        DESCRIPTION: Trigger commentary data update:
        DESCRIPTION: - change score OR
        DESCRIPTION: - change the event period
        EXPECTED: Update is processed and shown on the FE
        """
        pass

    def test_009_go_to_footballtennis_sport_icon_from_the_homepage___tap_in_play_tab_and_repeat_steps_2_8(self):
        """
        DESCRIPTION: Go to 'Football'/'Tennis' sport icon from the homepage -> tap 'In-Play' tab and repeat steps #2-8
        EXPECTED: 
        """
        pass

    def test_010_on_homepage_tap_in_play_tab_on_module_selector_ribbon_and_repeat_steps_2_8(self):
        """
        DESCRIPTION: On homepage tap 'In Play' tab on module selector ribbon and repeat steps #2-8
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_8_for_in_play_widget(self):
        """
        DESCRIPTION: Repeat steps #2-8 for In Play widget
        EXPECTED: 
        """
        pass
