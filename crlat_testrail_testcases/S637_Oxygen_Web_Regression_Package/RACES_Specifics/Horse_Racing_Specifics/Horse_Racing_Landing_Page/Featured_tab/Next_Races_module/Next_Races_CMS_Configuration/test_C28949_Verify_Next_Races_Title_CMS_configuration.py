import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28949_Verify_Next_Races_Title_CMS_configuration(Common):
    """
    TR_ID: C28949
    NAME: Verify 'Next Races' Title CMS configuration
    DESCRIPTION: This test case verifies Next Races title configuration in CMS
    DESCRIPTION: Story Ticket:
    DESCRIPTION: **BMA-6572 **CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_type_in_search_field_nextraces(self):
        """
        DESCRIPTION: Type in search field 'NEXTRACES'
        EXPECTED: NEXTRACES section is shown
        """
        pass

    def test_004_in_title_field_enteredit_name___press_submit(self):
        """
        DESCRIPTION: In '**Title**' field enter/edit name -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: 
        """
        pass

    def test_006_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: *   Horse Racing landing page is opened
        EXPECTED: *   'Next Races' module is displayed
        """
        pass

    def test_007_verify_next_races_title(self):
        """
        DESCRIPTION: Verify 'Next Races' title
        EXPECTED: *   New title is present
        EXPECTED: *   The header is displayed along the left hand side of the page
        """
        pass
