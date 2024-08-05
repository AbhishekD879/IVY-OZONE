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
class Test_C9618064_Races_displaying_meeting_statuses_on_landing_page_and_event_details_page(Common):
    """
    TR_ID: C9618064
    NAME: <Races>: displaying meeting statuses on landing page and event details page
    DESCRIPTION: This test case verifies displaying of different meetings statuses on <Race> landing page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 4 <Race> events:
    PRECONDITIONS: 1) Preplay race (race is not started yet)
    PRECONDITIONS: 2) Started race with enabled bet in running
    PRECONDITIONS: 3) Started race with disabled bet in running
    PRECONDITIONS: 4) Resulted race
    PRECONDITIONS: - You should have 4 international tote events:
    PRECONDITIONS: 1) Preplay race (race is not started yet)
    PRECONDITIONS: 2) Started race with enabled bet in running
    PRECONDITIONS: 3) Started race with disabled bet in running
    PRECONDITIONS: 4) Resulted race
    PRECONDITIONS: - You should be on <Race> landing page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_ladbrokes_only_verify_tab_name(self):
        """
        DESCRIPTION: [Ladbrokes ONLY] Verify tab name
        EXPECTED: Tab is called 'Meetings'
        """
        pass

    def test_002_ladbrokes_only_verify_race_statuses_displaying(self):
        """
        DESCRIPTION: [Ladbrokes ONLY] Verify race statuses displaying
        EXPECTED: **Ordinary events:**
        EXPECTED: 1) Preplay race:
        EXPECTED: - Has no status under race time
        EXPECTED: 2) Started race with enabled bet in running:
        EXPECTED: - Has 'LIVE' status below the race time
        EXPECTED: 3) Started race with disabled bet in running :
        EXPECTED: - Has red colored 'RACE OFF' status below the race time
        EXPECTED: 4) Resulted race:
        EXPECTED: - Has 'RESULT' status below the race time
        EXPECTED: **International tote events:**
        EXPECTED: 1) Preplay race:
        EXPECTED: - Has event name under time (4-5 letters)
        EXPECTED: - Has no status below race name
        EXPECTED: 2) Started race with enabled bet in running:
        EXPECTED: - Has event name under time (4-5 letters)
        EXPECTED: - Has 'LIVE' status below the race name
        EXPECTED: 3) Started race with disabled bet in running :
        EXPECTED: - Has event name under time (4-5 letters)
        EXPECTED: - Has red colored 'RACE OFF' status below the race name
        EXPECTED: 4) Resulted race:
        EXPECTED: - Has event name under time (4-5 letters)
        EXPECTED: - Has 'RESULT' status below the race name
        """
        pass

    def test_003_open_event_details_pages_of_events_with_different_statuses_from_next_races_pagecarousel_and_verify_displaying_of_statuses(self):
        """
        DESCRIPTION: Open event details pages of events with different statuses from "Next Races" page/carousel and verify displaying of statuses
        EXPECTED: **Ordinary events:**
        EXPECTED: - Only Preplay races are shown and they have no status under race time, only first 4-5 letters of event name
        EXPECTED: - Started Events disappear from Next Races events Ribbon after page refresh
        """
        pass

    def test_004_open_event_details_pages_of_events_with_different_statuses_from_the_same_typeeg_doncaster_steepledowns_etc_and_verify_displaying_of_statuses(self):
        """
        DESCRIPTION: Open event details pages of events with different statuses from the same Type(e.g. Doncaster, Steepledowns etc.) and verify displaying of statuses
        EXPECTED: **Ordinary events:**
        EXPECTED: 1) Preplay race:
        EXPECTED: - Has no status under race time
        EXPECTED: - First 4-5 letters of the event name are NOT shown
        EXPECTED: 2) Started race with enabled bet in running:
        EXPECTED: - Has 'LIVE' status below the race time
        EXPECTED: - Has no race name
        EXPECTED: 3) Started race with disabled bet in running :
        EXPECTED: - Has red colored 'RACE OFF' status below the race time
        EXPECTED: - Has no race name
        EXPECTED: 4) Resulted race:
        EXPECTED: - Has 'RESULT' status below the race time
        EXPECTED: - Has no race name
        """
        pass

    def test_005_open_event_details_pages_of_international_tote_events_with_different_statuses_and_verify_displaying_of_statuses(self):
        """
        DESCRIPTION: Open event details pages of international tote events with different statuses and verify displaying of statuses
        EXPECTED: **International tote events:**
        EXPECTED: 1) Preplay race:
        EXPECTED: - Has no status under race time
        EXPECTED: - First 4-5 letters of the event name are NOT shown
        EXPECTED: 2) Started race with enabled bet in running:
        EXPECTED: - Has 'LIVE' status below the race time
        EXPECTED: - Has no race name
        EXPECTED: 3) Started race with disabled bet in running :
        EXPECTED: - Has red colored 'RACE OFF' status below the race time
        EXPECTED: - Has no race name
        EXPECTED: 4) Resulted race:
        EXPECTED: - Has 'RESULT' status below the race time
        EXPECTED: - Has no race name
        """
        pass
