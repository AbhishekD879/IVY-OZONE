from random import choice

import pytest

import tests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C28604_Favourite_Functionality_in_Football_on_Betslip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28604
    NAME: Verify 'Favourite Match' functionality in Football events on Betslip
    DESCRIPTION: This Test Case verifies 'Favourite Match' functionality to Football events on Betslip
    """
    keep_browser_open = True
    favourite_counter = 1
    selection_ids_2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Events are created
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2)

            outcomes = next(((market['market']['children']) for market in events[0]['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            outcomes = next(((market['market']['children']) for market in events[1]['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids_2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            self._logger.info(f'*** First football event with selection IDs "{self.selection_ids}"')
            self._logger.info(f'*** Second football event with selection IDs "{self.selection_ids_2}"')
        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
            self.__class__.selection_ids_2 = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        selection_id, selection_id2 = choice(list(self.selection_ids.values())), choice(list(self.selection_ids_2.values()))
        self.open_betslip_with_selections(selection_ids=(selection_id, selection_id2))

    def test_003_enter_stake(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: Bet is placed successfully, Bet Receipt is shown
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_match_center_functionality(self):
        """
        DESCRIPTION: Verify Match Center functionality on the displayed Bet Receipt,
        EXPECTED: 'Add all to favourites' star icon is displayed
        """
        add_all_to_favourites = self.site.bet_receipt.match_center.has_add_all_to_favourites_button()
        self.assertTrue(add_all_to_favourites, msg='"Add all to favourites" is not displayed')

    def test_005_verify_add_all_to_favourites(self):
        """
        DESCRIPTION: Verify 'Add all to favourites' star icon after tapping on it
        """
        self.site.bet_receipt.match_center.add_all_to_favourites_button.click()
        self.assertTrue(self.site.bet_receipt.match_center.add_all_to_favourites_button.is_selected(),
                        msg='"Add all to favourites" button is not selected')

        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No one bet receipt section was found')
        first_section = list(sections.values())[0]
        self.assertTrue(list(first_section.items_as_ordered_dict.values())[0].favourite_icon.is_selected(),
                        msg='Favourites icon is not selected in the first receipt section')

    def test_006_verify_unselected_add_all_to_favourites(self):
        """
        DESCRIPTION: Verify 'Add all to favourites' star icon after tapping on it one more time
        """
        self.site.bet_receipt.match_center.add_all_to_favourites_button.click()
        add_all_to_favourites = self.site.bet_receipt.match_center.has_add_all_to_favourites_button()
        self.assertTrue(add_all_to_favourites, msg='"Add all to favourites" is not displayed')
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No one bet receipt section was found')
        first_section = list(sections.values())[0]
        self.assertFalse(list(first_section.items_as_ordered_dict.values())[0].favourite_icon.is_selected(expected_result=False),
                         msg='Favourites icon is selected in the first receipt section')

    def test_007_verify_go_to_favourites_button(self):
        """
        DESCRIPTION: Verify 'Done' button on Bet Receipt
        EXPECTED: After tapping on 'Done' button, user is redirected to the page he/she came from
        """
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('HomePage', timeout=3)
