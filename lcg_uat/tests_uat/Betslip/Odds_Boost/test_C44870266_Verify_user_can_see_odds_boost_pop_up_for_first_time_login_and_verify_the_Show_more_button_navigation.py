import pytest
import tests
import re
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.lad_prod
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870266_Verify_user_can_see_odds_boost_pop_up_for_first_time_login_and_verify_the_Show_more_button_navigation(Common):
    """
    TR_ID: C44870266
    NAME: Verify user can see odds boost pop up for first time login and verify the 'Show more' button navigation.
    PRECONDITIONS: Load application and Login into the application
    """
    keep_browser_open = True

    def test_001_login_into_application_by_user_with_generated_odds_boost_token(self):
        """
        DESCRIPTION: Login into Application by user with generated Odds boost token
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed (as overlay on Mobile, Tablet and as pop-up on Desktop)
        EXPECTED: ContentText1:'You have XX Odds Boost available' (1 is a value specific to the user as fetched on login)
        EXPECTED: On the login journey, this should be last* notification in the queue to appear - after any login messages, onboarding, touch ID etc.
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)

        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        dialog.username = tests.settings.odds_boost_user
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            self.site.close_all_dialogs(async_close=False, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        except Exception as e:
            self._logger.warning(e)
        odds_boost_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertTrue(odds_boost_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_ODDS_BOOST}" dialog is not displayed')
        actual_content = odds_boost_dialog.description
        expected_content = "You Have \d* Odds Boosts Available"
        self.assertTrue(re.search(expected_content, actual_content),
                        msg=f'Actual content: "{actual_content}" is not equal with the'
                            f'Expected content: "{expected_content}"')
        odds_boost_dialog.show_more_button.click()
        self.site.wait_content_state('oddsboost')
