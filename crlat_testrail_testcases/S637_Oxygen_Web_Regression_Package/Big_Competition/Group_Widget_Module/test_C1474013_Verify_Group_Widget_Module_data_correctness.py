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
class Test_C1474013_Verify_Group_Widget_Module_data_correctness(Common):
    """
    TR_ID: C1474013
    NAME: Verify Group Widget Module data correctness
    DESCRIPTION: This test case verifies Group Widget Module data correctness on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'GROUP_WIDGET' should be created, enabled and set up in CMS
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_group_widget_module(self):
        """
        DESCRIPTION: Go to Group Widget Module
        EXPECTED: 
        """
        pass

    def test_004_verify_groups_ordering(self):
        """
        DESCRIPTION: Verify Groups ordering
        EXPECTED: Groups are ordered in alphabetical order (e.g. Group A, Group B and so on)
        """
        pass

    def test_005_verify_group_name_correctness(self):
        """
        DESCRIPTION: Verify Group name correctness
        EXPECTED: Group name corresponds to **competitionModules.[i].groupModuleData.data.[j].tableName** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Groups returned to Group Widget Module
        """
        pass

    def test_006_verify_number_of_qualified_countries(self):
        """
        DESCRIPTION: Verify number of qualified countries
        EXPECTED: The number of qualified countries corresponds to **competitionModules.[i].groupModuleData.numberQualifiers** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        """
        pass

    def test_007_verify_team_name_correctness(self):
        """
        DESCRIPTION: Verify Team name correctness
        EXPECTED: Team name corresponds to **competitionModules.[i].groupModuleData.data.[j].teams.[k].abbreviation** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Groups returned to Group Widget Module
        EXPECTED: k - the number of all Countries returned to particular for Group
        """
        pass

    def test_008_verify_total_points_score_correctness(self):
        """
        DESCRIPTION: Verify Total Points score correctness
        EXPECTED: Total Points score value corresponds to **competitionModules.[i].groupModuleData.data.[j].teams.[k].totalPoints** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j - the number of all Groups returned to Group Widget Module
        EXPECTED: k - the number of all Countries returned to particular for Group
        """
        pass

    def test_009_verify_teams_ordering_within_group(self):
        """
        DESCRIPTION: Verify Teams ordering within Group
        EXPECTED: Teams are ordered in the same order as received in **teams** array in GET tab/sub tab response
        """
        pass
