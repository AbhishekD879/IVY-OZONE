import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C9726393_Event_Hub_Verify_Sport_Boosted_Selection_Which_Has_Handicap_Value_Available(Common):
    """
    TR_ID: C9726393
    NAME: Event Hub: Verify <Sport> Boosted Selection Which Has Handicap Value Available
    DESCRIPTION: This test case verifies Event hub Modules configured in CMS for <Sport> where Module consists of one selection retrieved by 'Selection ID'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See** 'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    PRECONDITIONS: 3) User is on Homepage > Event Hub tab
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages >Event Hub.
    PRECONDITIONS: 5) Featured Events module by Selection ID created in this event hub using Selection of <Sport> event with Handicap value available
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_for_mobiletabletload_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Created module with one selection is displayed only if:
        EXPECTED: *   Selection is from pre-match event from any market
        EXPECTED: *   Selection is from event with '**isStarted="true"**' attribute **AND **from market with attribute '**isMarketBetInRun="true"**'
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: * 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        EXPECTED: * 'Selection Name' contains handicap value displayed near it
        """
        pass

    def test_003_verify_handicap_value_correctness(self):
        """
        DESCRIPTION: Verify Handicap value correctness
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_004_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the Handicap value displaying
        EXPECTED: * Handicap value is displayed directly to the right of the outcome names
        EXPECTED: * Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_005_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify Sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_006_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: *   'Event Start Time' corresponds to '**startTime**' attribute
        EXPECTED: *   For events that occur Today date format is **"<Today> 12 hours **AM/PM**"**
        EXPECTED: *   For events that occur Tomorrow date format is **"**<Tomorrow> **12 hours **AM/PM**"**
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** 12 hours **AM/PM**"**
        """
        pass

    def test_007_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if drilldownTagNames attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        pass

    def test_008_verify_cash_out_and_star_label_on_top_right_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' and star label on top right corner
        EXPECTED: *   'CASH OUT' label is shown on Boosted selection header if  cashoutAvail="Y" on **Market level**
        EXPECTED: *   White start icon on red background is present on top right corner
        """
        pass

    def test_009_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
        """
        pass

    def test_010_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        pass

    def test_011_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_012_place_a_bet_by_clickingtapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by clicking/tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_013_click_anywhere_on_event_card_except_for_price_buttons_within_the_verified_module(self):
        """
        DESCRIPTION: Click anywhere on Event card (except for price buttons) within the verified module
        EXPECTED: Event Details page is opened
        """
        pass

    def test_014_for_mobiletabletrepeat_steps__1_7___trigger_situation_when_for_market_based_on_which_module_was_createdismarketbetinrunattribute_will_be_removed__refresh_page(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps # 1-7 -> Trigger situation when for market based on which module was created '**isMarketBetInRun'** attribute will be removed-> Refresh page
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Verified module is no more shown within 'Featured' tab
        """
        pass
