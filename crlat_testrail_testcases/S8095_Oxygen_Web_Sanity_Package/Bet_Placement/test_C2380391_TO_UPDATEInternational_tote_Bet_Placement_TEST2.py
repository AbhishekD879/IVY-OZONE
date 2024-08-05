import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2380391_TO_UPDATEInternational_tote_Bet_Placement_TEST2(Common):
    """
    TR_ID: C2380391
    NAME: (TO UPDATE)International tote Bet Placement [TEST2]
    DESCRIPTION: This test case verifies bet placement on International tote pools
    DESCRIPTION: *To be Updated*
    DESCRIPTION: Note:  Int Totes bet placement should be identical to UK tote bet placement!!!!!!
    DESCRIPTION: AUTOTESTS [C9776556] [C9836860] [C9864904] [C9858669]
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Int.Tote Tote feature is enabled in CMS
    PRECONDITIONS: * Win/Place/Show/Exacta/Trifecta pool types are available for Int.Tote Events Event
    PRECONDITIONS: * User should have a Int.Tote EDP open
    """
    keep_browser_open = True

    def test_001_navigate_to_the_win_pool_type(self):
        """
        DESCRIPTION: Navigate to the Win pool type
        EXPECTED: 'Win' Pool type is selected and highlighted
        """
        pass

    def test_002_set_at_least_one_stake_which_meets_correct_increment_and_the_minimum_bet_into_stake_box(self):
        """
        DESCRIPTION: Set at least one stake, which meets correct increment and the minimum bet, into stake box
        EXPECTED: * Stake is displayed with local currency  and is not highlighted in red
        EXPECTED: * 'Total Stake' field  conains combined value calculated from entered stake values
        EXPECTED: * 'Bet now' button becomes enabled
        """
        pass

    def test_003_click_on_bet_now_button(self):
        """
        DESCRIPTION: Click on 'Bet Now' button
        EXPECTED: * User's balance decreased on relevant amount of stake
        EXPECTED: * Bet Receipt appears at the bottom of the event detail page and contains:
        EXPECTED: * 'Bet Receipt' header, Success message " Your bet has been placed",
        EXPECTED: * Bet is shown in collapsed format: "+" collaping button,
        EXPECTED: * label "Tote <type Win/Place/Show>" ,** label "Stake <CC Pool currency and XX - stake amount> ",
        EXPECTED: * label "Total Stake <CC Pool currency and XX - total stake amount>",
        EXPECTED: * label "All bets are accepted with the <"Coral Betting Rules" link> as published in this site.",
        EXPECTED: * 'Continue' button enabled by default
        """
        pass

    def test_004_check_correctness_of_collapsed_bet_info_tote_type_win_stake_cc_pool_currency_and_xx___stake_amount__total_stake_cc_pool_currency_and_xx___total_stake_amount(self):
        """
        DESCRIPTION: Check correctness of collapsed Bet info:
        DESCRIPTION: * "Tote <type Win>"
        DESCRIPTION: * "Stake <CC Pool currency and XX - stake amount> "
        DESCRIPTION: * "Total Stake <CC Pool currency and XX - total stake amount>"
        EXPECTED: - In console from call https://bp-dev-coral.symphony-solutions.eu/Proxy/placeWinPoolBet
        EXPECTED: check parameters:
        EXPECTED: * betTypeRef:{id: "WN"/"PL"/"SH"}
        EXPECTED: * stake:{amount: "XX", currencyRef: {id: "GBP"/"USD"/"EUR"/"SEK"/"HKD"/"AUD"/"SGD"}}
        EXPECTED: * stake:{amount: "XX", currencyRef: {id: "GBP"/"USD"/"EUR"/"SEK"/"HKD"/"AUD"/"SGD"}}
        """
        pass

    def test_005_click_plus_collapsing_button(self):
        """
        DESCRIPTION: Click "+" collapsing button
        EXPECTED: - Button "+" is changed to "-"
        EXPECTED: - Additional information appears about Bet: <Selection name>,"Leg:" <Leg Event details>,  "Bet ID:" <Bet Reference ID>
        """
        pass

    def test_006_repeat_steps_2_5_for_place_pol_type_show_pool_type(self):
        """
        DESCRIPTION: Repeat steps 2-5 for:
        DESCRIPTION: * Place pol type
        DESCRIPTION: * Show pool type
        EXPECTED: 
        """
        pass

    def test_007_select_exacta_pool_type(self):
        """
        DESCRIPTION: Select "Exacta" pool type
        EXPECTED: * Exacta tab is selected
        EXPECTED: * Exacta racecard is opened
        """
        pass

    def test_008_select_1st_and_2nd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st" and "2nd" check boxes for any runners
        EXPECTED: * 'Bet Now' button becomes enabled
        """
        pass

    def test_009_enter_correct_increment_into_the_stake_field_that_meet_the_minimum_bet_requirements_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter correct increment into the 'Stake' field that meet the minimum bet requirements and tap 'Bet Now' button
        EXPECTED: * User's balance decreased on relevant amount of stake
        EXPECTED: * Bet Receipt appears at the bottom of the event detail page and contains:
        EXPECTED: * 'Bet Receipt' header, Success message " Your bet has been placed",
        EXPECTED: * Bet is shown in collapsed format: "+" collaping button,
        EXPECTED: * label "Tote <type Exacta>" ,** label "Stake <CC Pool currency and XX - stake amount> ",
        EXPECTED: * label "Total Stake <CC Pool currency and XX - total stake amount>",
        EXPECTED: * label "All bets are accepted with the <"Coral Betting Rules" link> as published in this site.",
        EXPECTED: * 'Continue' button enabled by default
        """
        pass

    def test_010_check_correctness_of_collapsed_bet_info_tote_type_exacta_stake_cc_pool_currency_and_xx___stake_amount__total_stake_cc_pool_currency_and_xx___total_stake_amount(self):
        """
        DESCRIPTION: Check correctness of collapsed Bet info:
        DESCRIPTION: * "Tote <type Exacta>"
        DESCRIPTION: * "Stake <CC Pool currency and XX - stake amount> "
        DESCRIPTION: * "Total Stake <CC Pool currency and XX - total stake amount>"
        EXPECTED: - In console from call https://bp-dev-coral.symphony-solutions.eu/Proxy/placeWinPoolBet
        EXPECTED: check parameters:
        EXPECTED: * betTypeRef:{id: "WN"/"PL"/"SH"}
        EXPECTED: * stake:{amount: "XX", currencyRef: {id: "GBP"/"USD"/"EUR"/"SEK"/"HKD"/"AUD"/"SGD"}}
        EXPECTED: * stake:{amount: "XX", currencyRef: {id: "GBP"/"USD"/"EUR"/"SEK"/"HKD"/"AUD"/"SGD"}}
        """
        pass

    def test_011_click_plus_collapsing_button(self):
        """
        DESCRIPTION: Click "+" collapsing button
        EXPECTED: - Button "+" is changed to "-"
        EXPECTED: - Additional information appears about Bet: <Selection name>,"Leg:" <Leg Event details>,  "Bet ID:" <Bet Reference ID>
        """
        pass

    def test_012_select_trifecta_pool_type(self):
        """
        DESCRIPTION: Select "Trifecta" pool type
        EXPECTED: * Trifecta tab is selected
        EXPECTED: * Trifecta racecard is opened
        """
        pass

    def test_013_select_1st_2nd_and_3rd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st", "2nd" and "3rd" check boxes for any runners
        EXPECTED: * 'Bet Now' button becomes enabled
        """
        pass

    def test_014_enter_correct_increment_into_the_stake_field_that_meet_the_minimum_bet_requirements_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter correct increment into the 'Stake' field that meet the minimum bet requirements and tap 'Bet Now' button
        EXPECTED: * User's balance decreased on relevant amount of stake
        EXPECTED: * Bet Receipt appears at the bottom of the event detail page and contains:
        EXPECTED: * 'Bet Receipt' header, Success message " Your bet has been placed",
        EXPECTED: * Bet is shown in collapsed format: "+" collaping button,
        EXPECTED: * label "Tote <type Trifecta>" ,** label "Stake <CC Pool currency and XX - stake amount> ",
        EXPECTED: * label "Total Stake <CC Pool currency and XX - total stake amount>",
        EXPECTED: * label "All bets are accepted with the <"Coral Betting Rules" link> as published in this site.",
        EXPECTED: * 'Continue' button enabled by default
        """
        pass

    def test_015_check_correctness_of_collapsed_bet_info_tote_type_trifecta_stake_cc_pool_currency_and_xx___stake_amount__total_stake_cc_pool_currency_and_xx___total_stake_amount(self):
        """
        DESCRIPTION: Check correctness of collapsed Bet info:
        DESCRIPTION: * "Tote <type Trifecta>"
        DESCRIPTION: * "Stake <CC Pool currency and XX - stake amount> "
        DESCRIPTION: * "Total Stake <CC Pool currency and XX - total stake amount>"
        EXPECTED: 
        """
        pass
