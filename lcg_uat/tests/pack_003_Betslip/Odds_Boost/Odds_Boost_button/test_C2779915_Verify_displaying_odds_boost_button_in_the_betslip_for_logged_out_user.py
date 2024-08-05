import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2779915_Verify_displaying_odds_boost_button_in_the_betslip_for_logged_out_user(BaseBetSlipTest):
    """
    TR_ID: C2779915
    NAME: Verify displaying odds boost button in the betslip for logged out user
    DESCRIPTION: Verify displaying odds boost button in the betslip (Single selections) for logged out user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    PRECONDITIONS: Add a single selection with added Stake to the Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
        PRECONDITIONS: Load application
        PRECONDITIONS: Do NOT login
        PRECONDITIONS: Add a single selection with added Stake to the Betslip
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Login button is not displayed')
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(
                LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        all_available_events=True,
                                                        additional_filters=cashout_filter,
                                                        in_play_event=False)[0]
            market = next((market for market in event['event']['children']), None)
            outcomes_resp = market['market']['children']
            self.__class__.all_selection_ids = [i['outcome']['id'] for i in outcomes_resp]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.all_selection_ids = list(event.selection_ids.values())

    def test_001_navigate_to_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.all_selection_ids[0])
        self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                         msg='Odds Boost header is displayed on betslip')

    def test_002_add_one_more_selection_and_navigate_to_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add one more selection and navigate to Betslip
        DESCRIPTION: Verify that odds boost button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.all_selection_ids[1])
        self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                         msg='Odds Boost header is displayed on betslip')
