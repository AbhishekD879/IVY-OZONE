import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


#@pytest.mark.crl_tst2  # yourcall out of scope for roxanne
#@pytest.mark.crl_stg2  # test case is not up date
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.football
@pytest.mark.competitions
@pytest.mark.mocked_data
@pytest.mark.cms
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-49502')
@pytest.mark.na
@vtest
class Test_C713686_Displaying_of_yourcall_icons_on_Football_Competitions(BaseBanachTest):
    """
    TR_ID: C713686
    VOL_ID: C9697692
    NAME: Displaying of yourcall icons on Football Competitions
    DESCRIPTION: This test case verifies logic of displaying of +B icons (BuildYourBet) on Сompetitions tab on Football page
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues (competitions) are added and turned on in YourCall page in CMS
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded and Competitions tab on Football page is opened
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    """
    keep_browser_open = True
    your_call_competition_name = 'ENGLAND'
    your_call_league_name = 'Premier League'
    competition_name = tests.settings.football_autotest_competition
    league_name = tests.settings.football_autotest_competition_league
    competition = None
    competitions = None
    league = None

    def verify_yourcall_icon(self, competition_name, league_name, expected_result=True):
        self.assertIn(competition_name, self.competitions,
                      msg=f'"{competition_name}" is not present in competitions list "{self.competitions.keys()}"')

        competition = self.competitions[competition_name]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(league_name.title(), leagues,
                      msg=f'"{league_name.title()}" is not present in leagues list "{leagues.keys()}"')

        self.__class__.league = leagues[league_name.title()]
        self.assertTrue(self.league.has_your_call_icon(expected_result=expected_result) is expected_result,
                        msg=f'Yourcall icon status on League "{league_name}" does not match expected result. '
                            f'Expected result: "{expected_result}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get OB event to use in mock service
        """
        self.create_ob_event_for_mock()

    def test_001_turned_on_required_yourcall_league_in_cms(self):
        """
        DESCRIPTION: Check if required #YourCall league enabled in CMS and turn it on if not
        DESCRIPTION: Check 'enableIcon' checkbox in CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon'
        """
        self.cms_config.your_call_league_switcher()
        self.cms_config.update_yourcall_icons_tabs()

    def test_002_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name="FOOTBALL")
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competitions tab is not active, active is "{active_tab}"')

    def test_003_within_expanded_class_accordions_observe_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Within expanded class accordions observe league (competition), that is returned from DS
        EXPECTED: '#' (yourcall icon) is displayed for appropriate competition on the right
        """
        self.__class__.competitions = \
            self.site.contents.tab_content.competitions_categories.items_as_ordered_dict
        self.assertTrue(self.competitions, msg='No competitions are present on page')
        self.verify_yourcall_icon(self.your_call_competition_name, self.your_call_league_name, expected_result=True)

    def test_004_click_on_any_league_competition(self):
        """
        DESCRIPTION: Click on any competition and Click 'Change Competition'
        """
        self.league.click()
        self.site.competition_league.title_section.competition_selector_link.click()

    def test_005_select_a_competition_group_class_from_the_list_that_contain_league_competition_from_step_1(self):
        """
        DESCRIPTION: Select a competition group(class) from the list that contain competition from step #1
        EXPECTED: * List of competitions within this group are shown
        EXPECTED: * '#' (yourcall icon) is displayed for appropriate competition on the right
        """
        competitions = self.site.competition_league.competition_list.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')

        self.assertIn(self.your_call_competition_name.upper(), competitions,
                      msg=f'"{self.your_call_competition_name.upper()}" is not present'
                          f' in competitions "{competitions.keys()}"')

        competition = competitions[self.your_call_competition_name.upper()]

        wait_for_result(lambda: self.your_call_league_name.title() in competition.items_as_ordered_dict,
                        name='Leagues list is loaded',
                        timeout=3,
                        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException)
                        )
        leagues = competition.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(self.your_call_league_name.title(), leagues,
                      msg=f'"{self.your_call_league_name.title()}" is not present in leagues "{leagues.keys()}"')

        league = leagues[self.your_call_league_name]
        self.softAssert(self.assertTrue, league.has_your_call_icon(),
                        msg=f'YourCall icon status on League {self.your_call_league_name} does not '
                        f'match expected result. Expected result: True')

    def test_006_repeat_steps_1_4_for_league_competition_that_is_added_and_enabled_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Repeat steps #1-4 for competition, that is NOT returned from Banach
        EXPECTED: '#' (yourcall icon) is NOT displayed
        """
        self.navigate_to_page(name='/')
        self.test_002_tap_sport()
        self.__class__.competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.competitions, msg='No competitions are present on page')
        self.verify_yourcall_icon(competition_name=self.competition_name, league_name=self.league_name,
                                  expected_result=False)
        self.league.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        self.site.competition_league.title_section.competition_selector_link.click()

        competitions = self.site.competition_league.competition_list.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')

        self.assertIn(self.competition_name.upper(), competitions,
                      msg=f'"{self.competition_name.upper()}" is not present in competitions "{competitions.keys()}"')

        competition = competitions[self.competition_name.upper()]
        competition.click()
        wait_for_result(lambda: self.your_call_league_name.title() in competition.items_as_ordered_dict,
                        name='Leagues list is loaded',
                        timeout=3,
                        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException)
                        )
        leagues = competition.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(self.league_name.title(), leagues,
                      msg=f'"{self.league_name.title()}" is not present in leagues "{leagues.keys()}"')

        league = leagues[self.league_name.title()]
        self.assertFalse(league.has_your_call_icon(expected_result=False),
                         msg=f'Yourcall icon status on League "{self.league_name}" does not match expected result. '
                             'Expected result: False')
