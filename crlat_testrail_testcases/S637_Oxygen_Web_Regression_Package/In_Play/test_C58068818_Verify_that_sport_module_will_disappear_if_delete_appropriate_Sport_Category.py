import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C58068818_Verify_that_sport_module_will_disappear_if_delete_appropriate_Sport_Category(Common):
    """
    TR_ID: C58068818
    NAME: Verify that sport module will disappear if delete appropriate "Sport Category"
    DESCRIPTION: This test case verifies that sport module will disappear from In Play Tab if delete appropriate "Sport Category"
    PRECONDITIONS: - CMS endpoints https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - CMS creds https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Sport' module is activated and visible for "In Play" in CMS -> Sport Pages -> Sport Categories
    """
    keep_browser_open = True

    def test_001__in_app___sports_carousel___in_play_verify_if_sport_module_is_available(self):
        """
        DESCRIPTION: * In App -> Sports Carousel -> In-Play
        DESCRIPTION: * Verify if 'Sport' module is available
        EXPECTED: 'Sport' module is available
        """
        pass

    def test_002__go_to_cms___sport_pages___sport_category_delete_current_sport(self):
        """
        DESCRIPTION: * Go to CMS -> Sport Pages -> Sport Category
        DESCRIPTION: * Delete current 'Sport'
        EXPECTED: 'Sport' is deleted from 'Sport Category'
        """
        pass

    def test_003__in_app_verify_if_current_module_is_available_verify_ws_response(self):
        """
        DESCRIPTION: * In App: verify if current module is available
        DESCRIPTION: * Verify WS response
        EXPECTED: * Current sport module is Not available
        EXPECTED: * IN_PLAY_SPORT_COMPETITION_CHANGED
        EXPECTED: removed:[sport_type_id]
        """
        pass

    def test_004_repeat_steps_1_3_for_coral(self):
        """
        DESCRIPTION: Repeat steps 1-3 for coral
        EXPECTED: 
        """
        pass
