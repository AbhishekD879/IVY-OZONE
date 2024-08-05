import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.footer
@pytest.mark.banach
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.high
@pytest.mark.mobile_only
@vtest
class Test_C22930126_Verify_My_Bets_counter_after_Build_Your_Bet_BetPlacement(BaseUserAccountTest, BaseBanachTest):
    """
    TR_ID: C22930126
    VOL_ID: C58833983
    NAME: Verify My Bets counter after Build Your Bet  BetPlacement
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after BYB Bet Placement
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True
    bet_amount = 1
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get banach event
        """
        self.check_my_bets_counter_enabled_in_cms()
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login()
        self.site.wait_content_state("Homepage")

        # for coral my bets is not present in footer
        if self.brand == 'ladbrokes':
            self.__class__.my_bets_initial_counter = int(self.get_my_bets_counter_value_from_footer())
        else:
            self.site.open_my_bets_open_bets()
            self.site.wait_splash_to_hide(5)
            self.__class__.my_bets_initial_counter = len(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict)

    def test_001_navigate_to_byb_tab_and_place_bet_for_any_byb_market(self):
        """
        DESCRIPTION: Navigate to BYB tab and place bet for any BYB market
        EXPECTED: Bet is placed successfully
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        match_betting.add_to_betslip_button.click()
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)

        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        summary_block.place_bet.scroll_to()
        summary_block.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip not appears')
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)
        self.site.byb_betslip_panel.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                        msg='Build Your Bet Receipt is not displayed')

    def test_002__close_byb_betslip_verify_my_bets_counter_on_the_footer_panel(self):
        """
        DESCRIPTION: * Close BYB Betslip
        DESCRIPTION: * Verify 'My Bets' counter on the Footer panel
        EXPECTED: My bets counter icon is increased by one
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')
        if self.brand == 'ladbrokes':
            counter_value = int(self.get_my_bets_counter_value_from_footer())
        else:
            self.site.open_my_bets_open_bets()
            self.site.wait_splash_to_hide(3)
            counter_value = len(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict)
        self.assertEqual(counter_value, self.my_bets_initial_counter + 1,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{self.my_bets_initial_counter + 1}"')
