import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  we cannot settle the events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C47763968_Verify_BOG_icon_on_My_Bets_section(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C47763968
    NAME: Verify BOG icon on My Bets section
    DESCRIPTION: This test case verifies that the BOG icon is displayed on the Bet Receipt and My Bets section
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has a positive balance
    PRECONDITIONS: * User has already placed a bet which is impacted by BOG
    PRECONDITIONS: * BOG has been enabled in CMS
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '2/3', 2: '1/3', 3: '1/4', 4: '1/6'}
    increased_Price = '10/1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: * Signposting toggle is Turn ON in the CMS
        DESCRIPTION: * User is logged in and has a positive balance
        DESCRIPTION: * User has already placed a bet which is impacted by BOG
        """
        bog_toggle_status = self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration']['BogToggle']['bogToggle']
        if not bog_toggle_status:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
            self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')

        event = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.event_id = event.event_id
        self.__class__.market_id = event.market_id
        self.__class__.created_event_name = event[6]['event']['name']
        self.__class__.selection_id = list(event.selection_ids.values())[0]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)
        self.assertTrue(self.site.bet_receipt.has_bog_icon_signpost(),
                        msg='"bog icon" signpost is not displayed')
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

    def test_001_open_open_bets_tab_in_my_bets_section(self):
        """
        DESCRIPTION: Open 'Open bets' tab in 'My Bets' section
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        self.site.open_my_bets_open_bets()
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertTrue(bet.bog_icon, msg='BOG icon is not displayed in open bet')
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{bet_name}"')
        betleg_name, betleg = list(betlegs.items())[0]
        self.__class__.actual_price = betleg.odds_value

    def test_002_switch_to_cash_out_tab(self):
        """
        DESCRIPTION: Switch to 'Cash out' tab
        EXPECTED: * 'Cash out' tab is displayed
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            wait_for_result(lambda: self.site.cashout.tab_content.accordions_list.is_displayed(timeout=10) is True,
                            timeout=60)
            bet_name, bet = self.site.cashout.tab_content.accordions_list. \
                get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name,
                        number_of_bets=1)
            self.assertTrue(bet.bog_icon, msg='BOG icon is not displayed in open bet')

    def test_003_verify_bog_icon_on_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'BOG' icon on 'Cash out' tab
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        # covered in step 2

    def test_004_switch_to_settled_bets_tab(self):
        """
        DESCRIPTION: Switch to 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab is displayed
        """
        # covered in step 5

    def test_005_verify_bog_icon_on_settled_bets_tab(self):
        """
        DESCRIPTION: Verify 'BOG' icon on 'Settled bets' tab
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        EXPECTED: * If **Start Price & Taken Price** are the same only starting price should be displayed
        EXPECTED: * If the **Price Taken** is bigger than the **Starting Price** then the bigger Price Taken should not be shown as struck out.
        EXPECTED: * If the **Starting Price** is bigger than the **Price Taken** then we should display both prices, the Price Taken will be struck out and the new bigger Starting Price will be displayed, as per designs.
        EXPECTED: **Designs**
        EXPECTED: Ladbrokes: https://zpl.io/VxvkMgk
        EXPECTED: Coral: https://zpl.io/Vq5nErm
        """
        self.site.go_to_home_page()
        # Setteling the bet
        self.ob_config.update_selection_result(event_id=self.event_id, selection_id=self.selection_id,
                                               market_id=self.market_id,
                                               price=self.increased_Price)
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        self.site.open_my_bets_settled_bets()
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        bet_name, settle_bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertTrue(settle_bet.bog_icon, msg='Bog icon is not displayed in bet history')
        self.assertTrue(settle_bet.odds_value, msg='the Price Taken is not strike out')
        self.assertEquals(settle_bet.odds_bog, self.increased_Price, msg="increased price is not displayed")
