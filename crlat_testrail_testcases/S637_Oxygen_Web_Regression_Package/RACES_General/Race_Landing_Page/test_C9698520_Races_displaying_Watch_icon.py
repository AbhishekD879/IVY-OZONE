import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9698520_Races_displaying_Watch_icon(Common):
    """
    TR_ID: C9698520
    NAME: <Races>: displaying 'Watch' icon
    DESCRIPTION: This test case verifies displaying of 'Watch' icons on Horse Racing and Greyhounds landing pages
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 <Race> events within one sub region configured on different dates:
    PRECONDITIONS: 1) With enabled streaming (for example 'At the Races stream available' check box which corresponds to the drilldownTagNames="EVFLAG_AVA" in TI)
    PRECONDITIONS: 2) With disabled streaming
    PRECONDITIONS: - You should be on <Race> landing page with opened switcher on event with enabled streaming
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_watch_icon(self):
        """
        DESCRIPTION: Verify displaying of 'Watch' icon
        EXPECTED: 'Watch' icon is displayed against the race type name
        """
        pass

    def test_002___open_the_day_switcher_with_event_with_disabled_streaming__verify_displaying_of_watch_icon(self):
        """
        DESCRIPTION: - Open the day switcher with event with disabled streaming
        DESCRIPTION: - Verify displaying of 'Watch' icon
        EXPECTED: 'Watch' icon is NOT displayed against the race type name
        """
        pass
