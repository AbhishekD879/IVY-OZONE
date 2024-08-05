import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29020_CMS_Control_of_Bet_Animation(Common):
    """
    TR_ID: C29020
    NAME: CMS Control of Bet Animation
    DESCRIPTION: This test case verifies CMS control of bet animation
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-6826 Animation of bet moving to betslip
    DESCRIPTION: *   Betslip animation and full page coverage
    PRECONDITIONS: To load CMS use the link: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: **NOTE**  For Ladbrokes betslip animation CMS configuration is not applicable
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_click_system_configuration_section(self):
        """
        DESCRIPTION: Click 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_go_to_the_generals_structure(self):
        """
        DESCRIPTION: Go to the 'GENERALS' structure
        EXPECTED: 
        """
        pass

    def test_004_set_betslipanimation__on_value_and_save_change(self):
        """
        DESCRIPTION: Set 'betSlipAnimation = On' value and save change
        EXPECTED: The change is saved successfully
        """
        pass

    def test_005_load_oxygen_app_andverify_presence_of_animation_while_selection_is_beeing_added(self):
        """
        DESCRIPTION: Load Oxygen app and verify presence of animation while selection is beeing added
        EXPECTED: Selection is added with animation
        """
        pass

    def test_006_go_back_to_cms(self):
        """
        DESCRIPTION: Go back to CMS
        EXPECTED: 
        """
        pass

    def test_007_setbetslipanimation__off_value_and_save_change(self):
        """
        DESCRIPTION: Set 'betSlipAnimation = Off' value and save change
        EXPECTED: The change is saved successfully
        """
        pass

    def test_008_load_oxygen_app_and_verify_absence_of_animation_while_selection_is_beeing_added_to_betslip(self):
        """
        DESCRIPTION: Load Oxygen app and verify absence of animation while selection is beeing added to Betslip
        EXPECTED: Selection is added to Betslip without animation
        """
        pass
