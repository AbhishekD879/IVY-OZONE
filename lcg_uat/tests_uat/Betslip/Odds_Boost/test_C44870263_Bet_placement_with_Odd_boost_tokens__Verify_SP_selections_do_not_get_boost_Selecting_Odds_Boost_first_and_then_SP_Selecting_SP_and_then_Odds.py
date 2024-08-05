import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-56755')  # Issue in Coral only. todo : Need to remove this marker after given bug was closed
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod - can't run on prod as this TC needs to grant odds boost to the user
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870263_Bet_placement_with_Odd_boost_tokens__Verify_SP_selections_do_not_get_boost_Selecting_Odds_Boost_first_and_then_SP_Selecting_SP_and_then_Odds_boost__Verify_Odd_boost_unavailable_popup_for_SP__Place_in_play_boosted_bet_and_verify_bet_receipt_and(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C44870263
    NAME: "Bet placement with Odd boost tokens - Verify SP selections do not get boost (Selecting Odds Boost first and then SP/ Selecting SP and then Odds boost) - Verify Odd boost unavailable popup for SP - Place in-play boosted bet and verify bet receipt and
    DESCRIPTION: "Bet placement with Odd boost tokens
    """
    keep_browser_open = True
    expected_sp_odds = 'SP'
    lp_price = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/5', 4: '3/2'}
    odds_boost_max_token_value = 50

    def test_001_load_application_and_login_into_the_applicationadd_selection_with_sp_only_availablenavigate_to_betslip_and_add_a_stakeverify_that_the_odds_boost_section_is_not_shown_in_the_betslip(self):
        """
        DESCRIPTION: Load application and Login into the application
        DESCRIPTION: Add selection with SP only available
        DESCRIPTION: Navigate to Betslip and add a stake
        DESCRIPTION: Verify that the Odds Boost section is NOT shown in the Betslip
        EXPECTED: BOOST' button is NOT shown
        EXPECTED: SP odds is shown
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        self.__class__.username = tests.settings.odds_boost_user
        self.site.login(username=self.username)

        self.navigate_to_page('oddsboost')
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, '"Odds boost section" are not displayed')
        self.__class__.available_count = [int(i) for i in odds_boost_sections[0].available_now.name.split() if i.isdigit()]

        racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms, sp=True)
        selection_ids = list(racing_event.selection_ids.values())[0]
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=selection_ids)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                         msg='"Odds Boost section and its contents" is shown in the Betslip')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1
        self.assertEqual(stake.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{stake.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')

    def test_002_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that Bet Receipt is shown
        EXPECTED: Bet Receipt is shown with SP odds
        """
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get(vec.betslip.SINGLE)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = list(section_items.values())[0]
        self.assertEqual(bet_info.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{bet_info.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')
        self.site.bet_receipt.footer.done_button.click()

    def test_003_add_selection_with_sp_availablenavigate_to_betslip_and_add_a_stake_to_the_selectionverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Add selection with SP available
        DESCRIPTION: Navigate to Betslip and add a Stake to the selection
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: 'BOOST' button
        EXPECTED: 'Tap to boost your betslip' text
        EXPECTED: 'i' icon
        """
        racing_event_lp = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, sp=True, lp=True,
                                                             lp_prices=self.lp_price)
        selection_id = list(racing_event_lp.selection_ids.values())[0]
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=selection_id)
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.__class__.stake = list(singles_section.values())[0]
        self.stake.amount_form.input.value = 1

        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg='"Boost" button is not shown on the Odds Boost section')
        actual_text = self.odds_boost_header.tap_to_boost_your_betslip_label.text
        self.assertEqual(actual_text, vec.odds_boost.BETSLIP_HEADER.subtitle,
                         msg=f'Actual Text: "{actual_text}" is not same as Expected text: "{vec.odds_boost.BETSLIP_HEADER.subtitle}"')
        self.assertTrue(self.odds_boost_header.info_button.is_displayed(), msg='"i" icon is not displayed')

    def test_004_tap_a_boost_button(self):
        """
        DESCRIPTION: Tap a 'BOOST' button
        EXPECTED: User can able to see boosted bets
        """
        self.odds_boost_header.boost_button.click()
        self.assertTrue(self.stake.has_boosted_odds, msg='"Odds" are not boosted')
        boosted_odds = self.stake.boosted_odds_container.price_value
        self.assertGreater(boosted_odds, self.lp_price[0],
                           msg=f'Boosted odds: "{boosted_odds}" are same as Original odds: "{self.lp_price[0]}')
        self.get_betslip_content().remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()

    def test_005_place_in_play_boosted_bet_and_verify_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place in-play boosted bet and verify bet receipt and my bets
        EXPECTED: Boosted bets will be shown in the my bets and bet receipt
        """
        self.navigate_to_page("Homepage")
        selection_ids = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, lp=True, sp=False, is_live=True,
                                                           lp_prices=self.lp_price).selection_ids
        selection_id = list(selection_ids.values())[0]
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=selection_id)
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1

        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='"Odds Boost section" is not shown in the Betslip')
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg='"Boost" button is not shown on the Odds Boost section')
        if odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled:
            odds_boost_header.boost_button.click()
        self.assertTrue(stake.has_boosted_odds, msg='"Odds" are not boosted')
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.navigate_to_page("Homepage")
        self.site.open_my_bets_open_bets()
        self.site.wait_splash_to_hide(3)
        bets = self.site.open_bets.tab_content.accordions_list
        self.assertTrue(bets.items_as_ordered_dict, msg='No "Bets" found in open bets tab')
        _, bet = bets.get_bet(bet_type='SINGLE', selection_ids=selection_id)
        self.assertGreater(bet.odds_value, self.lp_price[0],
                           msg=f'Boosted odds: "{bet.odds_value}" are same as Original odds: "{self.lp_price[0]}')
        # test_007
        self.navigate_to_page("Homepage")
        self.__class__.expected_betslip_counter_value = 0
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=list(selection_ids.values())[1])
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[1])
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='"Odds Boost section" is not shown in the Betslip')
        odds_boost_header.boost_button.click()

        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.odds_boost_max_token_value + 1
        exeeding_odds_boost_max_token_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP_EXCEEDED, timeout=5, verify_name=False)
        self.assertTrue(exeeding_odds_boost_max_token_dialog,
                        msg='User able to place boost bet more than boost token max value as popup not appeared')
        exeeding_odds_boost_max_token_dialog.ok_button.click()

        self.get_betslip_content().remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()

    def test_006_openbet_has_disabled_odd_boost_for_the_event__verify_user_cant_place_boosted_bets_on_the_event(self):
        """
        DESCRIPTION: Openbet has disabled odd boost for the event. , verify user can't place boosted bets on the event
        EXPECTED: user can't place boosted bets on the event
        """
        racing_event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, sp=False, lp=True,
                                                          lp_prices=self.lp_price, enhanced_odds=False)
        selection_ids = list(racing_event.selection_ids.values())[0]
        self.__class__.expected_betslip_counter_value = 0
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=selection_ids)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                         msg='"Odds Boost section and its contents" is shown in the Betslip')

    def test_007_verify_user_cant_place_boost_bet_more_than_boost_token_max_value(self):
        """
        DESCRIPTION: Verify user can't place boost bet more than boost token max value
        EXPECTED: User can't place boost bet more than boost token max value
        """
        # covered in step 5 to decrease the execution time by avoiding creation of event

    def test_008_verify_remaning_active_boost_token_count(self):
        """
        DESCRIPTION: Verify remaning active boost token count
        EXPECTED: User should be displayed with the remaining number of odds boost
        """
        self.navigate_to_page('oddsboost')
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, '"Odds boost section" are not displayed')
        updated_available_count = [int(i) for i in odds_boost_sections[0].available_now.name.split() if i.isdigit()]
        self.assertNotEqual(updated_available_count[0], self.available_count[0],
                            msg=f'Updated Available count: "{updated_available_count[0]}" is not less than Actual Available count: "{self.available_count[0]}"')
