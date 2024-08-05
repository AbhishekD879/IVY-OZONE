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
class Test_C28488_Verify_selection_data_and_placing_a_bet(Common):
    """
    TR_ID: C28488
    NAME: Verify selection data and placing a bet
    DESCRIPTION: This test case verifies selection data and placing a bet.
    PRECONDITIONS: 1) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) User is logged in
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_ltsportgticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Sport&gt;'  icon on the Sports Menu Ribbon
        EXPECTED: 'Sport' Landing Page is opened
        """
        pass

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: &lt;Sport&gt; Event Details page is opened
        """
        pass

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by tapping the section's header
        """
        pass

    def test_005_go_to_verified_selection_section(self):
        """
        DESCRIPTION: Go to verified selection section
        EXPECTED: Selection section is displayed within Market section
        """
        pass

    def test_006_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified Market
        """
        pass

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        pass

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
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
        EXPECTED: *   Confirmation message is shown
        """
        pass
