import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732143_Verify_BE_APIs_for_Static_Texts(Common):
    """
    TR_ID: C57732143
    NAME: Verify BE APIs for Static Texts
    DESCRIPTION: This test case verifies BE APIs for Static Texts using Postman collection
    PRECONDITIONS: CMS API specification (coral/admin):
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com
    PRECONDITIONS: 1. Actual version of Collection and Environment imported to Postman: https://confluence.egalacoral.com/display/SPI/OTF+API+Test+Cases+-+Postman
    PRECONDITIONS: 2. Select actual testing Environment by changing {{env}} variable to: dev0, dev1, dev2 and {{brand}} variable to: ladbrokes, bma
    PRECONDITIONS: 3. Login using 'CMS Login' POST method from 1-2-Free collection
    PRECONDITIONS: 4. Static Texts exist before testing
    """
    keep_browser_open = True

    def test_001___open_postman_collection_runner_and_choose_folder_1_2_free__static_texts__select_imported_environment_1_2_free__run_testing_by_clicking_or_run_game_button(self):
        """
        DESCRIPTION: - Open Postman Collection Runner and choose folder: '1-2-Free > Static Texts'
        DESCRIPTION: - Select imported Environment: '1-2-Free'
        DESCRIPTION: - Run testing by clicking or 'Run Game' button
        EXPECTED: All described tests should return **PASSED** status:
        EXPECTED: - Status code is 200
        EXPECTED: - Status code is 201
        EXPECTED: - Status code is 204
        EXPECTED: - Status code is 404
        EXPECTED: - Response is valid and have a body
        EXPECTED: - Body matches string
        EXPECTED: - Response value equal request value
        EXPECTED: - Response ID different from request ID
        """
        pass

    def test_002___run_update_an_existing_statictextotf_put_method__change_request_body_manually__verify_body_response(self):
        """
        DESCRIPTION: - Run 'Update an existing StaticTextOtf' PUT method
        DESCRIPTION: - Change request body manually
        DESCRIPTION: - Verify body response
        EXPECTED: - All tests for current method should return **PASSED** status
        EXPECTED: - Body consist values according to manually selected
        EXPECTED: - Static text updated and displayed on CMS and body consist same values
        """
        pass

    def test_003___run_public_retrieve_all_one_two_free_static_texts_get_method__verify_body_response(self):
        """
        DESCRIPTION: - Run '[Public] Retrieve all One-Two-Free Static Texts' GET method
        DESCRIPTION: - Verify body response
        EXPECTED: - All tests for current method should return **PASSED** status
        EXPECTED: - Body NOT consist values: id, brand, createdBy, updatedBy, enabled
        """
        pass
