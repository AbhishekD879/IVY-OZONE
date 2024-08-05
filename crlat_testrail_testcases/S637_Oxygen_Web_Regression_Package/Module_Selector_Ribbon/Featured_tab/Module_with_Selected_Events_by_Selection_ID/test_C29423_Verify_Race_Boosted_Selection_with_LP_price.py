import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29423_Verify_Race_Boosted_Selection_with_LP_price(Common):
    """
    TR_ID: C29423
    NAME: Verify <Race> Boosted Selection with 'LP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Race> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='LP'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch Oxygen application
        EXPECTED: Oxygen page is loaded
        """
        pass

    def test_002_go_to_cms___home_modules(self):
        """
        DESCRIPTION: Go to CMS -> Home Modules
        EXPECTED: Home Modules is loaded.
        """
        pass

    def test_003_click_create_feature_tab_module_button(self):
        """
        DESCRIPTION: Click 'Create Feature Tab Module' button
        EXPECTED: 'Featured Tab Module Editor' page is opened
        """
        pass

    def test_004_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: Field is populated.
        """
        pass

    def test_005_go_to_select_eventsby_field_and_selectselection_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Selection ID**
        EXPECTED: **Selection ID** is selected
        """
        pass

    def test_006_set_races_selection_id_where_pricetypecodeslp_use_link_from_preconditions_to_find_details_about_race_event(self):
        """
        DESCRIPTION: Set <Races> Selection ID where **priceTypeCodes="LP,"** (use link from Preconditions to find details about <Race> event)
        EXPECTED: Entered Selection ID is displayed
        """
        pass

    def test_007_click_load_selection___confirm_selection___save_module_button(self):
        """
        DESCRIPTION: Click 'Load Selection' -> 'Confirm Selection' -> 'Save Module' button
        EXPECTED: 
        """
        pass

    def test_008_load_oxygen_application_and_verify_the_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify the selection within created Module
        EXPECTED: Created module with one selection is displayed only if the selection is from non-started event from any market. The non-started event Open Bet attributes :
        EXPECTED: *   'Status'='A'
        EXPECTED: *   'isOff'='N/A'
        """
        pass

    def test_009_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        """
        pass

    def test_010_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute for Sports and to local time(**'name'** attribute) for Races
        EXPECTED: *   For events that occur Today date format is **"**<Today> 12 hours" for Races and **"**<Today> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur Tomorrow date format is **"**<Tomorrow> 12 hours" for Races and  "<Tomorrow> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** **12 hour AM/PM" for Sports and "DD-MM 12 hour" for Races
        """
        pass

    def test_011_verify_watch_live_icon_and_label(self):
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

    def test_012_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in a fractional format (**'priceDec'** in a decimal format) attributes values in SS response
        """
        pass

    def test_013_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        pass

    def test_014_open_betslip_page(self):
        """
        DESCRIPTION: Open BetSlip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_015_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_016_clicktap_anywhere_on_event_card_except_for_price_buttons_within_the_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within the verified module
        EXPECTED: Event Details page is opened
        """
        pass

    def test_017_repeat_steps_1_8__set_for_the_event_based_on_which_module_was_created_in_open_bet_the_following_the_event_will_be_startedstart_time__current_timeisoffyesnote_bet_in_play_list_should_not_be_checked_for_this_event_before_creating_module(self):
        """
        DESCRIPTION: Repeat steps 1-8 -> Set for the event, based on which module was created, in Open Bet the following (the event will be started):
        DESCRIPTION: Start time = current time
        DESCRIPTION: 'isOff'='Yes'
        DESCRIPTION: Note: 'Bet In Play list' should not be checked for this event before creating module
        EXPECTED: Verified module is no more shown within 'Featured' section after event has started
        """
        pass
