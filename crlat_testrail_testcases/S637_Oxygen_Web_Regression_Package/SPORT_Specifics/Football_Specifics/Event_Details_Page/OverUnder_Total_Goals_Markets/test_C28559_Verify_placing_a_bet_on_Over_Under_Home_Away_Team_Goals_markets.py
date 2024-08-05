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
class Test_C28559_Verify_placing_a_bet_on_Over_Under_Home_Away_Team_Goals_markets(Common):
    """
    TR_ID: C28559
    NAME: Verify placing a bet on Over/Under <Home/Away Team> Goals markets
    DESCRIPTION: This test case verifies placing a bet on 'Over/Under <Home/Away Team> Goals' market sections
    PRECONDITIONS: Football events with 'Over/Under <Home/Away Team> Goals' markets (Over/Under <Home/Away Team> Goals <figure afterward>, Over/Under First Half <Home/Away Team> Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Goals <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   **<figure afterward> **- variable part of market name shown in format 'X.5' as an amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: *   **<Home Team>** - name of the team that is shown first in the Event Name
    PRECONDITIONS: *   **<Away Team>** - name of the team that is shown second in the Event Name
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
    PRECONDITIONS: **Jira ticket: **BMA-3902
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

    def test_003_go_to_overunder_home_team_goals__section(self):
        """
        DESCRIPTION: Go to 'Over/Under **<Home Team> **Goals**** ****' section
        EXPECTED: Section is expanded and displayed correctly
        """
        pass

    def test_004_verify_market_section(self):
        """
        DESCRIPTION: Verify market section
        EXPECTED: Market section is displayed within 'Over/Under <Team Name> Goals' section and contains the following:
        EXPECTED: *   Market name
        EXPECTED: *   Price/odds buttons of  available options: 'Over', 'Under'
        EXPECTED: *   If price of any of those markets is not available - corresponding price/odds button is not shown
        """
        pass

    def test_005_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Selection name corresponds to <figure afterward> part of '**name**' attribute on the market level (e.g. **0.5 **of market with name="Over/Under <Home Team> Goals 0.5")
        """
        pass

    def test_006_verify_priceodds_buttons_correspondence_to_verified_markets(self):
        """
        DESCRIPTION: Verify Price/Odds buttons correspondence to verified markets
        EXPECTED: *   Price/odds buttons in 'Over' column correspond to 'Over' outcome data in SS response
        EXPECTED: *   Price/odds buttons in 'Under' column correspond to 'Under' outcome data in SS response
        """
        pass

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        pass

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
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

    def test_015_repeat_steps__4_14_for_overunderaway_teamgoals_market_section(self):
        """
        DESCRIPTION: Repeat steps № 4-14 for 'Over/Under **<Away Team> **Goals' market section
        EXPECTED: 
        """
        pass
