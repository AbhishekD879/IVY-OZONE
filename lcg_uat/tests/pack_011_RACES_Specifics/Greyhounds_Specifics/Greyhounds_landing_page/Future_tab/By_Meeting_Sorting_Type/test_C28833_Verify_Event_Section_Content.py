import pytest
import tests
from json import JSONDecodeError
from tests.base_test import vtest
from tests.Common import Common
from datetime import datetime
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
#@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C28833_Verify_Event_Section_Content(Common):
    """
    TR_ID: C28833
    NAME: Verify Event Section Content
    DESCRIPTION: This test case verifies event section content
    PRECONDITIONS: Request to check data:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-14T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-12T10:37:30.000Z&simpleFilter=event.classId:notIntersects:201&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            start_time = self.get_date_time_formatted_string(days=2, hours=2)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time)

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED:
        """
        self.site.wait_content_state('homepage')

    def test_002_from_the_sports_menu_ribbon_tap_race_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap <Race> icon
        EXPECTED: <Race> landing page is opened
        """
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)
        self.assertIn(vec.sb.SPORT_DAY_TABS.today.upper(), self.site.greyhound.tabs_menu.items_as_ordered_dict.keys(),
                      msg="Today Tab is not displayed")

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is selected
        """
        if self.brand == 'ladbrokes':
            future = vec.sb.TABS_NAME_FUTURE.upper()
        else:
            future = vec.sb.SPORT_DAY_TABS.future
        self.site.greyhound.tabs_menu.click_button(future)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(future).is_selected(),
                        msg='"future tab" is not present')

    def test_004_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to the** 'name' **attribute from the Site Server (including race local time)
        """
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        sections = list(sections.values())
        self.assertTrue(sections, msg='No sections found in Future tab')
        actual_url = self.get_response_url('/EventToOutcomeForClass')
        if not actual_url:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        response = do_request(method='GET', url=actual_url)
        for event in response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            event_name = event["event"]["name"]
            self.assertTrue(event_name, msg=f'Event name: "{event_name}" is not displayed.')
            date = event["event"]["startTime"]
            self.assertTrue(date, msg=f'Event date: "{date}" is not displayed')
            date_format = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            self.assertTrue(date_format, msg=f'Date format: "{date_format}" is not matching.')

    def test_005_verify_event_time(self):
        """
        DESCRIPTION: Verify event time
        EXPECTED: Event time is shown before the event name
        EXPECTED: Event time corresponds to the race local time (see **'name'** attribute)
        """
        # covered in step 4

    def test_006_verify_event_date(self):
        """
        DESCRIPTION: Verify event date
        EXPECTED: Event date corresponds to the Site Server response ( see **'startTime' **attribute)
        """
        # covered in step 4

    def test_007_verify_date_format(self):
        """
        DESCRIPTION: Verify date format
        EXPECTED: Date formats isthe following:
        EXPECTED: **DD-MM-YYYY**
        """
        # covered in step 4
