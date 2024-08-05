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
class Test_C28539_Verify_selection_data_and_placing_a_bet_on_Handicap_market(Common):
    """
    TR_ID: C28539
    NAME: Verify selection data and placing a bet on Handicap market
    DESCRIPTION: This test case verifies selection data and bet placement on Handicap market
    PRECONDITIONS: Football events with Handicap markets (name="Handicap Match Result", name="Handicap First Half", name="Handicap Second Half")
    PRECONDITIONS: To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN)
    PRECONDITIONS: Jira ticket: BMA-3900
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

    def test_003_go_to_handicap_results_market_section(self):
        """
        DESCRIPTION: Go to Handicap Results market section
        EXPECTED: Market section is expandable/collapsible and consists of '90 mins / 1st Half / 2nd Half' sections
        """
        pass

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within '90 mins / 1st Half / 2nd Half' sections and contains the following:
        EXPECTED: *   outcomes names correspond to the SS attribute 'name's for appropriate 'outcome ID'
        EXPECTED: *   Price/odds buttons
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown
        """
        pass

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified market
        """
        pass

    def test_006_verify_priceodds_button_correspondence_to_verified_market(self):
        """
        DESCRIPTION: Verify Price/Odds button correspondence to verified market
        EXPECTED: *   Price/odds buttons in '**90 mins**' filter correspond to 'Handicap Match Result' market data in SS response
        EXPECTED: *   Price/odds buttons in '**1st Half**' filter correspond to 'Handicap First Half' market data in SS response
        EXPECTED: *   Price/odds buttons in '**2nd Half**' filter correspond to 'Handicap Second Half' market data in SS response
        """
        pass

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with prices if outcome is suspended
        """
        pass

    def test_008_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with prices if outcome is suspended
        """
        pass

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        pass

    def test_010_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Add single selection to Betslip
        EXPECTED: Bet indicator displays 1
        """
        pass

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to 'Betslip'
        EXPECTED: The bet is present
        """
        pass

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fractional format or **'price Dec'** in decimal format)
        """
        pass

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Est. Returns**(Coral)/ **Pot. Returns** (Ladbrokes)
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Estimated Returns**(Coral)/ **Potential Returns** (Ladbrokes)
        """
        pass

    def test_014_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        pass
