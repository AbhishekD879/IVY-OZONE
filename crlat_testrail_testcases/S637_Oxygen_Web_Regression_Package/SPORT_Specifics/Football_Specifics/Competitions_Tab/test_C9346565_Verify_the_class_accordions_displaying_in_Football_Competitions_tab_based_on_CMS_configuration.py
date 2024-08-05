import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C9346565_Verify_the_class_accordions_displaying_in_Football_Competitions_tab_based_on_CMS_configuration(Common):
    """
    TR_ID: C9346565
    NAME: Verify the class accordions displaying in Football 'Competitions' tab based on CMS configuration
    DESCRIPTION: This test case verifies the class accordions displaying in Football 'Competitions' tab based on CMS configuration.
    PRECONDITIONS: 0. 'CompetitionsFootball' config should have 'Initial' checkbox being checked in CMS -> 'System Configuration' -> 'Config'
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Football Landing page
    PRECONDITIONS: 3. Click/Tap on 'Competition' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Football' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 5. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 6. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 7. IDs that are typically set in **'A-ZClassIDs'** field: 115,592,591,595,100,109,104,103,102,101,108,106,105,136,137,134,135,138,139,548,133,132,131,130,145,146,147,148,149,140,142,141,144,143,118,119,116,117,114,112,113,111,110,127,128,129,123,124,125,126,120,652,122,121,584,179,178,172,173,170,171,176,177,174,175,587,586,589,181,182,183,180,159,158,157,154,155,152,153,150,151,168,167,169,163,164,165,166,160,161,162,69,68,715,73,74,71,72,70,724,79,76,75,78,77,82,83,84,85,80,81,730,89,88,87,86,739,91,92,90,95,96,93,94,743,744,745,740,741,742,98,97,99,603,16291
    PRECONDITIONS: 8. IDs that are typically set in **'InitialClassIDs'** field:
    PRECONDITIONS: * International (Class ID = 115)
    PRECONDITIONS: * UEFA Club Comps (Class ID = 165)
    PRECONDITIONS: * England (Class ID = 97)
    PRECONDITIONS: * Scotland (Class ID=158)
    PRECONDITIONS: * Spain (Class ID=166)
    PRECONDITIONS: * Italy (Class ID=120)
    PRECONDITIONS: * Germany (Class ID=105)
    PRECONDITIONS: * France (Class ID=102)
    PRECONDITIONS: * Netherlands (Class ID=140)
    PRECONDITIONS: * USA (Class ID=176)
    PRECONDITIONS: **(!)** 'CompetitionsFootball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_verify_popular_and_a_z_class_accordions_displaying(self):
        """
        DESCRIPTION: Verify 'Popular' and 'A-Z' class accordions displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        """
        pass

    def test_002_remove_all_ids_from_initialclassids_field_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Remove all IDs from 'InitialClassIDs' field in CMS and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_003_reload_the_page_and_verify_popular_class_accordions_displaying(self):
        """
        DESCRIPTION: Reload the page and verify 'Popular' class accordions displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are NOT displayed
        EXPECTED: * The A-Z' class accordions are loaded with 'A-Z COMPETITIONS' label at the top of the page
        EXPECTED: * All accordions are collapsed by default
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are NOT displayed
        EXPECTED: * "No events found" is displayed
        """
        pass

    def test_004_for_desktopcheck_a_z_class_accordions_when_a_z_switcher_is_selected(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'A-Z' class accordions when 'A-Z' switcher is selected
        EXPECTED: **For Desktop:**
        EXPECTED: * 'A-Z' switcher is selected and highlighted
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: * The First accordion is expanded by default
        """
        pass

    def test_005_add_ids_to_initialclassids_field_and_remove_all_ids_from_a_zclassids_field_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Add IDs to 'InitialClassIDs' field and remove all IDs from 'A-ZClassIDs' field in CMS and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_006_reload_the_page_and_verify_a_z_class_accordions_displaying(self):
        """
        DESCRIPTION: Reload the page and verify 'A-Z' class accordions displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * The A-Z' class accordions are NOT displayed
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: **For Desktop:**
        EXPECTED: * 'A-Z' switcher is selected and highlighted
        EXPECTED: * The 'A-Z' class accordions are NOT displayed
        EXPECTED: * "No events found" is displayed
        """
        pass

    def test_007_restore_all_initialclassids_and_a_zclassids_values_back_to_those_that_were_set_at_the_start_of_the_test_case_execution_and_save_changes(self):
        """
        DESCRIPTION: Restore all 'InitialClassIDs' and 'A-ZClassIDs' values back to those that were set at the start of the test case execution and save changes.
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_008_repeat_steps_2_6_but_instead_of_removing_ids_replace_ids_with_those_which_are_not_related_to_a_valid_list_of_valuesie_kapcitapki_and_save_changes(self):
        """
        DESCRIPTION: Repeat steps 2-6, but instead of removing IDs, replace IDs with those which are not related to a valid list of values(i.e. 'kapci,tapki') and Save Changes
        EXPECTED: 
        """
        pass

    def test_009_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step 7
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_6_but_instead_of_removing_ids_replace_ids_with_with_non_existing_class_numbersvaluesie_06670666_and_save_changes(self):
        """
        DESCRIPTION: Repeat steps 2-6, but instead of removing IDs, replace IDs with with non-existing class numbers/values(i.e. '0667,0666') and Save Changes
        EXPECTED: 
        """
        pass
