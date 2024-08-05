import pytest
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live price updates cannot be tested on prod and hl
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.liveserv_updated
@pytest.mark.module_ribbon
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9726388_Featured_Module__Removing_Expired_Boosted_Selection_from_Module(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C9726388
    NAME: Featured Module - Removing Expired Boosted Selection from Module
    DESCRIPTION: This test case verifies that Boosted Selection is removed from displaying within Module on front-end
    PRECONDITIONS: 1) There is a Selection (Select Events by - 'Selection' in CMS) in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horse racing event
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp=False, sp=True)
        self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.__class__.eventID = event.event_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection',
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False,
            id=self.selection_id)['title'].upper()

    def test_001_go_to_home_page__featured_module(self):
        """
        DESCRIPTION: Go to Home page > Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()

    def test_002_find_module_with_a_selection_from_preconditions(self):
        """
        DESCRIPTION: Find module with a Selection from preconditions
        EXPECTED: Selection is displayed with correct outcome
        """
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        section.scroll_to()
        try:
            section.expand()
            self.assertTrue(section.is_expanded(bypass_exceptions=(), timeout=5), msg=f'{section.name} is not expanded')
        except (StaleElementReferenceException, VoltronException):
            section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.assertTrue(self.section.is_expanded(timeout=10), msg=f'{self.section.name} is not expanded')
        bet_buttons = self.section.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')

    def test_003_trigger_completionexpiration_one_of_the_event_that_include_the_selection(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the event that include the selection
        EXPECTED: The Selection of completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False)
        self.device.refresh_page()
        if self.device_type == 'desktop' and self.brand == 'ladbrokes':
            self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
            bet_buttons = self.section.get_available_prices()
            self.assertFalse(bet_buttons, msg='selections found')
        else:
            featured_module = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertFalse(section, msg=f'Section "{self.module_name}" is found on FEATURED tab')
