import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29364_LIVE_Stream_Widget_widget_configuration_in_CMS_N_A_Live_stream_under_betslip_is_not_using_anymore(Common):
    """
    TR_ID: C29364
    NAME: LIVE Stream Widget widget configuration in CMS [N/A Live stream under betslip is not using anymore]
    DESCRIPTION: This test case verifies CMS control of Live Stream widget
    DESCRIPTION: Jira tickets:
    DESCRIPTION: BMA-10099 LIVE Stream Widget
    DESCRIPTION: BMA-10102 CMS New widget section
    PRECONDITIONS: 1. User is logged in to CMS
    """
    keep_browser_open = True

    def test_001_go_to_cms_widgets_section(self):
        """
        DESCRIPTION: Go to CMS-Widgets section
        EXPECTED: 
        """
        pass

    def test_002_verify_live_stream_widget_displaying_in_application_appropriately_to_its_order_in_cms(self):
        """
        DESCRIPTION: Verify LIVE Stream Widget displaying in application appropriately to its order in CMS
        EXPECTED: LIVE Stream Widget in application is displayed appropriately to drag and drop order in CMS
        """
        pass

    def test_003_change_widgets_order_in_cms_and_reload_the_application(self):
        """
        DESCRIPTION: Change widgets order in CMS and reload the application
        EXPECTED: Widgets order is updated in application appropriately to the changes
        """
        pass

    def test_004_open_live_stream_widget_details_dialog_in_cms(self):
        """
        DESCRIPTION: Open LIVE Stream Widget details dialog in CMS
        EXPECTED: Dialog is opened with next elements:
        EXPECTED: *   Widget name
        EXPECTED: *   Expanded/Collapsed option
        EXPECTED: *   Display on Desktop/Tablet option
        EXPECTED: *   Inactive checkbox
        """
        pass

    def test_005_verify_widget_displaying_in_application_according_to_expandedcollapsed_option_settled_in_cms(self):
        """
        DESCRIPTION: Verify widget displaying in application according to Expanded/Collapsed option settled in CMS
        EXPECTED: *   Widget is expanded when Expanded option is selected in CMS
        EXPECTED: *   Widget is collapsed when Collapsed option is selected in CMS
        """
        pass

    def test_006_verify_widget_displaying_in_application_according_to_display_on_desktoptablet_option_settled_in_cms(self):
        """
        DESCRIPTION: Verify widget displaying in application according to Display on Desktop/Tablet option settled in CMS
        EXPECTED: *   widget is displayed on desktop if Desktop checkbox is selected in CMS
        EXPECTED: *   widget is displayed on tablet if Tablet checkbox is selected in CMS
        """
        pass

    def test_007_select_inactive_checkbox_and_check_that_widget_is_not_displayed_in_application_after_saving_the_changes(self):
        """
        DESCRIPTION: Select 'Inactive' checkbox and check that widget is not displayed in application after saving the changes
        EXPECTED: *   Widget is not displayed when inactive checkbox is selected in CMS
        EXPECTED: *   Widget is displayed when inactive checkbox is not selected in CMS
        """
        pass

    def test_008_verify_widget_displaying_on_mobile(self):
        """
        DESCRIPTION: Verify widget displaying on Mobile
        EXPECTED: Offer widget is NOT displayed on Mobile
        """
        pass
