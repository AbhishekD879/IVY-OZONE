import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1501655_Verify_Group_Individual_Module(Common):
    """
    TR_ID: C1501655
    NAME: Verify Group Individual Module
    DESCRIPTION: This test case verifies Group Individual Module on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'GROUP_INDIVIDUAL' should be created, enabled and set up in CMS
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_group_individual_module(self):
        """
        DESCRIPTION: Go to Group Individual Module
        EXPECTED: 
        """
        pass

    def test_004_verify_group_individual_module(self):
        """
        DESCRIPTION: Verify Group Individual Module
        EXPECTED: Group Individual Module is a table that consists of the next elements:
        EXPECTED: * 'POS' label and country position displayed in the column
        EXPECTED: * Country flag and abbreviation
        EXPECTED: * 'P' label and points value
        EXPECTED: * 'W' label and won value
        EXPECTED: * 'D' label and draw value
        EXPECTED: * 'L' label and lost value
        EXPECTED: * 'GD' label and goal diff value
        EXPECTED: * 'PTS' label and total matches value
        """
        pass

    def test_005_verify_country_position(self):
        """
        DESCRIPTION: Verify country position
        EXPECTED: Selected country position determines qualified teams within one Group (colored in dark blue)
        """
        pass

    def test_006_verify_data_updates_on_group_individual_module(self):
        """
        DESCRIPTION: Verify data updates on Group Individual Module
        EXPECTED: * Data in Group Individual Module is NOT updated automatically
        EXPECTED: * Data in Group Individual Module is updated only after page refresh
        """
        pass
