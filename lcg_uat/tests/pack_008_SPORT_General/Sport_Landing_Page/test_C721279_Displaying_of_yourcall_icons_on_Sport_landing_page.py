import pytest

from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # Coral Only
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.football
@pytest.mark.banach
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-2330')
class Test_C721279_Displaying_of_yourcall_icons_on_Sport_landing_page(BaseBanachTest):
    """
    TR_ID: C721279
    NAME: Displaying of yourcall icons on Sport landing page
    DESCRIPTION: This test case verifies logic of displaying of #yourcall or +B (BuildYourBet for Football only) icons on Sport Landing pages
    PRECONDITIONS: * Pre-match sport events with different start times of leagues with and without DS/Banach events available are created in OpenBet
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues leagues (competitions) are added and turned on in YourCall page in CMS
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    """
    keep_browser_open = True
    yc_league_name = None
    not_yc_league_name = None

    def get_league_section(self, league):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No sections present on page')
        self.assertIn(league, sections.keys(),
                      msg='League section: "%s" not found in sections list: ["%s"]'
                          % (league, ', '.join(sections.keys())))
        return sections[league]

    def verify_yourcall_icon_displaying_for_league(self, league, is_icon_displayed=True):
        # TODO - needs to be revisited after VOL-2330
        result = wait_for_result(lambda: league.group_header.has_byb_icon(),
                                 name="Yourcall icon to display",
                                 expected_result=is_icon_displayed,
                                 timeout=3)
        if is_icon_displayed:
            self.assertTrue(result, msg=f'YourCall icon "#" is not displayed for "{league.group_header.title_text}"')
        else:
            self.assertFalse(result, msg=f'YourCall icon "#" is displayed for "{league.group_header.title_text}"')
        icons_count = 1 if is_icon_displayed else 0
        if league.group_header.icons_count > icons_count:
            self.assertTrue(league.group_header.has_cash_out_mark(),
                            msg=f'League section "{league.group_header.title_text}" has no cash out icon')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if required #YourCall league enabled in CMS and turn it on if not
        DESCRIPTION: Check 'enableIcon' checkbox in CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon'
        DESCRIPTION: Create test events with #YourCall special markets available
        """
        self.cms_config.your_call_league_switcher()
        self.cms_config.update_yourcall_icons_tabs()

        event_params = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.yc_league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        self.ob_config.add_football_event_to_autotest_league2()
        self.__class__.eventID2 = event_params.event_id
        event_resp2 = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                                query_builder=self.ss_query_builder)
        self.__class__.event_name2 = normalize_name(event_resp2[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name2}"')

        self.__class__.not_yc_league_name = self.get_accordion_name_for_event_from_ss(event=event_resp2[0])

    def test_001_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to Sport landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_002_observe_section_header_accordion_of_league_that_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that are added and enabled in CMS and returned from DS
        EXPECTED: 'B+' (yourcall icon) is displayed on the right of module accordion/header for all sections
        EXPECTED: In case cash out icon is displayed, yourcall icon is displayed before it
        EXPECTED: 'Build your bet' icon is not present on League level, only on event card
        """
        yc_league_section = self.get_league_section(league=self.yc_league_name)
        self.verify_yourcall_icon_displaying_for_league(league=yc_league_section, is_icon_displayed=False)

        event = self.get_event_from_league(event_id=self.eventID, section_name=self.yc_league_name)
        self.assertTrue(event.has_byb_icon(),
                        msg=f'\'B+\' (yourcall icon) icon is not shown in: "{self.yc_league_name}"')

    def test_003_observe_section_header_accordion_of_league_that_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that are added and enabled in CMS and NOT returned from DS
        EXPECTED: 'B+' (yourcall icon) is not displayed
        """
        not_yc_league_section = self.get_league_section(league=self.not_yc_league_name)
        self.verify_yourcall_icon_displaying_for_league(league=not_yc_league_section, is_icon_displayed=False)
