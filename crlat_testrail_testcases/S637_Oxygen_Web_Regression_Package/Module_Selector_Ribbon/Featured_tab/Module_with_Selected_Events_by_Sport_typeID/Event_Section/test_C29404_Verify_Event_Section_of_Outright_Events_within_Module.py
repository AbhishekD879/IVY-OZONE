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
class Test_C29404_Verify_Event_Section_of_Outright_Events_within_Module(Common):
    """
    TR_ID: C29404
    NAME: Verify Event Section of Outright Events within Module
    DESCRIPTION: This test case verifies Event section within Module for events which are Outrights
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_cms___home_modules(self):
        """
        DESCRIPTION: Go to CMS -> Home Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_new_module_button(self):
        """
        DESCRIPTION: Tap 'New module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_go_to_select_eventsby_field_and_select_type_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Type ID**
        EXPECTED: 
        """
        pass

    def test_005_set_valid_type_idwhere_allsome_events_are_outrights(self):
        """
        DESCRIPTION: Set valid Type ID**, **where all/some events are **Outrights**
        EXPECTED: Entered Type ID is shown
        """
        pass

    def test_006_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_007_load_oxygen_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify events within created Module
        EXPECTED: All events have the same TypeId as was set on step №5
        """
        pass

    def test_008_go_to_event_section__verify_event_name(self):
        """
        DESCRIPTION: Go to Event section -> Verify Event Name
        EXPECTED: Event Name within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        """
        pass

    def test_009_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: * 'Watch Live' icon and label are NOT shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *   EVFLAG_AVA
        EXPECTED: *   EVFLAG_IVM
        EXPECTED: *   EVFLAG_PVM
        EXPECTED: *   EVFLAG_RVA
        EXPECTED: *   EVFLAG_RPM
        EXPECTED: *   EVFLAG_GVM
        """
        pass

    def test_010_verify_live_label(self):
        """
        DESCRIPTION: Verify 'LIVE' label
        EXPECTED: 'LIVE' label is shown if event has following attributes:
        EXPECTED: rawIsOffCode="Y" OR rawIsOffCode="-" AND isStarted="true"
        """
        pass

    def test_011_verifycash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is NOT shown if cashoutAvail="Y" on event level
        """
        pass

    def test_012_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is NOT displayed only for Football events within Module section
        """
        pass

    def test_013_tapanywhere_on_event_section_button(self):
        """
        DESCRIPTION: Tap anywhere on Event section button
        EXPECTED: Event Details Page is opened
        """
        pass
