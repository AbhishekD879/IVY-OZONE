import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094830_Verify_Back_button_in_Coral_app(BaseRacing):
    """
    TR_ID: C60094830
    NAME: Verify Back button in Coral app
    DESCRIPTION: Coral: Verify that back button is displayed inside the breadcrumbs area.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable horse racing bet filter.
        """
        if tests.settings.backend_env != 'prod':
            hr_bet_filter_status = self.cms_config.verify_and_update_bet_filter_horse_racing_status(status=True)
            self.assertTrue(hr_bet_filter_status, msg='Bet Filter is disabled')

    def test_001_launch_coral_app(self):
        """
        DESCRIPTION: Launch Coral App
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
                        race_started = event.is_resulted or event.has_race_off()
                        if not race_started:
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

    def test_004_validate_back_buttonindexphpattachmentsget118703011(self):
        """
        DESCRIPTION: Validate Back button
        DESCRIPTION: ![](index.php?/attachments/get/118703011)
        EXPECTED: 1: User should be able to view the Back button in the breadcrumbs area
        EXPECTED: 2: User should be able to navigate to previous page on clicking back button
        """
        # has_back_btn = self.site.has_back_button
        self.assertTrue(self.site.has_back_button, msg='Event details page doesn\'t have back button')
        self.site.back_button.click()
        self.site.wait_content_state('horse-racing')