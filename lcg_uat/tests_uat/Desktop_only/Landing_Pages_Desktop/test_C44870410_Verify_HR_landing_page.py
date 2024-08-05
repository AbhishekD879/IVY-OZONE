import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870410_Verify_HR_landing_page(Common):
    """
    TR_ID: C44870410
    NAME: "Verify HR landing page
    DESCRIPTION: Verify HR landing page and its relevant elements.
    PRECONDITIONS: HR page is displayed to both logged in and logged out users.
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com on Chrome browser.
        EXPECTED: https://msports.ladbrokes.com displayed on Chrome browser.
        """
        pass

    def test_002_verify_hr_landing_page_displayed_racecourse_meetings_with_respective_start_times___all_accordions_are_expanded(self):
        """
        DESCRIPTION: Verify HR landing page displayed racecourse meetings with respective start times - all accordions are expanded.
        EXPECTED: HR landing page displayed racecourse meetings with respective start times - all accordions are expanded.
        """
        pass

    def test_003_verify_meetings_sections_by_country(self):
        """
        DESCRIPTION: Verify meetings sections by country.
        EXPECTED: Meetings sections displayed by country.
        """
        pass

    def test_004_verify_meeting_events_displayed_by_chronological_order(self):
        """
        DESCRIPTION: Verify meeting events displayed by chronological order.
        EXPECTED: Meeting events displayed by chronological order.
        """
        pass

    def test_005_verify_resulted_events_display_racing_post_underneath_greyed_out_time(self):
        """
        DESCRIPTION: Verify resulted events display racing post underneath greyed out time.
        EXPECTED: Resulted events display racing post underneath greyed out time.
        """
        pass

    def test_006_verify_signposting_for_meeting_tote_cashout_watch_etc(self):
        """
        DESCRIPTION: Verify Signposting for meeting :
        DESCRIPTION: Tote, Cashout, Watch etc
        EXPECTED: Signposting displayed for meetings :
        EXPECTED: Tote, Cashout, Watch etc
        """
        pass

    def test_007_click_on_any_race_event_and_verigy_page_details(self):
        """
        DESCRIPTION: Click on any race event and verigy page details
        EXPECTED: Relevant race card page displayed with correct:
        EXPECTED: 1. Meeting and Date in Header.
        EXPECTED: 2. Breadcrumbs
        EXPECTED: 3. Race switcher with red market underneath displayed race.
        EXPECTED: 4. Display Time(24hr format) Meeting
        EXPECTED: 5. Name of race
        EXPECTED: 6. Race type, distance, going, Starts in timer
        EXPECTED: 7. Watch Live Sim Live commentary header
        """
        pass

    def test_008_verify_horse_information_is_displayed(self):
        """
        DESCRIPTION: Verify horse information is displayed
        EXPECTED: Horse information is displayed with correct:
        EXPECTED: 1.Name (In bold)
        EXPECTED: 2.Jockey/Trainer
        EXPECTED: 3.Form
        EXPECTED: 4.Show More V (hidden)(collapse displays RP/Spotlight info)
        EXPECTED: 5.Silk
        EXPECTED: 6.Horse number, Stall number in ()
        EXPECTED: 7. * D Bf C CD signposting
        EXPECTED: 8. RP verdict at bottom of page
        """
        pass
