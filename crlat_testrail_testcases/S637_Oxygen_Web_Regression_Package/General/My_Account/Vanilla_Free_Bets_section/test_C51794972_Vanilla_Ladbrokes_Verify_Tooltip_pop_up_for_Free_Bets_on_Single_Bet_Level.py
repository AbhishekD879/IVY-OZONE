import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C51794972_Vanilla_Ladbrokes_Verify_Tooltip_pop_up_for_Free_Bets_on_Single_Bet_Level(Common):
    """
    TR_ID: C51794972
    NAME: [Vanilla Ladbrokes] Verify Tooltip pop up for Free Bets on Single Bet Level
    DESCRIPTION: This test case verifies FreeBet "i" (information) icon pop up for Free Bets with Single Redemption values
    PRECONDITIONS: - User has FreeBet(s) available with next 'Single Redemption Values' on 'Any', 'Category', 'Class', 'Type', 'Event', 'Market', 'Selection' Bet Level
    PRECONDITIONS: - Instruction how to create a 'Redemption Value' & add a Free Bet to a user: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event
    PRECONDITIONS: - User with free bets is logged in an app
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_menu__offers__sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account menu > Offers > Sports Free Bets
        EXPECTED: Sports Free Bets Page is opened
        """
        pass

    def test_002_tap_on_i_information_icon_of_a_free_bet_that_applies_on_any_eventredemption_value__any(self):
        """
        DESCRIPTION: Tap on "i" (information) icon of a Free Bet that applies on any event
        DESCRIPTION: ('Redemption Value' = 'Any')
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for any events."
        """
        pass

    def test_003_tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_categoryredemption_value_is_set_on_category_level(self):
        """
        DESCRIPTION: Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Category
        DESCRIPTION: ('Redemption Value' is set on 'Category' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Category e.g. Football> events."
        """
        pass

    def test_004_tap_on_ok_buttonanywhere_outside_the_pop_up(self):
        """
        DESCRIPTION: Tap on OK button/anywhere outside the pop up
        EXPECTED: Pop up is closed
        """
        pass

    def test_005___close_the_pop_up__tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_classredemption_value_is_set_on_class_level(self):
        """
        DESCRIPTION: - Close the pop up
        DESCRIPTION: - Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Class
        DESCRIPTION: ('Redemption Value' is set on 'Class' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Class e.g. Football England> events."
        """
        pass

    def test_006___close_the_pop_up__tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_typeredemption_value_is_set_on_type_level(self):
        """
        DESCRIPTION: - Close the pop up
        DESCRIPTION: - Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Type
        DESCRIPTION: ('Redemption Value' is set on 'Type' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Type e.g. Premiere League> events."
        """
        pass

    def test_007___close_the_pop_up__tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_eventredemption_value_is_set_on_event_level(self):
        """
        DESCRIPTION: - Close the pop up
        DESCRIPTION: - Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Event
        DESCRIPTION: ('Redemption Value' is set on 'Event' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Event e.g. Chelsea vs Liverpool> event."
        """
        pass

    def test_008___close_the_pop_up__tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_marketredemption_value_is_set_on_market_level(self):
        """
        DESCRIPTION: - Close the pop up
        DESCRIPTION: - Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Market
        DESCRIPTION: ('Redemption Value' is set on 'Market' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Event e.g. Chelsea vs Liverpool> event."
        """
        pass

    def test_009___close_the_pop_up__tap_on_i_information_icon_of_a_free_bet_that_applies_on_a_sportraces_selectionredemption_value_is_set_on_selection_level(self):
        """
        DESCRIPTION: - Close the pop up
        DESCRIPTION: - Tap on "i" (information) icon of a Free Bet that applies on a <Sport/Races> Selection
        DESCRIPTION: ('Redemption Value' is set on 'Selection' level)
        EXPECTED: Pop up is displayed with text FreeBet:
        EXPECTED: "This Free Bet can be used for <Event e.g. Chelsea vs Liverpool> event."
        """
        pass
