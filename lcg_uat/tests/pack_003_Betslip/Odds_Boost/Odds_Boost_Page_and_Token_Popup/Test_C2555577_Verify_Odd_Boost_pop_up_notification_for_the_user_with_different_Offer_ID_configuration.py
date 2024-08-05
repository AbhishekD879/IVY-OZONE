import pytest
import re
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # ODD BOOST offers can not be granted on Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2555577_Verify_Odd_Boost_pop_up_notification_for_the_user_with_different_Offer_ID_configuration(BaseBetSlipTest):
    """
    TR_ID: C2555577
    NAME: Verify 'Odd Boost' pop-up notification for the user with different  'Offer ID' configuration
    DESCRIPTION: This test case verifies User closes login notification
    PRECONDITIONS: Enable "Odds Boost" Feature Toggle in CMS > Odds Boost
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load app
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user

    def test_000_preconditions(self):
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)

        self.site.login(self.username)
        self.site.wait_content_state(state_name="Homepage")
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        odds_boost_item = self.site.right_menu.items_as_ordered_dict.get(
            vec.bma.EXPECTED_RIGHT_MENU.odds_boosts)
        self.assertTrue(odds_boost_item, msg='"Odds Boost" item is not present in righrt menu.')
        self.__class__.before_odds_boost_count = odds_boost_item.badge_text
        self.site.right_menu.logout()
        self.site.wait_logged_out(timeout=10)

    def test_001_log_in_to_application_by_user_with_generated_odds_boost_token(self,odd_value=1):
        """
        DESCRIPTION: Log in to Application by user with generated Odds boost token
        EXPECTED: * User is logged in successfully
        EXPECTED: * OddsBoost token ID is displayed in Local storage
        EXPECTED: * The "Odds Boost" token notification is displayed
        EXPECTED: * ContentText1:'You have 1 Odds Boost available' (1 is a value specific to the user as fetched on login)
        EXPECTED: * On the login journey, this should be **last** notification in the queue to appear - after any login messages, onboarding, touch ID etc.
        """
        self.ob_config.grant_odds_boost_token(self.username, token_value=1)
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.__class__.odds_boost_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=40)
        self.assertTrue(self.odds_boost_dialog,
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_ODDS_BOOST}" dialog is not displayed')
        if self.brand == 'bma':
            actual_content = self.odds_boost_dialog.description.split('\n')[0]
        else:
            actual_content = self.odds_boost_dialog.description.split('\n')[1]
        expected_content = f"You Have {str(int(self.before_odds_boost_count)+odd_value)} Odds Boosts Available"
        self.assertTrue(re.search(expected_content, actual_content),
                        msg=f'Actual content: "{actual_content}" is not equal with the'
                            f'Expected content: "{expected_content}"')
        self.odds_boost_dialog.header_object.close_button.click()

    def test_002_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")

    def test_003_login_into_application_by_the_same_user_and_verify_that_odds_boost_token_notification_is_not_displaying(self):
        """
        DESCRIPTION: Login into Application by the same user and verify that "Odds Boost" token notification is NOT displaying
        EXPECTED: * User is logged in successfully
        EXPECTED: * The "Odds Boost" token notification is not displayed
        """
        self.site.login(username=self.username)
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=2)
        self.assertFalse(dialog,
                         msg='"Odds Boost" dialog should not be displayed on the screen')

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        self.test_002_log_out_from_application()

    def test_005_add_new_odds_boost_token_for_the_same_user_in_httpbackoffice_tst2coralcoukoffice_see_precondition(self):
        """
        DESCRIPTION: Add New Odds Boost token for the same user in http://backoffice-tst2.coral.co.uk/office (see precondition)
        EXPECTED: New Odds Boost token is added for this user
        """
        self.test_001_log_in_to_application_by_user_with_generated_odds_boost_token(odd_value=2)

    def test_006_login_into_application_with_the_same_user(self):
        """
        DESCRIPTION: Login into Application with the same user
        EXPECTED: * The "Odds Boost" token notification is displayed
        EXPECTED: * ContentText1:'You have 2 Odds Boost available' (2 is a value specific to the user as fetched on login)
        EXPECTED: * New Odd Boost OfferId (added in backoffice) is saved in Local Storage under the previous one
        """
        # Covered in Step 5
