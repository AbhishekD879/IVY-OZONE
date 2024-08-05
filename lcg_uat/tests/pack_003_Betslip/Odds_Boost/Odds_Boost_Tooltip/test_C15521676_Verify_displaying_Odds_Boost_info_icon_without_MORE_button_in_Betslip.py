import pytest
from tests.base_test import vtest
import tests
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant odds in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C15521676_Verify_displaying_Odds_Boost_info_icon_without_MORE_button_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C15521676
    NAME: Verify displaying Odds Boost info icon without MORE button in Betslip
    DESCRIPTION: This test case verifies that odds boost info icon is shown without MORE button in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Odds Boost tokens is added for USER1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 'More Link' is is empty in CMS for Odds Boost section
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add selection to the Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with a user and add selection to betslip
        """
        username = tests.settings.odds_boost_user
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None or odds_boost['moreLink'] is not None:
            self.cms_config.update_odds_boost_config(enabled=True)
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_ids = event.selection_ids[event.team1]
        self.ob_config.grant_odds_boost_token(username=username)
        self.site.login(username)
        self.open_betslip_with_selections(selection_ids=selection_ids)

    def test_001_navigate_to_betslipverify_that_i_icon_is_displaying_in_odds_boost_section(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'i' icon is displaying in odds boost section
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - Odds Boost header text
        EXPECTED: - Tap to Boost your betslip text with 'i' icon
        """
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')
        self.assertTrue(self.odds_boost_header.boost_button,
                        msg='"BOOST" button is not displayed')
        self.assertTrue(self.odds_boost_header.info_button,
                        msg='"INFO" icon is not displayed')
        self.assertTrue(self.odds_boost_header.odds_boost_label,
                        msg='"odds Boost" header text is not displayed')
        self.assertTrue(self.odds_boost_header.tap_to_boost_your_betslip_label,
                        msg=' "Tap to Boost" your betslip text')

    def test_002_tap_i_iconverify_that_the_tooltip_style_popup_is_displayed(self):
        """
        DESCRIPTION: Tap 'i' icon
        DESCRIPTION: Verify that the tooltip style popup is displayed
        EXPECTED: Popup with appropriate elements:
        EXPECTED: - Hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        EXPECTED: - 'Ok' button
        EXPECTED: - 'More' button is NOT shown
        """
        self.odds_boost_header.info_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP)
        self.assertTrue(self.dialog,
                        msg='"Odds Boost" dialog box not appeared')
        description = self.dialog.description.replace("\n\n", " ")
        self.assertEqual(vec.odds_boost.INFO_DIALOG.text, description,
                         msg=f' Actual text: "{description}" is not same as '
                             f' Expected text: "{vec.odds_boost.INFO_DIALOG.text}".')
        self.assertTrue(self.dialog.has_ok_button(),
                        msg='"Ok" button not displayed')
        self.assertFalse(self.dialog.has_more_button(expected_result=False),
                         msg='"More Button" is displayed')

    def test_003_tap_ok_buttonverify_that_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that popup is closed
        EXPECTED: Popup is closed
        """
        self.dialog.ok_button.click()
        popup_closed = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP, timeout=5)
        self.assertFalse(popup_closed,
                         msg='"Odds Boost" popup is not closed')
