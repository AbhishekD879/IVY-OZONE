import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28026_Verify_Tablet_Body_View(Common):
    """
    TR_ID: C28026
    NAME: Verify Tablet Body View
    DESCRIPTION: This test case verifies Tablet Body View
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application_on_tablet_device(self):
        """
        DESCRIPTION: Load Invictus application on Tablet device
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_tablet_bodyview_css_screen_width_in_portrait_mode1from_360_to_766px2_from_767_to_1023px3_from_1024_to_1279px4_from_1280px(self):
        """
        DESCRIPTION: Verify Tablet Body View :
        DESCRIPTION: ||#| CSS Screen Width in Portrait Mode
        DESCRIPTION: ||1|	from 360 to 766px
        DESCRIPTION: ||2| 	from 767 to 1023px
        DESCRIPTION: ||3| 	from 1024 to 1279px
        DESCRIPTION: ||4| 	from 1280px
        EXPECTED: Tablet View is displayed:
        EXPECTED: ||#|Tablet Body View
        EXPECTED: ||1| Mobile View
        EXPECTED: ||2| 2 Columns Layout (+Right Column)
        EXPECTED: ||3| 3 Columns Layout (+ Right and Left Column)
        EXPECTED: ||4| Desktop View (4 Columns and Header)
        """
        pass

    def test_003_verify_left_column_view(self):
        """
        DESCRIPTION: Verify Left Column View
        EXPECTED: Left Colum View display BMA Mobile Client
        """
        pass

    def test_004_verify_right_column_view(self):
        """
        DESCRIPTION: Verify Right Column View
        EXPECTED: Right Column Width is to 290 px
        EXPECTED: Right Column consists of next elements:
        EXPECTED: *   BetSlip widget;
        EXPECTED: *   CMS-controlled Offer Module widgets.
        """
        pass

    def test_005_rotate_device_from_portrait_to_landscape_mode_css_screen_width_in_landscape_mode1from_360_to_766px2_from_767_to_1023px3_from_1024_to_1279px4_from_1280px(self):
        """
        DESCRIPTION: Rotate device from Portrait to Landscape mode
        DESCRIPTION: ||#| CSS Screen Width in Landscape Mode
        DESCRIPTION: ||1|	from 360 to 766px
        DESCRIPTION: ||2| 	from 767 to 1023px
        DESCRIPTION: ||3| 	from 1024 to 1279px
        DESCRIPTION: ||4| 	from 1280px
        EXPECTED: Tablet body is rotated and Tablet View is displayed:
        EXPECTED: ||#|Tablet Body View
        EXPECTED: ||1| Mobile View
        EXPECTED: ||2| 2 Columns Layout (+Right Column)
        EXPECTED: ||3| 3 Columns Layout (+ Right and Left Column)
        EXPECTED: ||4| Desktop View (4 Columns and Header)
        """
        pass

    def test_006_rotate_device_from_landscape_to_portrait_mode_css_screen_width_in_portrait_mode1from_360_to_766px2_from_767_to_1023px3_from_1024_to_1279px4_from_1280px(self):
        """
        DESCRIPTION: Rotate device from Landscape to Portrait mode
        DESCRIPTION: ||#| CSS Screen Width in Portrait Mode
        DESCRIPTION: ||1|	from 360 to 766px
        DESCRIPTION: ||2| 	from 767 to 1023px
        DESCRIPTION: ||3| 	from 1024 to 1279px
        DESCRIPTION: ||4| 	from 1280px
        EXPECTED: Tablet body is rotated and Tablet View is displayed:
        EXPECTED: ||#|Tablet Body View
        EXPECTED: ||1| Mobile View
        EXPECTED: ||2| 2 Columns Layout (+Right Column)
        EXPECTED: ||3| 3 Columns Layout (+ Right and Left Column)
        EXPECTED: ||4| Desktop View (4 Columns and Header)
        """
        pass
