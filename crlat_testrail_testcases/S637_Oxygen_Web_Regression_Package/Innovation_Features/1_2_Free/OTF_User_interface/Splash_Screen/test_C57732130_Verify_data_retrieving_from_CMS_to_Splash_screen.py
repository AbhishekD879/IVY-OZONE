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
class Test_C57732130_Verify_data_retrieving_from_CMS_to_Splash_screen(Common):
    """
    TR_ID: C57732130
    NAME: Verify data retrieving from CMS to 'Splash screen'
    DESCRIPTION: This test case verifies data retrieving from CMS to 'Splash screen'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Static Text'
    PRECONDITIONS: 4. Tap on 'Create Static Text' button
    """
    keep_browser_open = True

    def test_001_populate_all_existing_fields_with_valid_data_and_save_it(self):
        """
        DESCRIPTION: Populate all existing fields with valid data and save it
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_splash_screen(self):
        """
        DESCRIPTION: Open 'Splash screen'
        EXPECTED: - All data retrieved from CMS and displayed:
        EXPECTED: - Main text (pull from CMS->static text-> splash page->pageText1)
        EXPECTED: - Play now button (pull from CMS->static text-> splash page->CTA1)
        EXPECTED: - Cancel button (pull from CMS->static text-> splash page->CTA2)
        EXPECTED: - All data successfully styled
        """
        pass
