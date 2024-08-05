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
class Test_C28528_Verify_selection_data_and_placing_a_bet_on_First_Second_Half_Correct_Score_market(Common):
    """
    TR_ID: C28528
    NAME: Verify selection data and placing a bet on  First/Second Half Correct Score market
    DESCRIPTION: This test case verifies selection data and bet placement on  First/Second Half Correct Score market
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Half Correct Score"
    PRECONDITIONS: *   PROD: name="1st Half Correct Score"
    PRECONDITIONS: **Jira ticket: **BMA-3861
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_first_halfcorrect_score_market_section(self):
        """
        DESCRIPTION: Go to 'First Half Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page (e.g. 'All Markets' tab)
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: All selections are displayed on 'Show All' section:
        EXPECTED: *   outcomes names correspond to the SS attribute 'name's for appropriate 'outcome ID'
        EXPECTED: *   Price/odds buttons
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown as N/A
        EXPECTED: * Any other selection without scores and with Price/Odds should be available.
        """
        pass

    def test_005_verify_data_of_priceodds_button_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen**
        """
        pass

    def test_006_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec**
        """
        pass

    def test_007_tap_on_default_add_to_betslip_ltpriceoddsgt_button(self):
        """
        DESCRIPTION: Tap on default 'Add to Betslip &lt;price/odds&gt;' button
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted on 'Show All' section automatically
        EXPECTED: *   If price is not available - Add to Betslip button become N/A
        """
        pass

    def test_008_tap_on_add_to_betslip_ltpriceoddsgt_button_again(self):
        """
        DESCRIPTION: Tap on 'Add to Betslip &lt;price/odds&gt;' button again
        EXPECTED: *   Bet indicator disappeared
        EXPECTED: *   Outcome on 'Show All' section is unhighlighted respectively
        """
        pass

    def test_009_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted on 'Show All' section automatically
        """
        pass

    def test_010_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to 'Bet Slip'
        EXPECTED: The bet is present
        """
        pass

    def test_011_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fractional format or **'price Dec'** in decimal format)
        """
        pass

    def test_012_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Est. Returns**(Coral)/ **Pot. Returns** (Ladbrokes)
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Estimated Returns**(Coral)/ **Potential Returns** (Ladbrokes)
        """
        pass

    def test_013_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        pass

    def test_014_repeat_steps_3_14_for_second_half_correct_score_market_section(self):
        """
        DESCRIPTION: Repeat steps 3-14 for 'Second Half Correct Score' market section
        EXPECTED: 
        """
        pass
