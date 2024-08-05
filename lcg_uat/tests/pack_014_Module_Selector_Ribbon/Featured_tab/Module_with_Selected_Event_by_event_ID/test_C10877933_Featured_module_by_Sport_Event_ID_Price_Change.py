import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # price updates are not for prod and hl
@pytest.mark.high
@pytest.mark.homepage_featured
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
@vtest
class Test_C10877933_Featured_module_by_Sport_Event_ID_Price_Change(BaseFeaturedTest):
    """
    TR_ID: C10877933
    VOL_ID: C12783672
    NAME: Featured module by <Sport> Event ID: Price Change
    DESCRIPTION: This test case verifies situation when price is changed for outcomes of  market on the 'Featured' tab (mobile/tablet)/ Featured section (desktop) of a module by <Sport> EventId
    PRECONDITIONS: 1. Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and contains event
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True
    initial_prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}
    new_price_1 = '11/17'
    new_price_2 = '33/5'
    new_price_3 = '1/5'
    new_price_4 = '1/17'

    def get_module(self):
        modules = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        ).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, modules,
                      msg=f'"{self.module_name}" module is not found among modules "{modules.keys()}"')
        return modules[self.module_name]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        DESCRIPTION: Create Featured module by eventID
        """
        params = self.ob_config.add_autotest_premier_league_football_event(lp=self.initial_prices,)
        self.__class__.eventID = params.event_id
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            params.team1, params.team2, params.selection_ids
        self.__class__.initial_prices[self.team1] = self.__class__.initial_prices['odds_home']
        self.__class__.initial_prices[self.team2] = self.__class__.initial_prices['odds_away']
        self.__class__.initial_prices['Draw'] = self.__class__.initial_prices['odds_draw']
        del self.__class__.initial_prices['odds_home'], self.__class__.initial_prices['odds_away'], self.__class__.initial_prices['odds_draw']

        self._logger.info(f'*** Created Football event with id "{self.eventID}"')

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_module()
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module}" module is not expanded')

    def test_002_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        EXPECTED: Other buttons are not changed if they are available
        """
        try:
            bet_buttons = self.module.get_available_prices()
        except (StaleElementReferenceException, VoltronException):
            self.__class__.module = self.get_module()
            bet_buttons = self.module.get_available_prices()
        bet_button_draw = bet_buttons.get('Draw')
        start_draw_price = bet_button_draw.outcome_price_text
        self.ob_config.change_price(selection_id=self.selection_ids[self.team2], price=self.new_price_1)

        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_ids[self.team2],
                                                                            price=self.new_price_1)
        self.assertTrue(price_update_received, msg='Price update was not received')

        try:
            bet_buttons = self.module.get_available_prices()
        except (StaleElementReferenceException, VoltronException):
            self.__class__.module = self.get_module()
            bet_buttons = self.module.get_available_prices()

        self.assertTrue(bet_buttons, msg=f'No selections found in module "{self.module_name}"')

        bet_button_team2 = bet_buttons.get(self.team2)
        self.assertTrue(bet_button_team2,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.module_name}"')
        bet_button_team2.scroll_to()
        self.assertTrue(bet_button_team2.is_price_changed(expected_price=self.new_price_1, timeout=2),
                        msg=f'Price of "{self.team2}" was not changed to "{self.new_price_1}"')
        bet_button_team1 = bet_buttons.get(self.team1)
        self.assertTrue(bet_button_team1,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')

        bet_button_draw = bet_buttons.get('Draw')
        self.assertTrue(bet_button_draw,
                        msg=f'Draw selection bet button is not found within module "{self.module_name}"')
        team1_price = bet_button_team1.outcome_price_text
        self.assertEqual(team1_price, self.initial_prices.get(self.team1),
                         msg=f'Price of "{self.team1}" "{team1_price}" is not the same as expected'
                             f' "{self.initial_prices.get(self.team1)}"')
        bet_button_draw = bet_buttons.get('Draw')
        draw_price = bet_button_draw.outcome_price_text
        self.assertEqual(draw_price, start_draw_price,
                         msg=f'Price of Draw "{draw_price}" is not the same as expected'
                             f' "{start_draw_price}"')

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        """
        try:
            self.module.collapse()
        except (StaleElementReferenceException, VoltronException):
            self.module = self.get_module()
            self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'"{self.module_name}" module is not collapsed')

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.new_price_2)

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        try:
            self.module.expand()
            self.assertTrue(self.module.is_expanded(timeout=3, bypass_exceptions=()),
                            msg=f'"{self.module_name}" module is not expanded')
        except (StaleElementReferenceException, VoltronException):
            self.module = self.get_module()
            self.module.expand()
            self.assertTrue(self.module.is_expanded(timeout=3), msg=f'"{self.module_name}" module is not expanded')
        self.assertTrue(self.module.is_expanded(timeout=3), msg=f'"{self.module_name}" module is not expanded')

        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_ids[self.team1],
                                                                            price=self.new_price_2)
        self.assertTrue(price_update_received, msg='Price update was not received')

        try:
            bet_buttons = self.module.get_available_prices()
        except (StaleElementReferenceException, VoltronException):
            self.module = self.get_module()
            bet_buttons = self.module.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found in module "{self.module_name}"')

    def test_006_trigger_price_change_for_a_few_outcomes_from_the_same_market(self):
        """
        DESCRIPTION: Trigger price change for a few outcomes from the same market
        EXPECTED: All 'Price/Odds' buttons display new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team2], price=self.new_price_3)
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.new_price_4)

        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_ids[self.team2],
                                                                            price=self.new_price_3)
        self.assertTrue(price_update_received, msg=f'Price update was not received for selection "{self.team2}",'
                                                   f' id: "{self.selection_ids[self.team2]}"')

        price_update2_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                             selection_id=self.selection_ids[self.team1],
                                                                             price=self.new_price_4)
        self.assertTrue(price_update2_received, msg=f'Price update was not received for selection "{self.team1}",'
                                                    f' id: "{self.selection_ids[self.team1]}"')

        try:
            bet_buttons = self.module.get_available_prices()
        except (StaleElementReferenceException, VoltronException):
            self.__class__.module = self.get_module()
            bet_buttons = self.module.get_available_prices()

        self.assertTrue(bet_buttons, msg=f'No selections found in module "{self.module_name}"')
        bet_button_team1 = bet_buttons.get(self.team1)
        self.assertTrue(bet_button_team1,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')
        self.assertTrue(bet_button_team1.is_price_changed(expected_price=self.new_price_4, timeout=2),
                        msg=f'Price of "{self.team1}" was not changed to "{self.new_price_4}"')

        bet_button_team2 = bet_buttons.get(self.team2)
        self.assertTrue(bet_button_team2,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.module_name}"')

        self.assertTrue(bet_button_team2.is_price_changed(expected_price=self.new_price_3, timeout=2),
                        msg=f'Price of "{self.team2}" was not changed to "{self.new_price_3}"')
