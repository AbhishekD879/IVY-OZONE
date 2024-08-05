import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C29428_Module_with_Selected_Events_by_Race_Grid(Common):
    """
    TR_ID: C29428
    NAME: Module with Selected Events by Race Grid
    DESCRIPTION: This test case verifies events retrieving by Race Grid (from Horse Racing category)
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8776 Decouple HR Grid and make it available for Featured Tab
    DESCRIPTION: *   BMA-9381 Remove HR Race Grid subtitles on Featured tab
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS -> Featured Tab Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_plus_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap '+ Create Featured Tab Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_go_to_select_eventsby_field_and_selectracegrid(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Race Grid**
        EXPECTED: 
        """
        pass

    def test_005_verify_race_type_id(self):
        """
        DESCRIPTION: Verify <Race> Type ID
        EXPECTED: <Race> Type ID is auto populated with  ID=21
        """
        pass

    def test_006_tap_save_module_button(self):
        """
        DESCRIPTION: Tap 'Save Module' button
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_007_load_invictus_application_and_verify_just_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify just created Module
        EXPECTED: *   Race Grid is present on 'Featured' tab
        EXPECTED: *   Race Grid contains events only from **UK & IRE** and **International **sections
        """
        pass

    def test_008_verify_hrrace_griddisplaying(self):
        """
        DESCRIPTION: Verify HR Race Grid displaying
        EXPECTED: *   **UK & IRE** and **International **sections are merged
        EXPECTED: *   **UK & IRE** and **International **titles are NOT shown
        EXPECTED: *   Current data is present at the top of module
        """
        pass
