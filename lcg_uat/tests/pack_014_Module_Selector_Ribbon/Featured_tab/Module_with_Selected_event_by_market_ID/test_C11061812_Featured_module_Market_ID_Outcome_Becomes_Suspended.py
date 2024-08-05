import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot suspend event in prod/beta
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C11061812_Featured_module_Market_ID_Outcome_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11061812
    NAME: Featured module Market ID: Outcome Becomes Suspended
    DESCRIPTION: This test case verifies situation when outcome/outcomes become suspended on Home page on the 'Featured' tab(mobile/tablet)
    PRECONDITIONS: 1. Module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in CMS and is expanded by default.
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: * Z.ZZ  - currently supported version of OpenBet SiteServer
    PRECONDITIONS: * XXXX - event ID
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = params.event_id
        market_id = params.default_market_id
        self.__class__.selection_ids = list(params.selection_ids.values())

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Market', id=market_id,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')

    def test_002_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_of_the_market(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True,
                                              active=False)
        sleep(3)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'S', msg=f'Not matching actual code "{selection["outcomeStatusCode"]}"'
                                                                  f'is not equal to "S"')

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * Only one Price/Odds button is disabled immediately
        EXPECTED: * The rest Price/Odds buttons of the same market are not changed
        """
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertFalse(bet_button1.is_enabled(timeout=15, expected_result=False),
                         msg=f'selection is active in "{self.module_name}" module')
        bet_button2 = self.module.get_bet_button_by_selection_id(self.selection_ids[1])
        self.assertTrue(bet_button2.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')
        bet_button3 = self.module.get_bet_button_by_selection_id(self.selection_ids[2])
        self.assertTrue(bet_button3.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')

    def test_004_change_attribute_for_this_eventoutcomestatuscodea_for_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        EXPECTED: * Price/Odds button of this outcome is not disabled anymore
        EXPECTED: * Price/Odds button becomes active
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True,
                                              active=True)
        sleep(3)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg="Not matching")
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')

    def test_005_find_another_event_with_priceodds_buttons_that_displaying_prices(self):
        """
        DESCRIPTION: Find another event with 'Price/Odds' buttons that displaying prices
        """
        # covered in above step
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_006_trigger_the_following_situation_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_of_the_market_or_win_or_each_way_for_races_market_type(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market (or 'Win Or Each Way' for <Races>) market type
        """
        self.test_002_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodes_for_one_of_the_outcomes_of_the_market()

    def test_007_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * Only one Price/Odds button is disabled immediately
        EXPECTED: * The rest Price/Odds buttons of the same market are not changed
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.test_003_verify_outcomes_for_the_event()

    def test_008_collapse_module(self):
        """
        DESCRIPTION: Collapse module
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_009_change_attribute_for_this_eventoutcomestatuscodea_for_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True,
                                              active=True)
        sleep(4)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        selection = event_details['children'][0]['market']['children'][0]['outcome']
        self.assertEqual(selection['outcomeStatusCode'], 'A', msg=f'Not matching actual code "{selection["outcomeStatusCode"]}"'
                                                                  f'is not equal to "A"')

    def test_010_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * Price/Odds button of this outcome is not disabled anymore
        EXPECTED: * Price/Odds button becomes active
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')
