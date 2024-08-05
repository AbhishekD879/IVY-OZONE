import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28972_Next_Races_widget_configuration_in_CMS(Common):
    """
    TR_ID: C28972
    NAME: Next Races widget configuration in CMS
    DESCRIPTION: This test case verifies Next Races widget configuration in CMS
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-10100 Next Races Widget
    PRECONDITIONS: 1. User is logged in to CMS
    PRECONDITIONS: 2. All required Next Races widget configurations are done
    """
    keep_browser_open = True

    def test_001_go_to_cms_widgets_section(self):
        """
        DESCRIPTION: Go to CMS-Widgets section
        EXPECTED: 
        """
        pass

    def test_002_verify_next_races_widget_displaying_in_application_appropriately_to_its_order_in_cms(self):
        """
        DESCRIPTION: Verify Next Races widget displaying in application appropriately to its order in CMS
        EXPECTED: Next Races widget in application is dispayed appropriately to its order in CMS
        """
        pass

    def test_003_change_widgets_order_in_cms_and_reload_the_application(self):
        """
        DESCRIPTION: Change widgets order in CMS and reload the application
        EXPECTED: Widgets order is updated in application appropriately to the changes
        """
        pass

    def test_004_open_next_races_widget_details_dialog_in_cms(self):
        """
        DESCRIPTION: Open Next Races widget details dialog in CMS
        EXPECTED: Dialog is opened with next elements:
        EXPECTED: *   Widget name
        EXPECTED: *   Expanded/Collapsed option
        EXPECTED: *   Display on Desktop/Tablet/Mobile option
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

    def test_007_verify_widget_displaying_on_mobile(self):
        """
        DESCRIPTION: Verify widget displaying on Mobile
        EXPECTED: Next Races widget is NOT displayed on Mobile
        """
        pass
