import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726257_Event_Hub_Verify_Module_Section(Common):
    """
        TR_ID: C9726257
    NAME: Event Hub: Verify Module Section
    DESCRIPTION: This test case verifies Module Section on the Event Hub tab (mobile/tablet)
    PRECONDITIONS: 1) Event Hub is configured in CMS and there are more than one event/selection in the module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX ?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) User is on Event Hub tab
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) 2 Featured Modules created in CMS > Sport Pages > Event Hub > Edit Event Hub. Modules are Active and are displayed on Event Hub tab in app.
        """
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        eventID1 = event_params1.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_footer = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=eventID1, page_type='eventhub', page_id=index_number,
            events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10, footer_link_url=tests.HOSTNAME)
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.__class__.event_hub_footer = module_footer['footerLink']['text']
        self.__class__.event_hub_footer_url_cms = module_footer['footerLink']['url']
        self.__class__.show_expanded_status = module_footer['showExpanded']
        self.__class__.no_of_events = module_footer['maxSelections']

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
    def test_001_verify_name_ofmodule(self):
        """
        DESCRIPTION: Verify name of **Module**
        EXPECTED: Module name corresponds to the name set in 'Module Title' field in CMS ('title' attribute)
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

        self.__class__.event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(self.event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')

    def test_002_verify_default_state_of_module(self):
        """
        DESCRIPTION: Verify default state of Module
        EXPECTED: Module is expanded/collapsed depending on value 'Expanded by default' selected in CMS ('showExpanded' attribute - true/false)
        """
        module_name, self.__class__.event_hub_module = list(self.event_hub_modules.items())[0]
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{module_name}" was not found on "{self.event_hub_tab_name}" tab')
        if self.show_expanded_status:
            self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                            msg=f'Module: "{self.event_hub_tab_name}" not expanded')

    def test_003_verify_icons_on_module_accordion_header(self):
        """
        DESCRIPTION: Verify icons on module accordion (header)
        EXPECTED: * 'Special' or 'Enhanced' badge can be displayed if configured
        EXPECTED: OR
        EXPECTED: * # (YourCall) icon and/or 'Cash Out' icon can be displayed if available
        """
        # Todo Data is not available

    def test_004_verify_footer_link_if_name_of_link_is_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Text of link corresponds to text set in 'Footer link text' field in CMS ('text' attribute)
        """
        footer_text = self.event_hub_module.show_more.text
        self.assertEqual(footer_text, self.event_hub_footer, msg=f'Footer link text is : "{footer_text}"'
                                                                 f' not expected as {self.event_hub_footer}')

    def test_005_verify_footer_link_if_name_of_link_is_not_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is NOT set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Footer link is shown in the format:
        EXPECTED: **View All <number of all events> <name of module> Events**
        """
        footer_text = self.event_hub_module.show_more.text
        if not self.event_hub_footer:
            self.assertEqual(footer_text, self.event_hub_footer, msg=f'Footer link text is : "{footer_text}"'
                                                                     f' not expected as {self.event_hub_footer}')

    def test_006_verify_number_of_events(self):
        """
        DESCRIPTION: Verify Number of Events
        EXPECTED: It is number of all existing events for verified ID of **Type**/*Market/Class*... depending on value selected in 'Select Events by' and 'Max Events to Display' fields
        """
        num_of_events_to_display = len(self.event_hub_modules)
        self.assertTrue(num_of_events_to_display <= self.no_of_events,
                        msg=f'Number of selections for module is not more then {self.no_of_events}'
                            f'current {num_of_events_to_display}')

    def test_007_clicktap_footer_link(self):
        """
        DESCRIPTION: Click/Tap Footer link
        EXPECTED: User is redirected to the url set in 'Footer link URL' field in CMS ('url' attribute - e.g. football/today)
        """
        self.event_hub_module.show_more.click()
        self.site.wait_content_state("Homepage")
        current_url = self.device.get_current_url()
        self.assertIn(self.event_hub_footer_url_cms, current_url, msg=f'Actual Url is : "{current_url}"'
                                                                      f' not matching with expected url as '
                                                                      f'{self.event_hub_footer_url_cms}')
