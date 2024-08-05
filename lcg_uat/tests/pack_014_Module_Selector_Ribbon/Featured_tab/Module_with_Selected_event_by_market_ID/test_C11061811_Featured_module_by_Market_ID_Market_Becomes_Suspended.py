import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend events in prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C11061811_Featured_module_by_Market_ID_Market_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C11061811
    NAME: Featured module by Market ID: Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when the market becomes suspended in Featured module by Market ID
    PRECONDITIONS: 1. Module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in CMS and is expanded by default.
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ  - currently supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event ID
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def verify_price_buttons(self, is_enabled=True):
        """
        Verifies if all Price/Odds buttons are enabled/disabled and if prices is still displayed
        :param is_enabled: specifies if the buttons are expected to be enabled
        """
        self.__class__.module = self.get_section(section_name=self.module_name)
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            if is_enabled:
                self.assertTrue(bet_button.is_enabled(timeout=60, expected_result=True),
                                msg=f'"{selection_name}" selection is not active in "{self.module_name}" module')
            else:
                self.assertFalse(bet_button.is_enabled(timeout=60, expected_result=False),
                                 msg=f'"{selection_name}" selection is not suspended in "{self.module_name}" module')
            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed in "{self.module_name}" module')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED: * The configured module is displayed on Featured tab and is expanded by default
        EXPECTED: * All 'Price/Odds' buttons are active
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = params.event_id
        self.__class__.market_id = params.default_market_id
        self.__class__.selection_ids = params.selection_ids

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Market', id=self.market_id,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED:
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        module = self.get_section(section_name=self.module_name)
        self.assertTrue(module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')

    def test_002_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED: Event is suspended
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=False)
        sleep(3)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        market = event_details['children'][0]['market']
        self.assertEqual(market['marketStatusCode'], 'S', msg=f'Actual marketStatusCode "{market["marketStatusCode"]}"'
                                                              f'is not equal to expected code "S"')

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this market immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.verify_price_buttons(is_enabled=False)

    def test_004_change_attribute_for_this_event_in_timarketstatuscodea(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"**
        EXPECTED: Event is active
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=True)
        sleep(3)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        market = event_details['children'][0]['market']
        self.assertEqual(market['marketStatusCode'], 'A', msg=f'Actual marketStatusCode "{market["marketStatusCode"]}"'
                                                              f'is not equal to expected code "A"')

    def test_005_verify_outcomes_for_the_market(self):
        """
        DESCRIPTION: Verify outcomes for the market
        EXPECTED: * All 'Price/Odds' buttons of this market immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this market are not disabled anymore
        """
        self.verify_price_buttons()

    def test_006_collapse_the_module_from_the_previous_step(self):
        """
        DESCRIPTION: Collapse the module from the previous step
        EXPECTED:
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_007_change_attribute_in_ti_for_this_eventmarketstatuscodes(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=False)
        sleep(4)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        market = event_details['children'][0]['market']
        self.assertEqual(market['marketStatusCode'], 'S', msg=f'Actual marketStatusCode "{market["marketStatusCode"]}"'
                                                              f'is not equal to expected code "S"')

    def test_008_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons(is_enabled=False)

    def test_009_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED:
        """
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_010_change_attribute_in_ti_for_this_eventmarketstatuscodea(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"**
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=True)
        sleep(3)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        market = event_details['children'][0]['market']
        self.assertEqual(market['marketStatusCode'], 'A', msg=f'Actual marketStatusCode "{market["marketStatusCode"]}"'
                                                              f'is not equal to expected code "A"')

    def test_011_expand_module_and_verify_outcomes_for_the_market(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the market
        EXPECTED: * All 'Price/Odds' buttons of this market immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this market are not disabled anymore
        """
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        self.verify_price_buttons()
