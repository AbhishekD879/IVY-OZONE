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
class Test_C57731996_QubitVerify_the_configuration_of_1_2_Free_iOS_App_toggle(Common):
    """
    TR_ID: C57731996
    NAME: [Qubit]Verify the configuration of 1-2-Free iOS App toggle
    DESCRIPTION: This test case verifies the configuration of 1-2-Free iOS App toggle
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The user is logged in to Qubit
    PRECONDITIONS: 3. User open app.qubit.com > Dashboard > Experiences > Draft
    PRECONDITIONS: 4. User select '1-2-Free'
    PRECONDITIONS: 5. User open `Publish Experience` edit mode to configure CMS fields
    PRECONDITIONS: USE IOS NATIVE APPLICATION
    """
    keep_browser_open = True

    def test_001_open_ios_app_section_on_qubit_cms(self):
        """
        DESCRIPTION: Open iOS app section on Qubit CMS
        EXPECTED: Fields successfully displayed with fields:
        EXPECTED: - iOS app OFF text
        EXPECTED: - iOS app URL
        EXPECTED: - iOS app URL text
        EXPECTED: - iOS app CTA text
        """
        pass

    def test_002_turn_on_ios_app_off_by_click_on_the_checkboxpopulate_other_fields_for_ios_app_section_with_valid_datasave_changes(self):
        """
        DESCRIPTION: Turn On 'iOS app OFF' by click on the checkbox
        DESCRIPTION: Populate other fields for iOS app section with valid data
        DESCRIPTION: Save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_003_tap_on_the_quick_link_play_1_2_free_on_homepage_or_football_sports_page(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on Homepage or Football sports page
        EXPECTED: Pop-up successfully displayed with elements:
        EXPECTED: - Text
        EXPECTED: "To play 1-2-Free on this device, please visit ladbrokes.com"
        EXPECTED: (retrieved from Qubit 'iOS app OFF text')
        EXPECTED: - Button to close
        EXPECTED: - Button to open the web version of 1-2-Free
        """
        pass

    def test_004_turn_off_ios_app_off_by_click_on_the_checkboxsave_changes(self):
        """
        DESCRIPTION: Turn Off 'iOS app OFF' by click on the checkbox
        DESCRIPTION: Save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_005_tap_on_the_quick_link_play_1_2_free_on_homepage_or_football_sports_page(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on Homepage or Football sports page
        EXPECTED: 1-2-Free successfully opened
        """
        pass
