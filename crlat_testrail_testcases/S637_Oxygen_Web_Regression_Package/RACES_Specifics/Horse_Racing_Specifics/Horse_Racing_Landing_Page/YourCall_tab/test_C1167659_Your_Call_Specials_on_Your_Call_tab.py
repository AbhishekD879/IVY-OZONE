import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1167659_Your_Call_Specials_on_Your_Call_tab(Common):
    """
    TR_ID: C1167659
    NAME: Your Call Specials on Your Call tab
    DESCRIPTION: This test case verifies the Your Call Specials accordion on YourCall tab for Horse Racing
    PRECONDITIONS: Horse Racing page is loaded and Horse Racing Your Call Specials selections available (Horse Racing Your Call Specials selections should be configured in TI).
    PRECONDITIONS: To retrieve all events with markets and selections for Horse Racing Your Call Specials type:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/TTTT
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: TTTT - Your Call Specials type id (15031)
    PRECONDITIONS: or
    PRECONDITIONS: Create selections if necessary:
    PRECONDITIONS: Under the category Horse Racing (category id = 21) select Daily Racing Specials class (id = 227), then select Your Call Specials Type, then add market created using 'YourCall Specials' market template
    """
    keep_browser_open = True

    def test_001_navigate_to_your_call_tab(self):
        """
        DESCRIPTION: Navigate to Your Call tab
        EXPECTED: * Your Call tab is loaded and Your Call Specials section is displayed below 'Tweet Now' button
        EXPECTED: * 'YourCall Specials' accordion is expanded by default and not collapsible
        """
        pass

    def test_002_verify_the_section_header(self):
        """
        DESCRIPTION: Verify the section header
        EXPECTED: * Section header contains # (YourCall) icon and is named "YourCall Specials"
        EXPECTED: * On **Desktop** section header is not displayed
        """
        pass

    def test_003_verify_the_section_content(self):
        """
        DESCRIPTION: Verify the section content
        EXPECTED: * Switcher tabs (for ex., Featured, Odds On, Events - 5/2, 50/1+, Antepost) are displayed at the top of accordion
        EXPECTED: * The amount of tabs is the same as amount of markets with selection(s) within response EventToOutcomeForType/<#YourCall type id> from OpenBet
        EXPECTED: * If the number of tabs are 5 or more then switcher to scroll tabs horizontally is available
        EXPECTED: * Tabs are ordered by **dispOrder** parameter for a markets from in EventToOutcomeForType (Type id for YourCall specials for HR) response. The lower the value, the higher the position
        EXPECTED: * Content of first tab is displayed by default
        """
        pass

    def test_004_verify_tabs_names(self):
        """
        DESCRIPTION: Verify tab's names
        EXPECTED: * Name of each tab is the same as corresponding market name from response EventToOutcomeForType/<#YourCall type id>
        """
        pass

    def test_005_verify_the_content_of_tabs(self):
        """
        DESCRIPTION: Verify the content of tabs
        EXPECTED: * Each tab contains selection(s) names and prices from corresponding market from response EventToOutcomeForType/<#YourCall type id>
        EXPECTED: * Selections are ordered by **dispOrder** parameter for a selection from in EventToOutcomeForType (Type id for YourCall specials for HR) response. The lower the value, the higher the position
        EXPECTED: * The name of each selection begins with "#YourCall" label
        EXPECTED: * For **Desktop** (starting from 1280 PX)  the selections within tab are displayed in 2 columns and ordered one by one from left to the right based
        """
        pass

    def test_006_on_mobiletablet_scroll_content_of_each_tab(self):
        """
        DESCRIPTION: On **Mobile/Tablet** scroll content of each tab
        EXPECTED: * Content of tabs is scrollable
        EXPECTED: * Tabs becomes sticky to the top and fixed below page header 'Horse Racing'
        """
        pass

    def test_007_verify_yourcall_tab_content_if_are_no_yourcall_specials_selections_available(self):
        """
        DESCRIPTION: Verify YourCall tab content if are no YourCall Specials selections available
        EXPECTED: Only the static text block and the 'tweet now' button are displayed
        """
        pass

    def test_008_for_mobile_add_any_available_selection_from_yourcall_tab_to_quickbet_place_a_bet(self):
        """
        DESCRIPTION: **[For mobile]**
        DESCRIPTION: * Add any available selection from YourCall tab to QuickBet
        DESCRIPTION: * Place a bet
        EXPECTED: * Selection is added to QuickBet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown
        """
        pass

    def test_009__add_any_available_selection_to_betslip_place_a_bet(self):
        """
        DESCRIPTION: * Add any available selection to Betslip
        DESCRIPTION: * Place a bet
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is shown
        """
        pass
