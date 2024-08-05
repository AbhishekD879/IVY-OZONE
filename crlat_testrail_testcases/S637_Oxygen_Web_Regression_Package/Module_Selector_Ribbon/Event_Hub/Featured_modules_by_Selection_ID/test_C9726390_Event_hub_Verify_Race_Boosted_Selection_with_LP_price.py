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
class Test_C9726390_Event_hub_Verify_Race_Boosted_Selection_with_LP_price(Common):
    """
    TR_ID: C9726390
    NAME: Event hub: Verify <Race> Boosted Selection with 'LP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Race> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='LP'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is on Homepage > Event Hub tab
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 5) Featured events module by Selection ID using ID of Race event is created in this Event Hub.
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_verify_the_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify the selection within created Module
        EXPECTED: Created module with one selection is displayed only if the selection is from non-started event from any market. The non-started event Open Bet attributes :
        EXPECTED: *   'Status'='A'
        EXPECTED: *   'isOff'='N/A'
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
        DESCRIPTION: Verify 'Event Start time' within created Module
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

    def test_005_verifycash_out_and_start_label_on_top_right_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' and start label on top right corner
        EXPECTED: 'CASH OUT' label is shown if cashoutAvail="Y" on Market level
        """
        pass

    def test_006_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in a fractional format (**'priceDec'** in a decimal format) attributes values in SS response
        """
        pass

    def test_007_for_the_special_offer_in_featured_section_verify_the_visibility_and_size_of_the_priceodds_button_for_various_screen_resolutions(self):
        """
        DESCRIPTION: For the 'Special' offer in 'Featured' section, verify the visibility and size of the 'Price/Odds' button for various screen resolutions
        EXPECTED: * The Price/Odd buttons remain visible throughout the various resolution changes.
        EXPECTED: * The size of the 'Price/Odds' button depends on the screen resolutions
        """
        pass

    def test_008_for_the_enhanced_offer_in_featured_section_verify_the_visibility_and_size_of_the_priceodds_button_for_various_screen_resolutions(self):
        """
        DESCRIPTION: For the 'Enhanced' offer in 'Featured' section, verify the visibility and size of the 'Price/Odds' button for various screen resolutions
        EXPECTED: * The Price/Odd buttons remain visible throughout the various resolution changes.
        EXPECTED: * The size of the 'Price/Odds' button depends on the screen resolutions
        """
        pass

    def test_009_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        pass

    def test_010_open_betslip_page(self):
        """
        DESCRIPTION: Open BetSlip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_011_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_012_clicktap_anywhere_on_event_card_except_for_price_buttons_within_the_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within the verified module
        EXPECTED: Event Details page is opened
        """
        pass

    def test_013_repeat_steps_1_7_gt_set_for_the_event_based_on_which_module_was_created_in_open_bet_the_following_the_event_will_be_startedstatussisoffyes(self):
        """
        DESCRIPTION: Repeat steps 1-7 -&gt; Set for the event, based on which module was created, in Open Bet the following (the event will be started):
        DESCRIPTION: 'Status'='S'
        DESCRIPTION: 'isOff'='Yes'
        EXPECTED: 
        """
        pass

    def test_014_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Verified module is still shown within 'Featured' section
        """
        pass
