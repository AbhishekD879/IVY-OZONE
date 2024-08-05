import pytest
import tests
from datetime import datetime
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.lad_beta2
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.reg156_fix
@vtest
class Test_C28798_Verify_event_name_displaying(BaseGreyhound):
    """
    TR_ID: C28798
    NAME: Verify event name displaying
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event
        EXPECTED: Racing event created
        """
        self.__class__.datafabric_data_present = False
        if tests.settings.backend_env == 'prod':
            try:
                event = self.get_event_details(datafabric_data=True)

                self.__class__.datafabric_data_present = True
                self.__class__.eventID = event.event_id
                self.__class__.event_name = event.event_name
                self.__class__.meeting_breadcrumb = event.type_name
                self.__class__.event_off_time = event.off_time
            except ThirdPartyDataException:
                event = self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)[0]
                self.__class__.eventID = event['event']['id']
                self.__class__.event_name = normalize_name(event['event']['name'])
                self.__class__.meeting_breadcrumb = event['event']['typeName']
                self.__class__.event_off_time = datetime.strptime(event['event']['startTime'], self.ob_format_pattern).strftime('%H:%M')
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
            self.__class__.eventID, self.__class__.event_off_time = event_params.event_id, event_params.event_off_time
            self.__class__.event_name = f'{self.event_off_time} {self.greyhound_autotest_name_pattern}'
            self.__class__.meeting_breadcrumb = self.greyhound_autotest_name_pattern

        self.__class__.is_mobile = True if self.device_type in ['mobile'] else False

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_002_look_at_the_event_name(self):
        """
        DESCRIPTION: Look at the event name
        EXPECTED: Event name corresponds to the **'name'** attribute
        EXPECTED: No matter what user timezone is the race local time is shown near the event name (as come from the Site Server)
        """
        breadcrumbs = self.site.greyhound_event_details.breadcrumbs.items_as_ordered_dict
        self.assertTrue(breadcrumbs, msg='Related breadcrumb is missing')
        if self.is_mobile:
            meeting_breadcrumb = list(breadcrumbs.keys())[1]
        else:
            meeting_breadcrumb = list(breadcrumbs.keys())[2]

        if len(self.meeting_breadcrumb) > 7 and self.device_type == 'mobile':
            self.meeting_breadcrumb = self.meeting_breadcrumb[:7] + '...'

        self.assertEqual(meeting_breadcrumb, self.meeting_breadcrumb,
                             msg=f'Breadcrumbs "{meeting_breadcrumb}" are not the same as expected "{self.meeting_breadcrumb}"')
        if not self.datafabric_data_present:
            actual_event_name = self.site.greyhound_event_details.event_title
            self.assertEqual(actual_event_name, self.event_name, msg=f'Event name "{actual_event_name}" '
                                                                     f'is not the same as expected "{self.event_name}"')

        actual_event_off_time = self.site.greyhound_event_details.tab_content.active_off_time
        self.assertEqual(actual_event_off_time, self.event_off_time,
                         msg=f'Event time "{actual_event_off_time}" '
                             f'is not the same as expected "{self.event_off_time}"')
