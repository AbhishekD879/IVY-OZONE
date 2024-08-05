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
class Test_C59489933_Verify_display_of_Generic_silk_is_same_as_N_R(Common):
    """
    TR_ID: C59489933
    NAME: Verify display of Generic silk is same as N/R
    DESCRIPTION: This test case verifies  Generic silk should be same as non-runner silk and should match with mock screens mentioned in Zeplin
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

    def test_002_click_on_any_event_from_uk_and_ire_for_which_bespoke_silk_is_not_provided_at_least_for_one_horse(self):
        """
        DESCRIPTION: Click on any event from UK and IRE for which bespoke silk is not provided at least for one horse
        EXPECTED: All the horse in EDP should have bespoke silk
        EXPECTED: for the horse which don't have bespoke silk should display generic silk
        """
        pass

    def test_003_verify_css_of_generic_silk(self):
        """
        DESCRIPTION: Verify CSS of generic silk
        EXPECTED: TBD
        """
        pass
