import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870359_Verify_user_sees_Acca_Insurance_signposting_on_five_fold_Acca_bet(Common):
    """
    TR_ID: C44870359
    NAME: Verify user sees Acca Insurance signposting on five fold Acca bet
    DESCRIPTION: "Verify user sees Acca Insurance signposting only when placed five fold Acca bet. Verify user sees signposting on Open Bets and Settled Bets"
    PRECONDITIONS: Acca insurance should be created on Open Bet for a user.
    PRECONDITIONS: To qualify for Acca Insurance, place a cash bet on football, in any of the following markets:
    PRECONDITIONS: Match Betting
    PRECONDITIONS: Both Teams To Score
    PRECONDITIONS: Match Result & Both Teams to Score
    PRECONDITIONS: Correct Score
    PRECONDITIONS: Total Goals Over/Under markets
    PRECONDITIONS: Condition:1. cumulative odds of 3/1, and 2. individual odds of 1/10 or greater, with five selections or more it can qualify.
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_add_four_selection_from_football_match_betting_market_to_betslip_and_verify_upsell_message(self):
        """
        DESCRIPTION: Add four selection from Football, Match betting market to betslip and verify upsell message
        EXPECTED: 'Add one more selection to qualify Acca Insurance' Message is displayed in betslip
        """
        pass

    def test_003_add_one_more_selection_and_verify_acca_insurance_icon_on_five_fold_accumulator(self):
        """
        DESCRIPTION: Add one more selection and verify Acca Insurance icon on Five fold accumulator
        EXPECTED: '5+ Acca' icon is displayed in betslip
        """
        pass

    def test_004_verify_acca_insurance_icon_in_bet_receipt(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in Bet receipt
        EXPECTED: '5+ Acca' icon is displayed in bet receipt
        """
        pass

    def test_005_verify_acca_insurance_icon_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in My bets open bets
        EXPECTED: '5+ Acca' icon is displayed in My bets Open bets
        """
        pass

    def test_006_verify_acca_insurance_icon_in_my_bets_settle_bets(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in My bets Settle bets
        EXPECTED: '5+ Acca' icon is displayed in My bets > settle bets
        """
        pass

    def test_007_repeat_step_2_to_6_for_different_or_combination_of_below_football_marketsboth_teams_to_scorematch_result__both_teams_to_scorecorrect_scoretotal_goals_overunder_markets(self):
        """
        DESCRIPTION: Repeat step #2 to #6 for different or combination of below football markets
        DESCRIPTION: Both Teams To Score
        DESCRIPTION: Match Result & Both Teams to Score
        DESCRIPTION: Correct Score
        DESCRIPTION: Total Goals Over/Under markets
        EXPECTED: 
        """
        pass
