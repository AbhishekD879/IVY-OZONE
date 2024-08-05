import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1108266_Verify_date_and_time_format_on_Virtual_Sports(Common):
    """
    TR_ID: C1108266
    NAME: Verify date and time format on Virtual Sports
    DESCRIPTION: This test case verifies date and time format on Virtual Sports
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_click_virtual_sports_in_sport_ribbon(self):
        """
        DESCRIPTION: Click Virtual Sports in Sport ribbon
        EXPECTED: Virtual Sports page opens with first Sport in the ribbon selected by default
        """
        pass

    def test_003_select_any_sport_event_and_verify_date_and_time_format_in_event_header(self):
        """
        DESCRIPTION: Select any Sport event and verify date and time format in Event header
        EXPECTED: Date and time should be in format %yyyy-mm-dd hh:mm%
        """
        pass

    def test_004_wait_untill_event_starts_and_verify_date_and_time(self):
        """
        DESCRIPTION: Wait untill event starts and verify date and time
        EXPECTED: 'LIVE' displayed instead of time: %yyyy-mm-dd LIVE%
        """
        pass
