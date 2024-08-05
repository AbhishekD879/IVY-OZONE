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
class Test_C60004610_Verify_New_Label_disabled_CMS__Market_Description(Common):
    """
    TR_ID: C60004610
    NAME: Verify New Label disabled CMS - Market Description
    DESCRIPTION: This test case verifies toggle option for "New" label if market  descripton table is blank
    PRECONDITIONS: 1. Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market Description should be enabled in CMS
    PRECONDITIONS: 4: Market description table should have description blank
    PRECONDITIONS: 5: New Label should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_003_click_on_any_race_which_has_the_market_template_available_for_which_description_is_added_and_new_label_is_configured_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market template available for which description is added and New label is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_004_validate_the_description_and_new_label_displayed(self):
        """
        DESCRIPTION: Validate the description and New Label displayed
        EXPECTED: New Label should not be displayed as the description is blank
        """
        pass

    def test_005_navigate_to_grey_hound_racing_and_repeat_5__6_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hound racing and repeat 5 & 6 steps
        EXPECTED: 
        """
        pass
