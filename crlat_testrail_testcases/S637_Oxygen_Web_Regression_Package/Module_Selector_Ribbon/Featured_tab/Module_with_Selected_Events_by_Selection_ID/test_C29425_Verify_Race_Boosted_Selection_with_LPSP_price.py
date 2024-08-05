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
class Test_C29425_Verify_Race_Boosted_Selection_with_LPSP_price(Common):
    """
    TR_ID: C29425
    NAME: Verify <Race> Boosted Selection with 'LP,SP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Races> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='LP,SP'.
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

    def test_001_go_to_cms___home_modules(self):
        """
        DESCRIPTION: Go to CMS -> Home Modules
        EXPECTED: 
        """
        pass

    def test_002_click_create_feature_tab_module_button(self):
        """
        DESCRIPTION: Click 'Create Feature Tab Module' button
        EXPECTED: 'Featured Tab Module Editor' page is opened
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_go_to_select_eventsby_field_and_selectselection_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Selection ID**
        EXPECTED: 
        """
        pass

    def test_005_set_races_selection_id_wherepricetypecodessplpuse_link_from_preconditions_to_find_details_about_race_event(self):
        """
        DESCRIPTION: Set <Races> Selection ID where **priceTypeCodes="SP,LP," **(use link from Preconditions to find details about <Race> event)
        EXPECTED: Entered Selection ID is shown
        """
        pass

    def test_006_click_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Click 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_007_load_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: Created module with one selection is displayed only if:
        EXPECTED: Selection is from non-started event from any market (with NO attribute '**isStarted="true"**' )
        """
        pass

    def test_008_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        """
        pass

    def test_009_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute for Sports and to local time(**'name'** attribute) for Races
        EXPECTED: *   For events that occur Today date format is **"**<Today> 12 hours" for Races and **"**<Today> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur Tomorrow date format is **"**<Tomorrow> 12 hours" for Races and  "<Tomorrow> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** **12 hour AM/PM" for Sports and "DD-MM 12 hour" for Races
        """
        pass

    def test_010_verify_watch_live_icon_and_label(self):
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

    def test_011_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: Just one price/odds button is shown with correct LP price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
        """
        pass

    def test_012_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        pass

    def test_013_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_014_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_015_click_anywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        pass

    def test_016_go_to_cms_home_module_open_created_module_on_the_previous_steps(self):
        """
        DESCRIPTION: Go to CMS->Home Module->open created module on the previous steps
        EXPECTED: 
        """
        pass

    def test_017_set_races_selection_id_wherepricetypecodessplpbutthere_are_no_pricenumpricedenpricedec_attributes_in_outcome_section_in_ss_responce_use_link_from_preconditions_to_find_details_about_race_event(self):
        """
        DESCRIPTION: Set <Races> Selection ID where **priceTypeCodes="SP,LP," **BUT there are NO priceNum/priceDen/priceDec attributes in outcome section in SS responce (use link from Preconditions to find details about <Race> event)
        EXPECTED: Entered Selection ID is shown
        """
        pass

    def test_018_repeat_steps__6_11(self):
        """
        DESCRIPTION: Repeat steps # 6-11
        EXPECTED: 
        """
        pass

    def test_019_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button with 'SP' label is shown
        """
        pass

    def test_020_repeat_steps__14_16(self):
        """
        DESCRIPTION: Repeat steps # 14-16
        EXPECTED: 
        """
        pass

    def test_021_repeat_steps_1_7__set_for_the_event_based_on_which_module_was_created_in_open_bet_the_following_the_event_will_be_startedstart_time__current_timeisoffyesnote_bet_in_play_list_should_not_be_checked_for_this_event_before_creating_module(self):
        """
        DESCRIPTION: Repeat steps 1-7 -> Set for the event, based on which module was created, in Open Bet the following (the event will be started):
        DESCRIPTION: Start time = current time
        DESCRIPTION: 'isOff'='Yes'
        DESCRIPTION: Note: 'Bet In Play list' should not be checked for this event before creating module
        EXPECTED: Verified module is no more shown within 'Featured' section after event has started
        """
        pass
