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
class Test_C28535_Verify_placing_a_bet_on_Half_Time_Full_Time_market(Common):
    """
    TR_ID: C28535
    NAME: Verify placing a bet on 'Half Time/Full Time' market
    DESCRIPTION: This test case verifies markets data and bet placement on 'Half Time/Full Time' market
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Jira ticket: **BMA-3863
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

    def test_003_go_to_half_timefull_time_market_section(self):
        """
        DESCRIPTION: Go to 'Half Time/Full Time' market section
        EXPECTED: *   Section is present on Event Details Page and titled 'Half Time/Full Time market section'
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_expandhalf_timefull_time_market_section(self):
        """
        DESCRIPTION: Expand 'Half Time/Full Time' market section
        EXPECTED: The list of available selections received from SS response are displayed within the market section
        """
        pass

    def test_005_add_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add selection to bet slip
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted automatically
        """
        pass

    def test_006_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   The following information is displayed in the Betslip for added selection:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on the event level)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        pass

    def test_007_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        pass

    def test_008_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        pass
