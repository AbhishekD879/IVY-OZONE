import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import normalize_name
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod # It is difficult to find event without primary market on prod
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.event_hub
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C14253858_Featured_module_by_Sport_Event_ID_Event_without_primary_market(Common):
    """
    TR_ID: C14253858
    VOL_ID: C58600176
    NAME: Featured module by <Sport> Event ID: Event without primary market
    DESCRIPTION: This test verifies the case when Event Hub Featured event module is created using Event that doesn't have a primary market available but has other active markets available(not primary markets)
    PRECONDITIONS: 1. Active Event Hub and Event Hub tab is created in CMS.
    PRECONDITIONS: 2. Featured module by Event id without primary market should be created in CMS-> Sport Pages -> Event Hub-> <eventHub> -> Featured events.
    PRECONDITIONS: 2. User should be on homepage <eventHub> tab
    PRECONDITIONS: List of primary markets:
    PRECONDITIONS: - Win or Each Way
    PRECONDITIONS: - Match Betting,
    PRECONDITIONS: - Match Results,
    PRECONDITIONS: - Extra Time Result,
    PRECONDITIONS: - Extra-Time Result,
    PRECONDITIONS: - Penalty Shoot-Out Winner,
    PRECONDITIONS: - To Qualify
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Active Event Hub and Event Hub tab is created in CMS.
        DESCRIPTION: 2. Featured module by Event id without primary market should be created in CMS-> Sport Pages -> Event Hub-> <eventHub> -> Featured events.
        DESCRIPTION: 2. User should be on homepage <eventHub> tab
        DESCRIPTION: List of primary markets:
        DESCRIPTION: - Win or Each Way
        DESCRIPTION: - Match Betting,
        DESCRIPTION: - Match Results,
        DESCRIPTION: - Extra Time Result,
        DESCRIPTION: - Extra-Time Result,
        DESCRIPTION: - Penalty Shoot-Out Winner,
        DESCRIPTION: - To Qualify
        """
        # Create event
        self.__class__.market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        football_config = self.ob_config.football_config
        event_params = self.ob_config.add_sport_event(
            class_id=football_config.autotest_class.class_id,
            category_id=football_config.category_id,
            type_id=football_config.autotest_class.autotest_premier_league.type_id,
            default_market_name=self.market_name,
            market_template_id=football_config.autotest_class.autotest_premier_league.market_template_id)

        eventID = event_params.event_id

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])

        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')

        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                              id=eventID,
                                                              page_type='eventhub',
                                                              page_id=index_number)
        self.__class__.module_name = module_data['title'].upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get('modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=60,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_find_featured_module_by_event_id_from_preconditions_and_verify_displaying_of_the_module(self):
        """
        DESCRIPTION: Find Featured module by Event Id from preconditions and verify displaying of the module
        EXPECTED: * Featured module by Event Id is displayed with the accordion
        EXPECTED: * Event inside the module is displayed without Market/Selections
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        events = self.event_hub_module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on "{self.module_name}"')
        self.__class__.event = events.get(self.event_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" was not found')

        has_markets = self.event.has_markets(expected_result=False)
        self.assertFalse(has_markets, msg=f'Markets are displayed for event "{self.event_name}"')

    def test_002_tap_on_the_event_inside_the_module_and_verify_redirection_to_the_event_details_page(self):
        """
        DESCRIPTION: Tap on the Event inside the module and verify redirection to the Event Details page
        EXPECTED: * User is redirected to Event Details Page
        EXPECTED: * Other active markets of the Event are shown on Event Details Page
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
        accordions_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions_list, msg='No market was found on page')
        market_name = self.market_name if self.brand == 'ladbrokes' else self.market_name.upper()
        self.assertTrue(accordions_list.get(market_name), msg=f'Market "{market_name}" was not found among markets '
                                                              f'"{accordions_list.keys()}"')
