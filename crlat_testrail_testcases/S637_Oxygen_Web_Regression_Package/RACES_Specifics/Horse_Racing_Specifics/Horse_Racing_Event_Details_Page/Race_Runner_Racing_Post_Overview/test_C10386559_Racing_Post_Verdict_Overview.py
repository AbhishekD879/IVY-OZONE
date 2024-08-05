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
class Test_C10386559_Racing_Post_Verdict_Overview(Common):
    """
    TR_ID: C10386559
    NAME: Racing Post Verdict Overview
    DESCRIPTION: This test case verifies Racing Post Verdict Overlay and displaying it on the Event Details page.
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_001_verify_racing_post_verdict_gt_label(self):
        """
        DESCRIPTION: Verify 'Racing Post Verdict &gt;' label
        EXPECTED: **Mobile:** 'Racing Post Verdict &gt;' label is settled in the bottom right-hand corner of the race information area
        EXPECTED: **Desktop:**
        EXPECTED: * Displaying of 'Racing Post Verdict' section depends on screen resolution. It is in the bottom of the race card  (width to 1279px) or on the right hand of the page (if width &gt; 1280px)
        EXPECTED: * 'Racing Post Verdict' label is aligned to the left
        """
        pass

    def test_002_mobile_tap_on_racing_post__verdict_gt(self):
        """
        DESCRIPTION: **Mobile:** Tap on 'Racing Post  Verdict &gt;'
        EXPECTED: **Mobile:** 'Racing Post  Verdict' overlay is  shown at the bottom of the page
        """
        pass

    def test_003_verify_racing_post_verdict_overview(self):
        """
        DESCRIPTION: Verify 'Racing Post Verdict' overview
        EXPECTED: 'Racing Post Verdict' consists of:
        EXPECTED: **Mobile:**
        EXPECTED: * 'Racing Post  Verdict' text, Close button (X) in the header
        EXPECTED: * Verdict summary text
        EXPECTED: * Course Map
        EXPECTED: * &lt;Race Time&gt; 'Most Tipped'
        EXPECTED: * 3 Most Tipped Horses for that race. Table:Horse Name, Tipster Names, Number of Total tips per horse
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: * A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: * List of all tips
        EXPECTED: **Desktop:**
        EXPECTED: * 'Racing Post Verdict' text in the header
        EXPECTED: * Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: * A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: * List of tips
        EXPECTED: * Course map
        EXPECTED: * Most Tipped
        EXPECTED: * 3 Most Tipped Horses for that race
        EXPECTED: Table:Horse Name, Tipster Names, Number of Total tips per horse
        """
        pass

    def test_004_verify_verdict_summary_text(self):
        """
        DESCRIPTION: Verify 'Verdict summary text'
        EXPECTED: * 'Summary text' is located first on the 'Racing Post' overlay
        EXPECTED: * 'Summary text' = 'verdict' attribute from Racing Post response
        """
        pass

    def test_005_verify_racing_post_star_rating(self):
        """
        DESCRIPTION: Verify 'Racing Post Star Rating'
        EXPECTED: DESKTOP
        EXPECTED: * 'Racing Post Star Rating' is located after Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' = TOP 3 'starRating' ORDER by DESC  from Racing Post response
        EXPECTED: * Runners with the same rating value are shown in alphabetical order
        EXPECTED: MOBILE:
        EXPECTED: * 'Racing Post Star Rating' is located after MOST TIPpED
        EXPECTED: * 'Racing Post Star Rating' = TOP 3 'starRating' ORDER by DESC  from Racing Post response
        EXPECTED: * Runners with the same rating value are shown in alphabetical order
        """
        pass

    def test_006_verify_most_tipped(self):
        """
        DESCRIPTION: Verify 'MOST TIPPED'
        EXPECTED: * &lt;Race Time&gt; 'Most Tipped'
        EXPECTED: It will display Top 3 most tipped horses
        """
        pass

    def test_007_verify_racing_post_tips(self):
        """
        DESCRIPTION: Verify 'Racing Post Tips'
        EXPECTED: * 'Racing Post Tips' is located after Racing Post Star Rating
        EXPECTED: * 'Racing Post Tips' = 'newspapers' array: 'name', 'selection' attributes from Racing Post response
        """
        pass

    def test_008_verify_course_map(self):
        """
        DESCRIPTION: Verify 'Course map'
        EXPECTED: **Desktop:**
        EXPECTED: * 'Course map'  is located at the bottom of Racing Post Verdict overlay
        EXPECTED: **MOBILE**
        EXPECTED: * 'Course map'  is located after the Racing Post Verdict summary text
        """
        pass
