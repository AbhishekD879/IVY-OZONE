import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1473946_Verify_Group_Widget_Module_displaying(Common):
    """
    TR_ID: C1473946
    NAME: Verify Group Widget Module displaying
    DESCRIPTION: This test case verifies Group Widget Module displaying
    PRECONDITIONS: * Have Big Competition created in CMS.
    PRECONDITIONS: * Have groups widget configured and enabled in CMS.
    """
    keep_browser_open = True

    def test_001_load_oxygen_page(self):
        """
        DESCRIPTION: Load Oxygen page
        EXPECTED: Oxygen page is loaded
        """
        pass

    def test_002_navigate_to_competition(self):
        """
        DESCRIPTION: Navigate to Competition
        EXPECTED: Competition landing page is loaded
        """
        pass

    def test_003_scroll_down_until_find_groups_widget_module(self):
        """
        DESCRIPTION: Scroll down until find Groups Widget module
        EXPECTED: Groups Widget module is present with scrollable carousel containing a table of each group
        """
        pass

    def test_004_scroll_to_right_and_left_over_groups_table_widget(self):
        """
        DESCRIPTION: Scroll to right and left over Groups table widget
        EXPECTED: Groups table widget acts as a carousel according to user action
        """
        pass

    def test_005_verify_groups_table_widget_layout(self):
        """
        DESCRIPTION: Verify Groups table widget layout
        EXPECTED: Groups table widget consists of the next info for each Group:
        EXPECTED: * Group name and '+' sign button
        EXPECTED: * Country position
        EXPECTED: * Country flag and abbreviation
        EXPECTED: * Total points value and 'pt' label
        """
        pass

    def test_006_verify_country_position(self):
        """
        DESCRIPTION: Verify country position
        EXPECTED: Selected country position determines qualified teams within one Group (colored in dark blue)
        """
        pass

    def test_007_tap_on_a_plus_sign_button(self):
        """
        DESCRIPTION: Tap on a '+' sign button
        EXPECTED: User is directed to respective group sub-tab
        """
        pass
