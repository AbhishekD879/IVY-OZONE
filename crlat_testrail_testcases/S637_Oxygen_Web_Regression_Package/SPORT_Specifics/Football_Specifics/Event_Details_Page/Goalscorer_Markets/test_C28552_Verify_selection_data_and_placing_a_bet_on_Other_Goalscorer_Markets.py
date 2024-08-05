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
class Test_C28552_Verify_selection_data_and_placing_a_bet_on_Other_Goalscorer_Markets(Common):
    """
    TR_ID: C28552
    NAME: Verify selection data and placing a bet on Other Goalscorer Markets
    DESCRIPTION: This test case verifies selection data and placing a bet on Other Goalscorer Markets
    PRECONDITIONS: 1) Football events with goalscorer markets (Last Goalscorer, Hat trick)
    PRECONDITIONS: 2) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Hat trick"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Hat-Trick"
    PRECONDITIONS: **Jira tickets: **BMA-3868
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

    def test_003_go_to_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: Section is expanded and displayed correctly
        """
        pass

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within Market section and contains the following:
        EXPECTED: *   Player name
        EXPECTED: *   2 price/odds buttons of  Goalscorer markets - 'Last Goalscorer', 'Hat trick'
        EXPECTED: *   If price of any of those markets is not available - corresponding price/odds button is not shown
        """
        pass

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for first market in the list for verified player
        """
        pass

    def test_006_verify_priceodds_buttons_correspondence_to_goalscorer_markets(self):
        """
        DESCRIPTION: Verify Price/Odds buttons correspondence to Goalscorer markets
        EXPECTED: *   Price/odds buttons in 'Last' column correspond to 'Last Goalscorer' market data in SS response
        EXPECTED: *   Price/odds buttons in 'Hatrick' column correspond to 'Hat trick' market data in SS response
        EXPECTED: **Note: **Name differences could be present for different events and environments
        """
        pass

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Selection (Price/Odds) is greyed out and disabled if it is suspended
        """
        pass

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Selection (Price/Odds) is greyed out and disabled if it is suspended
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
        EXPECTED: The bet is be present
        """
        pass

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attribute)
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

    def test_014_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap **'PLACE BET**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        pass
