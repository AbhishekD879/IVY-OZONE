import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.screen_resolution
@pytest.mark.reg157_fix
@vtest
class Test_C10386559_Ladbrokes_Racing_Post_Verdict_Overview(BaseRacing):
    """
    TR_ID: C10386559
    NAME: [Ladbrokes] Racing Post Verdict Overview
    DESCRIPTION: This test case verifies Racing Post Verdict Overlay and displaying it on the Event Details page.
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True
    maximized_browser = False

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find the event with Racing Post Verdict details
        DESCRIPTION: A user is on a Race Card (Event Details page) of an event with available Racing Post
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(event_complete_info=True, star_rating=['1', '2', '3', '4', '5'])
        if not self.event_info:
            raise SiteServeException('Racing events not available')
        self.__class__.event_id = list(self.event_info.keys())[0]
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.summary_response = self.event_info[self.event_id].get('verdict')
        self.__class__.newspapers = self.event_info[self.event_id].get('newspapers')
        self.__class__.course_graphics_ladbrokes = self.event_info[self.event_id].get('courseGraphicsLadbrokes')
        horses_details = {horse['horseName']: horse for horse in self.event_info[self.event_id]['horses']}
        horse_list = {horse: horse_details.get('starRating') for horse, horse_details in horses_details.items()}
        self.__class__.sorted_list = sorted(horse_list.items(), key=lambda x: x[1], reverse=True)[:3]
        self.__class__.expected_top_3_horses = [horse[0] for horse in self.sorted_list]

    def test_001_verify_racing_post_verdict__label(self):
        """
        DESCRIPTION: Verify 'Racing Post Verdict >' label
        EXPECTED: **Mobile:** 'Racing Post Verdict >' label is settled in the bottom right-hand corner of the race information area
        EXPECTED: **Desktop:**
        EXPECTED: * Displaying of 'Racing Post Verdict' section depends on screen resolution. It is in the bottom of the race card  (width to 1279px) or on the right hand of the page (if width > 1280px)
        EXPECTED: * 'Racing Post Verdict' label is aligned to the left
        """
        if self.device_type == 'mobile':
            self.assertTrue(self.site.racing_event_details.tab_content.has_post_info(),
                            msg='Racing Post info section is not found')
        else:
            self.__class__.racing_post_verdict = self.site.racing_event_details.racing_post_verdict
            self.assertTrue(self.racing_post_verdict, msg='"Racing Post Verdict" is not shown on desktop')

            self.device.set_viewport_size(width=1600, height=1600)
            first_screen_y_location = self.site.racing_event_details.racing_post_verdict.location.get('y')
            self.assertGreater(self.racing_post_verdict.location.get('x'), 800,
                               msg='"Racing Post Verdict" label is expected to be on the right hand of page (if width > 1280px)')

            self.device.set_viewport_size(width=1270, height=1270)
            self.assertGreater(self.racing_post_verdict.location.get('y'), first_screen_y_location,
                               msg='"Racing Post Verdict" label is expected to be at the bottom (width 1279px)')

    def test_002_mobile_tap_on_racing_post__verdict_(self):
        """
        DESCRIPTION: **Mobile:** Tap on 'Racing Post  Verdict >'
        EXPECTED: **Mobile:** 'Racing Post  Verdict' overlay is  shown at the bottom of the page
        """
        self.device.refresh_page()
        if self.device_type == 'mobile':
            self.site.racing_event_details.tab_content.post_info.click()
            self.__class__.racing_post_verdict = self.site.racing_event_details.racing_post_verdict
            self.assertTrue(self.racing_post_verdict, msg='"Racing Post Verdict overlay" is not shown')
            self.assertTrue(self.racing_post_verdict.is_at_bottom(),
                            msg='"Racing Post  Verdict" overlay is not shown at the bottom of the page')

    def test_003_verify_racing_post_verdict_overview(self):
        """
        DESCRIPTION: Verify 'Racing Post Verdict' overview
        EXPECTED: 'Racing Post Verdict' consists of:
        EXPECTED: **Mobile:**
        EXPECTED: * 'Racing Post  Verdict' text, Close button (X) in the header
        EXPECTED: * Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: * A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: * List of tips
        EXPECTED: **Desktop:**
        EXPECTED: * 'Racing Post Verdict' text in the header
        EXPECTED: * Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' subheader
        EXPECTED: * A table containing the star rating of the Top 03 Runners. The runners are ordered in star rating order, most to least.
        EXPECTED: * 'Racing Post Tips' subheader
        EXPECTED: * List of tips
        EXPECTED: * Course map (Desktop Map)
        """
        if self.device_type == 'mobile':
            wait_for_haul(5)
            title = self.racing_post_verdict.header.title
            self.assertTrue(self.racing_post_verdict.header.close_button, msg='Close button is not present')
        else:
            self.__class__.racing_post_verdict = self.site.racing_event_details.racing_post_verdict
            title = self.racing_post_verdict.header
            if self.course_graphics_ladbrokes:
                self.assertTrue(self.racing_post_verdict.course_map, msg='Course map (Desktop Map) is not present')

        expected_title = vec.racing.VERDICT
        self.assertEquals(title, expected_title,
                          msg=f'Actual title "{title}" is not same as expected title "{expected_title}"')

        self.__class__.summary = self.racing_post_verdict.summary
        self.assertTrue(self.summary, msg='Summary text is not present')

        expected_star_rating = vec.racing.RACING_POST_STAR_RATING
        self.assertEqual(self.racing_post_verdict.racing_post_rating.title, expected_star_rating,
                         msg=f'"Racing Post Star Rating" subheader "{self.racing_post_verdict.racing_post_rating.title}"'
                             f'is not equal to "{expected_star_rating}"')

        self.__class__.runners = self.racing_post_verdict.racing_post_rating.items_as_ordered_dict
        self.assertEqual(len(self.runners), 3,
                         msg=f'Expected Top 3 runners but found "{len(self.runners)}" runners')

        for runner_name, runners_details in self.runners.items():
            self.assertTrue(runners_details.has_star_container(),
                            msg=f'A table containing the star rating is not present for the runner "{runner_name}"')

        expected_post_tips = vec.racing.RACING_POST_TIPS
        self.assertEqual(self.racing_post_verdict.racing_post_tips.title, expected_post_tips,
                         msg=f'"Racing Post Tips" subheader "{self.racing_post_verdict.racing_post_tips.title}" '
                             f'is not equal to "{expected_post_tips}"')

        self.__class__.tips = self.racing_post_verdict.racing_post_tips.items_as_ordered_dict
        self.assertTrue(self.tips, msg='List of tips is not present')

    def test_004_verify_verdict_summary_text(self):
        """
        DESCRIPTION: Verify 'Verdict summary text'
        EXPECTED: * 'Summary text' is located first on the 'Racing Post' overlay
        EXPECTED: * 'Summary text' = 'verdict' attribute from Racing Post response
        """
        self.assertEquals(self.summary_response, self.racing_post_verdict.summary.name,
                          msg=f'Summary text {self.racing_post_verdict.summary.name} is not equal to verdict attribute'
                              f' "{self.summary_response}" from Racing Post response')

    def test_005_verify_racing_post_star_rating(self):
        """
        DESCRIPTION: Verify 'Racing Post Star Rating'
        EXPECTED: * 'Racing Post Star Rating' is located after Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' = TOP 3 'starRating' ORDER by DESC  from Racing Post response
        EXPECTED: * Runners with the same rating value are shown in alphabetical order
        """
        actual_top_3_horses = list(self.runners.keys())
        actual_top_3_horses = [top_horse.replace(' N/R','') for top_horse in actual_top_3_horses]
        self.assertEqual(self.expected_top_3_horses, actual_top_3_horses,
                         msg=f'expected top 3 horses are :"{self.expected_top_3_horses}" but actual  "{actual_top_3_horses}"')

    def test_006_verify_racing_post_tips(self):
        """
        DESCRIPTION: Verify 'Racing Post Tips'
        EXPECTED: * 'Racing Post Tips' is located after Verdict summary text
        EXPECTED: * 'Racing Post Tips' = 'newspapers' array: 'name', 'selection' attributes from Racing Post response
        """
        tips_list = [tip.split('\n')[1] for tip in self.tips]
        list_post_tips = [post_item['selection'] for post_item in self.newspapers]
        self.assertEqual(tips_list, list_post_tips,
                         msg=f'Actual value "{tips_list}" is not equal to expected value "{list_post_tips}"')

    def test_007_verify_course_map(self):
        """
        DESCRIPTION: Verify 'Course map'
        EXPECTED: * Only for Desktop
        EXPECTED: * 'Course map'  is located at the bottom of Racing Post Verdict overlay
        EXPECTED: * 'Course map' = 'courseGraphicsLadbrokes' attribute from Racing Post response
        """
        if self.device_type == 'desktop' and self.course_graphics_ladbrokes:
            course_map = self.racing_post_verdict.course_map
            self.assertEqual(course_map, self.course_graphics_ladbrokes,
                             msg=f'Actual value "{course_map}" not equal to expected value "{self.course_graphics_ladbrokes}"')
