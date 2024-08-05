import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.each_way
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C10687835_Verify_Each_Way_Option_on_the_Betslip_after_price_is_changed(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10687835
    NAME: Verify Each Way Option on the Betslip after price is changed
    """
    keep_browser_open = True
    prices = {0: '9/1'}
    new_price_increased = '10/1'
    blocked_hosts = ['*liveserve-*']

    def add_selection_id_and_name(self, event):
        self.__class__.selection_ids.append(list(event.selection_ids.values())[0])
        self.__class__.selection_names.append(list(event.selection_ids.keys())[0])

    def test_000_preconditions(self):
        """
        DESCRIPTION: To disable live updates, please enter and save next string into Host file (File: /etc/hosts). Reload the app.
        DESCRIPTION: PROD - 127.0.0.1 liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com
        DESCRIPTION: TST2 - 127.0.0.1 liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com
        DESCRIPTION: TI TST2 system - http://backoffice-tst2.coral.co.uk/ti
        DESCRIPTION: Create racing test event
        EXPECTED: Event is created
        """
        self.__class__.selection_ids = []
        self.__class__.selection_names = []

        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices)
        self.add_selection_id_and_name(event)

        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.add_selection_id_and_name(event)

        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.add_selection_id_and_name(event)

        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
        self.add_selection_id_and_name(event)

        self.site.login(username=tests.settings.betplacement_user)

    def test_001_add_multiple_selections_from_different_horse_racing_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selections (from different Horse Racing events) to the bet slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_navigate_to_the_bet_slip(self):
        """
        DESCRIPTION: Navigate to the bet slip
        EXPECTED: All selections from the previous step are present in the list
        EXPECTED: Accumulator bet is available
        """
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.__class__.multiples_section = sections.Multiples

        ui_selections = self.singles_section.keys()
        for selection_name in self.selection_names:
            self.assertIn(selection_name, ui_selections,
                          msg=f'Selection "{selection_name}" is not present among selections "{ui_selections}"')
        acca_bet_name = '4 Fold Acca'
        self.__class__.acca_bet = self.multiples_section.ordered_collection.get(acca_bet_name)
        self.assertTrue(self.acca_bet, msg=f'Accumulator bet is not available')

    def test_003_change_price_for_any_event_from_the_accumulator_please_note_that_stake_should_increase_eg_from_115_to_111(
            self):
        """
        DESCRIPTION: Change Price for any event from the accumulator (please note that stake should increase e.g. from 11/5 to 11/1)
        EXPECTED: Live updates should not work. User can't see price updates on the UI
        """
        self.ob_config.change_price(selection_id=self.selection_ids[0], price=self.new_price_increased)
        stake_name, stake = list(self.singles_section.items())[0]
        self.assertEqual(stake.odds, '9/1',
                         msg=f'User is able to see price updates on UI"{stake_name}" expected "{self.prices}"')

    def test_004_check_each_way_checkbox_enter_stake_into_accumulators_field(self):
        """
        DESCRIPTION: Check 'each way' checkbox enter stake into Accumulators field
        EXPECTED: Each Way check box should be checked into Accumulators field
        """
        each_way = self.acca_bet.has_each_way_checkbox()
        self.assertTrue(each_way, msg=f'Each Way checkbox is not present on stake "{self.acca_bet.name}"')

        self.acca_bet.each_way_checkbox.click()
        self.assertTrue(self.acca_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.acca_bet.amount_form.input.value = self.bet_amount

    def test_005_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on Bet now button
        EXPECTED: Accept and place bet button should be displayed
        """
        self.__class__.bet_now_button = self.get_betslip_content().bet_now_button
        self.bet_now_button.click()
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.selection_names[0])
        self.assertTrue(stake, msg=f'Stake "{self.selection_names[0]}" was not found')
        result = stake.wait_for_error_message()
        self.assertTrue(result, msg='Price change message was not shown')
        self.assertEqual(self.get_betslip_content().bet_now_button.name, vec.betslip.ACCEPT_BET,
                         msg=f'Actual button name, "{self.get_betslip_content().bet_now_button.name}" '
                             f'is not same as Expected: "{vec.betslip.ACCEPT_BET}"')

    def test_006_tap_on_accept_and_place_bet_button(self):
        """
        DESCRIPTION: Tap on Accept and place bet button
        EXPECTED: Bet should be placed successfully
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
