import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9771298_Event_Hub_Verify_Private_Market_tab_displayed_First_for_logged_in_user_if_Event_Hub_tab_was_configured_as_First_in_CMS(BasePrivateMarketsTest):
    """
    TR_ID: C9771298
    NAME: Event Hub: Verify Private Market tab displayed First for logged in user if Event Hub tab was configured as First in CMS
    DESCRIPTION: This test case verifies that Private Market tab is displayed First for logged in user if Event Hub tab was configured as First in CMS
    PRECONDITIONS: 1. Event Hub is created on CMS > Sport Pages > Event Hub
    PRECONDITIONS: 2. Module ribbon tab is configured and has Event Hub mapped. THis Module ribbon tab is configured ti be displayed First on FE.
    PRECONDITIONS: 3. User with Private Markets configured exists. (https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) 2 Featured Modules created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
        """
        event_params1 = self.ob_config.add_autotest_premier_league_football_event()
        eventID1 = event_params1.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=eventID1, page_type='eventhub', page_id=index_number,
            events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10)
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')
        self.site.wait_content_state_changed(timeout=5)

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_load_app_as_logged_out_user_navigate_to_homepage_and_verify_module_ribbon_tab_from_preconditions(self):
        """
        DESCRIPTION: Load app as logged out user, navigate to Homepage and Verify Module ribbon tab from preconditions
        EXPECTED: Event Hub Module ribbon tab is displayed first in ribbon.
        EXPECTED: User lands on this tab when he loads app.
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_002_login_as_user_from_preconditions(self):
        """
        DESCRIPTION: Login as user from preconditions
        EXPECTED: * User logged in
        EXPECTED: * Your Enhanced Markets tab appears in ribbon before Event Hub tab.
        EXPECTED: * User remains on Event Hub tab
        """
        user = tests.settings.betplacement_user
        self.site.login(username=user)
        self.site.wait_content_state(state_name='Homepage')
        self.trigger_private_market_appearance(user=user,
                                               expected_market_name=self.private_market_name)

    def test_003_navigate_somewhere_else_in_the_app_and_back_to_homepage(self):
        """
        DESCRIPTION: Navigate somewhere else in the app and back to Homepage
        EXPECTED: * User lands on Your Enhanced Markets tab.
        """
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        terms_and_conditions = private_market_tab_content.terms_and_conditions
        self.assertTrue(terms_and_conditions.is_displayed(), msg="Link is not displayed")
        terms_and_conditions.click()
        self.site.wait_content_state_changed(timeout=10)
        if self.brand == 'ladbrokes':
            has_back_btn = self.site.has_back_button
            self.assertTrue(has_back_btn, msg='Event details page doesn\'t have back button')
            self.site.back_button.click()
        else:
            self.site.back_button_click()
        self.site.wait_content_state_changed(timeout=10)
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        terms_and_conditions = private_market_tab_content.terms_and_conditions
        self.assertTrue(terms_and_conditions.is_displayed(), msg="Link is not displayed")
