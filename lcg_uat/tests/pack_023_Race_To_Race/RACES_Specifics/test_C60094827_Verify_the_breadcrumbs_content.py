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
class Test_C60094827_Verify_the_breadcrumbs_content(BaseRacing):
    """
    TR_ID: C60094827
    NAME: Verify the breadcrumbs content
    DESCRIPTION: Verify that Bet Filter is displayed to the right corner inside the breadcrumbs content.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

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
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        if self.brand == 'ladbrokes':
            all_items.get(vec.SB.HORSERACING).click()
        else:
            all_items.get(vec.SB.HORSERACING.upper()).click()
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
            if section_name in vec.racing.COUNTRY_SKIP_LIST or self.next_races_title in section_name:
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
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_validate_breadcrumbs_contentindexphpattachmentsget118703005indexphpattachmentsget118703006(self):
        """
        DESCRIPTION: Validate breadcrumbs content
        DESCRIPTION: ![](index.php?/attachments/get/118703005)
        DESCRIPTION: ![](index.php?/attachments/get/118703006)
        EXPECTED: User should be displayed "Bet Filter" to the right corner
        """
        has_bet_filter_link = self.site.racing_event_details.has_bet_filter_link
        self.assertTrue(has_bet_filter_link, msg='Event details page doesn\'t have back button')
        market_width = self.site.racing_event_details.sub_header.size["width"]
        bet_filter_location = self.site.racing_event_details.bet_filter_link.location.get('x')
        self.assertTrue(market_width / 2 < bet_filter_location,
                        msg='bet filter is not displayed on the right side of market header')
