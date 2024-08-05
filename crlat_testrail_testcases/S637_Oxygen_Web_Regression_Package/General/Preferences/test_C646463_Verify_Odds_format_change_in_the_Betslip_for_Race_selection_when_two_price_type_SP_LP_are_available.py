import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C646463_Verify_Odds_format_change_in_the_Betslip_for_Race_selection_when_two_price_type_SP_LP_are_available(Common):
    """
    TR_ID: C646463
    NAME: Verify Odds format change in the Betslip for <Race> selection when two price type SP, LP are available
    DESCRIPTION: This test case verify Odds format change in the Betslip for <Race> selection when two price type SP, LP are available
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: In order to set SP and LP price use TI tool http://backoffice-tst2.coral.co.uk/ti/ and tick 'LP Available'/'SP Available' checkboxes on the market level. Also, set particular values in 'Live Price' field for selections.
    """
    keep_browser_open = True

    def test_001_add_race_selection_that_contains_sp_and_lp_price_type_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add <Race> selection that contains SP and LP price type to the Betslip and open it
        EXPECTED: * Selection is added
        EXPECTED: * Dropdown with price types is displayed for the selection
        EXPECTED: * LP is selected by default
        """
        pass

    def test_002_coraltap_an_avatar_iconladbrokestap_an_avatar_icon_or_balance_button(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap an avatar icon
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap an avatar icon or balance button
        EXPECTED: **Coral:** / **Ladbrokes:**
        EXPECTED: **Mobile** 'Menu' page / **DESKTOP** 'Menu' pop-up is opened
        """
        pass

    def test_003_tap_on_settings_item___betting_settings(self):
        """
        DESCRIPTION: Tap on 'Settings' item -> 'Betting Settings'
        EXPECTED: **Coral:**
        EXPECTED: * 'Preferences' page is opened
        EXPECTED: * 'Select Odds Format' option is present with buttons 'Fractional' and 'Decimal'
        EXPECTED: * By default 'Fractional' button is selected, all 'Price/Odds' buttons display prices in fractional format
        EXPECTED: **Ladbrokes:**
        EXPECTED: * **Desktop** 'Account Settings' page is opened
        EXPECTED: * **Mobile** '<' Back button, avatar with balance, betslip icon are present on header
        EXPECTED: * 'Set Odds to' option is present with buttons 'Fractional' and 'Decimal'
        EXPECTED: * By default 'Fractional' button is selected, all 'Price/Odds' buttons display prices in fractional format
        """
        pass

    def test_004_switch_to_decimal_format_and_verify_changes_in_the_betslip(self):
        """
        DESCRIPTION: Switch to 'Decimal' format and verify changes in the Betslip
        EXPECTED: * 'Decimal' switcher is selected
        EXPECTED: * New 'buildBet' request is sent
        EXPECTED: * Price format is changed from 'Fractional' to 'Decimal' within dropdown in the Betslip
        """
        pass

    def test_005_switch_to_fractional_format_and_verify_changes_in_the_betslip(self):
        """
        DESCRIPTION: Switch to 'Fractional' format and verify changes in the Betslip
        EXPECTED: * 'Fractional' switcher is selected
        EXPECTED: * New 'buildBet' request is sent
        EXPECTED: * Price format is changed from 'Decimal' to 'Fractional' within dropdown in the Betslip
        """
        pass
