import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C2507461_Featured_Module_by_Race_TypeID__Verify_names_displaying_within_Featured_tab(BaseFeaturedTest, BaseGreyhound):
    """
    TR_ID: C2507461
    NAME: Featured: Module by <Race> TypeID - Verify names displaying within Featured tab
    DESCRIPTION: This test case verifies whether event/selection names are displayed correctly on the frontend for Featured tab module by <Race> TypeID
    PRECONDITIONS: 1) Featured Module by <Race> TypeID is created in CMS. Module should contain at least 1 Event and 1 Selection with long name. Name can be modified in TI or in CMS Featured Module edit page.
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
    PRECONDITIONS: Virtual HR/GH events are supported as well for Featured module created by RaceTypeID
    """
    keep_browser_open = True
    type_id = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Greyhound event
        """
        self.__class__.featured_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured) if self.device_type == 'mobile' \
            else vec.sb_desktop.FEATURED_MODULE_NAME
        self.setup_cms_next_races_number_of_events()
        event_params = self.ob_config.add_UK_greyhound_racing_event(time_to_start=10, ew_terms=self.ew_terms,
                                                                    cashout=True)
        self.__class__.type_id = self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.type_id
        self.__class__.eventID = event_params.event_id
        self.__class__.name_pattern = self.greyhound_autotest_name_pattern.upper() if self.brand == 'ladbrokes' \
            else self.greyhound_autotest_name_pattern
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.type_id, show_expanded=True, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_navigane_to_homepage__featured_tab(self):
        """
        DESCRIPTION: Navigate to Homepage > Featured tab
        EXPECTED: * Active Featured modules are displayed in Featured tab
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

    def test_002_expand_featured_module_from_preconditions(self):
        """
        DESCRIPTION: Expand Featured Module from Preconditions
        EXPECTED: * Events are displayed within the module as per CMS configuration
        EXPECTED: * <Race> events' long names are cropped and followed with '...' before the price/odds buttons / scores (if available)
        EXPECTED: * <Race> selection name are cropped and followed with '...' before the price/odds buttons / scores (if available)
        """
        if self.device == 'mobile':
            section1 = self.get_section(section_name=self.module_name)
            section1.expand()

    def test_003_verify_the_view_of_the_module(self):
        """
        DESCRIPTION: Verify the view of the module
        EXPECTED: **Coral** Module consists of:
        EXPECTED: - Header of the module with <Name> and 'See all' link (navigating to HR landing page)
        EXPECTED: - Below the header the next race information: time (eg. 14:10 ) / event name (eg. Fakenham)/ Each Way option (eg. E/W 1/4 odds - places 1-2") / places/ Start time (eg. Starts 13:18) / 'More' link (navigating the user to the specific race card)
        EXPECTED: - Race card with events and price odds buttons
        EXPECTED: - Any promo signposting icons (like 'Extra Place') are displayed at the top left corner of race card (NOT in the header of the module or on market level)
        EXPECTED: **Ladbrokes** Module consists of:
        EXPECTED: * Collapsible Header(Featured race) with 'See All' link navigating the user to the HR landing page
        EXPECTED: * Header with the Name, Time, countdown timer (when available), type of race, going and 'More' link navigating the user to the specific race card
        EXPECTED: * Below header goes E/W terms and watch icon (if the stream is available) at the top of race card
        EXPECTED: * Promo Icons when available (placed right above E/W terms) on the race card
        EXPECTED: * For each horse the full silk, Name of the horse, Name of the jockey and trainer, Form of the horse and odds button as per the design, and last 2 odds are displayed
        """
        featured_content = self.site.home.get_module_content(module_name=self.featured_name).accordions_list.items_as_ordered_dict
        self.assertTrue(featured_content, msg='"Featured" module does not contain any accordions')
        featured_modules = featured_content.keys()
        self.assertIn(self.module_name, featured_modules,
                      msg=f'Module "{self.module_name}" is not displayed. '
                          f'Please check list of all displayed modules:\n"{featured_modules}"')

        self.__class__.module = featured_content[self.module_name]
        self.assertTrue(self.module, msg='No accordions displayed in "Featured" section on Home page')
        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found in module "{self.module_name}"')
        for event_name, event in events.items():
            event.scroll_to()
            if self.brand == 'ladbrokes' or self.device_type == 'mobile':
                self.assertTrue(event.has_each_way_terms(), msg=f'Event "{self.event_name}" does not have Each Way Terms')
            self.assertTrue(event.has_view_full_race_card(),
                            msg=f'Event "{self.event_name}" does not View Full Race Card Link')
            outcomes = event.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for event "{self.event_name}"')
            for outcome_name, outcome in outcomes.items():
                outcome.bet_button.scroll_to()
                self.assertTrue(outcome.runner_info.has_silks, msg=f'Outcome "{outcome_name}" does not have silk')
                self.assertTrue(outcome.bet_button.outcome_price_text,
                                msg=f'Outcome "{outcome_name}" does not have price')

    def test_004_verify_names_displaying_for_virtual_horsesgreyhounds_within_featured_module(self):
        """
        DESCRIPTION: Verify names displaying for Virtual Horses/Greyhounds within Featured module
        EXPECTED: Expected result is the same as on step 3
        """
        # Covered in step 3
