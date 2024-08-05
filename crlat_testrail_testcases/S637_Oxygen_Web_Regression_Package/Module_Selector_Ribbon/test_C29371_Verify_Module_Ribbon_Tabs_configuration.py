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
class Test_C29371_Verify_Module_Ribbon_Tabs_configuration(Common):
    """
    TR_ID: C29371
    NAME: Verify Module Ribbon Tabs configuration
    DESCRIPTION: ******************************************************************************************
    DESCRIPTION: ******************************************************************************************
    DESCRIPTION: This test case verifies configuration of tabs on the Module Selector Ribbon on the Homepage.
    DESCRIPTION: To be run on mobile, tablet and desktop.
    DESCRIPTION: Will be updated with BMA-1520.
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: Data for 'ID' and 'URL' parameters for Module Ribbon Tabs in CMS https://confluence.egalacoral.com/display/SPI/Data+for+%27ID%27+and+%27URL%27+parameters+for+Module+Ribbon+Tabs+in+CMS
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_check_module_ribbon_tabs(self):
        """
        DESCRIPTION: Check Module Ribbon Tabs
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   Module Ribbon Tabs positioned below the Promotions Banner Carousel
        EXPECTED: *   'Featured' tab is selected by default ('Your Enhanced Multiples' - for logged in users who have private markets available)
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_verify_order_of_tabs_onmodule_ribbon_tabs(self):
        """
        DESCRIPTION: Verify order of tabs on Module Ribbon Tabs
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Order of tabs corresponds to the order in CMS ('Module Ribbon Tabs' tab)
        EXPECTED: **For desktop:**
        EXPECTED: * Order of sections is NOT CMS-controlled
        EXPECTED: * Sections are displayed in order mentioned in step 2
        """
        pass

    def test_004_open_module_ribbon_tabs_page_in_cms(self):
        """
        DESCRIPTION: Open Module Ribbon Tabs page in CMS
        EXPECTED: Module Ribbon Tabs page is opened
        """
        pass

    def test_005_tap_on_pluscreate_module_ribbon_tab_button(self):
        """
        DESCRIPTION: Tap on '+Create Module Ribbon Tab' button
        EXPECTED: 'Create a new Module Ribbon Tab' pop-up is opened
        """
        pass

    def test_006_verify_ui_elements_on_create_a_new_module_ribbon_tab_pop_up(self):
        """
        DESCRIPTION: Verify UI elements on 'Create a new Module Ribbon Tab' pop-up
        EXPECTED: * 'Title' field is present
        EXPECTED: * 'Directive Name' is present
        EXPECTED: * Dropdown with list of Directive Names is present
        EXPECTED: * 'ID' field is present
        EXPECTED: * 'URL' field is present
        EXPECTED: * 'Create' button is present
        EXPECTED: * 'cancel' button is present
        """
        pass

    def test_007_verified_required_fields(self):
        """
        DESCRIPTION: Verified required fields
        EXPECTED: * 'Title' field is required.
        EXPECTED: * 'ID' field is required
        EXPECTED: * 'URL' field is required
        """
        pass

    def test_008_fill_all_required_fields_by_correct_dataplease_note_that_id_and_url_fields_should_be_filled_according_to_the_selected_directive_name_httpsconfluenceegalacoralcomdisplayspidataplusforplus27id27plusandplus27url27plusparametersplusforplusmoduleplusribbonplustabsplusinpluscms_(self):
        """
        DESCRIPTION: Fill all required fields by correct data
        DESCRIPTION: (Please note that 'ID' and 'URL' fields should be filled according to the selected 'Directive Name' https://confluence.egalacoral.com/display/SPI/Data+for+%27ID%27+and+%27URL%27+parameters+for+Module+Ribbon+Tabs+in+CMS )
        EXPECTED: 
        """
        pass

    def test_009_tap_on_create_button_on_create_a_new_module_ribbon_tab_pop_up(self):
        """
        DESCRIPTION: Tap on 'Create' button on 'Create a new Module Ribbon Tab' pop-up
        EXPECTED: * Module Ribbon Tab is created
        EXPECTED: * Module Ribbon Tab page is opened
        EXPECTED: * 'Active' check-box is selected by default
        EXPECTED: * 'ID' field is not editable
        EXPECTED: * 'URL' field is not editable
        """
        pass

    def test_010_verify_name_of_tab_on_module_ribbon_tabs(self):
        """
        DESCRIPTION: Verify name of tab on Module Ribbon Tabs
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Name corresponds to 'Title' field in CMS
        EXPECTED: **For desktop:**
        EXPECTED: Section names are NOT CMS-controlled
        """
        pass

    def test_011_verify_tab_presenceabsence(self):
        """
        DESCRIPTION: Verify tab presence/absence
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Tab is shown/hidden depending on 'Active' parameter in CMS
        EXPECTED: **For desktop:**
        EXPECTED: Section availability is NOT CMS-controlled (except 'Featured' one)
        """
        pass

    def test_012_verify_tab_renaming(self):
        """
        DESCRIPTION: Verify tab renaming
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   It is possible to edit tab name of already created tab
        EXPECTED: *   Tab with edited name is displayed correctly on front-end
        EXPECTED: *   All data is displayed correctly within tab
        EXPECTED: **For desktop:**
        EXPECTED: Section names are NOT CMS-controlled
        """
        pass

    def test_013_verify_tab_deleting(self):
        """
        DESCRIPTION: Verify tab deleting
        EXPECTED: It is possible to delete tab by clicking on 'Delete module ribbon tab' button
        """
        pass
