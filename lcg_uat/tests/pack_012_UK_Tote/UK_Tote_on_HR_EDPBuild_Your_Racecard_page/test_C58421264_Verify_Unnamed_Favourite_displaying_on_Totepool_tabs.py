import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


# @pytest.mark.tst2  # Cannot create tote events in QA envs
# @pytest.mark.stg2  # Cannot create tote events in stg envs
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.races
@vtest
class Test_C58421264_Verify_Unnamed_Favourite_displaying_on_Totepool_tabs(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C58421264
    NAME: Verify "Unnamed Favourite" displaying on Totepool tabs
    DESCRIPTION: This test case verifies that "Unnamed Favourite" should be available for Quadpot, Placepot, Jackpot and Scoop 6 but NOT Win, Place, Exacta, and Trifecta
    PRECONDITIONS: Horse Racing Events with at least one UK Tote pool available (Place, Win, Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: Unnamed Favourite should be available for current Horse Racing Event.
    PRECONDITIONS: - User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: - Navigate to HR landing page
    PRECONDITIONS: - Choose the particular event from the 'Race Grid'
    PRECONDITIONS: - Select 'Tote' tab
    """
    keep_browser_open = True
    unnamed_favourite = vec.racing.UNNAMED_FAVORITE

    def test_000_preconditions(self):
        """
        DESCRIPTION:-Get Active Tote Events
        """
        event = self.get_uk_tote_event(uk_tote_win=True)
        self.__class__.eventID = event.event_id
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login(async_close_dialogs=False)

        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='"%s" tab is not opened' % vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.__class__.event_off_time = tab_content.event_off_times_list.selected_item
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.__class__.tote_types = section.grouping_buttons
        self.__class__.totes = self.tote_types.items_names

    def test_001_select_win_tab(self):
        """
        DESCRIPTION: Select 'Win tab
        EXPECTED: - 'Win' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        if vec.uk_tote.UK_TOTE_TABS.win in self.totes:
            win_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.win)
            self.assertTrue(win_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.win)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertNotEqual(self.unnamed_favourite, last_runner,
                                msg=f'Actual runner :"{last_runner}" is same as '
                                    f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Win" is not available for the race event.')

    def test_002_select_place_tab(self):
        """
        DESCRIPTION: Select 'Place' tab
        EXPECTED: - 'Place' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        if vec.uk_tote.UK_TOTE_TABS.place in self.totes:
            place_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.place)
            self.assertTrue(place_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.place)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertNotEqual(self.unnamed_favourite, last_runner,
                                msg=f'Actual runner :"{last_runner}" is same as '
                                    f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Place" is not available for the race event.')

    def test_003_select_exacta_tab(self):
        """
        DESCRIPTION: Select 'Exacta' tab
        EXPECTED: - 'Exacta' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        if vec.uk_tote.UK_TOTE_TABS.exacta in self.totes:
            exacta_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
            self.assertTrue(exacta_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.exacta)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertNotEqual(self.unnamed_favourite, last_runner,
                                msg=f'Actual runner :"{last_runner}" is same as '
                                    f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Exacta" is not available for the race event.')

    def test_004_select_trifecta_tab(self):
        """
        DESCRIPTION: Select 'Trifecta' tab
        EXPECTED: - 'Trifecta' tab is selected
        EXPECTED: - Unnamed Favourite is NOT displayed
        """
        if vec.uk_tote.UK_TOTE_TABS.trifecta in self.totes:
            trifecta_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.trifecta)
            self.assertTrue(trifecta_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.trifecta)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertNotEqual(self.unnamed_favourite, last_runner,
                                msg=f'Actual runner :"{last_runner}" is same as '
                                    f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Trifecta" is not available for the race event.')

    def test_005_select_placepot_tab(self):
        """
        DESCRIPTION: Select 'Placepot' tab
        EXPECTED: - 'Placepot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        if vec.uk_tote.UK_TOTE_TABS.placepot in self.totes:
            placepot_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.placepot)
            self.assertTrue(placepot_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.placepot)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertEqual(self.unnamed_favourite, last_runner,
                             msg=f'Actual runner :"{last_runner}" is not same as '
                                 f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Placepot" is not available for the race event.')

    def test_006_select_quadpot_tab(self):
        """
        DESCRIPTION: Select 'Quadpot' tab
        EXPECTED: - 'Quadpot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        if vec.uk_tote.UK_TOTE_TABS.quadpot in self.totes:
            quadpot_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.quadpot)
            self.assertTrue(quadpot_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.quadpot)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertEqual(self.unnamed_favourite, last_runner,
                             msg=f'Actual runner :"{last_runner}" is not same as '
                                 f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Quadpot" is not available for the race event.')

    def test_007_select_jackpot_tab(self):
        """
        DESCRIPTION: Select 'Jackpot' tab
        EXPECTED: - 'Jackpot' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        if vec.uk_tote.UK_TOTE_TABS.jackpot in self.totes:
            jackpot_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.jackpot)
            self.assertTrue(jackpot_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.jackpot)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertEqual(self.unnamed_favourite, last_runner,
                             msg=f'Actual runner :"{last_runner}" is not same as '
                                 f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Jackpot" is not available for the race event.')

    def test_008_select_scoop_6_tab(self):
        """
        DESCRIPTION: Select 'Scoop 6' tab
        EXPECTED: - 'Scoop 6' tab is selected
        EXPECTED: - Unnamed Favourite is displayed at the end of list
        """
        if vec.uk_tote.UK_TOTE_TABS.scoop6 in self.totes:
            scoop_6_tab_opened = self.tote_types.click_button(vec.uk_tote.UK_TOTE_TABS.scoop6)
            self.assertTrue(scoop_6_tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.scoop6)

            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section_name, section = list(sections.items())[0]
            last_runner = list(section.pool.items_as_ordered_dict.keys())[-1]
            self.assertTrue(last_runner, msg='No outcomes found')
            self.assertEqual(self.unnamed_favourite, last_runner,
                             msg=f'Actual runner :"{last_runner}" is not same as '
                                 f'Expected : "{self.unnamed_favourite}".')
        else:
            self._logger.info(msg='"Scoop6" is not available for the race event.')
