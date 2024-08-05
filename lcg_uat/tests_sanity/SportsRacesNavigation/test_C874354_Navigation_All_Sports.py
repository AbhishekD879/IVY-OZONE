import re
import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.all_sports
@pytest.mark.navigation
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C874354_Navigation_All_Sports(Common):
    """
    TR_ID: C874354
    NAME: Navigation All Sports
    DESCRIPTION: Verify that all sports are listed on "All Sports" page in alphabetical order
    DESCRIPTION: **NOTE:**
    DESCRIPTION: * Also, displaying of a Sport in 'A-Z Competitions' & 'Top Sports' sections based on availability of OB events
    DESCRIPTION: * To check whether events are available for a CategoryId:
    DESCRIPTION: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Event/?simpleFilter=event.categoryId:equals:{ID}&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.suspendAtTime:greaterThanOrEqual:YYYY-MM-DDTHH:MM:00.000&includeUndisplayed=false
    DESCRIPTION: * Displaying of a Sport depends on "hasEvents"="true/false" parameter received in "initial-data" response > sportCategories
    PRECONDITIONS: 1. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Football' with 'CategoryId'=16)
    PRECONDITIONS: - Events are available for a Category in Open Bet
    PRECONDITIONS: 2. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Darts' with 'CategoryId'=13)
    PRECONDITIONS: - Events are NOT available for a Category in Open Bet
    PRECONDITIONS: 3. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Non Open Bet 'CategoryId' e.g. Player Bets
    PRECONDITIONS: 4. 'Top Sports' are configured in CMS for some Sports e.g. Football, Horse Racing, Greyhounds
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Is Top Sport' check box is checked)
    PRECONDITIONS: 5. 'A-Z Sports' is configured in CMS for some Sports e.g. Basketball, Football, Greyhounds, Horse Racing etc
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 6. Make sure Connect section in A-Z is turned on in CMS: System configuration -> Connect -> menu
    PRECONDITIONS: 7. Oxygen application is loaded
    PRECONDITIONS: 8. 'All Sports' page is opened (A-Z Sports)
    """
    keep_browser_open = True
    all_sports_page = 'az-sports'
    all_sports_page_name = vec.sb.ALL_SPORTS

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Top Sports' are configured in CMS for some Sports
        PRECONDITIONS: 'A-Z Sports' is configured in CMS for some Sports
        """
        self.__class__.cms_top_sports = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                                         if all((not sport['disabled'],
                                                 sport['imageTitle'],
                                                 sport['hasEvents'],
                                                 sport['isTopSport']))]

        self.__class__.cms_az_sports_with_event = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                                                   if all((not sport['disabled'],
                                                           sport['imageTitle'],
                                                           sport['hasEvents'],
                                                           sport['showInAZ']))]
        for sport in self.cms_az_sports_with_event:
            new_string = re.sub(r'\s+', ' ', sport).strip()
            self.cms_az_sports_with_event[self.cms_az_sports_with_event.index(sport)] = new_string
        for sport in self.cms_top_sports:
            new_string = re.sub(r'\s+', ' ', sport).strip()
            self.cms_top_sports[self.cms_top_sports.index(sport)] = new_string
        if not self.cms_top_sports:
            raise CmsClientException('Top Sports are not configured in CMS for some Sports')

        if not self.cms_az_sports_with_event:
            raise CmsClientException('A-Z Sports are not configured in CMS for some Sports')

    def test_001_verify_page_header_and_back_button(self):
        """
        DESCRIPTION: Verify page header and Back button
        EXPECTED: * Page header is 'All Sports'
        EXPECTED: * Tap on Back button gets user back to previous page
        """
        self.navigate_to_page(name=self.all_sports_page)

        page_title = self.site.all_sports.header_line.page_title.title
        self.assertEqual(page_title, self.all_sports_page_name,
                         msg=f'Page header: "{page_title}" is not as expected: "{self.all_sports_page_name}"')

        self.site.back_button_click()
        self.site.wait_content_state('Homepage')

    def test_002_verify_top_sports_section(self):
        """
        DESCRIPTION: Verify 'Top Sports' section
        EXPECTED: * Section is displayed only if Top Sports are configured in CMS
        EXPECTED: * Sports are displayed in a list view
        EXPECTED: * No icon is displayed next to a Sport name
        EXPECTED: * Only Sports with the CMS setting 'is Top Sport?' are shown in this section
        EXPECTED: * Top Sports are ordered like configured in CMS (configurations made by dragging)
        """
        if self.device_type != "mobile":
            self.navigate_to_page(name=self.all_sports_page)
        else:
            footer_menu = self.cms_config.get_initial_data(cached=True).get('footerMenu')
            if not footer_menu:
                raise CmsClientException('Footer menu is not configured')
            self.__class__.all_sports_footer_item = next(
                (item['linkTitle'] for item in footer_menu if 'az-sports' in item['targetUri']), None)
            if not self.all_sports_footer_item:
                raise CmsClientException('"All Sports" is not configured for "Footer Menu"')
            footer_item_all_sports = self.all_sports_footer_item if self.brand != 'bma' else self.all_sports_footer_item.upper()
            self.__class__.all_sports_footer_button = \
                self.site.navigation_menu.get_footer_menu_item(name=footer_item_all_sports)
            self.assertTrue(self.all_sports_footer_button.is_displayed(), msg='"All Sports" button is not displayed')
            self.all_sports_footer_button.click()
        self.site.wait_content_state(state_name='AllSports')
        self.__class__.top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(self.top_sports, msg='No sports found in "Top Sports" section')

        for sport_name, sport in self.top_sports.items():
            self.assertFalse(sport.item_icon.is_displayed(expected_result=False),
                             msg=f'Sport icon for "{sport_name}" should not be displayed')

        top_sports_names = list(self.top_sports.keys())
        if self.brand == 'ladbrokes':
            if vec.SB.FANZONE in self.cms_top_sports:
                index = self.cms_top_sports.index(vec.SB.FANZONE)
                top_sports_names.insert(index, vec.SB.FANZONE)
        self.softAssert(self.assertListEqual, top_sports_names, self.cms_top_sports,
                        msg=f'Sports are not sorted in alphabetical A-Z order:'
                        f'\nActual: "{top_sports_names}"\nExpected: "{self.cms_top_sports}"')

    def test_003_verify_a_z_section(self):
        """
        DESCRIPTION: Verify 'A-Z' section
        EXPECTED: * Title is 'A-Z'
        EXPECTED: * Sports are displayed in a list view
        EXPECTED: * There are Sport name and icon
        EXPECTED: * Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        EXPECTED: * All sports are shown in alphabetical A-Z order
        """
        self.__class__.az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(self.az_sports, msg='No sports found in "A-Z Sports" section')

        for sport_name, sport in self.az_sports.items():
            self.assertTrue(sport.item_icon.is_displayed(),
                            msg=f'Sport icon for "{sport_name}" is not displayed')
            self.assertIn(sport_name, self.cms_az_sports_with_event,
                          msg=f'Sport "{sport_name}" should not be shown in the list')

    def test_004_verify_connect_section(self):
        """
        DESCRIPTION: Verify 'Connect' section
        EXPECTED: * There is the section 'Connect' at the bottom of the page
        EXPECTED: * The name of the section is 'Connect'
        EXPECTED: * Section contains list of items (that corresponds to CMS configurations) (one exception: 'User connect online' item is shown only for Logged in In-Shop user)
        EXPECTED: * 'Connect' section's items are ordered as configured in CMS:
        EXPECTED: Menu -> Connect menu
        EXPECTED: (configurations made by dragging)
        """
        # We do not validate Connect Section under A_Z sports

    def test_005_verify_sport_availability_in_a_z_categories_section_that_has_events_from_preconditions_1_eg_football(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has events (from Preconditions 1 e.g. Football)
        EXPECTED: Sport e.g. Football is available in 'A-Z Categories' section
        """
        # this is done in the scope of step 003

    def test_006_verify_sport_availability_in_a_z_categories_section_that_has_no_events_from_preconditions_2_eg_darts(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has no events (from Preconditions 2 e.g. Darts)
        EXPECTED: Sport e.g. Darts is NOT available in 'A-Z Categories' section
        """
        cms_az_sports = {sport['imageTitle'].strip(): sport['categoryId']
                         for sport in self.cms_config.get_sport_categories()
                         if all((not sport['disabled'], sport['imageTitle'], sport['showInAZ']))}

        cms_az_sports_without_event = set(cms_az_sports.keys()) - set(self.cms_az_sports_with_event)

        selected_sport_without_event = list(cms_az_sports_without_event)[0]

        self.assertNotIn(selected_sport_without_event, list(self.az_sports.keys()),
                         msg=f'Sport "{selected_sport_without_event}" should not be shown in the list')

    def test_007_verify_sport_availability_in_a_z_categories_section_with_non_ob_categoryid_from_preconditions_3_eg_player_bets(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section with non OB 'CategoryId' (from Preconditions 3 e.g. Player Bets)
        EXPECTED: Sport e.g. Player Bets is available in 'A-Z Categories' section
        """
        cms_az_sports_with_category_id_0 = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                                            if all((not sport['disabled'], sport['imageTitle'], sport['showInAZ'],
                                                   sport['categoryId'] == 0))]

        for sport_name in cms_az_sports_with_category_id_0:
            self.assertIn(sport_name, list(self.az_sports.keys()),
                          msg=f'Sport "{sport_name}" should not be shown in the list')

    def test_008_repeat_steps_5_7_for_sports_in_top_sports_section(self):
        """
        DESCRIPTION: Repeat steps 5-7 for sports in 'Top Sports' section
        EXPECTED: Results are the same
        """
        # step 5 verified in scope of of step 002
        cms_top_sports = {sport['imageTitle'].strip(): sport['categoryId'] for sport in self.cms_config.get_sport_categories()
                          if sport['isTopSport']}

        cms_top_sports_without_event = set(cms_top_sports.keys()) - set(self.cms_top_sports)

        if cms_top_sports_without_event:
            selected_sport_without_event = list(cms_top_sports_without_event)[0]

            self.assertNotIn(selected_sport_without_event, list(self.top_sports.keys()),
                             msg=f'Sport "{selected_sport_without_event}" should not be shown in the list')
        else:
            self._logger.warning("*** Skipping validation as there is no top sports without events")

        cms_top_sports_with_category_id_0 = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                                             if all((not sport['disabled'], sport['imageTitle'], sport['isTopSport'],
                                                    sport['categoryId'] == 0))]

        for sport_name in cms_top_sports_with_category_id_0:
            self.assertIn(sport_name, list(self.top_sports.keys()),
                          msg=f'Sport "{sport_name}" should not be shown in the list')
