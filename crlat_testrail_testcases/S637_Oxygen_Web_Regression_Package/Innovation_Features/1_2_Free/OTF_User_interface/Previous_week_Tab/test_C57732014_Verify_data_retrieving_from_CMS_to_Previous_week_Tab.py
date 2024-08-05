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
class Test_C57732014_Verify_data_retrieving_from_CMS_to_Previous_week_Tab(Common):
    """
    TR_ID: C57732014
    NAME: Verify data retrieving from CMS to 'Previous week Tab'
    DESCRIPTION: This test case verifies data retrieving from CMS to 'Previous week Tab'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Static texts'
    PRECONDITIONS: 4. User open edit mode for Previous week tab
    """
    keep_browser_open = True

    def test_001_populate_all_existing_fields_with_valid_data_and_save_it(self):
        """
        DESCRIPTION: Populate all existing fields with valid data and save it
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_previous_week_tab_on_1_2_free_ui(self):
        """
        DESCRIPTION: Open 'Previous week Tab' on 1-2-Free UI
        EXPECTED: All data retrieved from CMS and displayed:
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text > Current week Tab)
        EXPECTED: - 'You didn't play 1-2-Free last week' messages (Static text > Current week Tab)
        EXPECTED: - 'Already Played' messages (Static text > Current week Tab)
        EXPECTED: - Events from previous week
        EXPECTED: All data successfully styled
        """
        pass
