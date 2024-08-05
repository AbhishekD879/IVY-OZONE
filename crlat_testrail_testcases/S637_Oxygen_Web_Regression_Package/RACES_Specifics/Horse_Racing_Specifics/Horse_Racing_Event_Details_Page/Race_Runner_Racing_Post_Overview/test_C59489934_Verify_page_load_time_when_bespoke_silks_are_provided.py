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
class Test_C59489934_Verify_page_load_time_when_bespoke_silks_are_provided(Common):
    """
    TR_ID: C59489934
    NAME: Verify page load time when bespoke silks are provided
    DESCRIPTION: This test case verifies page load time is not impacted when bespoke silk is provided for all races(UK and International)
    DESCRIPTION: Since each generic silk is overriding with bespoke silk performance should not impact
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

    def test_002_click_on_hr_events_and_verify_page_load(self):
        """
        DESCRIPTION: Click on HR events and verify page load
        EXPECTED: Page load should not impact
        """
        pass
