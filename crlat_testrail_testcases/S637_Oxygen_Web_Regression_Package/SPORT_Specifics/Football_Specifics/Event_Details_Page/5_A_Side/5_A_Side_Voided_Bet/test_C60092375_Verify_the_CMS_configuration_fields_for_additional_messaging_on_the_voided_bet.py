import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60092375_Verify_the_CMS_configuration_fields_for_additional_messaging_on_the_voided_bet(Common):
    """
    TR_ID: C60092375
    NAME: Verify the CMS configuration fields for additional messaging on the voided bet
    DESCRIPTION: Verify the CMS configuration fields for additional messaging on the voided bet
    PRECONDITIONS: 1: User should have admin access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_with_admin_role(self):
        """
        DESCRIPTION: Login to CMS with admin role
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_cmssystem_configuration_structure_fiveasidevoidhandling(self):
        """
        DESCRIPTION: CMS>System Configuration> Structure> FiveASideVoidHandling
        EXPECTED: Configure the text to be displayed on Voided 5 A Side bet
        """
        pass

    def test_003_launch_ladbrokes_and_login(self):
        """
        DESCRIPTION: Launch Ladbrokes and login
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_004_navigate_to_settled_bets___5_a_side_voided_betspre_play_match(self):
        """
        DESCRIPTION: Navigate to settled bets - 5 A Side Voided bets
        DESCRIPTION: *Pre-Play Match*
        EXPECTED: Go TO 5 A Side button should be displayed with info text
        """
        pass
