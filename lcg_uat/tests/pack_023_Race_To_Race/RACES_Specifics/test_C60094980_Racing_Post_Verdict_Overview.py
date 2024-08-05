import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from time import sleep


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2  # feed is not available for qa2
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094980_Racing_Post_Verdict_Overview(BaseRacing):
    """
    TR_ID: C60094980
    NAME: Racing Post Verdict Overview
    DESCRIPTION: This test case verifies Racing Post Verdict Overlay and displaying it on the Event Details page.
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True
    maximized_browser = False
    most_tips_list = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find the event with Racing Post Verdict details
        DESCRIPTION: A user is on a Race Card (Event Details page) of an event with available Racing Post
        """
        event_info = self.get_event_details(race_form_info=True, racing_post_verdict=True, df_event_summary=True)
        event_id = event_info.event_id
        datafabric_data = event_info.datafabric_data
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        event_url = self.device.get_current_url()
        self.assertIn(event_id, event_url,
                      msg=f'Event id "{event_id}" is not found in current url "{event_url}"')
        self.__class__.summary_response = datafabric_data.get('verdict')
        self.__class__.newspapers = datafabric_data.get('newspapers')
        horse_list = {horse.get('horseName'): horse.get('starRating') for horse in datafabric_data.get('horses')}
        self.site.wait_content_state_changed(timeout=5)
        sorted_list = sorted(sorted(horse_list.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)[:3]
        for horse in self.newspapers:
            if horse.get('tips'):
                self.most_tips_list.update({horse.get('selection'): horse.get('tips')})
        most_tipped_list_sorted = sorted(self.most_tips_list.items(), key=lambda x: x[1], reverse=True)[:3]
        self.__class__.top_3_names = [horse[0].upper() for horse in sorted_list]
        self.__class__.top_3_horses = [horse_name[0] for horse_name in most_tipped_list_sorted]
        self.__class__.number_of_tips = [no_tips[1] for no_tips in most_tipped_list_sorted]

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
            self.assertGreater(self.racing_post_verdict.location.get('x'), 180,
                               msg='"Racing Post Verdict" label is expected to be on the right hand of page (if width > 1280px)')

            self.device.set_viewport_size(width=1270, height=1270)
            self.assertGreater(self.racing_post_verdict.location.get('y'), first_screen_y_location,
                               msg='"Racing Post Verdict" label is expected to be at the bottom (width 1279px)')

    def test_002_mobile_tap_on_racing_post__verdict_(self):
        """
        DESCRIPTION: **Mobile:** Tap on 'Racing Post  Verdict >'
        EXPECTED: **Mobile:** 'Racing Post  Verdict' overlay is  shown at the bottom of the page
        """
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
        EXPECTED: * Course Map
        EXPECTED: * <Race Time> 'Most Tipped'
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
        sleep(5)
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                title = self.racing_post_verdict.header.title
                self.assertTrue(self.racing_post_verdict.header.close_button, msg='Close button is not present')
            else:
                title = self.racing_post_verdict.header
            expected_title = vec.racing.VERDICT
            self.assertEquals(title, expected_title,
                              msg=f'Actual title "{title}" is not same as expected title "{expected_title}"')
        else:
            title = self.racing_post_verdict.header
            self.assertTrue(title, msg=f'Racing post verdict logo is not displayed')
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

        most_tips = self.racing_post_verdict.most_tipped.items_as_ordered_dict
        self.assertTrue(len(most_tips) <= 3, msg='More than 3 most tipped horses are displayed')

        expected_most_tipped = vec.racing.MOST_TIPPED
        self.assertEqual(self.racing_post_verdict.most_tipped.title, expected_most_tipped,
                         msg=f'"Most tipped" subheader "{self.racing_post_verdict.most_tipped.title}"'
                             f'is not equal to "{expected_most_tipped}"')
        horse_names = [tip.split('\n')[0] for tip in most_tips]
        for horse_name in horse_names:
            self.assertIn(horse_name, self.top_3_horses, msg=f'"Actual Horse names(at most 3):"{horse_name}"'
                                                             f'is not equal to expected Horse names"{self.top_3_horses}"')
        tipster_names = [tip.split('\n')[1] for tip in most_tips]
        self.assertTrue(tipster_names, msg='Tipster names are not present in the')
        actual_number_of_tips = [tip.split('\n')[2].replace(" TIPS", "") for tip in most_tips]
        self.assertEqual(actual_number_of_tips, self.number_of_tips,
                         msg=f'"Actual number of tips"{actual_number_of_tips}"'
                             f'is not equal to expected number of tips"{self.number_of_tips}"')

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
        EXPECTED: DESKTOP
        EXPECTED: * 'Racing Post Star Rating' is located after Verdict summary text
        EXPECTED: * 'Racing Post Star Rating' = TOP 3 'starRating' ORDER by DESC  from Racing Post response
        EXPECTED: * Runners with the same rating value are shown in alphabetical order
        EXPECTED: MOBILE:
        EXPECTED: * 'Racing Post Star Rating' is located after MOST TIPpED
        EXPECTED: * 'Racing Post Star Rating' = TOP 3 'starRating' ORDER by DESC  from Racing Post response
        EXPECTED: * Runners with the same rating value are shown in alphabetical order
        """
        runner_list = list(self.runners.keys())
        for runner in runner_list:
            self.assertIn(runner.upper(), self.top_3_names, msg=f'Racing Post Star Rating :"{runner}" '
                                                                f'is not equal to Top 3 runner "{self.top_3_names}"')

    def test_006_verify_most_tipped(self):
        """
        DESCRIPTION: Verify 'MOST TIPPED'
        EXPECTED: * <Race Time> 'Most Tipped'
        EXPECTED: It will display Top 3 most tipped horses
        """
        # covered in step 3

    def test_007_verify_racing_post_tips(self):
        """
        DESCRIPTION: Verify 'Racing Post Tips'
        EXPECTED: * 'Racing Post Tips' is located after Racing Post Star Rating
        EXPECTED: * 'Racing Post Tips' = 'newspapers' array: 'name', 'selection' attributes from Racing Post response
        """
        tips_list = [tip.split('\n')[1] for tip in self.tips]
        list_post_tips = [post_item['selection'] for post_item in self.newspapers]
        self.assertEqual(tips_list, list_post_tips,
                         msg=f'Actual value "{tips_list}" is not equal to expected value "{list_post_tips}"')

    def test_008_verify_course_map(self):
        """
        DESCRIPTION: Verify 'Course map'
        EXPECTED: **Desktop:**
        EXPECTED: * 'Course map'  is located at the bottom of Racing Post Verdict overlay
        EXPECTED: **MOBILE**
        EXPECTED: * 'Course map'  is located after the Racing Post Verdict summary text
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.racing_post_verdict.is_coursemap_at_bottom(),
                            msg='"Course Map" overlay is not shown at the bottom of the page')
        else:
            self.assertTrue(self.racing_post_verdict.is_coursemap_located_after_verdict(),
                            msg='"Course Map" overlay is not shown after the Racing Post Verdict summary text')
