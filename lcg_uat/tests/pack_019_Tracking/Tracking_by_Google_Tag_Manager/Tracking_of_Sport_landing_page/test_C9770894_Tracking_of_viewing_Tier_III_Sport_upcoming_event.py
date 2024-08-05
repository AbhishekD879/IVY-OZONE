import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@pytest.mark.reg157_fix
@vtest
class Test_C9770894_Tracking_of_viewing_Tier_III_Sport_upcoming_event(BaseDataLayerTest, BaseSportTest):
    """
    TR_ID: C9770894
    NAME: Tracking of viewing Tier III Sport upcoming event
    DESCRIPTION: This test case verifies the GA tracking of viewing upcoming event on sport landing page of Ties III type
    PRECONDITIONS: 1. Sports Page > Sports Categories > <any sport> is enabled in CMS
    PRECONDITIONS: 2. User is on <sport> landing page: Single view page
    PRECONDITIONS: All sports that are tier I and II are listed here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True
    expected_response = {'event': 'trackEvent',
                         'eventAction': '/sport/baseball',
                         'eventCategory': 'upcoming module',
                         'eventLabel': "view event",
                         }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Event
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_baseball_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(days=1), is_upcoming=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.eventName = event_params.ss_response["event"]["typeName"]
            self.__class__.event_team1 = event_params.team1
            self.__class__.event_team2 = event_params.team2
            self.__class__.event_teams = event_params.team1 + " v " + event_params.team2

    def test_001_click_on_any_event_from_upcoming_module(self):
        """
        DESCRIPTION: Click on any event from Upcoming module
        EXPECTED: User is redirected to EDP
        """
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state('baseball')
        if tests.settings.backend_env != 'prod':
            section = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict[
                "AUTO TEST - " + self.eventName.upper()]
            if self.brand != "ladbrokes":
                section.items_as_ordered_dict[self.event_teams].click()
            else:
                section.items_as_ordered_dict[self.event_team2 + " v " + self.event_team1].click()
        else:
            leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
            self.assertTrue(leagues, msg='Leagues not found')
            for league in leagues:
                fixture = league.fixture_header.date.name
                if fixture.title() != "Today":
                    next(iter(league.items_as_ordered_dict.items()))[1].click()
                    break
        #this step is importatnt to retrieve the upcoming module event tracking            
        #Getting Event From League
        event = leagues[0].items_as_ordered_dict.items()
        wait_for_haul()
        #Clicking On the Event
        list(event)[0][1].click()

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event': 'trackEvent', 'eventCategory': 'upcoming module ', 'eventAction': '<< LOCATION >>', 'eventLabel': 'view event', 'eventName': '<< EVENT NAME >>', 'eventID': '<< EVENT ID >>' }
        """
        wait_for_haul(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory',
                                                              object_value='upcoming module')
        if tests.settings.backend_env != 'prod':
            self.assertEqual(self.event_teams, actual_response.get("eventName"),
                             msg=f'"{self.event_teams}"eventName value "{actual_response.get("eventName")}" is not present in datalayer')
            self.assertEqual(int(self.eventID), actual_response.get("eventID"),
                             msg=f'"{self.eventID}"eventID value "{actual_response.get("eventID")}" is not present in datalayer')
        self.assertEqual(self.expected_response.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{self.expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(self.expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{self.expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(self.expected_response.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{self.expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(self.expected_response.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{self.expected_response.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')
