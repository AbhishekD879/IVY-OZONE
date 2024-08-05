import voltron.environments.constants as vec
import re

import pytest

import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.build_own_racecard
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1669315_Verify_Build_Your_Own_Racecard_section_on_Horse_Racing_Landing_page(BaseRacing):
    """
    TR_ID: C1669315
    VOL_ID: C9697659
    NAME: Verify 'Build Your Own Racecard' section on 'Horse Racing' Landing page
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' section on 'Horse Racing' Landing page
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    build_racecard_text_block = f'{vec.racing.BEGIN_TO} {vec.racing.BUILD_YOUR_OWN_RACE_CARD}. {vec.racing.SELECT_FROM_MEETINGS}'
    build_your_race_card_button_text = vec.racing.BUILD_YOUR_RACECARD_BUTTON
    horse_racing_tab_name = re.sub(r'\W+', '-', vec.racing.HORSE_RACING_TAB_NAME)
    featured_tab = vec.racing.RACING_DEFAULT_TAB_NAME

    def test_001_navigate_to_horse_racing_landing_page_featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page -> 'Featured' tab
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Build a Racecard' button is displayed at the top of the main content area and below the tabs
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.__class__.horse_racing = self.site.horse_racing
        selected_tab = self.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, self.featured_tab,
                         msg=f'{selected_tab} tab is selected by default instead of {self.featured_tab}')
        actual_build_card_text = self.horse_racing.tab_content.build_card.build_race_card_button.name
        self.assertEqual(actual_build_card_text, self.build_your_race_card_button_text,
                         msg=f'Actual text "{actual_build_card_text}" '
                             f'does not match expected f"{self.build_your_race_card_button_text}"')

    def test_002_verify_text_block(self):
        """
        DESCRIPTION: Verify text block
        EXPECTED: Text says: "Begin to Build Your Own Racecard. Select up to 10 races from any UK, IRE and International meetings"
        """
        actual_text_block = self.horse_racing.tab_content.build_card.build_race_card_text_block
        self.assertEqual(actual_text_block,
                         self.build_racecard_text_block,
                         msg=f'Actual text "{actual_text_block}" does not match expected '
                             f'f"{self.build_racecard_text_block}"')

    def test_003_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is clickable
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        self.horse_racing.tab_content.build_card.build_race_card_button.click()
        self.assertTrue(self.horse_racing.tab_content.build_card.exit_builder_button.is_enabled(),
                        msg="'Build a Racecard' button is not replaced by 'Exit Builder'")
        self.assertTrue(self.horse_racing.tab_content.build_card.close_icon.is_displayed(),
                        msg="'Close' icon is not shown near 'Exit Builder'")
        self.test_002_verify_text_block()

    def test_004_click_on_exit_builder_button(self):
        """
        DESCRIPTION: Click on 'Exit Builder' button
        EXPECTED: * 'Exit Builder' button is clickable
        EXPECTED: * 'Exit Builder' button with 'Close' icon is replaced by 'Build a Racecard'
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        self.horse_racing.tab_content.build_card.exit_builder_button.click()
        self.assertTrue(self.horse_racing.tab_content.build_card.build_race_card_button.is_enabled(),
                        msg="Exit Builder' button is not replaced by 'Build a Racecard.")
        self.test_002_verify_text_block()

    def test_005_click_on_build_a_racecard_button_again(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button again
        EXPECTED: 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        """
        self.horse_racing.tab_content.build_card.build_race_card_button.click()
        self.assertTrue(self.horse_racing.tab_content.build_card.exit_builder_button.is_enabled(),
                        msg="'Build a Racecard' button is not replaced by 'Exit Builder'")
        self.assertTrue(self.horse_racing.tab_content.build_card.close_icon.is_displayed(),
                        msg="'Close' icon is not shown near 'Exit Builder'")

    def test_006_click_on_close_icon(self):
        """
        DESCRIPTION: Click on 'Close' icon
        EXPECTED: * 'Close' icon is clickable
        EXPECTED: * 'Exit Builder' button with 'Close' icon is replaced by 'Build a Racecard' button
        EXPECTED: * Text at 'Build Your Own Racecard' section remains the same
        """
        self.horse_racing.tab_content.build_card.close_icon.click()
        self.test_002_verify_text_block()
