from datetime import datetime
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter
import tests
import re
import pytest
from crlat_ob_client.utils.date_time import validate_time
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.crl_prod  # Coral only
@pytest.mark.crl_hl
@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.user_journey_single_horse_race
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.race_form
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.races
@pytest.mark.high
@pytest.mark.reg158_fix
@pytest.mark.reg161_fix
@vtest
class Test_C1049082_Verify_Event_Details_Page(BaseRacing):
    """
    TR_ID: C1049082
    NAME: Verify Event Details Page
    DESCRIPTION: This test case verifies <Horse Racing> Event Details Page
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        if cls.virtual_races_enabled == 'Yes':
            cms_config.update_system_configuration_structure(config_item='NextRaces',
                                                             field_name='isVirtualRacesEnabled',
                                                             field_value='Yes')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Racing event with form info in SiteServe response
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(distance=True, going=True)
        if not self.event_info:
            raise SiteServeException('Racing events with distance and going details are not available')
        self.__class__.event_id = list(self.event_info.keys())[0]

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing Page
        EXPECTED: 'Horse Racing' Landing Page is loaded
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('HorseRacing')

    def test_002_verify_breadcrumbs_on_event_details_page_when_navigating_from_next_races_module(self):
        """
        DESCRIPTION: Verify Breadcrumbs on event details page when navigating from 'Next Races' module
        EXPECTED: Mobile&Tablet:
        EXPECTED: *Breadcrumbs are in format: 'Horse Racing' / 'Next Races'
        EXPECTED: *'Down' arrow right next to 'Horse Racing'/'Next Races' in breadcrumbs is available
        EXPECTED: Desktop:
        EXPECTED: *Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Horse racing' / '[Event Name]'
        """
        self.__class__.virtual_races_enabled = \
            self.cms_config.get_system_configuration_structure()['NextRaces']['isVirtualRacesEnabled']
        if self.virtual_races_enabled == 'Yes':
            self.cms_config.update_system_configuration_structure(config_item='NextRaces',
                                                                  field_name='isVirtualRacesEnabled',
                                                                  field_value='No')
            wait_for_haul(60)
            self.device.refresh_page()
            wait_for_haul(30)
        if tests.settings.backend_env != 'prod':
            autotest_event = self.get_event_from_next_races_module(event_name=self.event_name_10min.upper())
            autotest_event.click()

            self.site.wait_content_state(state_name='RacingEventDetails')

            breadcrumbs = list(self.site.racing_event_details.breadcrumbs.items_as_ordered_dict.keys())

            if self.device_type in ['mobile', 'tablet']:
                expected_breadcrumbs = ['Horse Racing', 'Next Ra...']
                self.assertEqual(breadcrumbs, expected_breadcrumbs, msg=f'Breadcrumbs "{breadcrumbs}" are not the '
                                                                        f'same as expected "{expected_breadcrumbs}"')
                self.assertTrue(self.site.racing_event_details.breadcrumbs.toggle_icon.is_displayed(),
                                msg='Toggle icon is not displayed')
            else:
                expected_breadcrumbs = ['Home', 'Horse Racing', self.horseracing_autotest_uk_name_pattern.replace('-', ' ')]
                self.assertEqual(expected_breadcrumbs, breadcrumbs, msg=f'Breadcrumbs {breadcrumbs} are not the '
                                                                        f'same as expected {expected_breadcrumbs}')
        else:
            next_races = self.get_next_races_section()
            events = next_races.items_as_ordered_dict
            self.assertTrue(events, msg='No events were found in Next races section')
            _, event = list(events.items())[0]
            event.click()
            self.site.wait_content_state_changed()

            breadcrumbs = list(self.site.racing_event_details.breadcrumbs.items_as_ordered_dict.keys())

            if self.device_type in ['mobile', 'tablet']:
                expected_breadcrumbs = ['Horse Racing', 'Next Ra...']
                self.assertEqual(breadcrumbs, expected_breadcrumbs, msg=f'Breadcrumbs "{breadcrumbs}" are not the '
                                                                        f'same as expected "{expected_breadcrumbs}"')
                self.assertTrue(self.site.racing_event_details.breadcrumbs.toggle_icon.is_displayed(),
                                msg='Toggle icon is not displayed')
            else:
                expected_breadcrumbs = ['Home', 'Horse Racing']
                self.assertEqual(expected_breadcrumbs, breadcrumbs[:-1],
                                 msg=f'Breadcrumbs {breadcrumbs[:-1]} are not the'
                                     f'same as expected {expected_breadcrumbs}')

    def test_003_verify_breadcrumbs_on_event_details_page_when_navigating_not_from_next_races_module(self):
        """
        DESCRIPTION: Verify Breadcrumbs on event details page when navigating NOT from 'Next Races' module
        EXPECTED: Mobile&Tablet:
        EXPECTED: *Breadcrumbs are displayed on a subheader in the format: 'Horse Racing / [Event Name]'
        EXPECTED: *Down' arrow right next to '[Event Name]' in breadcrumbs is available
        EXPECTED: Desktop:
        EXPECTED: *Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Horse racing' / '[Event Name]'
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.event_name = normalize_name(self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)[0]['event']['typeName'])
        breadcrumbs = self.site.racing_event_details.breadcrumbs.items_as_ordered_dict
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

        breadcrumbs = list(breadcrumbs.keys())

        if self.device_type in ['mobile', 'tablet']:
            expected_breadcrumbs_0 = 'Horse Racing'
            expected_breadcrumbs_1 = self.event_name[:7] + '...' if len(self.event_name) > 7 else self.event_name
            self.assertEqual(breadcrumbs[0], expected_breadcrumbs_0,
                             msg=f'Breadcrumbs "{breadcrumbs[0]}" are not the '
                                 f'same as expected "{expected_breadcrumbs_0}"')
            self.assertEqual(breadcrumbs[1], expected_breadcrumbs_1,
                             msg=f'Breadcrumbs "{breadcrumbs[1]}" are not the '
                                 f'same as expected "{expected_breadcrumbs_1}"')
            self.assertTrue(self.site.racing_event_details.breadcrumbs.toggle_icon.is_displayed(),
                            msg='Toggle icon is not displayed')
        else:
            expected_breadcrumbs = ['Home', 'Horse Racing', self.event_name]
            self.assertEqual(expected_breadcrumbs, breadcrumbs, msg=f'Breadcrumbs {breadcrumbs} are not the '
                                                                    f'same as expected {expected_breadcrumbs}')

    def test_004_verify_event_details_page_subheader_for_desktop(self):
        """
        DESCRIPTION: Verify Event details page subheader for DESKTOP
        EXPECTED: Event name consists of two parts: "event name" + "day of the week, day and month" (e.g. Cheltenham Wednesday 12th November) is left-alligned on the page subheader
        EXPECTED: 'Meetings' link and 'up' & 'down' arrows are shown right-aligned on the page subheader
        """
        if self.device_type in ['desktop']:
            event_time = self.site.racing_event_details.sub_header.event_time
            dt = datetime.strptime(self.event_info[self.event_id]['obStartTime'], '%Y-%m-%dT%H:%M:%S')
            event_day = int(dt.strftime('%d'))
            if 4 <= event_day <= 20 or 24 <= event_day <= 30:
                suffix = 'th'
            else:
                suffix = ['st', 'nd', 'rd'][event_day % 10 - 1]
            formatted_date = dt.strftime(f'%A %d{suffix} %B')
            parts_of_event_time = event_time.split()
            if len(parts_of_event_time[1]) == 3:
                parts_of_event_time[1] = '0' + parts_of_event_time[1]
            event_time = ' '.join(parts_of_event_time)
            validate_time(actual_time=event_time, format_pattern=formatted_date)
            self.assertTrue(self.site.racing_event_details.sub_header.meeting_selector.is_displayed(),
                            msg='Meeting list is not shown on the page')

            meeting_name = self.site.racing_event_details.sub_header.meeting_name
            self.assertEqual(meeting_name, self.event_name.upper(),
                             msg=f'Meeting name "{meeting_name}" is not the same '
                                 f'as expected "{self.event_name.upper()}"')

    def test_005_verify_distance(self):
        """
        DESCRIPTION: Verify Distance
        EXPECTED: * Race distance is present below the times ribbon
        EXPECTED: * The format of Race distance is: 'Distance: Xm Yf Zy'
        """
        expected_distance = self.event_info[self.event_id]['distance'].replace(' ', '')
        distance = self.site.racing_event_details.tab_content.race_details.race_distance
        actual_distance = distance.value.replace(' ', '')
        self.assertEqual(actual_distance, expected_distance,
                         msg=f'Event distance "{actual_distance}" is not the same '
                             f'as got from SiteServe response "{expected_distance}"')

    def test_006_verify_horse_racing_event_status(self):
        """
        DESCRIPTION: Verify 'Horse Racing' Event Status
        EXPECTED: * Race Event Status is displayed next to Distance
        EXPECTED: * If Race Event Status is not available, no blank or additional space is left
        """
        self.assertTrue(self.site.racing_event_details.tab_content.race_details.has_race_going(),
                    msg='Going status should be present, but it is not')
        going = self.site.racing_event_details.tab_content.race_details.race_going
        self.assertEqual(going.value.upper(), self.event_info[self.event_id]['going'].upper(),
                         msg=f"Event going label {going.value.upper()} is not the same as expected {self.event_info[self.event_id]['going'].upper()}")

    def test_007_verify_racing_post_verdict_icon_if_available(self):
        """
        DESCRIPTION: Verify 'Racing Post | Verdict' icon (if available)
        """
        self.assertTrue(self.site.racing_event_details.tab_content.has_post_info(),
                        msg='Racing Post info section is not found')
        self.assertTrue(self.site.racing_event_details.tab_content.post_info.has_logo_icon(),
                        msg='Racing Post logo icon is not found')

    def test_008_verify_summary_if_available(self):
        """
        DESCRIPTION: Verify 'Summary' (if available)
        EXPECTED: For **Desktop&Tablet:**
        EXPECTED: *  Summary text is fully shown
        EXPECTED: For **Mobile:**
        EXPECTED: *  100 symbols text is shown, the rest text is cut by '...'
        EXPECTED: *  'Show More' link is shown after '...' symbols
        """
        # This step is covered in C10436245

    def test_009_tap_on_show_more_link_if_available(self):
        """
        DESCRIPTION: Tap on 'Show More' link (if available)
        EXPECTED: *   Race information section expanded
        EXPECTED: *   'Show More' link changed into 'Show Less' link after tapping on it
        """
        # This step is covered in C10436245

    def test_010_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'Show Less' link
        EXPECTED: Race information section collapsed
        EXPECTED: 'Show Less' link changed into 'Show More' link
        """
        # This step is covered in C10436245
