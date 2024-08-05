import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml
from datetime import datetime


@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@vtest
class Test_C2986638_Verify_view_of_Splash_Screen(Common):
    """
    TR_ID: C2986638
    VOL_ID: C24628217
    NAME: View of Splash Screen
    DESCRIPTION: This test case verifies 'Splash screen' view
    PRECONDITIONS: The user is logged in
    PRECONDITIONS: Quick link 'Play 1-2-FREE predictor and win £150' is available on home page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register new user
        """
        is_configured = False
        time_format = self.ob_format_pattern
        time_format_2 = '%Y-%m-%dT%H:%M:%S.%fZ'
        for game in self.cms_config.get_one_two_free_games():
            try:
                date_to = datetime.strptime(game.get('displayTo'), time_format)
            except ValueError:
                date_to = datetime.strptime(game.get('displayTo'), time_format_2)

            try:
                date_from = datetime.strptime(game.get('displayFrom'), time_format)
            except ValueError:
                date_from = datetime.strptime(game.get('displayFrom'), time_format_2)

            if game.get('enabled') and date_to > datetime.now() > date_from:
                is_configured = True
                break
        if not is_configured:
            raise CmsClientException('There are no 1-2-Free active games')

        self.site.login()

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_on_home_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link on home page
        EXPECTED: 'Splash screen' is successfully opened and designed according to mockup
        EXPECTED: Innovation logo
        EXPECTED: Main text (pull from CMS->static text-> splash page->pageText1)
        EXPECTED: Play now button (pull from CMS->static text-> splash page->CTA1)
        EXPECTED: Cancel button (pull from CMS->static text-> splash page->CTA2)
        """
        self.navigate_to_page(name='1-2-free')
        self.assertTrue(self.site.one_two_free.one_two_free_welcome_screen.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')

        welcome_screen_settings = None
        for screen in self.cms_config.get_one_two_free_static_texts():
            if screen['pageName'] == 'Splash page':
                welcome_screen_settings = screen
                break
        self.assertTrue(welcome_screen_settings, msg='Welcome screen settings were not retrieved from CMS')
        welcome_screen = self.site.one_two_free.one_two_free_welcome_screen

        self.assertTrue(welcome_screen.logo.is_displayed(), msg='Welcome screen logo is not displayed')
        self.assertEqual(welcome_screen.play_button.name, welcome_screen_settings.get('ctaText1'),
                         msg=f'Play button name "{welcome_screen.play_button.name}"'
                             f'is not the same as expected "{welcome_screen_settings.get("ctaText1")}"')
        self.assertEqual(welcome_screen.cancel_button.name, welcome_screen_settings.get('ctaText2'),
                         msg=f'Cancel button name "{welcome_screen.cancel_button.name}"'
                             f'is not the same as expected "{welcome_screen_settings.get("ctaText2")}"')
        self.assertEqual(welcome_screen.text.replace('\n', '').replace(' ', ''),
                         cleanhtml(welcome_screen_settings.get('pageText1'), clean_buttons=True).replace('you&rsquo;ll', 'you’ll').replace('\n', '').replace('&euro;', '€').replace(' ', ''),
                         msg=f'Welcome screen text \n"{welcome_screen.text.replace(" ", "")}" \n'
                             f'is not the same as expected \n"{cleanhtml(welcome_screen_settings.get("pageText1"))}')
