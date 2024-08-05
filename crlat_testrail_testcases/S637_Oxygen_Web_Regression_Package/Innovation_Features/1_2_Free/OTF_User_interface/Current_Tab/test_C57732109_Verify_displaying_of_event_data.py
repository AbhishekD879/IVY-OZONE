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
class Test_C57732109_Verify_displaying_of_event_data(Common):
    """
    TR_ID: C57732109
    NAME: Verify displaying of event data
    DESCRIPTION: This test case verifies displaying of event data
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Game view'
    PRECONDITIONS: 4. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_001_populate_events_information_with_valid_data_and_save_it(self):
        """
        DESCRIPTION: Populate Events information with valid data and save it
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: All data retrieved from CMS and displayed
        EXPECTED: Event block consist:
        EXPECTED: - Match Number
        EXPECTED: - Kick off time (Time format: 17:30 SAT, 19:30 SAT, 16:00 SUN)
        EXPECTED: - Score predictions arrows
        EXPECTED: - Teams t-shirts
        EXPECTED: - Teams names
        EXPECTED: - TV icon
        """
        pass
