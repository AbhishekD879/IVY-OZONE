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
class Test_C28943_Exclude_Unnamed_Favourite_Selections_from_the_Next_Races_Module(Common):
    """
    TR_ID: C28943
    NAME: Exclude Unnamed Favourite Selections from the 'Next Races'  Module
    DESCRIPTION: This test case verifies that 'Unnamed Favourite' and 'Unnamed 2nd Favourite' selection shouldn't be displayed in the 'Next Races' Module module.
    DESCRIPTION: AUTOTEST Mobile: [C2760434]
    DESCRIPTION: AUTOTEST Desktop: [C2760440]
    PRECONDITIONS: There is <Race> event with 'Unnamed Favourite' and 'Unnamed 2nd Favourite' (e.g. two normal selections, 'Unnamed Favourite' and 'Unnamed 2nd Favourite)
    """
    keep_browser_open = True

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 'Unnamed Favourite' and 'Unnamed 2nd Favourite' won't appear in the list of selection on the 'Next Races' module
        """
        pass
