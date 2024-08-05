import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726391_Event_Hub_Verify_Race_Boosted_Selection_with_SP_price(Common):
    """
    TR_ID: C9726391
    NAME: Event Hub: Verify <Race> Boosted Selection with 'SP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Races> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='SP'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is on Homepage > Event Hub tab
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 5) Featured Events module by Selection ID is created in this Event Hub using ID of Race event.
    PRECONDITIONS: **NOTE: **Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_the_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load the Oxygen application and verify selection within created Module
        EXPECTED: Created module with one selection is displayed only if:
        EXPECTED: Selection is from non-started event from any market (with NO attribute '**isStarted="true"**' )
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: 'Selection Name' within module corresponds to &lt;name&gt; attribute from SS response OR to &lt;name&gt; set in CMS if name was overridden
        """
        pass

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute for Sports and to local time(**'name'** attribute) for Races
        EXPECTED: *   For events that occur Today date format is **"**&lt;Today&gt; 12 hours" for Races and **"**&lt;Today&gt; 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur Tomorrow date format is **"**&lt;Tomorrow&gt; 12 hours" for Races and  "&lt;Tomorrow&gt; 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** **12 hour AM/PM" for Sports and "DD-MM 12 hour" for Races
        """
        pass

    def test_004_verify_watch_live_icon_and_label(self):
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

    def test_005_verifycash_out_and_start_icon_label_on_right_top_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' and start icon  label on right top corner
        EXPECTED: *   'CASH OUT' label is shown if cashoutAvail="Y" on Market level
        EXPECTED: *   White start icon on red background is present on top right corner
        """
        pass

    def test_006_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button with 'SP' label is shown
        """
        pass

    def test_007_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        pass

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_009_place_a_bet_by_clicking_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by clicking 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_010_click_anywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        pass
