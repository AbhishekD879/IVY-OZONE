import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.user_journey_single_horse_race
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C1049883_Verify_Race_Landing_Page(BaseRacing):
    """
    TR_ID: C1049883
    NAME: Horse Racing Landing Page
    DESCRIPTION: This test case verifies Horse Racing landing page
    """
    keep_browser_open = True

    def test_000_open_racing_page(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        self.site.open_sport(name=vec.SB.HORSERACING.upper())

    def test_001_verify_tabs(self):
        """
        DESCRIPTION: Verify Horse Racing page tabs
        EXPECTED: Below tabs are shown:
        For Coral brand: The 'Featured', 'Future', 'Specials' tabs are displayed in one row.
        For Ladbrokes brand: The 'Meetings', 'Next races', 'Future' and 'Specials' tabs are displayed in one row.
        """
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No one menu tab was found on page')
        expected_tabs = vec.racing.RACING_TAB_NAMES
        self.assertTrue(len(tabs) <= len(expected_tabs),
                        msg='Tabs number is not correct. Actual number of tabs ({0}) isn\'t equal to expected ({1})'
                        .format(len(tabs), len(expected_tabs)))
        if 'SPECIALS' not in tabs:
            expected_tabs.remove('SPECIALS')
        self.assertListEqual(expected_tabs, list(tabs.keys()))
