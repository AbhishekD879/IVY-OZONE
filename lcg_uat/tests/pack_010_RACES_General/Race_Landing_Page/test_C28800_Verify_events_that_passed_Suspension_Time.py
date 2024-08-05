import pytest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend event in prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28800_Verify_events_that_passed_Suspension_Time(BaseRacing):
    """
    TR_ID: C28800
    NAME: Verify events that passed "Suspension Time"
    DESCRIPTION: This test case verifies events removing from the <Race> Landing Page if they passed "Suspension Time"
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-6526 As a TA I want to improve the caching efficiency of Horse Racing SiteServer data retrieval
    DESCRIPTION: *   BMA-7859
    DESCRIPTION: Note: According to the comment https://jira.egalacoral.com/browse/BMA-50477 miliseconds should not be rounded as described below
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Check "suspendAtTime="YYYY-MM-DDThh:mm:ssZ"" attribute to see the time, when the event should be removed from <Race> Landing Page
    PRECONDITIONS: Check **event.suspendAtTime** simple filter in **Networks **
    PRECONDITIONS: The **event.suspendAtTime** simple filter should simply be "2016-01-26T08:26:00.000Z" or "2016-01-26T08:26:30.000Z"
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:18.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:00.000
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:48.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:30.000
    """
    keep_browser_open = True
    datetime_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event
        EXPECTED: Events are created in OB
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2)
        self.__class__.eventID = event_params.event_id
        self.__class__.event_off_time = event_params.event_off_time

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        if self.brand != 'ladbrokes':
            self.navigate_to_page(name='greyhounds')
            self.site.wait_content_state('Greyhounds')
        else:
            self.navigate_to_page(name='greyhound-racing')
            self.site.wait_content_state('Greyhoundracing')

    def test_002_go_to_race_landing_page(self):
        """
        DESCRIPTION: Go to <Race> Landing page
        EXPECTED: Landing page is opened representing available events
        """
        click_button = self.site.greyhound.tabs_menu.click_button(button_name=vec.sb.SPORT_DAY_TABS.today.upper())
        try:
            self.assertTrue(click_button, msg=f'"{vec.sb.SPORT_DAY_TABS.today}" is not selected after click')
        except Exception:
            self.site.greyhound.tabs_menu.click_button(button_name=vec.sb.SPORT_DAY_TABS.today.upper())

    def test_003_checkeventsuspendattimesimple_filter_innetworksin_console(self):
        """
        DESCRIPTION: Check **event.suspendAtTime** simple filter in **Networks **(in Console)
        EXPECTED: The event.suspendAtTime simple filter should simply contain '00.000' seconds and milliseconds or '30.000' seconds and milliseconds
        EXPECTED: For example:
        EXPECTED: "2016-01-26T08:26:00.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        EXPECTED: or
        EXPECTED: "2016-01-26T08:26:30.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        """
        # https://jira.egalacoral.com/browse/BMA-50477 miliseconds should not be rounded as described above so verifying format

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]
        suspendat = resp['event']['suspendAtTime']
        self.assertRegexpMatches(suspendat, self.datetime_pattern,
                                 msg=f'Actual pattern {suspendat} is not matching with expected {self.datetime_pattern}')
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        section = sections[section_name]
        section.expand()
        self.assertTrue(section.is_expanded(),
                        msg=f'Section sections {vec.racing.UK_AND_IRE_TYPE_NAME.upper()} is not expanded')
        type_name = 'AUTOTEST' if self.brand == 'bma' else 'Autotest'
        meetings_list_ui = section.items_as_ordered_dict[type_name].items_names
        self.assertTrue(meetings_list_ui, msg=f'No meetings found in {vec.racing.UK_AND_IRE_TYPE_NAME.upper()}')
        self.assertIn(self.event_off_time, meetings_list_ui,
                      msg=f'Expected event "{self.event_off_time}" is not present in'
                          f'Actual event list "{meetings_list_ui}"')

    def test_004_pick_event_which_is_shown_on_landing_page_and_check_ss_response_for_it(self):
        """
        DESCRIPTION: Pick event which is shown on Landing Page and check SS response for it
        EXPECTED: **"suspendAtTime="YYYY-MM-DDThh:mm:ssZ""**** **attribute is present showing the time when event should be removed from the verified Landing Page
        """
        # covered in above step

    def test_005_wait_until_time_ofsuspendattimepassed___refresh_landing_page(self):
        """
        DESCRIPTION: Wait until time of **"suspendAtTime" **passed -> Refresh Landing page
        EXPECTED: Verified event is no more shown on  Landing Page
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        self.test_002_go_to_race_landing_page()
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        section = sections[section_name]
        section.expand()
        self.assertTrue(section.is_expanded(),
                        msg=f'Section sections {vec.racing.UK_AND_IRE_TYPE_NAME.upper()} is not expanded')

        type_name = 'AUTOTEST' if self.brand == 'bma' else 'Autotest'
        meetings_list_ui = section.items_as_ordered_dict[type_name].items_names
        self.assertTrue(meetings_list_ui, msg=f'No meetings found in {vec.racing.UK_AND_IRE_TYPE_NAME.upper()}')
        self.assertNotIn(self.event_off_time, meetings_list_ui,
                         msg=f'Expected event "{self.event_off_time}" is present in'
                         f'Actual event list "{meetings_list_ui}"')
