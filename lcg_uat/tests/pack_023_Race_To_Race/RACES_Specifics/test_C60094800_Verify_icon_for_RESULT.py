import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Involves creation of horse event not valid for prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094800_Verify_icon_for_RESULT(BaseRacing):
    """
    TR_ID: C60094800
    NAME: Verify icon for "RESULT"
    DESCRIPTION: Verify that icon is displayed before the "RESULT" text
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should be completed
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events
        EXPECTED: Racing events is created
        """
        event_params = self.ob_config.add_international_racing_event(number_of_runners=1)
        eventID = event_params.event_id
        marketID = event_params.market_id
        selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.event_off_time = event_params.event_off_time
        self.ob_config.update_selection_result(event_id=eventID, market_id=marketID,
                                               selection_id=selection_id)

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        # Covered in step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_result_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RESULT" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern
        meeting_name = name.upper() if self.brand != 'ladbrokes' else name
        section = sections.get(self.international_type_name)
        self.assertTrue(section, msg=f'Section: "{self.international_type_name}" is not found')
        meeting = section.items_as_ordered_dict.get(meeting_name)
        self.assertTrue(meeting, msg=f'Meeting: "{meeting_name}" is not found')
        events = meeting.items_as_ordered_dict
        self.assertIn(self.event_off_time, events,
                      msg=f'Event "{self.event_off_time}" was not found in "{events}"')
        event = events.get(self.event_off_time)
        self.assertTrue(event, msg=f'Event: "{self.event_off_time}" is not found')
        event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        event_off_times_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(event_off_times_list, msg='Horse racing events time panel is not displayed')
        event = event_off_times_list.get(self.event_off_time)
        self.assertTrue(event.is_resulted,
                        msg=f'Event : "{self.event_off_time}" is not result')
        result = wait_for_result(lambda: event_off_times_list[self.event_off_time].result, timeout=20)
        actual_font_size = result.css_property_value('font-size')
        self.assertEqual(actual_font_size, '9px' if self.brand == 'bma' else '10px',
                         msg=f'Result font size is not equal to "9px", actual result: "{actual_font_size}"')
        actual_font_family = result.css_property_value('font-family')
        self.assertIn('Lato' if self.brand == 'bma' else 'Roboto Condensed', actual_font_family,
                      msg=f'Result font family is not equal to "Lato", actual result "{actual_font_family}"')

    def test_004_validate_icon_for_result_statusindexphpattachmentsget111160935indexphpattachmentsget111160936(self):
        """
        DESCRIPTION: Validate icon for "RESULT" status
        DESCRIPTION: ![](index.php?/attachments/get/111160935)
        DESCRIPTION: ![](index.php?/attachments/get/111160936)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed icon before the status
        EXPECTED: 2: CSS
        EXPECTED: .Oval-2 {
        EXPECTED: width: 4px;
        EXPECTED: height: 4px;
        EXPECTED: border: solid 1px #000000;
        EXPECTED: }
        EXPECTED: Coral:
        EXPECTED: 1: User should be displayed icon before the status
        EXPECTED: 2: CSS
        EXPECTED: .Mask {
        EXPECTED: width: 375px;
        EXPECTED: height: 70px;
        EXPECTED: background-color: #f9fafe;
        EXPECTED: }
        """
        # Covered in step 3
