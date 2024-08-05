import pytest
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C2507417_Featured_Module_by_Sport_Race_Selections_ID__Verify_names_displaying_within_Featured_tab(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C2507417
    NAME: Featured: Module by <Sport>/<Race> Selections ID - Verify names displaying within Featured tab
    DESCRIPTION: This test case verifies whether selection names are displayed correctly on the frontend for Featured tab module by <Sport>/<Race> SelectionID
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) Featured Module by <Sport>/<Race> SelectionID is created in CMS. Module should contain a selection with long name. Name can be modified in TI or in CMS Featured Module edit page.
        PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
        PRECONDITIONS: (check <CMS_ENDPOINT> via 'devlog' function)
        PRECONDITIONS: 3) http://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
        PRECONDITIONS: XXX - the event ID
        PRECONDITIONS: X.XX - current supported version of OpenBet release
        PRECONDITIONS: LL - language (e.g. en, ukr)
        PRECONDITIONS: Where, domain is:
        PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
        PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
        PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
        PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=['1/5'])
        self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[0]
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Selection',
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10,
                                                                             show_expanded=False,
                                                                             id=self.selection_id)['title'].upper()

    def test_001_navigane_to_homepage__featured_tab(self):
        """
        DESCRIPTION: Navigane to Homepage > Featured tab
        EXPECTED: * Active Featured modules are displayed in Featured tab
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.featured_module = \
            self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        self.featured_module.scroll_to()

    def test_002_expand_featured_module_from_preconditions(self):
        """
        DESCRIPTION: Expand Featured Module from Preconditions
        EXPECTED: * Selection is shown within the module as per CMS configuration
        EXPECTED: * <Sport>/<Race> selection's long name is NOT cropped and is fully shown in several rows
        """
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        section.scroll_to()
        try:
            section.expand()
            self.assertTrue(section.is_expanded(bypass_exceptions=(), timeout=5),
                            msg=f'{section.name} is not expanded')
        except (StaleElementReferenceException, VoltronException):
            section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.assertTrue(section.is_expanded(timeout=10), msg=f'{section.name} is not expanded')
        bet_buttons = section.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found')
        selection_name_ui, selection_ui = list(bet_buttons.items())[0]
        self.assertEqual(selection_name_ui, self.selection_name,
                         msg=f'Actual selection name: "{selection_name_ui}"'
                             f' is not same as Expected selection name: "{self.selection_name}"')
