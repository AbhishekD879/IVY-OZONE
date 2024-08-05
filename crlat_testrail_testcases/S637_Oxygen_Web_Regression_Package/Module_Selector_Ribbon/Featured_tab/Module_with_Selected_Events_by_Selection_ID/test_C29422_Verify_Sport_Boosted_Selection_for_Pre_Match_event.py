import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29422_Verify_Sport_Boosted_Selection_for_Pre_Match_event(Common):
    """
    TR_ID: C29422
    NAME: Verify <Sport> Boosted Selection for Pre-Match event
    DESCRIPTION: This test case verifies Modules configured in CMS for <Sport> where Module consists of one selection retrieved by 'Selection ID'.
    DESCRIPTION: AUTOTEST [C2779944]
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
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

    def test_005_set_sport_selection_idfrom_pre_match_event(self):
        """
        DESCRIPTION: Set <Sport> Selection ID from Pre-Match event
        EXPECTED: Entered Selection ID is shown
        """
        pass

    def test_006_clicktap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Click/Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_007_load_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: Created module with selection is displayed in a separate section
        """
        pass

    def test_008_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: * 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        EXPECTED: * Name of a long selection is wrapped into a few lines without cutting the text
        """
        pass

    def test_009_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute
        EXPECTED: *   For events that occur Today date format is **HH:MM, Today**
        EXPECTED: *   For events that occur Tomorrow date format is **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_010_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        EXPECTED: (Coral only)
        """
        pass

    def test_011_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        pass

    def test_012_verify_that_cash_out_label_is_not_shown_on_the_top_right_corner(self):
        """
        DESCRIPTION: Verify that 'CASH OUT' label is not shown on the top right corner
        EXPECTED: 'CASH OUT' label is NOT shown on Boosted selection header if  cashoutAvail="Y" on **Market level**
        """
        pass

    def test_013_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
        """
        pass

    def test_014_clicktapanywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        pass
