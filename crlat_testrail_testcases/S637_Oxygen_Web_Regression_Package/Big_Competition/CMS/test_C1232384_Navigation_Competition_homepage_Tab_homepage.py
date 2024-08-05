import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1232384_Navigation_Competition_homepage_Tab_homepage(Common):
    """
    TR_ID: C1232384
    NAME: Navigation Competition homepage <> Tab homepage
    DESCRIPTION: This test case verifies navigation new Competition homepage <> new Tab homepage
    PRECONDITIONS: Have at least one big competition with at least one main tab, sub-tab and module already created.
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_big_competition_section(self):
        """
        DESCRIPTION: Go to Big Competition section
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_tap_on_a_competition_previously_created(self):
        """
        DESCRIPTION: Tap on a Competition previously created
        EXPECTED: Competition homepage is loaded.
        EXPECTED: Tabs created in preconditions are present
        EXPECTED: Navigation tree is displayed at the top of tab homepage composed by:
        EXPECTED: * 'Competition homepage' > 'Competition' name
        """
        pass

    def test_004_proceed_with_some_changes_for_instanceuntick_activedisabled_checkbox(self):
        """
        DESCRIPTION: Proceed with some changes, for instance:
        DESCRIPTION: Untick Active/Disabled 'Checkbox'
        EXPECTED: 
        """
        pass

    def test_005_tap_on_competition_homepage(self):
        """
        DESCRIPTION: Tap on 'Competition homepage'
        EXPECTED: A popup window appears with:
        EXPECTED: * Message: 'Your changes are not saved. Exit page without saving?'
        EXPECTED: CTA buttons: 'Yes' and 'No
        """
        pass

    def test_006_tap_no_cta(self):
        """
        DESCRIPTION: Tap 'No' CTA
        EXPECTED: User stays on 'Edit Big Competition' page.
        """
        pass

    def test_007_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps #4-6
        EXPECTED: 
        """
        pass

    def test_008_tap_yes_cta(self):
        """
        DESCRIPTION: Tap 'Yes' CTA
        EXPECTED: Changes are not saved.
        EXPECTED: User is redirected to Competitions homepage.
        """
        pass

    def test_009_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_010_tap_save_changes_button(self):
        """
        DESCRIPTION: Tap 'Save Changes' button
        EXPECTED: A popup window appears with:
        EXPECTED: * Message: 'Are you sure you want to save this: (competition name)?'
        EXPECTED: CTA buttons: 'Yes' and 'No
        """
        pass

    def test_011_tap_yes_and_then_ok_buttons(self):
        """
        DESCRIPTION: Tap 'Yes' and then 'Ok' buttons
        EXPECTED: Changes are saved.
        """
        pass

    def test_012_tap_on_competition_homepage(self):
        """
        DESCRIPTION: Tap on 'Competition homepage'
        EXPECTED: * User is redirected to'Competition homepage'
        EXPECTED: * No pop-up should be displayed
        """
        pass

    def test_013_repeat_steps_3_12_for_competition_tabs_sub_tabs_and_modules(self):
        """
        DESCRIPTION: Repeat steps 3-12 for Competition tabs, sub-tabs and modules
        EXPECTED: Behavior should be the same
        """
        pass
