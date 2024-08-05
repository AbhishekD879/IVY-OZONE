import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C76617_NOT_valid_after_OX982Add_Edit_Delete_League(Common):
    """
    TR_ID: C76617
    NAME: [NOT valid after OX98.2]Add/Edit/Delete League
    DESCRIPTION: This test case verifies adding/editing/deleting leagues for Bet Receipt banners and 'Player Bets' tab on 'Event Details' page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-16377 (CMS: Player Bets banner on Bet Receipt)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16377
    PRECONDITIONS: * User is logged in to CMS:
    PRECONDITIONS: *  dev: https://invictus.coral.co.uk/keystone/signin
    PRECONDITIONS: * At least one banner is created (Banners -> Bet Receipt Banners Mobile)
    PRECONDITIONS: * User is logged in to Oxygen application.
    PRECONDITIONS: * User has enough funds to place a bet
    PRECONDITIONS: **Note**:
    PRECONDITIONS: Combination of **League Url** and **BetBuilder URL** is used for configuration of navigation to 'Player Bets' page from 'Player Bets' tab on Event Details page
    PRECONDITIONS: Combination of **Redirection URL** and **BetBuilder URL** is used for configuration of navigation to 'Player Bets' page from Bet Receipt banner
    PRECONDITIONS: In order to set up navigation from Bet Receipt banner on to any page within Oxygen application or to any external page (e. g. Coral Gaming products) only Redirection URL is used.  League Url and BetBuilder URL fields can be empty.
    PRECONDITIONS: [Guide for Bet Receipt banners in CMS] [1].
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/Guide+for+Bet+Receipt+banners+in+CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_leagues(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues
        EXPECTED: *   Page with list of leagues is opened
        EXPECTED: *   ' + Create League' button is present
        """
        pass

    def test_002_add_new_league_via_clicking_plus_create_league_buttonfill_in_all_fields_select_banner_and_save_it(self):
        """
        DESCRIPTION: Add new league via clicking '+ Create League' button.
        DESCRIPTION: Fill in all fields, select banner and save it
        EXPECTED: New league appears in the list
        """
        pass

    def test_003_in_oxygen_application_place_a_bet_on_event_from_created_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from created league
        EXPECTED: Bet Receipt is shown with clickable banner
        """
        pass

    def test_004_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Tab for league defined in 'BetBuilder URL' field is selected by default on slide with list of players
        """
        pass

    def test_005_in_oxygen_application_navigate_to_event_details_page_for_event_from_created_league_and_tap_player_bets_tab(self):
        """
        DESCRIPTION: In Oxygen application navigate to Event Details Page for event from created league and tap 'Player Bets' tab
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Tab for league defined in 'BetBuilder URL' field is selected by default on slide with list of players
        """
        pass

    def test_006_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_betbuilder_url_and_league_url(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change BetBuilder URL and League Url
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_007_in_oxygen_application_navigate_to_event_details_page_for_event_from_edited_league_and_tap_player_bets_tab(self):
        """
        DESCRIPTION: In Oxygen application navigate to Event Details Page for event from edited league and tap 'Player Bets' tab
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Tab for new league defined in 'BetBuilder URL' field is selected by default on slide with list of players
        """
        pass

    def test_008_in_oxygen_application_place_a_bet_on_event_from_edited_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_009_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Deafult tab is selected by default on slide with list of players
        """
        pass

    def test_010_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_betbuilder_url_and_redirection_url(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change BetBuilder URL and Redirection URL
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_011_in_oxygen_application_place_a_bet_on_event_from_edited_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_012_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Tab for new league defined in 'BetBuilder URL' field is selected by default on slide with list of players
        """
        pass

    def test_013_in_oxygen_application_navigate_to_event_details_page_for_event_from_edited_league_and_tap_player_bets_tab(self):
        """
        DESCRIPTION: In Oxygen application navigate to Event Details Page for event from edited league and tap 'Player Bets' tab
        EXPECTED: * 'Player Bets' page is opened
        EXPECTED: * Deafult tab is selected by default on slide with list of players
        """
        pass

    def test_014_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_only_redirection_url_eg_football(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change only Redirection URL (e.g. football)
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_015_in_oxygen_application_place_a_bet_on_event_from_edited_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_016_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: Page from 'Redirection URL' filed for edited league is opened
        """
        pass

    def test_017_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_type_id(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change Type Id
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_018_in_oxygen_application_place_a_bet_on_event_from_edited_league_with_new_type_id(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league with new Type Id
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_019_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: Page from 'Redirection URL' filed for edited league is opened
        """
        pass

    def test_020_in_oxygen_application_place_a_bet_on_event_from_edited_league_with_old_type_id(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league with old Type Id
        EXPECTED: Bet Receipt is shown without clickable banner
        """
        pass

    def test_021_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_only_redirection_url_to_external_link_eg_casino_homepage_httpmcasinocoralcouk(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change only Redirection URL to external link (e.g. Casino homepage: http://mcasino.coral.co.uk)
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_022_in_oxygen_application_place_a_bet_on_event_from_edited_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_023_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * Page from 'Redirection URL' field for created in step #3 sport league is opened
        EXPECTED: * In case of redirection to external Coral related page (not Oxygen application) user is logged in
        """
        pass

    def test_024_navigate_to_cms_page_with_leagues_select_league_created_in_step_2_and_change_only_redirection_url_to_external_link_on_one_of_the_casino_games_eg_roulette_httpmobilegamescoralcoukgamescasino57platformindexhtmlgamero_gusernameluketestcoralreal1temptokenzjrjpcp39ijebzpedfbbeacqolcg8oailanguageen_or_httpmcasinocoralcoukgamingsamurai_sunsetrefbma_or_httpmcasinocoralcoukgamingblackjackrefbma_or__httpmcasinocoralcoukgamingpremium_blackjackrefbma_or_httpmcasinocoralcoukgamingpremium_european_rouletterefbma_(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select league created in step #2 and change only Redirection URL to external link on one of the casino games (e.g. Roulette: http://mobilegames.coral.co.uk/games/casino/57/platform/index.html?game=ro_g&username=luketestcoral&real=1&temptoken=ZjRjPCP39IjeBZpEDFBBEACQoLCg8OAI&language=en& or http://mcasino.coral.co.uk/gaming/Samurai-Sunset?ref=bma or http://mcasino.coral.co.uk/gaming/blackjack?ref=bma or  http://mcasino.coral.co.uk/gaming/Premium-Blackjack?ref=bma or http://mcasino.coral.co.uk/gaming/Premium-European-Roulette?ref=bma )
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_025_in_oxygen_application_place_a_bet_on_event_from_edited_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from edited league
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_026_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * Page from 'Redirection URL' field for created in step #3 sport league is opened
        EXPECTED: * In case of redirection to external Coral related page (not Oxygen application) user is logged in
        """
        pass

    def test_027_navigate_to_cms_page_with_leagues_and_delete_league_created_in_step_2(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues and delete league created in step #2
        EXPECTED: New league is removed from the list
        """
        pass

    def test_028_in_oxygen_application_place_a_bet_on_event_from_removed_league(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from removed league
        EXPECTED: Bet Receipt is shown without Player Bets clickable banner
        """
        pass
