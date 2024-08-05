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
class Test_C28472_TO_EDIT_Verify_Scoreboard_configuration_on_System_Configuration_level(Common):
    """
    TR_ID: C28472
    NAME: TO EDIT Verify Scoreboard configuration on System Configuration level
    DESCRIPTION: This test case verifies Scoreboard configuration in CMS on System Configuration level
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: Sport specific scoreboard configuration can be checked via this path: Menus -> Sport Categories -> open chosen sport
    """
    keep_browser_open = True

    def test_001_go_toscoreboardsection_in_system_configuration_tab_cms(self):
        """
        DESCRIPTION: Go to **Scoreboard **section in System Configuration tab (CMS)
        EXPECTED: 
        """
        pass

    def test_002_set_showscoreboard__yes__tapsubmit_button(self):
        """
        DESCRIPTION: Set **showScoreboard **= 'Yes' => Tap 'Submit' button
        EXPECTED: 
        """
        pass

    def test_003_go_to_refreshed_invictus_application__open_details_page_of_verifiedlive_event(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Open Details Page of verified Live event
        EXPECTED: Scoreboard is present
        """
        pass

    def test_004_setshowscoreboard_no__tapsubmit_button(self):
        """
        DESCRIPTION: Set **showScoreboard **= 'No' => Tap 'Submit' button
        EXPECTED: 
        """
        pass

    def test_005_go_to_refreshed_invictus_application__open_details_page_of_verified_live_event(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Open Details Page of verified Live event
        EXPECTED: Scoreboard is absent
        """
        pass

    def test_006_verify_scoreboardurl_field(self):
        """
        DESCRIPTION: Verify **scoreboardUrl **field
        EXPECTED: *   **scoreboardUrl **is editable, where it is possible to specify the scoreboard URL
        EXPECTED: *   default value:
        EXPECTED: ​​*scoreboards-tst2.coral.co.uk/getWidget/0/*
        """
        pass

    def test_007_change_scoreboardurl_link__tap_submit_button(self):
        """
        DESCRIPTION: Change scoreboardUrl link => Tap 'Submit' button
        EXPECTED: 
        """
        pass

    def test_008_go_to_refreshed_invictus_application__open_details_page_of_verified_live_event(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Open Details Page of verified Live event
        EXPECTED: Scoreboard is absent
        """
        pass

    def test_009_set_default_scoreboardurl_link__tap_submit_button(self):
        """
        DESCRIPTION: Set default scoreboardUrl link => tap 'Submit' button
        EXPECTED: 
        """
        pass

    def test_010_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step №3
        EXPECTED: 
        """
        pass
