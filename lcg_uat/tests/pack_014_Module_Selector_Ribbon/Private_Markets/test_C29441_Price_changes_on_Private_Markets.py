import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
# @pytest.mark.stg2 #TODO VOL-2175
@pytest.mark.liveserv_updates
@pytest.mark.private_markets
@pytest.mark.module_ribbon
@pytest.mark.promotions_banners_offers
@pytest.mark.desktop
@pytest.mark.homepage
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-2175')
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-56552')
@vtest
class Test_C29441_Price_changes_on_Private_Markets(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C29441
    NAME: Price changes on Private Markets
    DESCRIPTION: This test case verifies Price changes on Private Markets
    PRECONDITIONS: User should be logged in and has Private Market available
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True
    new_price = '2/1'
    price = '1/2'
    final_price = None
    selection_id = None

    @classmethod
    def custom_tearDown(cls):
        if cls.final_price != cls.price:
            cls.get_ob_config().change_price(selection_id=cls.selection_id, price=cls.price)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event in OB TI and set up private market
        DESCRIPTION: Log in with user with Private Markets available
        EXPECTED: Event created and Private Market is set up
        EXPECTED: User with Private Markets is logged in
        """
        self.__class__.selection_id = super().pm_selection_id
        user = tests.settings.user_with_private_market
        self.site.login(username=user, async_close_dialogs=False)
        self.trigger_private_market_appearance(
            user=user,
            expected_market_name=self.private_market_name)

    def test_001_trigger_price_change_for_private_market_outcome(self):
        """
        DESCRIPTION: Trigger price change for private market outcome
        EXPECTED: 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: *   blue color if price has decreased
        EXPECTED: *   pink color if price has increased
        """
        if self.device_type == 'mobile':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            tab_name = self.expected_sport_tabs.private_market
            self.assertTrue(tabs, msg='No tabs are displayed at the Home page')
            self.assertIn(tab_name, tabs.keys(), msg=f'Tab "{tab_name}" is not displayed for the user')
            self.assertTrue(tabs[tab_name].is_selected(), msg=f'Tab "{tab_name}" is not selected by default')

        pm_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        markets = pm_tab_content.accordions_list.items_as_ordered_dict
        market = markets.get(self.private_market_name.upper())
        self.assertTrue(market, msg=f'Market "{self.private_market_name.upper()}" is not found')
        market.show_all_button.click()

        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)
        self.__class__.final_price = self.new_price
        result = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id, price=self.new_price)
        self.assertTrue(result, msg=f'Price update for "{self.selection_id}" is not received')

        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are displayed')
        self.assertIn(self.private_outcome_name, outcomes.keys(), msg=f'Outcome "{self.outcome_name}" is not displayed')

        self.__class__.outcome = outcomes.get(self.private_outcome_name)
        self.assertTrue(self.outcome, msg=f'Outcome "{self.private_outcome_name}" is not found in "{outcomes.keys()}"')
        price_changed = self.outcome.bet_button.is_price_changed(expected_price=self.new_price, timeout=2)
        self.assertTrue(price_changed, msg=f'Price for Private Market outcome did not change. \n'
                        f'Actual price: {self.outcome.bet_button.name} is not as expected: {self.new_price}')

    def test_002_in_ti_tool_decrease_the_price_for_linked_lp_selection_in_application_verify_live_price_update(self):
        """
        DESCRIPTION: - In TI tool decrease the price for linked LP selection
        DESCRIPTION: - In application verify live price update
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price)

        result = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id, price=self.price)
        self.assertTrue(result, msg=f'Price update for "{self.selection_id}" is not received')

        price_changed = self.outcome.bet_button.is_price_changed(expected_price=self.price, timeout=5)
        self.assertTrue(price_changed, msg=f'Price for Private Market outcome did not change. \n'
                        f'Actual price: {self.outcome.bet_button.name} is not as expected: {self.price}')

        self.__class__.final_price = self.outcome.bet_button.name
