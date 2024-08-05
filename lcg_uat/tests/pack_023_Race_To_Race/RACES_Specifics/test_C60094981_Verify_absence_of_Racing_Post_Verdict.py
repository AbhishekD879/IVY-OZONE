import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@vtest
class Test_C60094981_Verify_absence_of_Racing_Post_Verdict(Common):
    """
    TR_ID: C60094981
    NAME: Verify absence of Racing Post Verdict
    DESCRIPTION: This test case verifies whether Racing Post Verdict (or it's part) doesn't display if there is no info for separate event Racing Post Verdict in a response from Racing Post API
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    PRECONDITIONS: * To get the event with needed no/empty attributes, it is possible to block the racing post call in console (network)
    """
    keep_browser_open = True

    def test_001__find_an_event_with_noempty_racing_post_verdict_section_in_api_open_that_event_in_the_app_horse_racing__event(self):
        """
        DESCRIPTION: * Find an event with ***no/empty Racing Post Verdict section*** in [API]
        DESCRIPTION: * Open that event in the app (Horse racing > Event)
        EXPECTED: **Mobile:** 'Racing Post Verdict >' label is absent in the race information area
        EXPECTED: **Desktop:** 'Racing Post Verdict' section is absent
        """
        pass

    def test_002__find_an_event_with_noempty_verdict_summary_text_in_racing_post_verdict_section_in_api_open_that_event_in_the_app_horse_racing__event(self):
        """
        DESCRIPTION: * Find an event with ***no/empty 'Verdict summary text'*** in Racing Post Verdict section in [API]
        DESCRIPTION: * Open that event in the app (Horse racing > Event)
        EXPECTED: **Mobile:** 'Racing Post Verdict >' label is settled in the bottom left-hand corner of the race information area
        EXPECTED: **Desktop:** 'Racing Post Verdict' section is present
        """
        pass

    def test_003_mobile_tap_on_racing_post__verdict_(self):
        """
        DESCRIPTION: **Mobile:** Tap on 'Racing Post  Verdict >'
        EXPECTED: **Mobile:** 'Racing Post  Verdict' overlay is  shown at the bottom of the page
        """
        pass

    def test_004_verify_racing_post_verdict_overview(self):
        """
        DESCRIPTION: Verify 'Racing Post Verdict' overview
        EXPECTED: * Verdict summary text is absent
        EXPECTED: * All other sections are displayed
        EXPECTED: The list of all 'Racing Post Verdict'  sections:
        EXPECTED: **Mobile:**
        EXPECTED: * 'Racing Post  Verdict' text, Close button (X) in the header
        EXPECTED: - Verdict summary text
        EXPECTED: * Course Map
        EXPECTED: * Most Tipped
        EXPECTED: -3 Most Tipped Horses for that race
        EXPECTED: Table:Horse Name, Tipster Names, Number of Total tips per horse
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: -A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: -List of tips
        EXPECTED: **Desktop:**
        EXPECTED: * 'Racing Post Verdict' text in the header
        EXPECTED: - Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: - A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: - List of tips
        EXPECTED: * Most Tipped
        EXPECTED: - 3 Most Tipped Horses for that race
        EXPECTED: Table:Horse Name, Tipster Names, Number of Total tips per horse
        EXPECTED: * Course map
        """
        pass

    def test_005_repeat_steps_2_4_for_racing_post_star_rating(self):
        """
        DESCRIPTION: Repeat Steps #2-4 for ***Racing Post Star Rating***
        EXPECTED: * Racing Post Star Rating is absent
        EXPECTED: * All other sections are displayed
        """
        pass

    def test_006_repeat_steps_2_4_for_racing_post_tips(self):
        """
        DESCRIPTION: Repeat Steps #2-4 for ***Racing Post Tips***
        EXPECTED: * Racing Post Tips is absent
        EXPECTED: * All other sections are displayed
        """
        pass

    def test_007_desktop_and_mobilerepeat_steps_2_4_for_course_map__map(self):
        """
        DESCRIPTION: **Desktop and Mobile**
        DESCRIPTION: Repeat Steps #2-4 for ***Course map ( Map)***
        EXPECTED: * Course map is absent
        EXPECTED: * All other sections are displayed
        """
        pass
