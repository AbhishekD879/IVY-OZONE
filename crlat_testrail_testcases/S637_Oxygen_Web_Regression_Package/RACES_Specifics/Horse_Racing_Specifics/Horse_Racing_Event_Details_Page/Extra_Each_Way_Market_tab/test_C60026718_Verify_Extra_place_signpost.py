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
class Test_C60026718_Verify_Extra_place_signpost(Common):
    """
    TR_ID: C60026718
    NAME: Verify Extra place signpost
    DESCRIPTION: Verify that Extra place signpost is displayed when "EXTRA EACH WAY" market is also available and displayed.
    PRECONDITIONS: 1: Horse racing event should be available.
    PRECONDITIONS: 2: "EXTRA EACH WAY" market should be available for the event.
    PRECONDITIONS: 3: Extra place should be configured for the event in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_perform_login(self):
        """
        DESCRIPTION: Perform Login
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_003_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_004_click_on_any_uk_and_ireland_race_which_has_extra_each_way_market___extra_place_available(self):
        """
        DESCRIPTION: Click on any UK and Ireland race which has "EXTRA EACH WAY" market  & Extra place available
        EXPECTED: User should be navigated to Event details page.
        """
        pass

    def test_005_validate_extra_each_way_market(self):
        """
        DESCRIPTION: Validate "EXTRA EACH WAY" market
        EXPECTED: 1: User should be displayed "EXTRA EACH WAY"
        EXPECTED: 2: Selections should be displayed
        """
        pass

    def test_006_validate_extra_place_signpost(self):
        """
        DESCRIPTION: Validate Extra place signpost
        EXPECTED: User should be able to see Extra place signpost for the event.
        """
        pass
