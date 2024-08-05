import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod - cant be executed on prod as OB is involved in event creation and overask triggering
@pytest.mark.hl
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59898512_Selection_is_suspended_after_counter_offer_is_given_and_before_the_Place_Bet_button_is_clicked(BaseBetSlipTest):
    """
    TR_ID: C59898512
    NAME: Selection is suspended after counter offer is given and before the Place Bet button is clicked
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = {0: '1/20'}
    new_price = '1/10'

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp_prices=self.prices,
                                                                                 max_bet=self.max_bet,
                                                                                 max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.first_selection = event_params.team1
        self.__class__.event_name = f'{self.first_selection} v {event_params.team2}'
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_make_a_selection_from_any_sportrace_and_try_and_place_a_bet_with_a_stake_greater_than_its_max_stake_so_that_overask_is_triggered(self):
        """
        DESCRIPTION: Make a selection from any sport/race and try and place a bet with a stake greater than its max stake so that Overask is triggered.
        EXPECTED: You should have tried to place a bet that triggers Overask and the bet should be in the Overask flow.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_make_any_type_of_counter_offer_in_ti(self):
        """
        DESCRIPTION: Make any type of counter offer in TI.
        EXPECTED: You should have given any type of counter offer and the counter offer should be seen on the front end.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask panel is not closed')
        sections = self.get_betslip_sections().Singles
        self.__class__.stake_to_suspend = sections[self.first_selection]
        stake_odd_value = sections.overask_trader_offer.stake_content.odd_value.value
        odd_value = stake_odd_value.strip(' x')
        self.assertEqual(odd_value, self.new_price,
                         msg=f'Actual price :"{odd_value}" is not same as'
                             f'Expected price :"{self.new_price}"')

    def test_003_suspend_the_selection_in_openbetti(self):
        """
        DESCRIPTION: Suspend the selection in Openbet/TI.
        EXPECTED: The selection should be suspended and the counter offer on the front end should reflect this i.e. it should show the selection greyed out in the counter offer and a message should be seen
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True)
        result = self.stake_to_suspend.is_suspended(timeout=60)
        self.assertTrue(result, msg='Selection is not suspended')
        betslip = self.get_betslip_content()
        betnow_section_error = betslip.error
        self.assertEqual(betnow_section_error, vec.betslip.SINGLE_DISABLED,
                         msg=f'Actual error "{betnow_section_error}" != Expected '
                             f'error "{vec.betslip.SINGLE_DISABLED}"')
        self.assertFalse(betslip.confirm_overask_offer_button.is_enabled(timeout=10),
                         msg='Bet Now button is not disabled')

    def test_004_verify_that_the_place_bet_button_is_not_clickable_and_that_you_cannot_place_the_bet(self):
        """
        DESCRIPTION: Verify that the Place Bet button is not clickable and that you cannot place the bet
        EXPECTED: The Place Bet button should not be clickable and you should not be able to place the bet
        """
        #  Covered in step test_003

    def test_005_click_on_the_cancel_button_and_verify_that_the_counter_offer_closes(self):
        """
        DESCRIPTION: Click on the Cancel button and verify that the counter offer closes.
        EXPECTED: The counter offer should close.
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()

    def test_006_check_my_bets_open_bets_to_make_sure_it_doesnt_show_that_the_bet_was_placed(self):
        """
        DESCRIPTION: Check My Bets->Open Bets to make sure it doesn't show that the bet was placed.
        EXPECTED: No bet should be showing in My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()
        open_bets = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())
        self.assertNotIn(self.event_name, open_bets, msg='cancelled bet is present in openbets')
