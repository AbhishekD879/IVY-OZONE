import pytest
import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.lad_stg2 # one two free is not available in lower env
# @pytest.mark.lad_tst2 # one two free is not available in lower env
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.other
@pytest.mark.reg156_fix
@vtest
class Test_C57732107_Verify_data_retrieving_from_CMS_to_Current_Tab(Common):
    """
    TR_ID: C57732107
    NAME: Verify data retrieving from CMS to 'Current Tab'
    DESCRIPTION: This test case verifies data retrieving from CMS to 'Current Tab'
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Please look for some insights on a pages as follow:
        PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
        PRECONDITIONS: 1. The user is logged in to CMS
        PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
        PRECONDITIONS: 3. User opens 'Game view'
        PRECONDITIONS: 4. User open Detail View for existing game
        """
        username = tests.settings.betplacement_user
        self.site.login(username)
        self.navigate_to_page('1-2-free')
        self.assertTrue(self.site.one_two_free.one_two_free_welcome_screen.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')

    def test_001_populate_all_existing_fields_with_valid_data_and_save_it_in_game_detail_view_and__in_cms(self):
        """
        DESCRIPTION: Populate all existing fields with valid data and save it in Game Detail View and  in CMS
        EXPECTED: All changes are saved successfully
        """
        cms_games_tab_details = self.cms_config.get_one_two_free_games_tab_details()[0]
        self.assertTrue(cms_games_tab_details,
                        msg=f'CMS games data is available.')

    def test_002_open_current_tab_on_1_2_free_uisee_howplustoplusrunplusunpublishedplusqubitplusvariationplusonplusladbrokes_documentation_in_preconditions(
            self):
        """
        DESCRIPTION: Open 'Current Tab' on 1-2-Free UI
        DESCRIPTION: (see How+to+run+unpublished+Qubit+variation+on+Ladbrokes documentation in preconditions)
        EXPECTED: All data retrieved from CMS and displayed
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text-> Current page-> pageText1)
        EXPECTED: - 'Deadline missed' messages (Static text-> Current page-> pageText3)
        EXPECTED: - 'Already Played' messages (Static text-> Current page-> pageText4)
        EXPECTED: - Submit (Static text-> Current page-> ctaText1)
        EXPECTED: - Events(CMS->Active game):
        EXPECTED: - Event number: *e.g. Match 1*
        EXPECTED: - Date of event: *e.g. 15:00 MON*
        EXPECTED: - Team name *Liverpool*
        EXPECTED: - Team kits
        EXPECTED: - Event TV icon *BBC*
        EXPECTED: All data successfully styled
        """
        one_two_free = self.site.one_two_free
        wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                        timeout=15)
        one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                            expected_result=True),
                                        timeout=15)
        self.assertTrue(one_two_free.one_two_free_current_screen.close.is_displayed(),
                        msg='Close button not displayed on one two free')
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        static_text = self.cms_config.get_one_two_free_static_texts()[1]

        ui_expan_collapse_text = one_two_free.one_two_free_current_screen.already_entered_text.text.split('\n')[0]
        cms_expand_collapse_text = \
        static_text['pageText1'].split('<p>')[1].split('<strong>')[1].split('</strong>')[0]

        # deadline_missed_msg = static_text['pageText3'].split('1-2')[0].split("<p>")[1]
        # TODO as data is not available we can not add UI validation for deadline missed message

        cms_already_Played_text = static_text['pageText4'].split('1-2')[0].split('>')[1]
        ui_already_Played_text = \
            self.site.one_two_free.one_two_free_current_screen.already_entered_text.text.split('1-2')[0].strip()

        if ui_expan_collapse_text == cms_expand_collapse_text:
            self.assertEqual(ui_expan_collapse_text, cms_expand_collapse_text,
                             msg=f'Actual message "{ui_expan_collapse_text}" '
                                 f'is not the same as expected "{cms_expand_collapse_text}"')
        else:
            self.assertEqual(ui_already_Played_text.rstrip().lstrip(), cms_already_Played_text,
                             msg=f'Actual message "{ui_already_Played_text.rstrip()}" '
                                 f'is not the same as expected "{cms_already_Played_text}"')

        cms_submit_button_text = static_text['ctaText1'].split('1-2')[0]
        ui_submit_button_text = one_two_free.one_two_free_current_screen.submit_button.name
        self.assertEqual(cms_submit_button_text, ui_submit_button_text,
                         msg=f'Actual message "{ui_submit_button_text}" '
                             f'is not the same as expected "{cms_submit_button_text}"')

        matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for match in matches:
            self.assertTrue(match.match_start_date,
                            msg=f'match start time is not displayed for "{match.name}".')
            for shirt in list(match.items_as_ordered_dict.values()):
                self.assertTrue(shirt.silk_icon.is_displayed(),
                                msg=f' Teams t-shirts not displayed for "{match.name}".')
                self.assertTrue(shirt.name,
                                msg=f'Team names not displayed for "{match.name}".')

            score_switchers = match.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.decrease_score_down_arrow.is_displayed(),
                                msg=f'Down arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.score,
                                msg=f'Score is not displayed for "{match.name}".')
