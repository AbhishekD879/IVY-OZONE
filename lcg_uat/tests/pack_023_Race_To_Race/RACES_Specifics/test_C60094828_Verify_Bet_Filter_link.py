import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094828_Verify_Bet_Filter_link(BaseRacing):
    """
    TR_ID: C60094828
    NAME: Verify Bet Filter link
    DESCRIPTION: Verify that user is able to click Bet Filter link.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True
    section_skip_list = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL', 'ENHANCED RACES', 'NEXT RACES',
                         'OFFERS & FEATURED RACES', 'EXTRA PLACE RACES']

    def verify_bet_filter_page(self):
        self.site.wait_content_state(state_name='HorseRacingBetFilterPage')
        bet_filter = self.site.horseracing_bet_filter
        self.assertEqual(bet_filter.page_title.text, vec.bet_finder.BF_HEADER_TITLE,
                         msg=f'Bet filter page\'s title is incorrect.\n Expected is "{bet_filter.page_title.text}", '
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')

        if self.brand == 'bma':
            self.assertEqual(bet_filter.header_line.page_title.sport_title, vec.bet_finder.BF_HEADER_TITLE,
                             msg=f'Bet filter header line title is incorrect.\n '
                             f'Expected is "{bet_filter.header_line.page_title.sport_title}",'
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')

        self.assertEqual(bet_filter.description.text, vec.bet_finder.BF_HEADER_TEXT,
                         msg=f'Bet filter page description is incorrect.\n '
                         f'Expected is "{bet_filter.description.text}", '
                         f'Actual is "{vec.bet_finder.BF_HEADER_TEXT}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable horse racing bet filter
        """
        if tests.settings.backend_env != 'prod':
            hr_bet_filter_status = self.cms_config.verify_and_update_bet_filter_horse_racing_status(status=True)
            self.assertTrue(hr_bet_filter_status, msg='Bet Filter is disabled')
            self.ob_config.add_UK_racing_event(number_of_runners=1)

    def test_001_launch_ladbrokes_coral_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral App
        EXPECTED: App should be opened
        """
        # Covered in step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.brand == 'ladbrokes':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.HORSERACING).click()
        else:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.HORSERACING.upper()).click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_race(self):
        """
        DESCRIPTION: Click on any race
        EXPECTED: User should be navigated to the Event details page
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        found_event = False
        for section_name, section in sections.items():
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        if 'race-on' in event.get_attribute('class'):
                            event.click()
                            self.site.wait_splash_to_hide()
                            found_event = True
                            break
                    if found_event is True:
                        break
                    else:
                        continue
                if found_event is True:
                    break
                else:
                    continue
        self.site.wait_content_state_changed()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_click_on_bet_filter_link(self):
        """
        DESCRIPTION: Click on "Bet Filter" link
        EXPECTED: 1: User should be able to click the "Bet Filter" link
        EXPECTED: 2: User should be navigated to Bet Filter section
        """
        has_bet_filter_link = self.site.racing_event_details.has_bet_filter_link
        self.assertTrue(has_bet_filter_link, msg='Event details page doesn\'t have back button')
        self.site.racing_event_details.bet_filter_link.click()
        self.site.wait_content_state_changed(timeout=10)
        self.verify_bet_filter_page()
