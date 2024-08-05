import voltron.environments.constants as vec
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
@pytest.mark.safari
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C1274042_Verify_WATCH_FREE_for_Not_Started_Race(BaseRacing):
    """
    TR_ID: C1274042
    NAME: Verify WATCH FREE for Not Started Race
    DESCRIPTION: This test case verifies visualization (LiveSim) for Not Started Race on Event Details page under Media Area.
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Event is NOT started yet
    PRECONDITIONS: *   Make sure there is mapped race visualization for tested event
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """
    keep_browser_open = True

    def test_000_create_events(self):
        """
        DESCRIPTION: Add racing event with start time more than 5 minutes to UK & IRE, International and Virtual types
        EXPECTED: Racing event added
        """
        event_params = self.ob_config.add_UK_racing_event(time_to_start=15)
        self.__class__.eventID, self.__class__.event_off_time, self.__class__.marketID, self.__class__.selection_ids = \
            event_params.event_id, event_params.event_off_time, event_params.market_id, event_params.selection_ids
        self._logger.info(f'*** Created event with ID {self.eventID}')
        self.__class__.created_event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'
        self.__class__.brand_is_ladbrokes = self.brand == 'ladbrokes'
        self.__class__.device_is_mobile = self.device_type == 'mobile'

    def test_001_go_to_the_event_details_page_of_verified_event_from_uk__ire_groupmore_that_15_minutes_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Go to the event details page of verified event (from 'UK & IRE' group) **more **that 15 minutes before the scheduled race-off time
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of 'WATCH FREE' button filling all available width
        EXPECTED: * Button 'WATCH FREE' is inActive by default
        EXPECTED: **For Desktop:**
        EXPECTED: * Event details page is opened
        EXPECTED: *   Media area consists of 'WATCH FREE' button aligned from right side
        EXPECTED: *   Button 'WATCH FREE' is inActive by default
        EXPECTED: *   Relevant icon is NOT shown next to the 'WATCH FREE' label
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(self.horse_racing_edp.has_watch_free_button(),
                        msg=f'Watch Free button was not found for event "{self.created_event_name}"')
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(
            expected_result=False),
            msg='Watch Free button is active')

    def test_002_refresh_the_page_if_it_more_then_5_minutes_left_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Refresh the page if it **more** then 5 minutes left before the scheduled race-off time
        EXPECTED: The area below 'WATCH FREE' button is collapsed
        EXPECTED: 'WATCH FREE' button is inActive
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(
            expected_result=False),
            msg='Watch Free button is active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertFalse(result, msg='Visualisation video is shown')

    def test_003_click_tap_inactive_watch_free_button(self):
        """
        DESCRIPTION: Click/Tap inActive 'WATCH FREE' button
        EXPECTED: *   The area below 'WATCH FREE' button is expanded
        EXPECTED: *   'WATCH FREE' button becomes Active
        EXPECTED: *   Content of Quantum Leap iFrame is shown
        EXPECTED: *   Visualisation is shown for logged out user
        EXPECTED: *   An information link labeled "Find out more about Watch Free here" appears under Media Area on the page **for Mobile/Tablet**
        EXPECTED: *   "Find out more about Watch Free here" widget is displayed in the 3rd column or below the event card **for Desktop**
        EXPECTED: *   NOTE: An information link labeled "Find out more about Watch Free here" removed for Ladbrokes - BMA-44862
        """
        self.horse_racing_edp.watch_free_button.click()
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg='Watch Free button is not active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')
        if not self.brand_is_ladbrokes:
            if self.device_is_mobile:
                self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                                msg='Watch Free info link is not present')
                link_text = self.horse_racing_edp.watch_free_info_link.name
                self.assertEqual(link_text, vec.sb.WATCH_FREE_INFORMATION,
                                 msg=f'Link label "{link_text}" is not the same as expected '
                                     f'"{vec.sb.WATCH_FREE_INFORMATION}"')
            if not self.device_is_mobile:
                sections = self.horse_racing_edp.accordions_list.items_as_ordered_dict
                watch_free_widget = sections.get(vec.sb_desktop.WATCH_FREE_HEADER.title())
                self.assertTrue(watch_free_widget, msg=f'Can not find section: "{vec.sb_desktop.WATCH_FREE_HEADER}"')

    def test_004_click_tap_active_watch_free_button(self):
        """
        DESCRIPTION: Click/Tap Active 'WATCH FREE' button
        EXPECTED: *   The area below 'WATCH FREE' button is collapsed
        EXPECTED: *   'WATCH FREE' button becomes inActive
        EXPECTED: *   The information link is no longer displayed **for Mobile/Tablet**
        EXPECTED: *   "Find out more about Watch Free here" widget is still displayed in the 3rd column or below the event card **for Desktop**
        """
        self.horse_racing_edp.watch_free_button.click()
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                         msg='Watch Free button is active')
        self.assertFalse(self.horse_racing_edp.has_watch_free_info_link(expected_result=False),
                         msg='Watch Free info link is not present')

    def test_005_log_in_app(self):
        """
        DESCRIPTION: Login to Oxygen application
        EXPECTED: User successfully logged
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_006_clicktap_inactive_watch_free_button(self):
        """
        DESCRIPTION: Click/Tap inActive 'WATCH FREE' button
        EXPECTED: *   The area below 'WATCH FREE' button is expanded
        EXPECTED: *   'WATCH FREE' button becomes Active
        EXPECTED: *   Content of Quantum Leap iFrame is shown
        EXPECTED: *   Visualisation is shown for  logged in user
        EXPECTED: *   An information link labeled "Find out more about Watch Free here" appears under Media Area on the page **for Mobile/Tablet**
        EXPECTED: *   "Find out more about Watch Free here" widget is displayed in the 3rd column or below the event card **for Desktop**
        """
        self.assertFalse(self.horse_racing_edp.is_selected(expected_result=False),
                         msg='Watch Free button is active')
        self.horse_racing_edp.watch_free_button.click()
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg='Watch Free button is not active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')
        if not self.brand_is_ladbrokes:
            if self.device_is_mobile:
                link_text = self.horse_racing_edp.watch_free_info_link.name
                self.assertEqual(link_text, vec.sb.WATCH_FREE_INFORMATION,
                                 msg=f'Link label "{link_text}" is not the same as expected '
                                     f'"{vec.sb.WATCH_FREE_INFORMATION}"')
            elif not self.device_is_mobile:
                sections = self.horse_racing_edp.accordions_list.items_as_ordered_dict
                watch_free_widget = sections.get(vec.sb_desktop.WATCH_FREE_HEADER.title())
                self.assertTrue(watch_free_widget, msg=f'Can not find section: "{vec.sb_desktop.WATCH_FREE_HEADER}"')

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: All validations from step #4 are pass
        """
        self.test_004_click_tap_active_watch_free_button()
