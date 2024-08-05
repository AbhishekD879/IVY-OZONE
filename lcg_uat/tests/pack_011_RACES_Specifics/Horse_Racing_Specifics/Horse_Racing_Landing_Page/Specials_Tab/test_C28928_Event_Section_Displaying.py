import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.desktop
@pytest.mark.specials
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.low
@pytest.mark.screen_resolution
@vtest
class Test_C28928_Event_Section_Displaying(BaseRacing):
    """
    TR_ID: C28928
    NAME: Event Section Displaying
    """
    keep_browser_open = True

    @staticmethod
    def get_events_list_from_response(response: list) -> list:
        """
        Having Siteserve response, gets events list, sorted in alphabetical order, ascending
        :param response: Siteserve response (list of dicts)
        :return: list of events sorted in alphabetical order, ascending
        """
        events_list_ss = [[event_resp['event']['name'], event_resp['event']['startTime']] for event_resp in response]
        sorted_event = sorted(events_list_ss, key=lambda x: x[1])

        return [event[0] for event in sorted_event]

    def get_racing_specials_event(self, event_name):
        racing_specials_section = self.sections.get(self.racing_specials_name)
        self.assertTrue(racing_specials_section,
                        msg=f'"{self.racing_specials_name}" section was not found '
                            f'in list of sections: "{", ".join(self.sections.keys())}"')
        racing_specials_events = racing_specials_section.items_as_ordered_dict
        self.assertTrue(racing_specials_events, msg=f'No events found in "{self.racing_specials_name}" section')
        event_with_10_selections = racing_specials_events.get(event_name)
        self.assertTrue(event_with_10_selections,
                        msg=f'Event {event_name} is not found among events: "{", ".join(racing_specials_events.keys())}"')
        return event_with_10_selections

    def test_000_create_events(self):
        """
        DESCRIPTION: Create racing specials events
        EXPECTED: Events are created in OB
        """
        self.__class__.racing_specials_name = vec.racing.RACING_SPECIALS_NAME.title() if self.device_type == 'desktop'\
            else vec.racing.RACING_SPECIALS_NAME
        # first section on page is Price Bomb, we need to have more than 1 event in it for step 3
        self.ob_config.add_price_bomb_racing_event(time_to_start=5)
        self.ob_config.add_price_bomb_racing_event(time_to_start=15)

        self.ob_config.add_mobile_exclusive_racing_event()

        event_params = self.ob_config.add_racing_specials_event(number_of_runners=2, time_to_start=20)
        self.__class__.eventID, self.__class__.event_off_time, self.__class__.selection_ids = \
            event_params.event_id, event_params.event_off_time, event_params.selection_ids
        self.__class__.event_name = f'{self.event_off_time} {self.horseracing_autotest_specials_name_pattern}'
        self._logger.info('*** Event id: %s, event off time: %s, selection ids: %s'
                          % (self.eventID, self.event_off_time, list(self.selection_ids.values())))

        event_params_2 = self.ob_config.add_racing_specials_event(number_of_runners=10, time_to_start=10)
        self.__class__.eventID_2, self.__class__.event_off_time_2, self.__class__.selection_ids_2 = \
            event_params_2.event_id, event_params_2.event_off_time, event_params_2.selection_ids
        self.__class__.event_name_2 = f'{self.event_off_time_2} {self.horseracing_autotest_specials_name_pattern}'
        self._logger.info('*** Event id: %s, event off time: %s, selection ids: %s'
                          % (self.eventID_2, self.event_off_time_2, self.selection_ids_2.values()))

        event_params_3 = self.ob_config.add_racing_specials_event(number_of_runners=9, time_to_start=15)
        self.__class__.eventID_3, self.__class__.event_off_time_3, self.__class__.selection_ids_3 = \
            event_params_3.event_id, event_params_3.event_off_time, event_params_3.selection_ids
        self.__class__.event_name_3 = f'{self.event_off_time_3} {self.horseracing_autotest_specials_name_pattern}'
        self._logger.info('*** Event id: %s, event off time: %s, selection ids: %s'
                          % (self.eventID_3, self.event_off_time_3, self.selection_ids_3.values()))

    def test_001_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_click_tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'SPECIALS' tab
        EXPECTED: 'SPECIALS' tab is opened
        """
        self.site.horse_racing.tabs_menu.click_button('SPECIALS')

    def test_003_open_check_particular_event_section(self):
        """
        DESCRIPTION: Open / check particular event section
        EXPECTED: Events which are related to particular type are shown
        """
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found on Specials page')
        self.__class__.section = self.sections.get(self.racing_specials_name)
        self.assertTrue(self.section,
                        msg=f'"{self.racing_specials_name}" was not found in sections "{", ".join(self.sections.keys())}"')
        self.__class__.events = self.section.items_as_ordered_dict
        self.assertTrue(self.events, msg='No events found on Specials page')

        query = self.ss_query_builder
        query.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'SP'))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus))
        self.__class__.resp = self.ss_req.ss_event_to_outcome_for_class(class_id=self.ob_config.horseracing_config.horse_racing_specials.class_id,
                                                                        query_builder=query)
        expected_events = self.get_events_list_from_response(response=self.resp)
        self.__class__.expected_events = [x.upper() for x in expected_events]
        self._logger.debug('*** Expected events "%s"' % self.expected_events)
        self.assertListEqual(list(self.events.keys()), self.expected_events,
                             msg=f'Actual displayed events:\n"{list(self.events.keys())}"\n expected got '
                             f'from SiteServe response:\n"{self.expected_events}"')

    def test_004_verify_events_ordering(self):
        """
        DESCRIPTION: Verify events ordering
        EXPECTED: Events are ordered by race local time  within one section
        """
        time_disp_order = set([(event['event']['name'], event['event']['startTime']) for event in self.resp])
        events_by_time_order = [x for x, _ in sorted(time_disp_order, key=lambda x: (x[1], x[0]))]
        events = [x for x in self.events if x.title() in events_by_time_order]
        self.assertListEqual(list(self.events.keys()), events,
                             msg=f'Actual displayed events:\n"{list(self.events.keys())}"\n expected got '
                             f'from SiteServe response:\n"{events}"')

    def test_005_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: *   First event section within first Competitions accordion is expanded by default
        EXPECTED: *   All other event sections are collapsed by default
        EXPECTED: *   Event section is expandable / collapsible
        EXPECTED: *   For Mobile:
        EXPECTED: *   Maximum 4 selections are displayed within event section
        EXPECTED: *   'Show all' button is present if there are more than 4 selections within events section
        """
        first_section_name, first_section = list(self.sections.items())[0]
        self.assertTrue(first_section.is_expanded(),
                        msg=f'First section "{first_section_name}" is not expanded by default')
        first_section_events = first_section.items_as_ordered_dict
        first_event_name, self.__class__.first_event = list(first_section_events.items())[0]
        self.assertTrue(self.first_event.is_expanded(timeout=2),
                        msg=f'Event "{first_event_name}" is not expanded by default')

        for event_name, event in list(first_section_events.items())[1:]:
            self.assertFalse(event.is_expanded(),
                             msg=f'Event "{event_name}" is not collapsed by default')

        if not self.device_type == 'desktop':
            self.__class__.event_with_10_selections = self.get_racing_specials_event(event_name=self.event_name_2)
            self.event_with_10_selections.expand()
            selections = self.event_with_10_selections.items_as_ordered_dict
            self.assertEqual(len(selections), 4,
                             msg=f'"{len(selections)}" selections are displayed for event "{self.event_name_2}", '
                             f'but it is expected to have 4 selections displayed after clicking Show All button')
            self.assertTrue(self.event_with_10_selections.has_show_all_button,
                            msg=f'Event "{self.event_name_2}" does not have Show All button')

    def test_006_verify_show_all_button(self):
        """
        DESCRIPTION: Verify 'Show all' button
        EXPECTED: All available selections are present after clicking / tapping 'Show all' button
        """
        self.__class__.event_with_10_selections = self.get_racing_specials_event(event_name=self.event_name_2)
        if self.device_type == 'desktop':
            self.event_with_10_selections.expand()
        self.event_with_10_selections.show_all_button.click()
        self.__class__.event_with_10_selections = self.get_racing_specials_event(event_name=self.event_name_2)
        selections = self.event_with_10_selections.items_as_ordered_dict
        self.assertEqual(len(selections), 10,
                         msg=f'"{len(selections)}" selections are displayed for event "{self.event_name_2}", '
                         f'but it is expected to have 10 selections displayed after clicking Show All button')

    def test_007_verify_event_section_displaying_for_desktop(self):
        """
        DESCRIPTION: Verify event section displaying for Desktop
        EXPECTED: Maximum 9 selections are displayed within event section for 1600 and 1280px screen resolutions
        EXPECTED: *   'Show More' button is present if there are more than 9 selections within events section for 1600 and 1280px screen resolutions
        EXPECTED: *  Maximum 8 selections in two rows are displayed within event section for 1025 and 970px screen resolutions
        EXPECTED: * *   'Show More' button is present if there are more than 8 selections within events section for 1025 and 970px screen resolutions
        """
        if self.device_type == 'desktop':
            self.device.set_viewport_size(width=1600, height=1280)
            self.__class__.event_with_10_selections = self.get_racing_specials_event(event_name=self.event_name_2)
            self.event_with_10_selections.expand()
            self.assertTrue(self.event_with_10_selections.has_show_all_button,
                            msg=f'Event "{self.event_name_2}" does not have Show All button')

            self.device.set_viewport_size(width=1025, height=970)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found on Specials page')
            self.__class__.event_with_9_selections = self.get_racing_specials_event(event_name=self.event_name_3)
            self.event_with_9_selections.expand()
            self.assertTrue(self.event_with_9_selections.has_show_all_button,
                            msg=f'Event "{self.event_name_3}" does not have Show All button')
