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
class Test_C9346567_Verify_Leagues_Types_displaying_in_Tennis_Competitions_tab_based_on_CMS_configuration(Common):
    """
    TR_ID: C9346567
    NAME: Verify Leagues (Types) displaying in Tennis 'Competitions' tab based on CMS configuration
    DESCRIPTION: This test case verifies the Leagues (Types) displaying in Tennis 'Competitions' tab based on CMS configuration.
    PRECONDITIONS: 0. 'CompetitionsTennis' config should have 'Initial' checkbox being checked in CMS -> 'System Configuration' -> 'Config'
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Leagues (Types) Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Tennis' and put class ID's in 'InitialClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 5. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 6. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_002_remove_all_ids_from_initialclassids_field_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Remove all IDs from 'InitialClassIDs' field in CMS and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_003_reload_the_page_and_verify_the_leagues_types_displaying(self):
        """
        DESCRIPTION: Reload the page and verify the Leagues (Types) displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The Leagues (Types) are NOT displayed
        EXPECTED: * "No events found" text is displayed instead
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected and highlighted
        EXPECTED: * The Leagues (Types) are NOT displayed
        EXPECTED: * "No events found" text is displayed instead
        """
        pass

    def test_004_add_validactive_ids_to_initialclassids_field_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Add valid(active) IDs to 'InitialClassIDs' field in CMS and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_005_reload_the_page_and_verify_the_leagues_types_displaying(self):
        """
        DESCRIPTION: Reload the page and verify the Leagues (Types) displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_006_replace_ids_in_initialclassids_field_in_cms_with_those_which_are_not_related_to_a_valid_list_of_valuesie_kapcitapki_and_save_changes(self):
        """
        DESCRIPTION: Replace IDs in 'InitialClassIDs' field in CMS, with those which are not related to a valid list of values(i.e. 'kapci,tapki') and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_007_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: E.R. match those described in step 3
        """
        pass

    def test_008_repeat_steps_4_and_5(self):
        """
        DESCRIPTION: Repeat steps 4 and 5
        EXPECTED: E.R. match those described in steps 4 and 5
        """
        pass

    def test_009_replace_ids_in_initialclassids_field_in_cms_with_non_existing_class_numbersvaluesie_06670666_and_save_changes(self):
        """
        DESCRIPTION: Replace IDs in 'InitialClassIDs' field in CMS, with non-existing class numbers/values(i.e. '0667,0666') and Save Changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_010_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: E.R. match those described in step 3
        """
        pass
