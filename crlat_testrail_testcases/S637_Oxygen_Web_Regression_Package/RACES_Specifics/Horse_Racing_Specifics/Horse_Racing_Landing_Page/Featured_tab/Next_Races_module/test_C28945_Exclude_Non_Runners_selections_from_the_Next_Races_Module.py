import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28945_Exclude_Non_Runners_selections_from_the_Next_Races_Module(Common):
    """
    TR_ID: C28945
    NAME: Exclude Non-Runners selections from the 'Next Races' Module
    DESCRIPTION: This test case verifies that 'Non-Runners' will be excluded from the 'Next Races' module.
    PRECONDITIONS: There is <Race> event with 'Non-Runners' (e.g. event which contains 3 or less selection and one of those selections is 'non-runner')
    PRECONDITIONS: 'Non-Runners' is a selection which contains **'N/R'** text next to it's name
    """
    keep_browser_open = True

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 'Non-Runners' won't appear in the 'Next Races' module
        """
        pass
