import pytest
from crlat_ob_client.utils.date_time import validate_time

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.races
@vtest
class Test_C28837_Verify_Event_Details_Page(BaseGreyhound):
    """
    TR_ID: C28837
    NAME: Verify Greyhound Event Details Page
    DESCRIPTION: This test case verifies Greyhound Event Details Page
    """
    keep_browser_open = True

    @classmethod
    def custom_setUp(cls):
        ob_config = cls.get_ob_config()
        cls.get_ss_config()
        if tests.settings.backend_env != 'prod':
            cls.suspend_old_events(class_ids=ob_config.backend.ti.greyhound_racing.class_ids)
        if tests.settings.cms_env != 'prd0':
            cls.setup_cms_next_races_number_of_events()

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        if cls.virtual_races_enabled == 'Yes':
            cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                             field_name='isVirtualRacesEnabled',
                                                             field_value='Yes')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get greyhound event
        """
        cms_initial_data = self.get_initial_data_system_configuration().get('RacingDataHub')
        if not cms_initial_data:
            cms_initial_data = self.cms_config.get_system_configuration_item('RacingDataHub')
        if not cms_initial_data:
            raise CmsClientException('RacingDataHub section not found in System Config')
        self.__class__.datafabric_enabled = cms_initial_data.get('isEnabledForGreyhound') is True

        if self.datafabric_enabled and tests.settings.backend_env == 'prod':
            params = self.get_event_details(datafabric_data=True)
            self.__class__.verdict = params.verdict
            self.__class__.expected_distance = params.distance
            self.__class__.status = params.datafabric_data['raceType']
            self.__class__.event_time = params.event_date_time
            self.__class__.type_name = ' '.join(params.event_name.split(' ')[1:]).replace('|', '') if \
                self.device_type == 'desktop' else params.type_name
        elif tests.settings.backend_env == 'prod':
            race_info = self.get_initial_data_system_configuration().get('raceInfo')
            if not race_info:
                race_info = self.cms_config.get_system_configuration_item('raceInfo')
            if not race_info or not race_info.get('timeFormEnabled'):
                raise CmsClientException('Time Form is disabled in CMS')
            params = self.get_event_details(time_form_info=True)
            self.__class__.verdict = params.verdict
            self.__class__.expected_distance = params.distance
            self.__class__.status = params.grade
            self.__class__.event_time = params.event_date_time
            self.__class__.type_name = ' '.join(params.event_name.split(' ')[1:]).replace('|', '') if \
                self.device_type == 'desktop' else params.type_name
        else:
            params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, time_to_start=6)
            event_off_time = params.event_off_time
            self.__class__.expected_distance = False
            self.__class__.status = False
            self.__class__.verdict = False
            self.__class__.created_event_name = f'{event_off_time} {self.greyhound_autotest_name_pattern.upper()}'
            self.__class__.nr_event_time = params.event_date_time

        self.__class__.eventID = params.event_id

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page
        EXPECTED: Landing page is opened
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_002_verify_breadcrumbs_on_next_races_event_details_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs on next races event details page
        EXPECTED: Mobile&Tablet:
        EXPECTED: Breadcrumbs are in format: 'Greyhound / Next Races'
        EXPECTED: 'Down' arrow right next to 'Greyhound'/'Next Races' in breadcrumbs is available
        EXPECTED: Desktop:
        EXPECTED: Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Greyhound racing' / '[Event Name]'
        """
        current_tab = self.site.greyhound.tabs_menu.current
        if current_tab != 'NEXT RACES' and self.brand == 'ladbrokes':
            self.site.greyhound.tabs_menu.click_button(button_name='NEXT RACES')
        self.__class__.virtual_races_enabled = \
        self.cms_config.get_system_configuration_structure()['GreyhoundNextRaces']['isVirtualRacesEnabled']
        if self.virtual_races_enabled == 'Yes':
            self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                                  field_name='isVirtualRacesEnabled',
                                                                  field_value='No')
            wait_for_haul(60)
            self.device.refresh_page()
        if tests.settings.backend_env != 'prod':
            if self.brand != 'ladbrokes':
                event = self.get_event_from_next_races_module(event_name=self.created_event_name)
                event.click()
            else:
                result = self.site.greyhound.tab_content.grouping_buttons.click_button(
                    vec.sb.SPORT_DAY_TABS.today.upper())
                self.assertTrue(result, msg=f'Current tab "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                                            f'is not the same as expected "{vec.sb.SPORT_DAY_TABS.today.upper()}"')
                events = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(events, msg='There\'s no greyhound events')
                event = events.get(self.created_event_name)
                self.assertTrue(event, msg=f'Event "{self.created_event_name}" is not found')
                event.header.click()

            self.site.wait_content_state(state_name='GreyHoundEventDetails')

            breadcrumbs = list(self.site.greyhound_event_details.breadcrumbs.items_as_ordered_dict.keys())

            if self.device_type in ['mobile', 'tablet']:
                expected_breadcrumbs = ['Greyhounds', 'Next Races']
                self.assertEqual(breadcrumbs, expected_breadcrumbs, msg=f'Breadcrumbs {breadcrumbs} are not the '
                                                                        f'same as expected {expected_breadcrumbs}')
                self.assertTrue(self.site.greyhound_event_details.breadcrumbs.toggle_icon.is_displayed(),
                                msg='Toggle icon is not displayed')
            else:
                breadcrumbs_cap = breadcrumbs
                expected_breadcrumbs = ['Home', 'Greyhound racing', self.greyhound_autotest_name_pattern]
                self.assertEqual(expected_breadcrumbs, breadcrumbs_cap,
                                 msg=f'Breadcrumbs {breadcrumbs_cap} are not the same '
                                     f'as expected {expected_breadcrumbs}')
        else:
            if self.brand == 'ladbrokes':
                current_tab = self.site.greyhound.tabs_menu.current
                self.assertEqual(current_tab, vec.racing.RACING_NEXT_RACES_NAME,
                                 msg=f'Currently opened tab is "{current_tab}" '
                                     f'instead of "{vec.racing.RACING_NEXT_RACES_NAME}"')
                events = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            else:
                next_races = self.get_next_races_section()
                events = next_races.items_as_ordered_dict

            self.assertTrue(events, msg='No events were found in Next races section')
            event = list(events.values())[-1]
            event.header.click() if self.brand == 'ladbrokes' else event.click()
            self.site.wait_content_state(state_name='GreyHoundEventDetails')

            breadcrumbs = list(self.site.greyhound_event_details.breadcrumbs.items_as_ordered_dict.keys())

            if self.device_type in ['mobile', 'tablet']:
                expected_breadcrumbs = ['Greyhounds', 'Next Ra...']
                self.assertEqual(breadcrumbs, expected_breadcrumbs, msg=f'Breadcrumbs "{breadcrumbs}" are not the '
                                                                        f'same as expected "{expected_breadcrumbs}"')
                self.assertTrue(self.site.greyhound_event_details.breadcrumbs.toggle_icon.is_displayed(),
                                msg='Toggle icon is not displayed')
            else:
                expected_breadcrumbs = ['Home', 'Greyhound racing']
                self.assertEqual(expected_breadcrumbs, breadcrumbs[:-1],
                                 msg=f'Breadcrumbs {breadcrumbs[:-1]} are not the '
                                     f'same as expected {expected_breadcrumbs}')

    def test_003_verify_event_details_page_subheader(self):
        """
        DESCRIPTION: Verify event details page subheader
        EXPECTED: Mobile&Tablet:
        EXPECTED: Breadcrumbs are displayed on a subheader in format:
        EXPECTED: For meetings: 'Greyhound / [Event Name]'
        EXPECTED: 'Down' arrow right next to '[Event Name]'/'Next Races' in breadcrumbs is available
        EXPECTED: Desktop:
        EXPECTED: Event name consists of two parts: "event name" + "day of the week, day and month" (e.g. Cheltenham Wednesday 12th November) is left-alligned on the page subheader
        EXPECTED: 'Meetings' link and 'up' & 'down' arrows are shown right-aligned on the page subheader
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

        if self.device_type in ['mobile', 'tablet']:
            if tests.settings.backend_env != 'prod':
                expected_breadcrumbs = ['Greyhounds', self.greyhound_autotest_name_pattern]
            else:
                if len(self.type_name) > 7:
                    expected_breadcrumbs = ['Greyhounds', self.type_name[:7] + '...']
                else:
                    expected_breadcrumbs = ['Greyhounds', self.type_name]

            breadcrumbs = list(self.site.greyhound_event_details.breadcrumbs.items_as_ordered_dict.keys())
            self.assertEqual(expected_breadcrumbs, breadcrumbs,
                             msg=f'Breadcrumbs "{breadcrumbs}" are not the same as expected "{expected_breadcrumbs}"')
            self.assertTrue(self.site.greyhound_event_details.breadcrumbs.toggle_icon.is_displayed(),
                            msg='Toggle icon is not displayed')
        else:
            event_time = self.site.greyhound_event_details.sub_header.event_time
            breadcrumbs = list(self.site.greyhound_event_details.breadcrumbs.items_as_ordered_dict.keys())

            format_pattern = self.get_time_format_pattern_for_desktop(event_time)
            validate_time(actual_time=event_time, format_pattern=format_pattern)

            self.assertTrue(self.site.greyhound_event_details.sub_header.meeting_selector.is_displayed(),
                            msg='Meeting list is not shown on the page')

            breadcrumbs_cap = breadcrumbs
            if tests.settings.backend_env != 'prod':
                expected_breadcrumbs = ['Home', 'Greyhound racing', self.greyhound_autotest_name_pattern]
            else:
                expected_breadcrumbs = ['Home', 'Greyhound racing', self.type_name.replace(' DG', '')]
            self.assertEqual(expected_breadcrumbs, breadcrumbs_cap, msg=f'Breadcrumbs {breadcrumbs_cap} are not the '
                                                                        f'same as expected {expected_breadcrumbs}')

    def test_004_verify_distance(self):
        """
        DESCRIPTION: Verify distance
        EXPECTED: Race distance is present next to event name and displayed via '/'
        EXPECTED: The format of Race distance is : 'Distance: Xm'
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

        if self.expected_distance:
            self.assertTrue(self.site.greyhound_event_details.tab_content.race_details.has_race_distance(),
                            msg='Distance not found')
            distance = self.site.greyhound_event_details.tab_content.race_details.race_distance
            expected_distance = f'{self.expected_distance}m'
            self.assertEqual(distance.name, expected_distance,
                             msg=f'Event distance "{distance.name}" is not the same '
                                 f'as got from response "{expected_distance}"')
        else:
            self._logger.warning('*** No distance available, skipping the verification')

    def test_005_verify_event_status(self):
        """
        DESCRIPTION: Verify Race Event Status
        EXPECTED: Coral:
        EXPECTED: Race Grade is displayed under Event Name and distance
        EXPECTED: If Race Grade is not available, no blank or additional space is left
        EXPECTED: Ladbrokes:
        EXPECTED: Race Type is displayed under Event Name and to the right of race distance
        """
        if self.status:
            status_object = self.site.greyhound_event_details.tab_content.grade
            actual_status = status_object.name if self.brand == 'ladbrokes' else status_object.value
            self.assertEqual(actual_status, self.status,
                             msg=f'Race grade "{actual_status}" is not the same as expected "{self.status}"')
        else:
            self._logger.warning('*** No race grade available, skipping the verification')

    def test_006_verify_timeform_label(self):
        """
        DESCRIPTION: Verify 'Timeform' label (if available)
        EXPECTED: For **mobile&tablet:
        EXPECTED: ** 'Timeform' label has left alignment and located under event status
        EXPECTED: For desktop:
        EXPECTED: 'Timeform' label has located in the second column of the display area
        """
        if self.datafabric_enabled or tests.settings.backend_env != 'prod':
            self._logger.warning('*** Skipping verification, timeform is not available')
            return

        self.assertTrue(self.site.greyhound_event_details.tab_content.timeform_overview.logo_icon,
                        msg='Timeform label is not shown')

    def test_007_verify_summary_if_available(self):
        """
        DESCRIPTION: Verify 'Summary' (if available)
        EXPECTED: For Desktop&Tablet:
        EXPECTED: * Summary text is fully shown
        EXPECTED: For Mobile:
        EXPECTED: *100 symbols text is shown, the rest text is cut by '...'
        EXPECTED: *'Show More' link is shown after '...' symbols
        """
        if self.datafabric_enabled or tests.settings.backend_env != 'prod':
            self._logger.warning('*** Skipping verification, timeform is not available')
            return

        if self.verdict:
            self.__class__.timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview
            if self.device_type == 'mobile':
                self.assertTrue(self.timeform_overview.summary_text.is_truncated(), msg='Summary text is not truncated')
                self.assertTrue(self.timeform_overview.has_summary_button, msg='No Show More button found')
            else:
                self.assertFalse(self.timeform_overview.summary_text.is_truncated(), msg='Summary text is truncated')
        else:
            self._logger.warning('*** No "Summary" text available, skipping the verification')

    def test_008_tap_on_show_more_link(self):
        """
        DESCRIPTION: Tap on 'Show More' link (if available)
        EXPECTED: Race information section expanded
        EXPECTED: 'Show More' link changed into 'Show Less' link after tapping on it
        """
        if self.datafabric_enabled or tests.settings.backend_env != 'prod':
            self._logger.warning('*** Skipping verification, timeform is not available')
            return

        if self.verdict:
            if self.device_type == 'mobile':
                expected_button_name = 'Show Less'
                self.timeform_overview.show_summary_button.click()
                result = wait_for_result(
                    lambda: self.timeform_overview.show_summary_button.name == expected_button_name,
                    name=f'Button to have name {expected_button_name}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{self.timeform_overview.show_summary_button.name}" '
                                            f'is not the same as expected "{expected_button_name}"')
                self.assertFalse(self.timeform_overview.summary_text.is_truncated(),
                                 msg='Summary text is still truncated')
            else:
                self._logger.warning('*** Show More link is not supposed to be shown on Desktop and Tablet')
        else:
            self._logger.warning('*** No "Summary" text available, skipping the verification')

    def test_009_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'Show Less' link
        EXPECTED: Race information section collapsed
        EXPECTED: 'Show Less' link changed into 'Show More' link
        """
        if self.datafabric_enabled or tests.settings.backend_env != 'prod':
            self._logger.warning('*** Skipping verification, timeform is not available')
            return

        if self.verdict:
            if self.device_type in ['mobile']:
                expected_button_name = 'Show More'
                self.timeform_overview.show_summary_button.click()
                result = wait_for_result(
                    lambda: self.timeform_overview.show_summary_button.name == expected_button_name,
                    name=f'Button to have name {expected_button_name}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{self.timeform_overview.show_summary_button.name}" '
                                            f'is not the same as expected "{expected_button_name}"')
                self._logger.debug(f'*** Summary text value "{self.timeform_overview.summary_text.value}"')
                self.assertTrue(self.timeform_overview.summary_text.is_truncated(), msg='Summary text is not truncated')
            else:
                self._logger.warning('*** Show More link is not supposed to be shown on Desktop and Tablet')
        else:
            self._logger.warning('*** No "Summary" text available, skipping the verification')
