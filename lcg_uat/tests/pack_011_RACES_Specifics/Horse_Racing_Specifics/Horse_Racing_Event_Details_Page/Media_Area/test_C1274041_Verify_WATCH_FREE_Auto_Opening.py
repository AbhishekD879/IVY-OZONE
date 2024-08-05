import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.watch_free
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1274041_Verify_WATCH_FREE_Auto_Opening(BaseRacing):
    """
    TR_ID: C1274041
    NAME: Verify WATCH FREE Auto Opening
    DESCRIPTION: This test case verifies visualization (LiveSim) auto opening on Event Details page under Media Area
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """

    keep_browser_open = True

    def test_000_create_events(self):
        """
        DESCRIPTION: Add racing event with start time more than 5 minutes to UK & IRE, International and Virtual types
        EXPECTED: Racing event added
        """
        event_params = self.ob_config.add_UK_racing_event(time_to_start=6)
        self.__class__.eventID, self.__class__.event_off_time, self.__class__.marketID, self.__class__.selection_ids =\
            event_params.event_id, event_params.event_off_time, event_params.market_id, event_params.selection_ids
        self.__class__.created_event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'
        self._logger.info(f'*** Created event with ID {self.eventID}')
        self.__class__.brand_is_ladbrokes = self.brand == 'ladbrokes'
        self.__class__.device_is_mobile = self.device_type == 'mobile'

    def test_001_go_to_the_event_details_page_of_a_race_from_uk_ire_group_when_it_is_more_than_5_minutes_left_before_the_race_off_time(self):
        """
        DESCRIPTION: Go to the event details page of a race (from 'UK & IRE' group) when it is **more than 5 minutes** left before the race off time
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_navigate_to_media_area(self):
        """
        DESCRIPTION: Navigate to media area
        EXPECTED: * Media area consists of 'WATCH FREE' button filling all available width
        EXPECTED: * Button 'WATCH FREE' is inActive by default
        """
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(self.horse_racing_edp.has_watch_free_button(),
                        msg=f'Watch Free button was not found for event "{self.created_event_name}"')
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(
                         expected_result=False),
                         msg='Watch Free button is active')

    def test_003_stay_on_event_details_page_and_verify_visualisations_automatic_launching_if_it_is_5_minutes_left_before_the_race_off_time(self):
        """
        DESCRIPTION: Stay on Event Details page and verify Visualisations automatic launching if it is **5 minutes** left before the race off time
        EXPECTED: *   The area below 'WATCH FREE' button is expanded automatically
        EXPECTED: *   Visualisation video object is shown
        EXPECTED: *   Visualisation video is playing
        EXPECTED: * An information link labeled "Find out more about Watch Free here" appears below Race information on the page
        """
        self.horse_racing_edp.watch_free_button.click()
        self.site.wait_splash_to_hide(2)
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')
        if not self.brand_is_ladbrokes and self.device_is_mobile:
            self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                            msg='Watch Free info link is not present')

    def test_004_go_to_the_event_details_page_of_a_race_from_uk__ire_group_when_it_isless_than_5_minutesleft_before_the_race_off_time(self):
        """
        DESCRIPTION: Go to the event details page of a race (from 'UK & IRE' group) when it is **less than 5 minutes **left before the race off time
        EXPECTED: *   Event Details page is opened
        EXPECTED: *   The area below 'WATCH FREE' button is expanded automatically
        EXPECTED: *   Visualisation video object is shown
        EXPECTED: *   Visualisation video is playing
        EXPECTED: * An information link labeled "Find out more about Watch Free here" appears below Race information on the page
        """
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='HomePage', timeout=5)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.horse_racing_edp.watch_free_button.click()
        self.site.wait_splash_to_hide(2)
        self.assertTrue(self.horse_racing_edp.watch_free_area,
                        msg='Visualisation video is not shown')
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg='Watch Free button is not active')
        if not self.brand_is_ladbrokes and self.device_is_mobile:
            self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                            msg='Watch Free info link is not present')

    def test_005_login(self):
        """
        DESCRIPTION: Login to Oxygen application
        EXPECTED: User successfully logged
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_006_repeat_steps_1_5(self):
        """
        DESCRIPTION: Go to UK_IRE event page and repeat steps #1-5 for logged in user
        EXPECTED: All validations from steps #1-4 are pass
        """
        self.test_000_create_events()
        self.test_001_go_to_the_event_details_page_of_a_race_from_uk_ire_group_when_it_is_more_than_5_minutes_left_before_the_race_off_time()
        self.test_002_navigate_to_media_area()
        self.test_003_stay_on_event_details_page_and_verify_visualisations_automatic_launching_if_it_is_5_minutes_left_before_the_race_off_time()
        self.test_004_go_to_the_event_details_page_of_a_race_from_uk__ire_group_when_it_isless_than_5_minutesleft_before_the_race_off_time()
