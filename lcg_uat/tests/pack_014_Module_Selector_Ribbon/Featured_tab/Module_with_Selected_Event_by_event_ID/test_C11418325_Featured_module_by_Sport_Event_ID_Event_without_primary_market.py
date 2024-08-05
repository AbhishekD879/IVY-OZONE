import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create events without primary market in prod/beta
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C11418325_Featured_module_by_Sport_Event_ID_Event_without_primary_market(BaseFeaturedTest):
    """
    TR_ID: C11418325
    NAME: Featured module by <Sport> Event ID: Event without primary market
    DESCRIPTION: This test verifies the case when Feature event module is created using Event that doesn't have a primary market available but has other active markets available(not primary markets)
    PRECONDITIONS: 1. Featured module by Event id without primary market should be created in CMS-> Featured Tab Module
    PRECONDITIONS: 2. User should be on homepage Featured tab.
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
        DESCRIPTION: 1. Featured module by Event id without primary market should be created in CMS-> Sport Pages -> Event Hub-> <eventHub> -> Featured events.
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

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_find_featured_module_by_event_id_from_preconditions_and_verify_displaying_of_the_module(self):
        """
        DESCRIPTION: Find Featured module by Event Id from preconditions and verify displaying of the module
        EXPECTED: * Featured module by Event Id is displayed with the accordion
        EXPECTED: * Event inside the module is displayed without Market/Selections
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        module = self.get_section(section_name=self.module_name)
        self.assertTrue(module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        events = module.items_as_ordered_dict
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
