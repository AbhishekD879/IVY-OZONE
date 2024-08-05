import dateutil
import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from datetime import datetime, timedelta


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.grey_hounds_specific
@pytest.mark.sports_specific
@pytest.mark.races
@pytest.mark.reg156_fix
@vtest
class Test_C28829_Verify_data_for_Future_tab(BaseRacing):
    """
    TR_ID: C28829
    NAME: Verify data for 'Future' tab
    DESCRIPTION: This test case verifies data which is displayed in 'Future' tab
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

        # GreyHound Cms Pre Checks
        greyhound_category_id = 19
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        all_sports = self.cms_config.get_sport_categories()
        greyhound = next((sport for sport in all_sports if sport.get('categoryId') == greyhound_category_id and
                          sport.get("imageTitle").upper() == sport_name.upper()), None)
        if greyhound:
            self.cms_config.update_sport_category(greyhound.get("id"),
                                                  disabled=False,
                                                  showInAZ=True,
                                                  showInHome=True)
        else:
            raise CmsClientException("Greyhound Sport Category not Configured in CMS")

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Application is loaded
        """
        self.site.wait_content_state('homepage')

    def test_002_on_the_homepage_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On the homepage tap <Race> icon from the sports menu ribbon
        EXPECTED: 1.  <Race> landing page is opened
        EXPECTED: 2.  'Today' tab is displayed
        """
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)
        self.assertIn(vec.sb.SPORT_DAY_TABS.today.upper(), self.site.greyhound.tabs_menu.items_as_ordered_dict.keys(),
                      msg="Today Tab is not displayed")

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: 'By Meeting' sorting type is selected by default
        """
        if self.brand == 'ladbrokes':
            future = vec.sb.TABS_NAME_FUTURE.upper()
        else:
            future = vec.sb.SPORT_DAY_TABS.future
        self.site.greyhound.tabs_menu.click_button(future)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(future).is_selected(),
                        msg='"future tab" is not present')
        actual_sub_tab = self.site.greyhound.tab_content.current
        self.assertEqual(actual_sub_tab.title(), vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING.title(),
                         msg=f'Actual tabs: "{actual_sub_tab}" is not equal with the'
                             f'Expected tab: "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_004_chack_data_which_is_displayed_in_future_tab(self):
        """
        DESCRIPTION: Check data which is displayed in 'Future' tab
        EXPECTED: 1.  A list of all future's racing is displayed
        EXPECTED: 2.  Data corresponds to the Site Server response
        EXPECTED: 3.  Event start times correspond to day after tomorrow's date and further (see **'startTime'** attribute)
        """
        if self.brand != 'ladbrokes':
            actual_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
                                 f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')
        if self.brand == 'ladbrokes':
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        sections = list(sections.values())
        self.assertTrue(sections, msg='No sections found in today meetings tab')
        actual_url = self.get_response_url('/EventToOutcomeForClass')
        if not actual_url:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        response = do_request(method='GET', url=actual_url)
        for event in response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            event_start_time = event["event"]["startTime"]
            event_time = dateutil.parser.parse(event_start_time)
            current_uk_time = datetime.utcnow() + timedelta(hours=1)
            self.assertTrue((event_time.replace(tzinfo=None) - current_uk_time.replace(tzinfo=None)).days >= 1,
                            msg="The startTime is not day after tomorrow dates")
