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
class Test_C29408_CMS_Verify_Events_Retrieving_by_Race_TypeID(Common):
    """
    TR_ID: C29408
    NAME: CMS: Verify Events Retrieving by <Race> TypeID
    DESCRIPTION: This test case verifies Events Retrieving by <Race> TypeID (from Horse Racing and Greyhounds categories)
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: - CMS https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Ladbrokes OpenBet System https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: - Coral OpenBet System https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: - For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    PRECONDITIONS: "Auto-refresh events" Checkbox is not checked
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_open_featured_tab_modulesclick_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Go to CMS and open FEATURED TAB MODULES
        DESCRIPTION: Click "Create FEATURED TAB MODULE" button
        EXPECTED: 
        """
        pass

    def test_002_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_003_go_to_select_eventsby_field_and_select_racetype_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Race Type ID**
        EXPECTED: 
        """
        pass

    def test_004_set_valid_race_type_id(self):
        """
        DESCRIPTION: Set valid <Race> Type ID
        EXPECTED: Entered <Race> Type ID is shown
        """
        pass

    def test_005_tap_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_006_load_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load application and verify events within created Module
        EXPECTED: All events have the same <Race> TypeId as was set on step №4
        """
        pass
