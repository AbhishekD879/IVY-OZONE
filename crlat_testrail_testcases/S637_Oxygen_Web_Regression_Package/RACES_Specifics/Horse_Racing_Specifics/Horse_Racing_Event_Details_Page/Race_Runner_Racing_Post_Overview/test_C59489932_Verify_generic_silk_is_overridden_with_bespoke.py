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
class Test_C59489932_Verify_generic_silk_is_overridden_with_bespoke(Common):
    """
    TR_ID: C59489932
    NAME: Verify generic silk is overridden with bespoke
    DESCRIPTION: This test case verifies generic silk is overridden with bespoke silk when bespoke silk is provided for all races(UK and International)
    PRECONDITIONS: 1.Generic silk should display for all the horses by default
    PRECONDITIONS: If bespoke silk present it should display otherwise generic silk should present
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

    def test_004_to_confirm_above_step_right_click_on_any_bespoke_silk_and_inspect_and_copy_complete_url_and_make_notechange_image_id_with_dummy_id_and_see_in_febackground_image_urlhttpsaggregationladbrokescomsilksracingpostxxxx(self):
        """
        DESCRIPTION: To confirm above step right click on any bespoke silk and inspect and copy complete URL and make note
        DESCRIPTION: change image id with dummy id and see in FE
        DESCRIPTION: background-image: url("https://aggregation.ladbrokes.com/silks/racingpost/xxxx
        EXPECTED: In FE generic silk should be displayed
        """
        pass

    def test_005_again_inspect_and_paste_the_url_which_is_copied_from_above_step(self):
        """
        DESCRIPTION: Again inspect and paste the URL which is copied from above step
        EXPECTED: Bespoke silk should display
        """
        pass
