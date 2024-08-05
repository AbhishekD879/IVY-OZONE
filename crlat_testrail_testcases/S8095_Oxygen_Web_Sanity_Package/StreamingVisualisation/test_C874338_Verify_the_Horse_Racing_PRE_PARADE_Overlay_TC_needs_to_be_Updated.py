import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C874338_Verify_the_Horse_Racing_PRE_PARADE_Overlay_TC_needs_to_be_Updated(Common):
    """
    TR_ID: C874338
    NAME: Verify the Horse Racing 'PRE-PARADE' Overlay [ TC needs to be Updated]
    DESCRIPTION: Video Streaming - Verify that the customer can see the 'PRE-PARADE' (Quantum Leap) Visualization for Horse Racing events
    DESCRIPTION: **This TC needs to be updated as per OX 108 change**
    PRECONDITIONS: Horse Racing event:
    PRECONDITIONS: - which is about to start
    PRECONDITIONS: - is from a Type that has "QL Streaming available" flag ticked
    PRECONDITIONS: - is from a Type that has "Is in UK" or "Is Irish" flag ticked
    PRECONDITIONS: - if perform stream is mapped to event, then 'CSBIframeSportIds' should be disabled in CMS>System Config>Structure>performGroup
    PRECONDITIONS: - Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: All in all, this is the condition when 'LIVESIM' button is shown:
    PRECONDITIONS: ngIf="sportName !== 'greyhound' && eventEntity.isUKorIRE && !shouldShowCSBIframe"
    PRECONDITIONS: **NOTE:** 'Find out more about Watch free here' hyperlink was removed for Ladbrokes (BMA-44862)
    """
    keep_browser_open = True

    def test_001_go_to_a_hr_event_from_uk__ire_group_more_than_15_minutes_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Go to a HR event (from 'UK & IRE' group) **more than 15 minutes** before the scheduled race-off time
        EXPECTED: For Mobile/Tablet:
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of ' PRE-PARADE' and 'LIVE STREAM'/'WATCH' buttons and not auto-expanded
        EXPECTED: For Desktop:
        EXPECTED: * Event details page is opened
        EXPECTED: * Media area consists of ' PRE-PARADE' and 'LIVE STREAM'/'WATCH' buttons
        EXPECTED: * The Button 'PRE-PARADE' button is inActive by default and not auto-expanded
        EXPECTED: * Relevant icon is NOT shown next to the ' PRE-PARADE' label
        """
        pass

    def test_002_refresh_the_page_when_theres_more_than_5_minutes_left_before_the_scheduled_race_off_time(self):
        """
        DESCRIPTION: Refresh the page when there's **more than 5 minutes** left before the scheduled race-off time
        EXPECTED: * The area below 'PRE-PARADE' button is collapsed
        EXPECTED: * 'PRE-PARADE' button is inActive
        """
        pass

    def test_003_clicktap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' button
        EXPECTED: * The area below 'PRE-PARADE' button is expanded
        EXPECTED: * Content of Quantum Leap iFrame is shown
        EXPECTED: * Visualisation is shown for logged out user
        EXPECTED: * An information link labeled "Find out more about Watch Free here" appears under Media Area on the page for **Mobile/Tablet on Coral**
        EXPECTED: * 'PRE-PARADE' button becomes 'DONE' on Ladbrokes (Mobile, Tablet and Desktop)
        """
        pass

    def test_004_clicktap_on_the_pre_parade_coral__done_ladbrokes_button(self):
        """
        DESCRIPTION: Click/Tap on the 'PRE-PARADE' (Coral) / 'DONE' (Ladbrokes) button
        EXPECTED: For Coral:
        EXPECTED: * The area below 'PRE-PARADE' button is collapsed
        EXPECTED: * The information link is no longer displayed
        EXPECTED: For Ladbrokes:
        EXPECTED: * The area below 'DONE' button is collapsed
        EXPECTED: * 'DONE' label on button changes to 'PRE-PARADE'
        """
        pass
