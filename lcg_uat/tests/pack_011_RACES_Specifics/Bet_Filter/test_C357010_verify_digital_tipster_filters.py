import random
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException

@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.low
@vtest
class Test_C357010_VerifyDigitalTipsterFilters(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357010
    NAME: Verify Digital Tipster Filters
    DESCRIPTION: This test case verifies Supercomputer filters at Bet Finder page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Jira ticket:
        PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
        PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
        PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
        PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
        PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
        PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if not cms_config:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not cms_config.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')

    def test_001_verify_filtering_by_selection(self):
        """
        DESCRIPTION: Verify filtering by selection.
        DESCRIPTION: Check off 'selection' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "S"} param
        """
        self.get_bets()
        self.openBetFilterPage()
        filter = 'Selection' if self.brand == 'bma' else 'SELECTION'
        self.verify_filters([filter], type='digital_tipster_filter', unselect=False)
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after returning from Bet Filter Results page')
        self.site.horseracing_bet_filter.save_selection_button.click()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after refreshing the page')

    def test_002_verify_filtering_by_alternative(self):
        """
        DESCRIPTION: Verify filtering by alternative.
        DESCRIPTION: Check off 'alternative' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "A"} param
        """
        filter = 'Alternative' if self.brand == 'bma' else 'ALTERNATIVE'
        self.verify_filters([filter], type='digital_tipster_filter', unselect=False)
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after returning from Bet Filter Results page')
        self.site.horseracing_bet_filter.save_selection_button.click()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after refreshing the page')

    def test_003_verify_filtering_by_each_way(self):
        """
        DESCRIPTION: Verify filtering by each-way.
        DESCRIPTION: Check off 'each-way' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "E"} param
        """
        filter = 'Each-Way' if self.brand == 'bma' else 'EACH-WAY'
        self.verify_filters([filter], type='digital_tipster_filter', unselect=False)
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after returning from Bet Filter Results page')
        self.site.horseracing_bet_filter.save_selection_button.click()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter),
                        msg=f'["{filter}"] filter is not selected after refreshing the page')

    def test_004_verify_the_supercomputer_filters_work_as_radio_buttons(self):
        """
        DESCRIPTION: Verify the supercomputer filters work as radio buttons
        EXPECTED: - Once clicked > option is selected. One more click on the same option de-selects it.
        EXPECTED: - Once clicked on option A, then click on option B selects option B and auto-deselects option A.
        """
        DTF = vec.bet_finder.DTF
        self.__class__.filter = random.choice(DTF)
        filter_to_click = 'Each-Way' if self.brand == 'bma' else 'EACH-WAY'
        self.site.horseracing_bet_filter.items_as_ordered_dict[filter_to_click].click()  # to unselect
        self.site.horseracing_bet_filter.items_as_ordered_dict[self.filter].click()
        for filter in DTF:
            if filter == self.filter:
                self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter),
                                msg='Filter [%s] should be selected' % filter)
            else:
                self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=filter, expected_result=False),
                                 msg='Filter [%s] is selected while [%s] should be.' % (filter, self.filter))
                # This is also verified by unselect=False in previous steps.
                # If these filters don't work as radiobuttons incorrect number of bets will be shown.

    def test_005_verify_supercomputer_filters_plus_refreshre_navigation(self):
        """
        DESCRIPTION: Verify Supercomputer filters + refresh/re-navigation
        EXPECTED: - Supercomputer filters selected value should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        pass
        # Verified in previous steps

    def test_006_verify_supercomputer_filters_plus_reset(self):
        """
        DESCRIPTION: Verify Supercomputer filters + Reset
        EXPECTED: - Supercomputer filters value should clear on Reset
        """
        self.site.horseracing_bet_filter.reset_link.click()
        self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=self.filter, expected_result=False),
                         msg='Filter [%s] is still selected after clicking Reset.' % (self.filter))