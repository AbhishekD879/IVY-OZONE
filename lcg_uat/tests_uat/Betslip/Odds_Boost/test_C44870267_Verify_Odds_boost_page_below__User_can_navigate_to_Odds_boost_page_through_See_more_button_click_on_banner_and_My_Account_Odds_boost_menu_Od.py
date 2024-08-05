import pytest
import tests
from time import sleep
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from datetime import datetime, timedelta


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't executed on prod, Can't add odds boost token on prod
@pytest.mark.uat
@pytest.mark.h1
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870267_Verify_Odds_boost_page_below__User_can_navigate_to_Odds_boost_page_through_See_more_button_click_on_banner_and_My_Account_Odds_boost_menu_Odds_boost_page_logo_and_hard_corded_messages_Terms_and_conditions_section_Verify_token_display_order_(Common):
    """
    TR_ID: C44870267
    NAME: "Verify Odds boost page below  - User can navigate to Odds boost page through 'See more' button click on banner and My Account >Odds boost menu -Odds boost page logo and hard corded messages -Terms and conditions section -Verify token display order (
    """
    keep_browser_open = True

    def navigation_of_odds_boost_page(self):
        self.site.close_all_dialogs()
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        if self.brand == 'bma':
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            self.site.wait_content_state_changed()
            menu_items = self.site.right_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='Offers menu has no items available.')
            self.site.right_menu.click_item(item_name=vec.odds_boost.PAGE.title.upper())
        else:
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
            self.site.wait_splash_to_hide(timeout=1)
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        self.site.close_all_dialogs()

    def validation_of_odds_boost_page(self):
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, '"Odds boost section" are not displayed')
        tokens = odds_boost_sections[1].items_as_ordered_dict.items()
        self.assertTrue(tokens, msg='"Boost token" is not displayed')
        if self.brand == 'bma':
            for token_name, token in tokens:
                if token_name == 'for_at_testing':
                    token.click()
                    sleep(2)
                    break
        else:
            for token_name, token in tokens:
                if token_name == 'automation_offer':
                    token.click()
                    sleep(1)
                    break

    def test_001_navigate_to_the_odds_boost_information_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost information page
        EXPECTED: User is navigated to the Odds Boost information page
        EXPECTED: User can navigate to Odds boost page through 'See more' button click on banner and My Account >Odds boost menu
        EXPECTED: -Odds boost page logo and hard corded messages
        EXPECTED: -Terms and conditions section
        """
        # Odds Boost information page has validated in step 3
        self.__class__.username_one = tests.settings.betplacement_user

    def test_002_tap_on_generic_token_which_can_be_used_on_any_bet(self):
        """
        DESCRIPTION: Tap on generic token which can be used on ANY bet
        EXPECTED: User is navigated to the homepage
        """
        self.site.login(username=self.username_one)
        self.ob_config.grant_odds_boost_token(username=self.username_one)
        self.navigation_of_odds_boost_page()
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())[1]
        token = list(odds_boost_sections.items_as_ordered_dict.values())[0]
        token.click()
        self.site.wait_content_state('homepage')
        self.site.logout()

    def test_003_tap_on_generic_token_which_has_a_category_class_or_type_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on generic token which has a category, class or type hierarchy associated with it
        EXPECTED: User is navigated to the respective category landing page
        """
        self.site.login(username=self.username_one)
        self.site.close_all_dialogs()
        category_id = self.ob_config.backend.ti.greyhound_racing.category_id
        exp_date_1 = datetime.now() + timedelta(hours=2)
        self.ob_config.grant_odds_boost_token(username=self.username_one, level='category',
                                              id=category_id, expiration_date=exp_date_1)
        self.navigation_of_odds_boost_page()
        self.validation_of_odds_boost_page()
        actual_title = self.site.greyhound.header_line.page_title.title
        if self.brand == 'bma':
            self.assertEqual(actual_title, vec.sb.GREYHOUND.upper(),
                             msg=f'Actual title: "{actual_title}" is not equal with the'
                                 f'Expected title: "{vec.sb.GREYHOUND.upper()}"')
        else:
            self.assertEqual(actual_title, vec.sb.GREYHOUND,
                             msg=f'Actual title: "{actual_title}" is not equal with the'
                                 f'Expected title: "{vec.sb.GREYHOUND}"')
        self.site.logout()

    def test_004_tap_on_token_which_has_an_event_market_or_selection_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on token which has an event, market or selection hierarchy associated with it
        EXPECTED: User is navigated to the respective event detail page
        """
        self.site.login(username=self.username_one)
        self.site.close_all_dialogs()
        event_id = self.ob_config.add_badminton_event_to_autotest_league().event_id
        exp_date_2 = datetime.now() + timedelta(hours=4)
        self.ob_config.grant_odds_boost_token(username=self.username_one, level='event',
                                              id=event_id, expiration_date=exp_date_2)
        self.navigation_of_odds_boost_page()
        self.validation_of_odds_boost_page()
        event_data = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.assertTrue(event_data, msg=f'Can not get event info with id {event_id} from SiteServe')
