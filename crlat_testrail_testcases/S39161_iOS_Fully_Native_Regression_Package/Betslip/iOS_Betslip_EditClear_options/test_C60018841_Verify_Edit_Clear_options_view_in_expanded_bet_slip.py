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
class Test_C60018841_Verify_Edit_Clear_options_view_in_expanded_bet_slip(Common):
    """
    TR_ID: C60018841
    NAME: Verify Edit/Clear options view in expanded bet slip
    DESCRIPTION: Test case verifies  view of Edit/Clear options in expanded bet slip
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Sports book home page is opened
    PRECONDITIONS: User has added 2 or more selections to bet slip (e.g.: 5 selections)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Coral - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2ae62b7f82157bc985bf3
    PRECONDITIONS: Ladbrokes - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea989678beef8bc2366aa76
    """
    keep_browser_open = True

    def test_001__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * bet slip expanded
        EXPECTED: *  "Edit" and "Remove All / Clear" buttons are displayed in the left top of bet slip
        EXPECTED: Coral / Ladbrokes designs :
        EXPECTED: ![](index.php?/attachments/get/121107913) ![](index.php?/attachments/get/121107914)
        """
        pass

    def test_002__user_taps_on_remove_all__clear_option__in_expanded_bet_slip(self):
        """
        DESCRIPTION: * User taps on "Remove All / Clear option"  in expanded bet slip
        EXPECTED: *  "Remove all?" popup with options to Confirm or Cancel appears
        EXPECTED: Coral / Ladbrokes designs :
        EXPECTED: ![](index.php?/attachments/get/121107915) ![](index.php?/attachments/get/121107916)
        """
        pass

    def test_003__user_taps_on_cancel__button_on_the_popup(self):
        """
        DESCRIPTION: * User taps on "Cancel"  button on the popup
        EXPECTED: * "Remove all?" popup disappears
        EXPECTED: * bet slip remains expanded
        EXPECTED: * amount of selections in bet slip remains the same
        """
        pass

    def test_004__user_taps_on_remove_all__clear_option__in_expanded_bet_slip(self):
        """
        DESCRIPTION: * User taps on "Remove All / Clear option"  in expanded bet slip
        EXPECTED: *  "Remove all?" popup with options to Confirm or Cancel appears
        """
        pass

    def test_005__user_taps_away_from_the_remove_all_popup(self):
        """
        DESCRIPTION: * User taps away from the "Remove all?" popup
        EXPECTED: * "Remove all?" popup disappears
        EXPECTED: * bet slip remains expanded
        EXPECTED: * amount of selections in bet slip remains the same
        """
        pass

    def test_006__user_taps_on_remove_all__clear_option__in_expanded_bet_slip(self):
        """
        DESCRIPTION: * User taps on "Remove All / Clear option"  in expanded bet slip
        EXPECTED: *  "Remove all?" popup with options to Confirm or Cancel appears
        """
        pass

    def test_007__user_clicks_on_remove_button_on_the_remove_all_popup(self):
        """
        DESCRIPTION: * User clicks on "Remove" button on the "Remove all?" popup
        EXPECTED: * All selections in bet slip were removed
        EXPECTED: * bet slip empty and closed
        """
        pass

    def test_008__user_added_2_or_more_selections_to_bet_slip_eg_5_selections(self):
        """
        DESCRIPTION: * User added 2 or more selections to bet slip (e.g.: 5 selections)
        EXPECTED: * Selections were added to bet slip (e.g.: 5 selections)
        EXPECTED: * bet slip collapsed
        """
        pass

    def test_009__enable_dark_theme_on_tested_devicesettings___display__brightness___select_dark_theme(self):
        """
        DESCRIPTION: * Enable Dark Theme on tested device
        DESCRIPTION: (Settings -> Display & Brightness -> Select "Dark" theme)
        EXPECTED: * Dark Theme enabled on tested device
        """
        pass

    def test_010__repeat_steps_1_7_verify_that_app_in_dark_mode_conforms_to_coral__ladbrokes_dark_theme_designs(self):
        """
        DESCRIPTION: * Repeat steps 1-7
        DESCRIPTION: * Verify that app in Dark mode conforms to Coral / Ladbrokes Dark theme designs
        EXPECTED: * Results from steps 1-7
        EXPECTED: * App with enabled Dark theme  conforms  to Coral / Ladbrokes Dark theme designs
        EXPECTED: **(Expanded bet slip)** Coral / Ladbrokes designs :
        EXPECTED: ![](index.php?/attachments/get/121107918) ![](index.php?/attachments/get/121107919)
        EXPECTED: **("Remove all?" popup)** Coral / Ladbrokes designs :
        EXPECTED: ![](index.php?/attachments/get/121107920) ![](index.php?/attachments/get/121107921)
        """
        pass
