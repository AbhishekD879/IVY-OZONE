import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.Common import Common

@pytest.mark.prod
#@pytest.mark.hl
# @pytest.mark.tst2  #Specials and Outright usually are available on Prod
# @pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.frequent_blocker
@vtest
class Test_C59187359_Verify_simpleFilterclasshasOpenEvent_query_parameter_in_Class_request_on_Special_tab(Common):
    """
    TR_ID: C59187359
    NAME: Verify  simpleFilter=class.hasOpenEvent query parameter in Class request on 'Special' tab
    DESCRIPTION: This test case verifies simpleFilter=class.hasOpenEvent query parameter in Class request on 'Special' tab for different Sports(Tier 1, Tier 2)
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball), one event from Tier 2 and Tier 2 sport Outright(e.g. Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: Example of Class request:
    PRECONDITIONS: "https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&responseFormat=json&simpleFilter=class.categoryId:equals:16&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent"
    PRECONDITIONS: - Sport page configurations can be found here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: - What is considered as Class that contains Event that is open for betting:
    PRECONDITIONS: The item contains (or is, or belongs to) a displayed Event on which betting is either currently offered, or has been offered in the last few minutes, or is expected to be offered in the next few minutes. Settled events will not be included; temporarily suspended events will be.
    PRECONDITIONS: Notes:
    PRECONDITIONS: Does not currently take into account the details of the Markets and Outcomes within the Event.
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page___special_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Special' tab
        EXPECTED: Football Special tab opened
        """
        self.__class__.specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials
        specials_tab_name = self.get_sport_tab_name(name=self.specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.football.FOOTBALL_TITLE)
        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(specials_tab_name)
        self.assertEqual(tabs_menu.current, specials_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} is not as expected "{specials_tab_name}"')

    def test_002_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.football_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        self.assertTrue(response, msg=f'No response from site server')
        for res in response:
            if res['class']['hasOpenEvent']:
                self.assertTrue(response, msg=f'No site server response with hasOpenEvent query parameter')
            else:
                self.assertFalse(response, msg=f'Response from site server with hasOpenEvent query parameter')

    def test_003_navigate_to_special_tab_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(
            self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: Sport Landing page opened
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name='tennis')
        tennis_specials_tab_name = self.get_sport_tab_name(name=self.specials_tab_cms_name,
                                                           category_id=self.ob_config.tennis_config.category_id)
        tabs_menu = self.site.tennis.tabs_menu
        tabs_menu.click_button(tennis_specials_tab_name)
        selected_tab = self.site.tennis.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.specials_tab_cms_name,
                                                    self.ob_config.tennis_config.category_id)
        self.assertEqual(selected_tab, expected_tab_name,
                         msg=f'Selected tab is: "{selected_tab}" instead of: "{expected_tab_name}"')

    def test_004_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(
            self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.tennis_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.tennis_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        self.assertTrue(response, msg=f'No response from site server')
        for res in response:
            if res['class']['hasOpenEvent']:
                self.assertTrue(response, msg=f'No site server response with hasOpenEvent query parameter')
            else:
                self.assertFalse(response, msg=f'Response from site server with hasOpenEvent query parameter')

    def test_005_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(
            self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: Sport Landing page opened
        """
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state('baseball')
        self.site.baseball.tabs_menu.click_button(self.specials_tab_cms_name.upper())
        current_tab_name = self.site.baseball.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.specials_tab_cms_name,
                                                    self.ob_config.baseball_config.category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Expected tab: "{current_tab_name}", Actual Tab: "{expected_tab_name}"')

    def test_006_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(
            self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.baseball_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.baseball_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        self.assertTrue(response, msg=f'No response from site server')
        for res in response:
            if res['class']['hasOpenEvent']:
                self.assertTrue(response, msg=f'No site server response with hasOpenEvent query parameter')
            else:
                self.assertFalse(response, msg=f'Response from site server with hasOpenEvent query parameter')

    def test_007_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(
            self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: Sport Landing page opened
        """
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                    self.ob_config.golf_config.category_id)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_008_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(
            self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.golf_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.golf_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        self.assertTrue(response, msg=f'No response from site server')
        for res in response:
            if res['class']['hasOpenEvent']:
                self.assertTrue(response, msg=f'No site server response with hasOpenEvent query parameter')
            else:
                self.assertFalse(response, msg=f'Response from site server with hasOpenEvent query parameter')
