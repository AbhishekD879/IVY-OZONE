import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094799_Verify_the_CSS_for_RESULT_status(Common):
    """
    TR_ID: C60094799
    NAME: Verify the CSS for "RESULT" status
    DESCRIPTION: Verify the CSS for "RESULT" status as mentioned in the design
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should be completed
    """
    keep_browser_open = True

    def verify_css_for_result(self, font_family, font_size, font_weight, color):
        result = self.racing_event_details.items_as_ordered_dict.get(self.resulted_event_name)
        self.assertTrue(result.is_resulted,
                        msg=f'Event "{self.resulted_event_name}" is not resulted event')
        actual_font_family = result.event_resulted.value_of_css_property('font-family')
        actual_font_size = result.event_resulted.value_of_css_property('font-size')
        actual_font_weight = result.event_resulted.value_of_css_property('font-weight')
        actual_color = self.rgba_to_hex(result.event_resulted.value_of_css_property('color'))

        self.assertIn(font_family, actual_font_family,
                      msg=f'Required font family :"{font_family}" is not in '
                          f'Actual font family: "{actual_font_family}".')
        self.assertEqual(font_size, actual_font_size,
                         msg=f'Actual font size :"{actual_font_size}" is not same as '
                             f'Expected font size: "{font_size}".')
        self.assertEqual(font_weight, actual_font_weight,
                         msg=f'Actual font weight :"{actual_font_weight}" is not same as '
                             f'Expected font weight: "{font_weight}".')
        self.assertEqual(color, actual_color,
                         msg=f'Actual font color :"{actual_color}" is not same as '
                             f'Expected font color: "{color}".')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create Horse racing event
        """
        class_events = self.get_suspended_event_for_class(class_id=223, return_all_events=True)
        for event in class_events:
            try:
                if event['event']['eventStatusCode'] == 'S' and event['event']['isResulted']:
                    self.__class__.resulted_event_id = event['event']['id']
                    self.__class__.resulted_event_name = event['event']['name'][:5].strip()
                    self._logger.info(f"****{event['event']['name']} is resulted event")
                    break
            except Exception:
                self._logger.info(f"****{event['event']['name']} is not resulted event")
        else:
            raise Exception('Suspended/ Resulted event not found')

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_result_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RESULT" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        self.navigate_to_edp(event_id=self.resulted_event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()
        self.__class__.racing_event_details = self.site.racing_event_details.tab_content.event_off_times_list
        other_races = self.racing_event_details.items_as_ordered_dict
        self.assertTrue(other_races,
                        msg='All other races in that meeting point are displayed for the user to scroll')
        for race_time, race in other_races.items():
            self.assertTrue(race.is_enabled(),
                            msg=f'"{race_time}" is not enabled to click')

    def test_004_validate_result_status_cssindexphpattachmentsget111160934indexphpattachmentsget111160933(self):
        """
        DESCRIPTION: Validate "RESULT" status CSS
        DESCRIPTION: ![](index.php?/attachments/get/111160934)
        DESCRIPTION: ![](index.php?/attachments/get/111160933)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed "RESULT" status.
        EXPECTED: 2: CSS for "RESULT" should be as mentioned in the design
        EXPECTED: .RESULT {
        EXPECTED: font-family: Roboto;
        EXPECTED: font-size: 10px;
        EXPECTED: font-weight: 700;
        EXPECTED: color: #000000;
        EXPECTED: }
        EXPECTED: Coral:
        EXPECTED: CSS
        EXPECTED: .RESULT {
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 9px;
        EXPECTED: font-weight: normal;
        EXPECTED: color: #41494e;
        EXPECTED: }
        """
        event_selected = self.racing_event_details.selected_item
        self.assertEqual(self.resulted_event_name, event_selected,
                         msg=f'Actual Event:"{self.resulted_event_name}" is not same as'
                             f'Expected Event: "{event_selected}"')
        if self.brand == 'bma':
            self.verify_css_for_result(font_family='Lato', font_size='9px', font_weight='400', color='#41494e')
        else:
            self.verify_css_for_result(font_family='Roboto', font_size='10px', font_weight='700', color='#000000')
