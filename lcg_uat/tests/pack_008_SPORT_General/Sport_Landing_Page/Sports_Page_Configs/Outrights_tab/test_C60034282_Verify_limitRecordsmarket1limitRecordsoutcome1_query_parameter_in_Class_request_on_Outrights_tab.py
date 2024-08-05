import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from json import JSONDecodeError
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.frequent_blocker
@vtest
class Test_C60034282_Verify_limitRecordsmarket1limitRecordsoutcome1_query_parameter_in_Class_request_on_Outrights_tab(BaseSportTest):
    """
    TR_ID: C60034282
    NAME: Verify "limitRecords=market:1 and limitRecords=outcome:1" query parameter in Class request on 'Outrights' tab
    DESCRIPTION: This test case verifies "limitRecords=market:1&limitRecords=outcome:1" query parameter in Class request on 'Outrights' tab for different Sports (Tier 1, Tier 2)
    DESCRIPTION: To Update: Class request never contained "limitRecords=market:1&limitRecords=outcome:1" query parameters, this is only available in data requests like:
    DESCRIPTION: https://ss-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/58?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.eventSortCode:intersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=event.suspendAtTime:greaterThan:2020-11-12T11:59:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
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
            self.assertIn('limitRecords=market:1', event_to_outcome_response,
                          msg=f'Expected: "limitRecords=market:1" is not present in Actual: "{event_to_outcome_response}"')
            self.assertIn('limitRecords=outcome:1', event_to_outcome_response,
                          msg=f'Expected: "limitRecords=outcome:1" is not present in Actual: "{event_to_outcome_response}"')

    def test_000_precondition(self):
        """
        DESCRIPTION: Create sport events ex:Football, tennis
        DESCRIPTION: Enable the Outrights tab in CMS
        """
        self.__class__.outright_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper()
        if tests.settings.backend_env != "prod":
            self.ob_config.add_autotest_premier_league_football_outright_event()
            self.ob_config.add_american_football_outright_event_to_autotest_league()
            self.ob_config.add_tennis_outright_event_to_autotest_league()
            self.ob_config.add_hockey_event_outright_event()
            tennis_category_id = self.ob_config.tennis_config.category_id
            football_category_id = self.ob_config.football_config.category_id
            hockey_category_id = 54
            american_football_category_id = self.ob_config.american_football_config.category_id
            category_id = {"football": football_category_id, "tennis": tennis_category_id,
                           "hockey": hockey_category_id, "american_football": american_football_category_id}
            for category in category_id:
                tab_id = self.cms_config.get_sport_tab_id(sport_id=category_id[category],
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights)
                self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                         sport_id=category_id[category])

    def test_001_navigate_to_football_landing_page___outrights_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Outrights' tab
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        self.site.open_sport(name='FOOTBALL')
        try:
            self.site.wait_content_state('football')
            if self.site.football.tabs_menu.items_as_ordered_dict.get(self.outright_tab).is_displayed():
                result = self.site.football.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
                actual_tab = self.site.football.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.outrights,
                                 msg=f'OUTRIGHTS tab is not active, active is "{actual_tab}"')
                if self.site.football.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='football outright')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under Outright Tab')

    def test_002_search_eventtooutcomeforclass_in_dev_tools___networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(
            self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -> Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        # Covered in search_eventtooutcomeforclass_in_dev_tools step

    def test_003_navigate_to_outrights_tab_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(
            self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        self.navigate_to_page(name='sport/tennis')
        try:
            self.site.wait_content_state('tennis')
            if self.site.tennis.tabs_menu.items_as_ordered_dict.get(self.outright_tab).is_displayed():
                result = self.site.tennis.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
                actual_tab = self.site.tennis.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.outrights,
                                 msg=f'OUTRIGHTS tab is not active, active is "{actual_tab}"')
                if self.site.tennis.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='tennis outright')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under Outright Tab')

    def test_004_search_eventtooutcomeforclass_in_dev_tools___networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(
            self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -> Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        # covered in test_003 step

    def test_005_navigate_to_outrights_tab_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(
            self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        self.navigate_to_page('sport/hockey')
        try:
            self.site.wait_content_state('hockey')
            if self.site.hockey.tabs_menu.items_as_ordered_dict.get(self.outright_tab).is_displayed():
                result = self.site.hockey.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
                actual_tab = self.site.hockey.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.outrights,
                                 msg=f'OUTRIGHTS tab is not active, active is "{actual_tab}"')
                if self.site.hockey.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='hockey outright')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under Outright Tab')

    def test_006_search_eventtooutcomeforclass_in_dev_tools___networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(
            self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -> Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        # Covered in test_005 step

    def test_007_navigate_to_outrights_tab_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(
            self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        self.navigate_to_page(name='sport/american-football')
        try:
            self.site.wait_content_state('american-football')
            if self.site.american_football.tabs_menu.items_as_ordered_dict.get(self.outright_tab).is_displayed():
                result = self.site.american_football.tabs_menu.click_button(
                    self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper())
                self.assertTrue(result, msg=f'"{self.expected_sport_tabs.outrights}" is not opened')
                actual_tab = self.site.american_football.tabs_menu.current
                self.assertEqual(actual_tab, self.expected_sport_tabs.outrights,
                                 msg=f'OUTRIGHTS tab is not active, active is "{actual_tab}"')
                if self.site.american_football.tab_content.accordions_list.is_displayed():
                    try:
                        self.search_eventtooutcomeforclass_in_dev_tools(sport='american-football outright')
                    except Exception:
                        raise Exception('LimitRecords Query Parameter is not present')
        except Exception:
            raise SiteServeException('There are no available events under Outright Tab')

    def test_008_search_eventtooutcomeforclass_in_dev_tools___networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(
            self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -> Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        # Covered in test_007 step
