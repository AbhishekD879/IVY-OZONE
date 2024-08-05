import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@pytest.mark.module_ribbon
@pytest.mark.adhoc_suite
@pytest.mark.lad_prod
@vtest
class Test_C65940569_MRT__Verify_the_5_A_side_tab_display_and_navigationLads(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65940569
    NAME: MRT - Verify the 5-A-side tab display and navigation(Lads)
    DESCRIPTION: This test case is to verify the 5-A-side tab display and navigation
    DESCRIPTION: -
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for module ribbon tab in the CMS
    PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
    PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
    PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Module ribbon tab title
    PRECONDITIONS: -Directive name option from dropdown like Featured, Coupon,In-play, Live stream,Multiples, next races, top bets, Build your bet
    PRECONDITIONS: -id as - 5ASL
    PRECONDITIONS: -URL as - https://beta-sports.ladbrokes.com/5-a-side/lobby
    PRECONDITIONS: -Click on "Create" CTA button
    PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -IOS
    PRECONDITIONS: -Android
    PRECONDITIONS: -Windows Phone
    PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
    PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
    PRECONDITIONS: -Click on "Save changes" button
    PRECONDITIONS: 6)Check "Tutorial overlay" in 5-A-side-->Leaderboard Tutorial overlay
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: checking whether show down overlay is enable or disable
        PRECONDITIONS: creating contest for 5-A-SIDE to validate tutorials.
        """
        # getting all showdown overlay data and checking whether showdown overlay is enable or disable
        self.__class__.cms_overlay_response = self.cms_config.get_show_down_overlay()

        # if showdown overlay is disable, making it enable in cms
        if not self.cms_overlay_response['overlayEnabled']:
            self.cms_config.enable_disable_show_down_overlay(enabled=True)

        # creating 5-A-SIDE contest in cms
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.contest_name = f"Auto_test_{event_name}_C65271569"
        self.__class__.contest_response = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                                                       description="auto_test_five_a_side_contest",
                                                                                       entryStake="0.10",
                                                                                       size="10",
                                                                                       teams="10", event_id=event_id,
                                                                                       isInvitationalContest=True,
                                                                                       isPrivateContest=False)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage')

    def test_002_click_on_5_a_side_tab(self):
        """
        DESCRIPTION: Click on 5-A-side tab
        EXPECTED: 5-A-side Lobby should be displayed.[Welcome tutorial will be displayed on initial load]
        """
        # checking whether 5-A-SIDE is enabled or disable in cms
        # if 5-A-SIDE tab is not there in cms module ribbon tabs, creating 5-A-SIDE tab in mrt in cms
        five_a_side_tab = next(
            (tab_data for tab_data in self.cms_config.module_ribbon_tabs.all_tabs_data if
             tab_data['title'].upper() == '5-A-SIDE'), None)
        if not five_a_side_tab:
            self.cms_config.module_ribbon_tabs.create_tab(title='5-A-SIDE',
                                                          directive_name='Featured',
                                                          internal_id='5ASL',
                                                          url='https://beta-sports.ladbrokes.com/5-a-side/lobby',
                                                          universalSegment=True
                                                          )
            self.cms_config.module_ribbon_tabs._created_tabs.pop()

        # checking whether 5-A-SIDE is there in module ribbon tabs or not in homepage
        five_a_side_tab = next(
            (tab for tab_name,tab in self.site.home.tabs_menu.items_as_ordered_dict.items() if tab_name.upper() == '5-A-SIDE'), None)
        five_a_side_tab.click()
        self.site.wait_content_state_changed(timeout=20)

    def test_003_click_on_get_started_button_in_welcome_tutorial(self):
        """
        DESCRIPTION: Click on "Get Started" Button in Welcome tutorial
        EXPECTED: Lobby Tutorial should be displayed
        """
        actual_header_title = wait_for_result(lambda:self.site.five_a_side_lobby.header_title.upper(),
                                              name="waiting for the next page to open and get title"
                                              ,bypass_exceptions=VoltronException)
        expected_header_title = self.cms_overlay_response['headerTitle'].upper()
        self.assertEqual(actual_header_title, expected_header_title, msg=f'actual header title {actual_header_title} '
                                                                         f'is not equal to expected header title {expected_header_title}')
        actual_section_title = self.site.five_a_side_lobby.section_title.upper()
        expected_section_title = self.cms_overlay_response['sectionTitle'].upper()
        self.assertEqual(actual_section_title, expected_section_title,
                         msg=f'actual section title {actual_header_title} '
                             f'is not equal to expected section title {expected_section_title}')
        actual_preview_title = self.site.five_a_side_lobby.preview_title.upper()
        expected_preview_title = self.cms_overlay_response['previewTitle'].upper()
        self.assertEqual(actual_section_title, expected_section_title,
                         msg=f'actual preview title {actual_preview_title} '
                             f'is not equal to expected preview title {expected_preview_title}')
        self.site.five_a_side_lobby.get_started_button.click()

    def test_004_verify__screens_of_lobby_tutorial(self):
        """
        DESCRIPTION: Verify  screens of Lobby tutorial
        EXPECTED: Continue tutorial by clicking on next button. Finish the Tutorial by clicking on Finish button
        """
        wait_for_result(lambda: self.site.five_a_side_lobby.welcome_header is not None, name="waiting for the next page to open")
        actual_welcome_header = self.site.five_a_side_lobby.welcome_header.upper()
        expected_welcome_header = self.cms_overlay_response['plWelcomeTitle'].upper()
        self.assertEqual(actual_welcome_header, expected_welcome_header,
                         msg=f'actual welcome header {actual_welcome_header} '
                             f'is not equal to expected welcome header {expected_welcome_header}')
        actual_welcome_line_1 = self.site.five_a_side_lobby.welcome_line_1.upper()
        expected_welcome_line_1 = self.cms_overlay_response['lobbyWelcome1'].upper()
        self.assertEqual(actual_welcome_line_1, expected_welcome_line_1,
                         msg=f'actual welcome line 1 {actual_welcome_line_1} '
                             f'is not equal to expected welcome line 1 {expected_welcome_line_1}')
        actual_welcome_line_2 = self.site.five_a_side_lobby.welcome_line_2.upper()
        expected_welcome_line_2 = self.cms_overlay_response['lobbyWelcome2'].upper()
        self.assertEqual(actual_welcome_line_2, expected_welcome_line_2,
                         msg=f'actual welcome line 2 {actual_welcome_line_2} '
                             f'is not equal to expected welcome line 2 {expected_welcome_line_2}')
        actual_welcome_line_3 = self.site.five_a_side_lobby.welcome_line_3.upper()
        expected_welcome_line_3 = self.cms_overlay_response['lobbyWelcome3'].upper()
        self.assertEqual(actual_welcome_line_3, expected_welcome_line_3,
                         msg=f'actual welcome line 3 "{actual_welcome_line_3}" '
                             f'is not equal to expected welcome line 3 "{expected_welcome_line_3}"')
        wait_for_result(lambda: self.site.five_a_side_lobby.lobby_next_button is not None, name="waiting for the click button")
        self.site.five_a_side_lobby.lobby_next_button.click()
        wait_for_haul(20)
        actual_entry_info_title = self.site.five_a_side_lobby.entry_info_title.upper()
        expected_entry_info_title = self.cms_overlay_response['lobbyEntryInfo'].upper()
        self.assertEqual(actual_entry_info_title, expected_entry_info_title,
                         msg=f'actual entry info title {actual_entry_info_title} '
                             f'is not equal to expected entry info title {expected_entry_info_title}')
        wait_for_result(lambda: self.site.five_a_side_lobby.lobby_next_button, name="waiting for lobby next button to display")
        self.site.five_a_side_lobby.lobby_next_button.click()
        wait_for_haul(20)
        actual_showdown_card_title = self.site.five_a_side_lobby.showdown_card_title.upper()
        expected_showdown_card_title = self.cms_overlay_response['lobbyShowdownCardInfo'].upper()
        self.assertEqual(actual_showdown_card_title, expected_showdown_card_title,
                         msg=f'actual showdown card title "{actual_showdown_card_title}" '
                             f'is not equal to expected showdown card title "{expected_showdown_card_title}"')
        wait_for_result(lambda: self.site.five_a_side_lobby.finish_button, name="waiting for finish button to display")
        self.site.five_a_side_lobby.finish_button.click()

    def test_005_verify_by_clicking_on_contest(self):
        """
        DESCRIPTION: Verify by clicking on Contest
        EXPECTED: Pre Event overlay tutorial should be displayed
        """
        contests = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.items()
        contest = next((contest for contest_name, contest in contests if contest_name.upper() == self.contest_response['name'].upper()), None)
        contest.click()
        self.site.wait_content_state_changed(timeout=20)

    def test_006_verify_screens_of_pre_event_tutorial(self):
        """
        DESCRIPTION: Verify  screens of Pre Event tutorial
        EXPECTED: Continue tutorial by clicking on next button. Finish the Tutorial by clicking on Finish button
        """
        actual_welcome_page_title = wait_for_result(lambda: self.site.five_a_side_leaderboard.welcome_page_title.upper(),
                                                    name="waiting for next page and welcome page title",
                                                    bypass_exceptions=VoltronException)
        expected_welcome_page_title = self.cms_overlay_response['liveHeaderTitle'].upper()
        self.assertEqual(actual_welcome_page_title, expected_welcome_page_title,
                         msg=f'actual welcome page title {actual_welcome_page_title} '
                             f'is not equal to expected welcome title title {expected_welcome_page_title}')
        actual_welcome_page_content = self.site.five_a_side_leaderboard.welcome_page_content.upper()
        expected_welcome_page_content = self.cms_overlay_response['liveSectionTitle'].upper()
        self.assertEqual(actual_welcome_page_content, expected_welcome_page_content,
                         msg=f'actual welcome page content {actual_welcome_page_content} '
                             f'is not equal to expected welcome title content {expected_welcome_page_content}')
        actual_welcome_page_footer = self.site.five_a_side_leaderboard.welcome_page_footer.upper()
        expected_welcome_page_footer = self.cms_overlay_response['liveFooterTitle'].upper()
        self.assertEqual(actual_welcome_page_footer, expected_welcome_page_footer,
                         msg=f'actual welcome page footer {actual_welcome_page_footer} '
                             f'is not equal to expected welcome title footer {expected_welcome_page_footer}')
        self.site.five_a_side_leaderboard.pre_event_next_button.click()
        wait_for_result(lambda: self.site.five_a_side_leaderboard.rules_entry_information, name="waiting for next page and rules entry information")
        actual_rules_entry_information = self.site.five_a_side_leaderboard.rules_entry_information.upper()
        expected_rules_entry_information = self.cms_overlay_response['plRulesEntryInfo'].upper()
        self.assertEqual(actual_rules_entry_information, expected_rules_entry_information,
                         msg=f'actual rules entry info {actual_rules_entry_information} '
                             f'is not equal to expected rules entry info {expected_rules_entry_information}')
        self.site.five_a_side_leaderboard.rei_next_button.click()
        wait_for_result(lambda: self.site.five_a_side_leaderboard.build_team_information, name="waiting for next page and build team information")
        actual_build_team_information = self.site.five_a_side_leaderboard.build_team_information.upper()
        expected_build_team_information = self.cms_overlay_response['plBuildTeamInfo'].upper()
        self.assertEqual(actual_build_team_information, expected_build_team_information,
                         msg=f'actual build team info {actual_build_team_information} '
                             f'is not equal to expected build team info {expected_build_team_information}')
        self.site.five_a_side_leaderboard.bti_next_button.click()
        wait_for_result(lambda: self.site.five_a_side_leaderboard.rules_button_information, name="waiting for next page and rules button informatrion")
        actual_rules_button_info = self.site.five_a_side_leaderboard.rules_button_information.upper()
        expected_rules_button_info = self.cms_overlay_response['plBulesButtonInfo'].upper()
        self.assertEqual(actual_rules_button_info, expected_rules_button_info,
                         msg=f'actual rules button info {actual_rules_button_info} '
                             f'is not equal to expected rules button info {expected_rules_button_info}')
        self.site.five_a_side_leaderboard.rbi_finish_button.click()

    def test_007_verify_5_a_side_contest_details(self):
        """
        DESCRIPTION: Verify 5-A-side contest details
        EXPECTED: user able to see details of contest which are configured in CMS
        """
        # verifying description in contest as per cms in FE
        actual_contest_name = self.site.five_a_side_leaderboard.contest_name.upper()
        expected_contest_name = self.contest_response['description'].upper()
        self.assertEqual(actual_contest_name, expected_contest_name, msg=f'Actual contest name "{actual_contest_name}"'
                                                                         f'is not same as expected contest name "{expected_contest_name}"')
        # verifying max entries in contest as per cms in FE
        actual_max_entries = self.site.five_a_side_leaderboard.total_entries.text
        expected_max_entries = self.contest_response['maxEntries']
        self.assertIn(expected_max_entries, actual_max_entries, msg=f'expected max entries "{expected_max_entries} '
                                                                    f'is not in actual max entries "{actual_max_entries}"')
        # verifying entries per user in contest as per cms in FE
        actual_entries_per_user = self.site.five_a_side_leaderboard.total_entries.text
        expected_entries_per_user = self.contest_response['maxEntriesPerUser']
        self.assertIn(expected_entries_per_user, actual_entries_per_user, msg=f'expected max entries "{expected_entries_per_user} '
                                                                              f'is not in actual max entries "{actual_entries_per_user}"')

    def test_008_verify_live_leaderboard(self):
        """
        DESCRIPTION: Verify Live Leaderboard
        EXPECTED: Once event is live, Live Leaderboard tutorial should be displayed and can see updates of particular event.
        """
        # Cannot be automated Live contests in 5-A-SIDE

    def test_009_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: 5-A-side contests will not be seen in Lobby[For test users]
        EXPECTED: 5-A-side contests will  be seen in Lobby[For Real users]
        """
        # cannot automate for real user whether contests are visible or not after logout
        self.site.logout()
        five_a_side_tab = next((tab for tab_name, tab in self.site.home.tabs_menu.items_as_ordered_dict.items() if tab_name.upper() == '5-A-SIDE'), None)
        five_a_side_tab.click()
        self.site.wait_content_state_changed()
        sections = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict
        self.assertFalse(sections, msg='5-A-side contests are visible in Lobby')
