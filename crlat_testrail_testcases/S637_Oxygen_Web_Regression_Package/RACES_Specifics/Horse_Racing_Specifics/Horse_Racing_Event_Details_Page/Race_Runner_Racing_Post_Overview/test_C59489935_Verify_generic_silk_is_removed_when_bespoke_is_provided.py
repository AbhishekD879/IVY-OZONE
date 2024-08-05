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
class Test_C59489935_Verify_generic_silk_is_removed_when_bespoke_is_provided(Common):
    """
    TR_ID: C59489935
    NAME: Verify generic silk is removed when bespoke is provided
    DESCRIPTION: This test case verifies generic silk is removed when bespoke silk is provided for all races(UK and International)
    PRECONDITIONS: 1.Generic silk should display for all the horses by default
    PRECONDITIONS: If bespoke silk present it should display, otherwise generic silk should present
    """
    keep_browser_open = True

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        pass

    def test_002_verify_generic_silk_is_showing_while_page_load(self):
        """
        DESCRIPTION: Verify generic silk is showing while page load
        EXPECTED: While page load generic silk should display
        """
        pass

    def test_003_verify_if_bespoke_silk_present_it_should_display_otherwise_generic_silk_should_present(self):
        """
        DESCRIPTION: Verify If bespoke silk present it should display otherwise generic silk should present
        EXPECTED: 
        """
        pass

    def test_004_verify_generic_silk_is_not_shown_when_bespoke_is_displayed(self):
        """
        DESCRIPTION: Verify generic silk is not shown when bespoke is displayed
        EXPECTED: Since on page load we are showing generic silk and overriding with bespoke silk it should not display again
        EXPECTED: ![](index.php?/attachments/get/115417132)
        """
        pass
