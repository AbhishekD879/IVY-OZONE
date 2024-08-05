import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1502721_Verify_auto_scrolling_to_a_current_Knockout_Round(Common):
    """
    TR_ID: C1502721
    NAME: Verify auto scrolling to a current Knockout Round
    DESCRIPTION: This test case verifies auto scrolling to 'Current' Knockouts Round, which is set in CMS
    PRECONDITIONS: - Big Competition > Competition (e.g. World Cup) is configured in CMS
    PRECONDITIONS: - All Knockout Rounds (Round of 16, Quarterfinals, Semifinals, Finals) are correctly configured in CMS. Use test case: https://ladbrokescoral.testrail.com/index.php?/cases/view/1473948
    PRECONDITIONS: - Any round is set as 'Current' in CMS (taken from "active"=true object in MS response)
    PRECONDITIONS: - Coral app is opened
    PRECONDITIONS: - To check MS response go to Network > {tab ID} (response) > "competitionModules" >"rounds"
    """
    keep_browser_open = True

    def test_001_navigate_to_big_competition_eg_world_cup__tab_eg_knockouts(self):
        """
        DESCRIPTION: Navigate to Big Competition (e.g. World Cup) > Tab (e.g. 'Knockouts')
        EXPECTED: Knockouts tab is opened
        """
        pass

    def test_002_verify_auto_scrolling_to_current_activetrue_object_in_ms_response(self):
        """
        DESCRIPTION: Verify auto scrolling to 'Current' ("active"=true object in MS response)
        EXPECTED: * 'Current' ("active"=true in MS response) is auto scrolled to
        EXPECTED: * It is possible to scroll through the page to other rounds with ("active"=false object in MS response)
        """
        pass

    def test_003__in_cms_check_current_for_another_round__save_changes_in_app_verify_auto_scrolling_to_current_activetrue_object_in_ms_response(self):
        """
        DESCRIPTION: * In CMS: Check 'Current' for another round > 'Save Changes'
        DESCRIPTION: * In app: Verify auto scrolling to 'Current' ("active"=true object in MS response)
        EXPECTED: * 'Current' ("active"=true in MS response) is auto scrolled to
        EXPECTED: * It is possible to scroll through the page to other rounds with ("active"=false object in MS response)
        """
        pass

    def test_004__in_cms_uncheck_current_for_a_round__save_changes_in_app_verify_displaying_of_rounds(self):
        """
        DESCRIPTION: * In CMS: Uncheck 'Current' for a round > 'Save Changes'
        DESCRIPTION: * In app: Verify displaying of rounds
        EXPECTED: * No auto scrolling applies
        EXPECTED: * All rounds are displayed in order they are set in CMS (taken from MS response)
        """
        pass
