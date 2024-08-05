import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29110_Each_Way_Calculations_for_Singles_Selections_with_Free_Bet(Common):
    """
    TR_ID: C29110
    NAME: Each Way Calculations for Singles Selections with Free Bet
    DESCRIPTION: This test case verifies each way calculations for singles selections when free bet is selected
    DESCRIPTION: Formula mentioned in TC is same to provided in comment by PO  in ticket https://jira.egalacoral.com/browse/BMA-5351
    PRECONDITIONS: Make sure <RACE> events have each way option available (terms are shown for market)
    PRECONDITIONS: Example of SS response:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForEvent/xxxxxx?simpleFilter=event.suspendAtTime:greaterThan:xxxx-xx-xxTxx:xx:xx.000Z&priceHistory=true&externalKeys=event&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_to_applicaiton(self):
        """
        DESCRIPTION: Log in to applicaiton
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_several_lp_selections_from_different_ltracegt_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several 'LP' selections from different &lt;Race&gt; events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_go_to_bet_slip_singles_section(self):
        """
        DESCRIPTION: Go to 'Bet Slip', 'Singles' section
        EXPECTED: 'Singles' section is shown
        """
        pass

    def test_005_select_free_bet_from_the_drop_down_menuleave_the_stake_field_empty(self):
        """
        DESCRIPTION: Select free bet from the drop down menu
        DESCRIPTION: Leave the stake field empty
        EXPECTED: Free bet is selected
        """
        pass

    def test_006_select_each_way_option_and_verify_estimated_returns_value(self):
        """
        DESCRIPTION: Select each way option and verify 'Estimated Returns' value
        EXPECTED: Est.Returns = Return1 + Return2
        EXPECTED: When Odds have a Fractional Format :
        EXPECTED: Return1 = ((1/2 * freebet) * Odds) + (1/2 * freebet) - freebet
        EXPECTED: Return2 = ((1/2 * freebet) * Odds * (eachnum/eachden)) +  (1/2 * freebet)
        EXPECTED: where eachnum/eachden = eachWayFactorNum/eachWayFactorDen taken from SS response of the event or in TI
        EXPECTED: When Odds have a Decimal Format :
        EXPECTED: Return1 = ((1/2 * freebet) * (Odds-1)) + (1/2 * freebet) - freebet
        EXPECTED: Return2 = ((1/2 * freebet) * (Odds-1) * (eachnum/eachden)) +  (1/2 * freebet)
        """
        pass

    def test_007_select_free_bet_from_the_dropdownenter_some_stake_amount_in_a_stake_field(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        DESCRIPTION: Enter some stake amount in a stake field
        EXPECTED: Free bet is selected
        EXPECTED: 'Stake' field is pre-populated by value entered
        """
        pass

    def test_008_select_each_way_option_for_selection_and_verify_estimated_returns_filed(self):
        """
        DESCRIPTION: Select each way option for selection and verify 'Estimated Returns' filed
        EXPECTED: Est.Returns = Return1 + Return2
        EXPECTED: When Odds have a Fractional Format :
        EXPECTED: Return1 = (stake + (1/2 * freebet)) * Odds + (stake + (1/2 * freebet)) - freebet
        EXPECTED: Return2 = ((stake + (1/2 * freebet)) * Odds * (eachnum/eachden)) + (stake + (1/2 * freebet))
        EXPECTED: When Odds have a Decimal Format :
        EXPECTED: Return1 = (stake + (1/2 * freebet)) * (Odds-1) + (stake + (1/2 * freebet)) - freebet
        EXPECTED: Return2 = ((stake + (1/2 * freebet)) * (Odds-1) * (eachnum/eachden)) + (stake + (1/2 * freebet))
        """
        pass

    def test_009_repeat_steps__3___8_for_sp_selections(self):
        """
        DESCRIPTION: Repeat steps # 3 - 8 for 'SP' selections
        EXPECTED: 'Estimated Returns' will always be equal to 'N/A' value
        """
        pass
