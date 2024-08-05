import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732111_Verify_appearing_of_events_in_start_time_order(Common):
    """
    TR_ID: C57732111
    NAME: Verify appearing of events in start time order
    DESCRIPTION: This test case verifies appearing of events in start time order
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Game view'
    PRECONDITIONS: 4. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_001_create_few_events_with_different_start_time_during_this_week_and_save_it(self):
        """
        DESCRIPTION: Create few Events with different start time (during this week) and save it
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - All data retrieved from CMS and displayed
        EXPECTED: - Events appear in start time order
        """
        pass
