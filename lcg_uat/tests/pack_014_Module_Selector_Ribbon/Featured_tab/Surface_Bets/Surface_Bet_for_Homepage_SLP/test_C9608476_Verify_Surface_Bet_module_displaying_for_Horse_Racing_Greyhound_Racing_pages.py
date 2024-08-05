import pytest
import tests
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod   # cannot modify cms / create modules on prod
@pytest.mark.medium
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.cms
@vtest
class Test_C9608476_Verify_Surface_Bet_module_displaying_for_Horse_Racing_Greyhound_Racing_pages(BaseFeaturedTest):
    """
    TR_ID: C9608476
    VOL_ID: C9771292
    NAME: Verify Surface Bet module displaying for Horse Racing/Greyhound Racing pages
    DESCRIPTION: Test case verifies that Surface bets aren't shown on Racing landing pages
    PRECONDITIONS: Currently both Greyhound racing and Horse racing are present in the list of Sports Categories and can be selected
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Greyhound and Horse racing categories in the CMS
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: There are a few valid Surface Bets added to the Greyhound and Horse racing categories in the CMS
        """
        horse_category_id = self.ob_config.horseracing_config.category_id
        gh_category_id = self.ob_config.backend.ti.greyhound_racing.category_id

        cms_surface_bet_horse_racing = self.cms_config.get_sport_module(sport_id=horse_category_id,
                                                                        module_type='SURFACE_BET')[0]
        if cms_surface_bet_horse_racing['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Horse Racing')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet_horse_racing)

        cms_surface_bet_greyhound = self.cms_config.get_sport_module(sport_id=gh_category_id,
                                                                     module_type='SURFACE_BET')[0]
        if cms_surface_bet_greyhound['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Greyhounds')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet_greyhound)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=horse_category_id)[0]
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available horseracing outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id1 = list(selection_ids.values())[0]
            event = self.get_active_events_for_category(category_id=gh_category_id)[0]
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Greyhound event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available GH outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id2 = list(selection_ids.values())[0]

        else:
            self.__class__.selection_id1 = list(self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1).selection_ids.values())[0]
            self.__class__.selection_id2 = list(self.ob_config.add_UK_racing_event(number_of_runners=1).selection_ids.values())[0]

        self.cms_config.add_surface_bet(selection_id=self.selection_id1,
                                        categoryIDs=[horse_category_id, gh_category_id])
        self.cms_config.add_surface_bet(selection_id=self.selection_id2,
                                        categoryIDs=[horse_category_id, gh_category_id])

    def test_001_in_the_application_on_the_greyhound_racing_landing_page_verify_the_surface_bet_module_isnt_shown(self):
        """
        DESCRIPTION: In the application, on the Greyhound racing landing page verify the Surface Bet module isn't shown
        EXPECTED: Surface Bet module isn't shown
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

        surface_bet_module = self.site.greyhound.tab_content.has_surface_bets(expected_result=False)
        self.assertFalse(surface_bet_module, msg='Surface bet module is shown on Greyhound racing landing page')

    def test_002_on_the_horse_racing_landing_page_verify_the_surface_bet_module_isnt_shown(self):
        """
        DESCRIPTION: On the Horse racing landing page verify the Surface Bet module isn't shown
        EXPECTED: Surface Bet module isn't shown
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horse-Racing')

        surface_bet_module = self.site.horse_racing.tab_content.has_surface_bets(expected_result=False)
        self.assertFalse(surface_bet_module, msg='Surface bet module is shown on Horse racing landing page')
