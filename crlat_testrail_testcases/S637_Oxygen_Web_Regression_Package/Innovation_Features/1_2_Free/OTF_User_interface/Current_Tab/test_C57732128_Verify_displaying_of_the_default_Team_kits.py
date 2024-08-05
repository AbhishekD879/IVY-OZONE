import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732128_Verify_displaying_of_the_default_Team_kits(Common):
    """
    TR_ID: C57732128
    NAME: Verify displaying of the default Team kits
    DESCRIPTION: This test case verifies default icon displaying of Team Kit icon when it isn't retrieved from CMS
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: to check image use following:{CMS env/akamai}/images/uploads/teamKit/croatia.svg
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. Current Game is configured in CMS
    PRECONDITIONS: 3. Do not Add Team Kits to the events in the Current Game
    """
    keep_browser_open = True

    def test_001_open_current_tab_on_otf_ui(self):
        """
        DESCRIPTION: Open Current Tab on OTF UI
        EXPECTED: Team Kits image should be displayed for all events
        """
        pass

    def test_002_verify_that_default_greyed_image_is_shown_when_it_is_not_configured_in_cmsnetwork__gamegamestateactive___on_the_event_level___home_team__see_teamkiticon_parameter__no_value_should_be_set(self):
        """
        DESCRIPTION: Verify that default (greyed) image is shown when it is not configured in CMS:
        DESCRIPTION: Network-> game?gameState=Active -> on the event level -> home team-> see **teamKitIcon** parameter-> no value should be set
        EXPECTED: Default image should shown on FE
        EXPECTED: ![](index.php?/attachments/get/27572)
        """
        pass
