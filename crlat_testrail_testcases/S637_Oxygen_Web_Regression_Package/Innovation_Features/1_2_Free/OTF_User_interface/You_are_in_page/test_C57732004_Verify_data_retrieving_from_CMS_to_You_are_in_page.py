import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C57732004_Verify_data_retrieving_from_CMS_to_You_are_in_page(Common):
    """
    TR_ID: C57732004
    NAME: Verify data retrieving from CMS to 'You are in' page
    DESCRIPTION: This test case verifies data retrieving from CMS to 'You are in' page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Static text'
    PRECONDITIONS: 4. User open edit mode for 'You are in' page
    """
    keep_browser_open = True

    def test_001_populate_all_existing_fields_with_valid_data_and_save_it_in_cms(self):
        """
        DESCRIPTION: Populate all existing fields with valid data and save it in CMS
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_you_are_in_page_on_1_2_free_ui(self):
        """
        DESCRIPTION: Open 'You are in' page on 1-2-Free UI
        EXPECTED: All data retrieved from CMS and displayed
        EXPECTED: - Innovation logo
        EXPECTED: - Main text (pull from CMS->static text-> You are in page -> pageText1)
        EXPECTED: All data styled correctly
        """
        pass
