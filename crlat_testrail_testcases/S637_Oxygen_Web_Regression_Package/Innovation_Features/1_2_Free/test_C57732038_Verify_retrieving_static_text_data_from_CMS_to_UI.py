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
class Test_C57732038_Verify_retrieving_static_text_data_from_CMS_to_UI(Common):
    """
    TR_ID: C57732038
    NAME: Verify retrieving static text data from CMS to UI
    DESCRIPTION: This test case verifies retrieving static text data from CMS to UI
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001_make_changes_for_each_field_of_static_texts_on_cms(self):
        """
        DESCRIPTION: Make changes for each field of Static texts on CMS
        EXPECTED: Changes to each field successfully saved
        """
        pass

    def test_002_open_1_2_free_ui(self):
        """
        DESCRIPTION: Open 1-2-Free UI
        EXPECTED: All text changes correctly retrieved and displayed on UI
        """
        pass
