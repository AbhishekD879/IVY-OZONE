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
class Test_C28032_Verify_Right_Column(Common):
    """
    TR_ID: C28032
    NAME: Verify Right Column
    DESCRIPTION: This test case verifies Right Column
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-7842 RIGHT COLUMN: Implementing Rightcolumn widget
    DESCRIPTION: *   BMA-36921 TABLET - Betslip - Header and Sub header
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_app_on_tablet_device(self):
        """
        DESCRIPTION: Load Invictus app on tablet device
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_right_column_presence(self):
        """
        DESCRIPTION: Verify Right Column presence
        EXPECTED: Right Column is applicable to all sportsbook pages
        """
        pass

    def test_003_verify_right_column_content(self):
        """
        DESCRIPTION: Verify Right Column content
        EXPECTED: Right Column consists of next elements:
        EXPECTED: *   BetSlip widget;
        EXPECTED: *   CMS-controlled Offer Module widgets.
        """
        pass

    def test_004_verify_fixed_width_of_each_widget(self):
        """
        DESCRIPTION: Verify fixed width of each widget
        EXPECTED: Width for each widgets is 320 px
        """
        pass

    def test_005_rotate_device(self):
        """
        DESCRIPTION: Rotate device
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps__2_4(self):
        """
        DESCRIPTION: Repeat steps # 2-4
        EXPECTED: 
        """
        pass
