import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.races
@vtest
class Test_C874353_Navigation_Horse_Racing(Common):
    """
    TR_ID: C874353
    NAME: Navigation Horse Racing
    DESCRIPTION: TO COVER
    DESCRIPTION: Races Landing page
    DESCRIPTION: Next 4
    DESCRIPTION: Next Races widget
    DESCRIPTION: Quantum Leap
    DESCRIPTION: Results
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile - [C47786772]
    DESCRIPTION: Desktop - [C48047419]
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True

    def test_001_click_on_horse_racing_button_from_the_main_menu(self):
        """
        DESCRIPTION: Click on Horse Racing button from the Main Menu
        EXPECTED: 1. Horse Racing Page is loaded
        EXPECTED: 2. The Featured tab is selected by default
        EXPECTED: 3. "Enhanced Races" (if available) is displayed on the top of the page
        EXPECTED: 4. Under the "Enhanced Races" > "Next Races" module
        EXPECTED: 5. 'Starts in' label with countdown clock “MM:SS” is available for events that start less than 45 minutes in 'Next Races’ > REMOVED FOR NOW: Once next race status is received, it is displayed on corresponding badges
        EXPECTED: 6. "UK & IRE" section is displayed followed by "International" ( divided by coutries) and then "Virtual"
        EXPECTED: 7. "Enhanced Multiples" module (if available) is displayed below  "International"
        EXPECTED: 8. The Horse Racing meetings with video stream available should be marked with "Play" icon
        EXPECTED: On Desktop:
        EXPECTED: - Enhanced Multiples carousel (if available)
        EXPECTED: - "UK & IRE" section is displayed followed by "International" and then "Virtual"
        EXPECTED: **For screen width > 970 px, 1025px next modules are displayed below in main display area
        EXPECTED: **For screen width 1280px, 1600px next modules are displayed on the second column of the display area
        EXPECTED: - "Next Races" module
        EXPECTED: - "Enhanced Races" module
        EXPECTED: - "Virtuals" carousel
        EXPECTED: - "YourCall Specials" module
        """
        pass

    def test_002_click_on_specials_if_availableyourcallresults_tabs(self):
        """
        DESCRIPTION: Click on Specials (if available)/Yourcall/Results tabs
        EXPECTED: Check that each tab loads proper information
        """
        pass

    def test_003_navigate_to_featured_tab_and_select_any_horse_racing_event_eg_kempton_640(self):
        """
        DESCRIPTION: Navigate to Featured tab and select any Horse Racing event (e.g. Kempton 6:40)
        EXPECTED: 1. The Horse Racing event race card is loaded
        EXPECTED: 2. The meeting selector is available on the top of the page in format Horse Racing/*Type name* (opens an overlay)
        EXPECTED: 3. The event selector (time ribbon) is displayed right under the the meeting selector
        EXPECTED: 4. There is an are with the race details (name, distance, Racing Post info and Video stream button)
        EXPECTED: 5. The Win or Each Way market is selected by default
        EXPECTED: 6. Check that the Each Way terms is displayed right under the market name
        EXPECTED: 7. Check that the selections are correctly displayed (with silks - if available) and SP or LP
        """
        pass

    def test_004_check_all_other_markets_of_the_event(self):
        """
        DESCRIPTION: Check all other markets of the event
        EXPECTED: Each market is correctly loaded showing the selections (Each Way terms - if available, silks - if available)
        """
        pass

    def test_005_select_a_different_meeting_from_the_meeting_selector(self):
        """
        DESCRIPTION: Select a different meeting from the meeting selector
        EXPECTED: The first event from the selected meeting should be loaded by default
        """
        pass

    def test_006_select_a_different_event_from_the_event_selector(self):
        """
        DESCRIPTION: Select a different event from the event selector
        EXPECTED: The selected event is loaded
        """
        pass
