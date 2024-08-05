import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.deeplink
@pytest.mark.critical
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29095_C29105_C18636106_C18636107_Verify_Adding_Selections_via_Direct_Link(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29095
    TR_ID: C29105
    TR_ID: C18636106
    TR_ID: C18636107
    NAME: Verify Adding Selections via Direct Link
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Creating test event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections "{self.selection_ids}"')
        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place single bet
        """
        self.place_single_bet()

    def test_004_check_bet_receipt_displayed(self):
        """
        DESCRIPTION: Check if user was redirected to bet receipt
        """
        self.check_bet_receipt_is_displayed()
