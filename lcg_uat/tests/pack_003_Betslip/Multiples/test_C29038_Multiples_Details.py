import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.medium
@vtest
class Test_C29038_Multiples_Details(BaseBetSlipTest):
    """
    TR_ID: C29038
    NAME: Multiples Details
    DESCRIPTION: This test case verifies information displayed on Multiples page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test data
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()

            self.__class__.selection_id_1 = event.selection_ids[event.team1]
            self.__class__.selection_id_2 = event_2.selection_ids[event_2.team1]
        else:
            events = self.get_active_events_for_category(number_of_events=2)
            selections = []
            for event in events:
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Match Betting' and market['market'].get('children'):
                        selections.append(market['market']['children'][0]['outcome']['id'])
                        break
            self.__class__.selection_id_1 = selections[0]
            self.__class__.selection_id_2 = selections[1]

    def test_001_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_002_go_to_multiples_section(self):
        """
        DESCRIPTION: Open Betslip and scroll to 'Multiples' section
        EXPECTED: Multiples are available for added selections.
        EXPECTED: Section title is "Multiples (#)" where # is number of available Multiple Types
        """
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertEqual(self.multiples_section.name, vec.betslip.MULTIPLES,
                         msg='Incorrect multiples section name\nActual: "%s"\nExpected: "%s"'
                             % (self.multiples_section.name, vec.betslip.MULTIPLES))

    def test_003_verify_number_of_multiples(self):
        """
        DESCRIPTION: Verify number of Multiples
        EXPECTED: The number of available Multiples is displayed near section title in brackets and corresponds to the number of Multiples displayed on the page below
        """
        expected_count = f'({len(self.multiples_section.keys())})'
        self.assertEqual(self.get_betslip_content().betslip_sections_list.multiple_selections_count, expected_count,
                         msg=f'Selection number "{self.get_betslip_content().betslip_sections_list.multiple_selections_count}" '
                             f'is not the same as expected "{expected_count}"')

    def test_004_verify_information_icon(self):
        """
        DESCRIPTION: Verify 'Information' icon
        EXPECTED: 'Information' icon should be available for each of the Multiple bet type that is formed in the Multiples section of the Betslip
        EXPECTED: When the Icon is clicked a popup with informative text, which describes this type of the bet, should appear
        """
        self.__class__.stake_name, self.__class__.stake = list(self.multiples_section.items())[0]
        self.assertTrue(self.stake.information_button, msg='"Information" icon is not displayed near the selection name')

        self.stake.information_button.click()
        selection_info_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_DOUBLE_SELECTION_INFORMATION)
        self.assertTrue(selection_info_dialog, msg='"Selection Information" pop-up should be displayed at this point')

        selection_info_dialog.click_ok()
        self.assertTrue(selection_info_dialog.wait_dialog_closed(),
                        msg='Failed to close "Selection Information" pop-up')

    def test_005_verify_multiple_bet_type_name(self):
        """
        DESCRIPTION: Verify Multiple Bet Type name
        EXPECTED: Multiple Bet Type name should be displayed next to the 'Information' icon
        """
        self.assertEqual(self.stake_name, vec.betslip.DBL, msg='Incorrect multiple bet type name')

    def test_006_verify_number_of_bets_for_multiple_type(self):
        """
        DESCRIPTION: Verify Number of Bets for Multiple Type
        EXPECTED: Number of Bets should be displayed next to the Multiple bet type name and should display the number of bets involved in a Multiple. Value it taken from server
        """
        self.assertEqual(self.stake.bets_multiplier, '(x1)', msg='Incorrect number of bets')

    def test_007_verify_stake_field(self):
        """
        DESCRIPTION: Verify 'Stake' field
        EXPECTED: 'Stake' field to enter the amount, titled 'Stake', should be present right below each Multiple bet type
        EXPECTED: Default value is £0.00 (currency symbol corresponds to user's currency)
        """
        self.assertEqual(self.stake.amount_form.label, 'Stake', msg='Incorrect title of "Stake" field')
        self.assertEqual(self.stake.amount_form.default_value, 'Stake',
                         msg='The multiple stake amount is: "%s" but should be "Stake")'
                             % self.stake.amount_form.default_value)

    def test_008_verify_est_returns(self):
        """
        DESCRIPTION: Verify 'Est. Returns'
        EXPECTED: 'Est. Returns' field is available for each Multiple Type
        EXPECTED: Default value is £0.00  (currency symbol corresponds to user's currency) or N/A (in case selection with SP price was added)
        """
        self.assertTrue(self.stake.est_returns_label, msg='"Est. Returns" field is not displayed')
        self.assertTrue(self.stake.est_returns, msg='"Est. Returns" field is not displayed')

        label = vec.betslip.POTENTIAL_RESULTS if self.brand != 'bma' else vec.betslip.ESTIMATED_RESULTS
        self.assertEqual(self.stake.est_returns_label.text, label,
                         msg=f'Incorrect label of "{label}" field\n'
                             f'Actual: {self.stake.est_returns_label.text}\nExpected: "{label}"')
        self.assertEqual(self.stake.est_returns, '0.00',
                         msg=f'{label} amount is: "{self.stake.est_returns}" '
                             f'but should be "Stake")')

    def test_009_enter_stake_for_multiple(self):
        """
        DESCRIPTION: Enter 'Stake' for Multiple
        EXPECTED: 'Est. Returns' field is calculated for this Multiple bet
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        odds = self.stake.odds
        self.verify_estimated_returns(est_returns=float(self.get_betslip_content().total_estimate_returns),
                                      odds=odds, bet_amount=self.bet_amount)
