import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot undisplay event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C2496177_Featured_Module__Removing_Expired_Race_Events_from_Module(BaseGreyhound, BaseFeaturedTest):
    """
    TR_ID: C2496177
    NAME: Featured Module - Removing Expired <Race> Events from Module
    DESCRIPTION: This test case verifies that <Race> events are removed from displaying within Module on front-end
    PRECONDITIONS: 1) There are at least 2 <Race> (Select Events by - 'Race Type ID' in CMS) events in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
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

    def test_001_go_to_home_page__featured_module(self):
        """
        DESCRIPTION: Go to Home page > Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
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
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False)
        self.device.refresh_page()
        event = self.module.items_as_ordered_dict
        self.assertFalse(event, msg="expired event is not removed from front-end")

    def test_002_find_module_with_racetypeid_events_from_preconditions(self):
        """
        DESCRIPTION: Find module with <Race>typeID) events from preconditions
        EXPECTED: Events are displayed with correct outcomes
        """
        # covered in step 1

    def test_003_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        # covered in step 1
