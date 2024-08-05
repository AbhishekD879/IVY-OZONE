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
class Test_C57732144_Verify_BE_APIs_for_Teem_Kits(Common):
    """
    TR_ID: C57732144
    NAME: Verify BE APIs for Teem Kits
    DESCRIPTION: This test case verifies BE APIs for Teem Kits using Postman collection
    PRECONDITIONS: CMS API specification (coral/admin):
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com
    PRECONDITIONS: 1. Actual version of Collection and Environment imported to Postman: https://confluence.egalacoral.com/display/SPI/OTF+API+Test+Cases+-+Postman
    PRECONDITIONS: 2. Select actual testing Environment by changing {{env}} variable to: dev0, dev1, dev2 and {{brand}} variable to: ladbrokes, bma
    PRECONDITIONS: 3. Login using 'CMS Login' POST method from 1-2-Free collection
    PRECONDITIONS: 4. Teem Kits exist before testing
    """
    keep_browser_open = True

    def test_001___open_postman_collection_runner_and_choose_folder_1_2_free__teem_kits__select_imported_environment_1_2_free__run_testing_by_clicking_or_run_game_button(self):
        """
        DESCRIPTION: - Open Postman Collection Runner and choose folder: '1-2-Free > Teem Kits'
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

    def test_002___open_upload_new_svg_image_for_teamkit_put_method__add_attached_romasvg_file_as_body_key___file_romasvg__run_method__verify_body_response(self):
        """
        DESCRIPTION: - Open 'Upload new SVG image for TeamKit' PUT method
        DESCRIPTION: - Add attached 'Roma.svg' file as Body KEY - file: Roma.svg
        DESCRIPTION: - Run method
        DESCRIPTION: - Verify body response
        EXPECTED: - All tests for current method should return **PASSED** status
        EXPECTED: - Body consist 'teamKitIcon' value with selected kit file path 'Roma.svg'
        EXPECTED: - Teem Kit displayed on CMS and OTF
        """
        pass

    def test_003___run_delete_svg_image_for_team_kit_det_method__verify_body_response(self):
        """
        DESCRIPTION: - Run 'Delete SVG image for Team Kit' DET method
        DESCRIPTION: - Verify body response
        EXPECTED: - All tests for current method should return **PASSED** status
        EXPECTED: - Body 'teamKitIcon' value = null
        EXPECTED: - Teem Kit NOT displayed on CMS and default team kit displayed on OTF
        """
        pass
