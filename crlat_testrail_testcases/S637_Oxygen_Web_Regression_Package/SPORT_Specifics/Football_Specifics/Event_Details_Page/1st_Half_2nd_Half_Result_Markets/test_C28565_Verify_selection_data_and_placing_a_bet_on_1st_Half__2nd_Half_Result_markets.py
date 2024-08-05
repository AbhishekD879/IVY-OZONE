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
class Test_C28565_Verify_selection_data_and_placing_a_bet_on_1st_Half__2nd_Half_Result_markets(Common):
    """
    TR_ID: C28565
    NAME: Verify selection data and placing a bet on 1st Half / 2nd Half Result markets
    DESCRIPTION: This test case verifies selection data and bet placement on 1st Half / 2nd Half Result markets
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result  markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    PRECONDITIONS: **Jira ticket: **BMA-4074
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

    def test_003_go_to_1st_half__2nd_half_result_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' section
        EXPECTED: Section is expandable/collapsible and displayed correctly
        """
        pass

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within '1st Half / 2nd Half Result' section and contains the following:
        EXPECTED: *   Selection &lt;Team name&gt;/&lt;Draw&gt;
        EXPECTED: *   Price/odds button
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
        EXPECTED: *   Price/odds buttons in '**1st Half Result**' tab correspond to 'First-Half Result' market data in SS response
        EXPECTED: *   Price/odds buttons in '**2nd Half Result**' tab correspond to 'Second-Half Result' market data in SS response
        EXPECTED: **Note: **Name differences could be present for different events and environments
        """
        pass

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        pass

    def test_008_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        pass

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        pass

    def test_010_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is present
        """
        pass

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        pass

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        pass

    def test_014_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        pass
