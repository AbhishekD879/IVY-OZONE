import pytest
import tests
from tests.base_test import vtest
from crlat_ob_client.offer import Offer
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod-->applicable only for qa2 as we can not create private markets in prod
@pytest.mark.uat
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870309_Verify_availability_bet_placement_and_bet_history_for_Private_market(BaseCashOutTest, BasePrivateMarketsTest):
    """
    TR_ID: C44870309
    NAME: Verify availability, bet placement and bet history for Private market.
    PRECONDITIONS: 1. User is assigned private market token in Open Bet.
    PRECONDITIONS: 2. User is logged in the application.
    """
    keep_browser_open = True
    bet_amount = 1

    def test_001_place_a_bet_with_the_following_conditions_1_the_selection_should_be_from_football___premier_league_competition2_the_oddsprice_value_should_be_greater_than_13_stake_should_be_1_while_placing_the_betafter_the_bet_is_placed_navigate_to_the_home_page_and_verify(self):
        """
        DESCRIPTION: Place a bet with the following conditions:-
        DESCRIPTION: 1. The selection should be from Football -> Premier League competition
        DESCRIPTION: 2. The odds/price value should be greater than 1.
        DESCRIPTION: 3. Stake should be £1 while placing the bet.
        DESCRIPTION: After the bet is placed, navigate to the Home page and verify.
        EXPECTED: A tab 'Enhanced Markets' id displayed besides the 'Highlights' tab/Home page.
        """
        user = tests.settings.betplacement_user
        self.site.login(username=user)
        offer_id = self.ob_config.backend.ob.private_market_offer.offer_id
        offer = Offer(env=tests.settings.backend_env, brand=self.brand)
        self.trigger_private_market_appearance(user=user, expected_market_name=self.private_market_name)
        offer.give_offer(username=user, offer_id=offer_id)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('homepage')

    def test_002_click_on_the_tab_enhanced_markets_verify(self):
        """
        DESCRIPTION: Click on the tab Enhanced Markets. Verify.
        EXPECTED: Private market for the user is displayed with selection name and odds/price.
        """
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='"No tabs" are displayed at the Home page')

            tab_name = self.expected_sport_tabs.private_market
            self.assertIn(tab_name, tabs.keys(), msg=f'Tab "{tab_name}" is not displayed for the user')
            self.assertTrue(tabs[tab_name].is_selected(), msg=f'"{tab_name}" tab is not selected by default')
        else:
            sections = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(sections, msg='"Desktop sections" are not present')
            private_market_section = sections.get(self.expected_sport_tabs.private_market)
            self.assertTrue(private_market_section,
                            msg=f'Section "{self.expected_sport_tabs.private_market}" is not '
                                f'present in "{sections.keys()}"')
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        markets = private_market_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='"Private markets" are not found')
        market = markets.get(self.private_market_name.upper())
        self.assertTrue(market, msg=f'Market "{self.private_market_name.upper()}" not found in "{markets.keys()}"')
        if market.has_show_all_button:
            market.show_all_button.click()
        wait_for_result(lambda: self.private_outcome_name in market.items_as_ordered_dict,
                        timeout=3)

        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='"No outcomes" are displayed')
        self.assertIn(self.private_outcome_name, outcomes.keys(),
                      msg=f'Outcome "{self.private_outcome_name}" is not displayed')
        price = outcomes[self.private_outcome_name].bet_button.name
        self.assertTrue(price, msg=f'"{price}" is not displayed')

    def test_003_place_a_bet_on_the_private_market_and_verify(self):
        """
        DESCRIPTION: Place a bet on the private market and verify.
        EXPECTED: Bet on private market is placed successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.pm_selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.navigate_to_page('homepage')

    def test_004_navigate_to_my_bets_and_verify_in_open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets and verify in Open Bets.
        EXPECTED: The bet placed on private market in step 3 is displayed.
        """
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.private_outcome_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
