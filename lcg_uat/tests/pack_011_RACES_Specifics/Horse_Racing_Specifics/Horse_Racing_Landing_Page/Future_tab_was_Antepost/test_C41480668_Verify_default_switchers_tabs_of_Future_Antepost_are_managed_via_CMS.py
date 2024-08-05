import pytest
import voltron.environments.constants as vec
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry_if_exception_type, wait_fixed, stop_after_attempt, retry
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #can't edit CMS and Can't create events
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@vtest
class Test_C41480668_Verify_default_switchers_tabs_of_Future_Antepost_are_managed_via_CMS(Common):
    """
    TR_ID: C41480668
    NAME: Verify default switchers tabs of 'Future' (Antepost) are managed via CMS
    DESCRIPTION: This test case verifies default switchers tabs of 'Future' (Antepost) are  managed via CMS
    PRECONDITIONS: 1. Make sure 'National Hunt' switcher tab name is default in CMS
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to Horse Racing landing page ('Future' tab is available)
    PRECONDITIONS: **OB configurations:**
    PRECONDITIONS: 1) To create HR Future event use TI tool:
    PRECONDITIONS: a) 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: b) 'Antepost' check box should be checked on market level (Market Template= 'Outright' with name 'Ante-post')
    PRECONDITIONS: c) Event start time should be in the future (like 2 days from now)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - If flags 'Flat', 'National Hunt', 'International' are not checked on event level, events are not displayed on the landing page
    PRECONDITIONS: - If flag 'Antepost' is not checked on market level, new designs do not apply on HR EDP
    PRECONDITIONS: **CMS configurations:**
    PRECONDITIONS: To setup default switcher tab use CMS:
    PRECONDITIONS: System configuration -> structure -> defaultAntepostTab -> tabName -> **'tab name'**
    PRECONDITIONS: where
    PRECONDITIONS: **'tab name'** - should be the same as existing switcher tab name (e.g. Flat, National Hunt, International)
    PRECONDITIONS: Request to check data on 'Future' tab:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-09T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-07T11:22:30.000Z&simpleFilter=event.classId:notIntersects:227&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_FT,EVFLAG_IT,EVFLAG_NH&simpleFilter=event.drilldownTagNames:contains:EVFLAG_AP&externalKeys=event&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create antepost events (which are expected to be displayed on Future tab on HR EDP).
        """
        self.ob_config.add_international_racing_event(number_of_runners=1, is_flat=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))
        self.ob_config.add_international_racing_event(number_of_runners=1, is_national_hunt=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))
        self.ob_config.add_international_racing_event(number_of_runners=1, is_international=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')
        if self.brand == 'bma':
            self.cms_config.update_system_configuration_structure(config_item='defaultAntepostTab',
                                                                  field_name='tabNmae',
                                                                  field_value="FLAT, NATIONAL HUNT, INTERNATIONAL")
        else:
            self.cms_config.update_system_configuration_structure(config_item='defaultAntepostTab',
                                                                  field_name='tabName',
                                                                  field_value="FLAT, NATIONAL HUNT, INTERNATIONAL")

    @retry(stop=stop_after_attempt(6), wait=wait_fixed(wait=20),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_defaultAntePostTab_from_cms(self):
        if self.brand == 'bma':
            self.__class__.defaultAntePostTab = self.cms_config.get_system_configuration_structure()['defaultAntepostTab']['tabNmae']
        else:
            self.__class__.defaultAntePostTab = self.cms_config.get_system_configuration_structure()['defaultAntepostTab']['tabName']
        self.assertEquals(self.defaultAntePostTab, "FLAT, NATIONAL HUNT, INTERNATIONAL", msg="tabName is not expected")

    def test_001_navigate_to_future_tab(self):
        """
        DESCRIPTION: Navigate to 'Future' tab
        EXPECTED: * Future' tab is opened
        EXPECTED: * Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions)
        EXPECTED: * Default switcher tab (determined in CMS e.g. 'National Hunt') is opened
        """
        self.get_defaultAntePostTab_from_cms()
        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_FUTURE_TAB_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not selected after click')
        switchers = self.site.horse_racing.tab_content.grouping_buttons.items_as_ordered_dict.keys()
        self.assertTrue(switchers, msg='No switchers present on page')
        for index, switcher in enumerate(list(switchers)):
            if index == 0:
                self.assertEquals(switcher, "FLAT", msg="Default tab is not equal to FLAT")
            self.assertIn(switcher, self.defaultAntePostTab,
                          msg=f'"{switcher}" is not present in "{self.defaultAntePostTab}"')

    def test_002_setup_other_switchers_tabs_eg_flat_international_in_cmssystem_configuration___structure___defaultanteposttab___tabname___tab_nameand_repeat_step_1(
            self):
        """
        DESCRIPTION: Setup other switchers tabs (e.g. Flat, International) in CMS
        DESCRIPTION: (System configuration -> structure -> defaultAntepostTab -> tabName -> **'tab name'**)
        DESCRIPTION: and repeat step 1
        EXPECTED: * Future' tab is opened
        EXPECTED: * Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions)
        EXPECTED: * Default switcher tab (determined in CMS) is opened
        """
        if self.brand == 'bma':
            self.cms_config.update_system_configuration_structure(config_item='defaultAntepostTab',
                                                                  field_name='tabNmae',
                                                                  field_value="FLAT, NATIONAL HUNT, INTERNATIONAL")
        else:
            self.cms_config.update_system_configuration_structure(config_item='defaultAntepostTab',
                                                                  field_name='tabName',
                                                                  field_value="FLAT, NATIONAL HUNT, INTERNATIONAL")
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_FUTURE_TAB_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not selected after click')
        switchers = self.site.horse_racing.tab_content.grouping_buttons.items_as_ordered_dict.keys()
        self.assertTrue(switchers, msg='No switchers present on page')
        for index, switcher in enumerate(list(switchers)):
            if index == 0:
                self.assertEquals(switcher, "FLAT", msg="Default tab is not equal to FLAT")
            self.assertIn(switcher, self.defaultAntePostTab,
                          msg=f'"{switcher}" is not present in "{self.defaultAntePostTab}"')
