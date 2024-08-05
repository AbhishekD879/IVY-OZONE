import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot create event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C2496182_Featured_Module__Removing_Expired_Sport_Events_from_Module(BaseFeaturedTest):
    """
    TR_ID: C2496182
    NAME: Featured Module - Removing Expired <Sport> Events from Module
    DESCRIPTION: This test case verifies that <Sport> events are removed from displaying within Module on front-end
    PRECONDITIONS: 1) There are at least 2 <Sport> (Select Events by - 'Type' in CMS) events in module section
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
        DESCRIPTION: Create Football event and featured tab with selection - type
        """
        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.featured_module = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=type_id, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False, footer_link_url='https://sports.coral.co.uk/', show_all_events=True)

        event_1 = self.ob_config.add_football_event_to_featured_autotest_league()
        event_2 = self.ob_config.add_football_event_to_featured_autotest_league()

        self.__class__.eventID_1 = event_1.event_id
        self.__class__.event_names = [f'{event_1.team1} v {event_1.team2}', f'{event_2.team1} v {event_2.team2}']
        self.__class__.prices = []
        outcomes = event_1.ss_response['event']['children'][0]['market']['children']
        for outcome in outcomes:
            price_resp = outcome["outcome"]["children"][0]["price"]
            self.prices.append(f'{price_resp["priceNum"]}/{price_resp["priceDen"]}')

        self.__class__.featured_module = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=type_id, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False, footer_link_url='https://sports.coral.co.uk/', show_all_events=True)
        self.__class__.featured_module_name = self.featured_module['title'].upper()

        self._logger.info(f'*** Created Featured Module: "{self.featured_module_name}"')

    def test_001_go_to_home_page__featured_module(self):
        """
        DESCRIPTION: Go to Home page > Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_002_find_module_with_sport_events_from_preconditions(self):
        """
        DESCRIPTION: Find module with <Sport> events from preconditions
        EXPECTED: Events are displayed with correct outcomes
        """
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        section = featured_module.accordions_list.items_as_ordered_dict.get(self.featured_module_name)
        self.assertTrue(section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')
        section.expand()
        event_name = [event_name for event_name in section.items_as_ordered_dict.keys()]
        self.assertEqual(sorted(self.event_names),
                         sorted(event_name), msg=f'Event from UI "{event_name} is not matching "{self.event_names}""')
        outcomes = section.items_as_ordered_dict[event_name[0]].template.items_names
        self.assertEqual(sorted(self.prices), sorted(outcomes),
                         msg=f'Outcome on UI "{outcomes} is not matching with "{self.prices}""')

    def test_003_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=False, active=False)

        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        self.site.wait_splash_to_hide()

        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        section = featured_module.accordions_list.items_as_ordered_dict.get(self.featured_module_name)
        self.assertTrue(section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')

        section.expand()
        cards = section.items_as_ordered_dict
        self.assertIn(self.event_names[1], list(cards.keys()),
                      msg=f'Event name "{self.event_names[1]}" is not in "{list(cards.keys())}"')
