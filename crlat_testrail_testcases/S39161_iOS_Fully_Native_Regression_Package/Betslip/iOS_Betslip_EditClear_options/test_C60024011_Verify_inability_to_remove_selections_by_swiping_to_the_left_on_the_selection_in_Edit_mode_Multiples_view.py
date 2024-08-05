import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C60024011_Verify_inability_to_remove_selections_by_swiping_to_the_left_on_the_selection_in_Edit_mode_Multiples_view(Common):
    """
    TR_ID: C60024011
    NAME: Verify inability to  remove selections by swiping to the left on the selection in 'Edit' mode (Multiples view)
    DESCRIPTION: Test case verifies inability to remove selections from bet slip in 'Edit mode' by swiping to the left on selection (Multiples view)
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Sports book home page is opened
    PRECONDITIONS: User has added 2 or more selections to bet slip (e.g.: 5 selections)
    PRECONDITIONS: Bet slip expanded
    PRECONDITIONS: "Edit" and "Remove All / Clear" buttons are displayed in the left top of bet slip
    PRECONDITIONS: Coral / Ladbrokes designs :
    PRECONDITIONS: ![](index.php?/attachments/get/121107913) ![](index.php?/attachments/get/121107914)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Coral - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2ae62b7f82157bc985bf3
    PRECONDITIONS: Ladbrokes - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea989678beef8bc2366aa76
    """
    keep_browser_open = True

    def test_001__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * bet slip expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107981) ![](index.php?/attachments/get/121107982)
        """
        pass

    def test_002__swipe_to_the_left_on_any_selection_to_display_remove_button(self):
        """
        DESCRIPTION: * Swipe to the left on any selection to display "Remove" button
        EXPECTED: * no ability to swipe to the left
        EXPECTED: * "Remove" button is not display
        EXPECTED: * bet slip remains expanded
        EXPECTED: * bet slip in "Edit" mode with ability to update selections with a 'X' option next to each selection
        """
        pass

    def test_003__tap_on_done_button(self):
        """
        DESCRIPTION: * Tap on 'Done' button
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip "Edit" mode disabled
        EXPECTED: * no ability to update selections with a 'X' option next to each selection
        EXPECTED: * selection wasn't deleted from bet slip
        """
        pass

    def test_004__swipe_to_the_left_on_any_selection_to_display_remove_button(self):
        """
        DESCRIPTION: * Swipe to the left on any selection to display "Remove" button
        EXPECTED: * "Remove" button is  display
        EXPECTED: * bet slip remains expanded
        EXPECTED: * bet slip "Edit" mode disabled
        EXPECTED: * no ability to update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107997) ![](index.php?/attachments/get/121107998)
        """
        pass

    def test_005__swipe_to_the_right_on_selected_selection_to_close_remove_button(self):
        """
        DESCRIPTION: * Swipe to the right on selected selection to close "Remove" button
        EXPECTED: * selection wasn't removed from bet slip view
        EXPECTED: * bet slip remains expanded
        EXPECTED: * no ability to update selections with a 'X' option next to each selection
        """
        pass

    def test_006__swipe_to_the_left_on_any_selection_to_display_remove_button(self):
        """
        DESCRIPTION: * Swipe to the left on any selection to display "Remove" button
        EXPECTED: * "Remove" button is  display
        EXPECTED: * bet slip remains expanded
        EXPECTED: * bet slip "Edit" mode disabled
        EXPECTED: * no ability to update selections with a 'X' option next to each selection
        """
        pass

    def test_007__tap_remove_button_to_delete_selection(self):
        """
        DESCRIPTION: * Tap Remove" button to delete selection
        EXPECTED: * selection was deleted
        EXPECTED: * bet slip remains expanded
        EXPECTED: * bet slip "Edit" mode disabled
        EXPECTED: * no ability to update selections with a 'X' option next to each selection
        """
        pass

    def test_008__enable_dark_theme_on_tested_device_settings___display__brightness___select_dark_theme(self):
        """
        DESCRIPTION: * Enable Dark Theme on tested device (Settings -> Display & Brightness -> Select "Dark" theme)
        EXPECTED: * Dark Theme enabled on tested device
        """
        pass

    def test_009__repeat_steps_1_7_verify_that_app_in_dark_mode_conforms_to_coral__ladbrokes_dark_theme_designs(self):
        """
        DESCRIPTION: * Repeat steps 1-7
        DESCRIPTION: * Verify that app in Dark mode conforms to Coral / Ladbrokes Dark theme designs
        EXPECTED: * Results from steps 1-7
        EXPECTED: * App with enabled Dark theme conforms to Coral / Ladbrokes Dark theme designs
        EXPECTED: ![](index.php?/attachments/get/121108000) ![](index.php?/attachments/get/121108001)
        """
        pass
