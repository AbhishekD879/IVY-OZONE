import pytest
import tests
from json import JSONDecodeError
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.frequent_blocker
@vtest
class Test_C60034280_Verify_limitRecordsoutcome2_query_parameter_in_Class_request_on_Special_tab(BaseSportTest):
    """
    TR_ID: C60034280
    NAME: Verify  "limitRecords=outcome:2" query parameter in Class request on 'Special' tab
    DESCRIPTION: This test case verifies "limitRecords=outcome:2" query parameter in Class request on 'Special' tab for different Sports (Tier 1, Tier 2)
    DESCRIPTION: "limitRecords=outcome:2" query parameter is added to limit the number of outcomes to 2 as prices are displayed only in case if 1 outcome is available and in case if there are more outcomes - link to edp page is shown
    DESCRIPTION: NOTE: Specials data is received in /EventToOutcomeForClass not in Class request!
    PRECONDITIONS: Configurations:
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball), one event from Tier 2 and Tier 2 sport Outright(e.g. Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: To check SiteServ request go to dev tools -> Network -> XHR
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

    def search_eventtooutcomeforclass_in_dev_tools(self, sport):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -> Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        event_to_outcome_response = self.get_response_url('EventToOutcomeForClass')
        if not event_to_outcome_response:
            raise SiteServeException(f'No event data available for sport "{sport}"')
        else:
            self.assertIn('limitRecords=outcome:2', event_to_outcome_response,
                          msg=f'Expected: "limitRecords=outcome:2" is not present in Actual: "{event_to_outcome_response}"')

    def test_000_precondition(self):
        """
        DESCRIPTION: Create sport events ex:Football, tennis
        DESCRIPTION: Enable the Specials tab in CMS
        """
        self.__class__.specials_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials.upper()
        if tests.settings.backend_env != "prod":
            self.ob_config.add_autotest_premier_league_football_event(special=True)
            self.ob_config.add_tennis_event_to_autotest_trophy(special=True)
            self.ob_config.add_hockey_event_to_super_league(special=True)
            self.ob_config.add_baseball_event_to_autotest_league(special=True)
            tennis_category_id = self.ob_config.tennis_config.category_id
            football_category_id = self.ob_config.football_config.category_id
            hockey_category_id = 54
            baseball_category_id = self.ob_config.baseball_config.category_id
            category_id = {"football": football_category_id, "tennis": tennis_category_id,
                           "hockey": hockey_category_id, "baseball": baseball_category_id}
            for category in category_id:
                tab_id = self.cms_config.get_sport_tab_id(sport_id=category_id[category],
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials)
                self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                         sport_id=category_id[category])

    def test_001_navigate_to_football_landing_page___special_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Special' tab
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        self.site.open_sport(name='FOOTBALL')
        try:
            self.site.wait_content_state('football')
            if self.site.football.tabs_menu.items_as_ordered_dict.get(self.specials_tab).is_displayed():
                result = self.site.football.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.specials}" is not opened')
                actual_tab = self.site.football.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.specials,
                                 msg=f'Specials tab is not active, active is "{actual_tab}"')
                if self.site.football.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='football specials')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under specials Tab')

    def test_002_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        # Covered in search_eventtooutcomeforclass_in_dev_tools step

    def test_003_navigate_to_special_tab_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        self.navigate_to_page(name='sport/tennis')
        try:
            self.site.wait_content_state('tennis')
            if self.site.tennis.tabs_menu.items_as_ordered_dict.get(self.specials_tab).is_displayed():
                result = self.site.tennis.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.specials}" is not opened')
                actual_tab = self.site.tennis.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.specials,
                                 msg=f'SPECIALS tab is not active, active is "{actual_tab}"')
                if self.site.tennis.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='tennis specials')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under specials Tab')

    def test_004_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        # Covered in test_003 step

    def test_005_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        self.navigate_to_page(name='sport/hockey')
        try:
            self.site.wait_content_state('hockey')
            if self.site.hockey.tabs_menu.items_as_ordered_dict.get(self.specials_tab).is_displayed():
                result = self.site.hockey.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.specials}" is not opened')
                actual_tab = self.site.hockey.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.specials,
                                 msg=f'SPECIALS tab is not active, active is "{actual_tab}"')
                if self.site.hockey.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='hockey specials')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under specials Tab')

    def test_006_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        # Covered in test_005 step

    def test_007_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        self.navigate_to_page(name='sport/baseball')
        try:
            self.site.wait_content_state('baseball')
            if self.site.baseball.tabs_menu.items_as_ordered_dict.get(self.specials_tab).is_displayed():
                result = self.site.baseball.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.specials}" is not opened')
                actual_tab = self.site.baseball.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.specials,
                                 msg=f'SPECIALS tab is not active, active is "{actual_tab}"')
                if self.site.baseball.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='baseball specials')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under specials Tab')

    def test_008_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        # Covered in test_007 step
