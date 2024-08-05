from datetime import datetime
import pytest
from crlat_cms_client.cms_client import fake
from crlat_cms_client.utils.date_time import get_date_time_as_string
from faker import Faker
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.surface_bets
@pytest.mark.adhoc_suite
@pytest.mark.Big_Competition
@vtest
class Test_C65866507_Verify_surface_bet_created_for_any_big_competition_like_World_Cup_under_Sports_Category(BaseBetSlipTest):
    """
    TR_ID: C65866507
    NAME: Verify surface bet created for any big competition like World Cup under Sports Category
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports
    """
    keep_browser_open = True
    faker = Faker()
    competition_name = f'Auto big competition {faker.name()}'
    competition_title = f'Auto{faker.name()}'
    new_id = faker.random.randint(200, 1000)

    def verify_surface_bets_on_fe(self, expected_result=True):
        import time
        wait_time = 1  # Wait time in seconds
        max_polling_time = 120  # Maximum polling time in seconds (2 minutes)

        if expected_result:
            start_time = time.time()

            while time.time() - start_time < max_polling_time:
                has_surface_bet = self.site.big_competitions.tab_content.has_surface_bets(expected_result=expected_result)

                if has_surface_bet:
                    # Reading the surface bets in big competitions
                    surface_bets = self.site.big_competitions.tab_content.surface_bets.items_as_ordered_dict
                    if surface_bets.get(self.surface_bet_title):
                        break  # Break the loop if the condition is met

                wait_for_haul(wait_time)

            self.assertTrue(has_surface_bet, "Surface Bets Content is not Shown on Big competitions")

            # Checking if the expected title is in the list of surface bets
            self.assertIn(self.surface_bet_title, list(surface_bets.keys()),
                          f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')

            return surface_bets.get(self.surface_bet_title)
        else:
            start_time = time.time()

            while time.time() - start_time < max_polling_time:
                has_surface_bet = self.site.big_competitions.tab_content.has_surface_bets(
                    expected_result=expected_result)
                if not has_surface_bet:
                    break  # Break the loop if the condition is met
                time.sleep(wait_time)
            self.assertFalse(has_surface_bet,msg=f'surface bet : "{self.surface_bet_title}" which is not ment to present is found in on big competitions')

    def check_module_status_and_create_surface_bet(self, selection_id: int = None, eventID=[], active=True,create=False):
        # Get the SPORT_MODULE related to the new sport ID
        sports_module_event_hub = self.cms_config.get_sport_module(sport_id=self.new_id, module_type=None)
        # Initialize a variable to hold the surface bet module's CMS configuration
        surface_bet_module_cms = None
        # Find the SURFACE_BET module within the SPORT_MODULE list
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_module_cms = module
                break
        # Get the status of the surface bet module (whether it's disabled or not)
        surface_bet_module_status = next((module['disabled'] for module in sports_module_event_hub
                                          if module['moduleType'] == 'SURFACE_BET'), None)
        # Check if the surface bet module should be activated based on its status and the 'active' parameter
        if surface_bet_module_status is True or not active:
            self.cms_config.change_sport_module_state(sport_module=surface_bet_module_cms, active=active)
        # If 'create' is True, add a new surface bet with specific parameters
        if create:
            # Adding a sports module to the Big competition hub
            surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                          categoryIDs=[0, self.new_id],
                                                          eventIDs=eventID,
                                                          edp_on=True,
                                                          title=f'Auto C65866507 {fake.name_female()}',
                                                          highlightsTabOn=True,
                                                          svg_icon='football',
                                                          svg_bg_id=self.svg_bg_id,
                                                          svg_bg_image=self.sb_bg_img_path,
                                                          displayOnDesktop=True,
                                                          )
            return surface_bet

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: Surface bet Creation in CMS:
        PRECONDITIONS: 1.Login to Environment specific CMS
        PRECONDITIONS: 2.Click Sports from side navigation and select 'World cup' option from sports category
        PRECONDITIONS: 3.Click 'Surface Bet Module' and click 'Create Surface bet'
        PRECONDITIONS: 4.Check the checkbox 'Enabled', 'Display on Highlights tab', 'Display on EDP' and 'Display in Desktop'
        PRECONDITIONS: 5.Enter All fields like
        PRECONDITIONS: Active Checkbox
        PRECONDITIONS: Title
        PRECONDITIONS: EventIds (Create with EventId)
        PRECONDITIONS: Show on Sports select 'All Sports'
        PRECONDITIONS: Show on EventHub
        PRECONDITIONS: Content Header
        PRECONDITIONS: Content
        PRECONDITIONS: Was Price
        PRECONDITIONS: Selection ID
        PRECIONDITIONS: Display From
        PRECONDITONS: Display To
        PRECONDITIONS: SVG Icon
        PRECONDITIONS: SVG Background
        PRECONDITIONS: 6.Check segment as 'Universal'
        PRECONDITIONS: 7.Click Save Changes
        PRECONDITIONS: Check the Sort Order of Surface bet Module
        PRECONDITIONS: Navigate to Sports-->All Sports-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
        """
        # Check if the environment is 'prod'
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            self.__class__.eventID = event['event']['id']
            self.__class__.typeid = event['event']['typeId']
            # Extract outcomes from the event
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            # Create a dictionary of event selections
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            # Assign the first selection ID from the event selections
            selection_id = list(event_selection.values())[0]

            # Set SVG background information based on brand
            self.__class__.svg_bg_id = None
            if self.brand != 'bma':
                self.__class__.svgBg = None
                self.__class__.sb_bg_img_path = None
            else:
                self.__class__.svgBg = None
                self.__class__.sb_bg_img_path = None
        else:
            # Add a new football event to the England Premier League
            event = self.ob_config.add_football_event_to_england_premier_league()
            # Assign the selection ID based on the added event
            selection_id = event.selection_ids[event.team1]
            # Assign event ID based on the added event
            self.__class__.eventID = event.event_id
            # Set SVG background information based on brand
            self.__class__.svg_bg_id = 'surface-bet-bg-bigc'
            if self.brand != 'bma':
                self.__class__.svgBg = 'background-image: url("https://cms-stg.ladbrokes.com/cms/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg");'
                self.__class__.sb_bg_img_path = '/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg'
            else:
                self.__class__.svgBg = 'background-image: url("https://cms-stg.coral.co.uk/cms/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg");'
                self.__class__.sb_bg_img_path = '/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg'
        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=self.typeid,
                                                                 competition_name=self.competition_name,
                                                                 title=self.competition_title)
        # Assign IDs and URIs from the new competition data
        new_competition_id = new_competition.get('id')
        new_competition_uri = new_competition.get('uri')
        # Construct the URL for the new category
        self.__class__.new_category_ulr = f'big-competition{new_competition_uri}'
        # Create a new tab under the created Big competition
        new_tab_id = self.cms_config.create_tab_for_big_competition(competition_id=new_competition_id,
                                                                    tab_name='highlight').get('id')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new module under the tab which is created
        new_module = self.cms_config.create_module_for_big_competation(competition_id=new_competition_id,
                                                                       tab_id=new_tab_id, module_name='surfaceBet',
                                                                       module_type='SURFACEBET')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new sport category for the Big competition which is created
        new_sports = self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                                           ssCategoryCode=self.new_id, targetUri=self.new_category_ulr,
                                                           tier='UNTIED', showInAZ=True, showInHome=True)
        # Wait for a short time
        wait_for_haul(2)
        # Check module status and create a new surface bet
        self.__class__.surface_bet = self.check_module_status_and_create_surface_bet(selection_id=selection_id,
                                                                                     eventID=[self.eventID],
                                                                                     create=True)
        # Assign surface bet title and ID from the created surface bet
        self.__class__.surface_bet_title = self.surface_bet.get("title").upper()
        self.__class__.surface_bet_id = self.surface_bet.get('id')
        # Wait for a short time
        wait_for_haul(2)
        # Update the surface module for the big competition
        self.cms_config.update_surface_module_for_big_competition(surfaceBets=[self.surface_bet_id],
                                                                  module_id=new_module.get('id'),
                                                                  module_name='surfaceBet')

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.site.login()

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        """
        # covered in test case C5865541

    def test_003_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        # covered in test_004_validate_the_surface_bet_is_displayed_under_big_competition_world_cup

    def test_004_validate_the_surface_bet_is_displayed_under_big_competition_world_cup(self):
        """
        DESCRIPTION: Validate the surface bet is displayed under big competition 'World cup'
        EXPECTED: Surface bet created should reflect only on big competition 'World Cup' as per CMS config
        """
        self.navigate_to_page(self.new_category_ulr)
        # Get the surface bet which is created among the surface bets in big competitions
        surface_bet = self.verify_surface_bets_on_fe()  # Fetch the surface bet object
        surface_bet.scroll_to()  # Scroll to the surface bet element
        # Check if the SVG icon matches the configured value in CMS
        self.assertEqual(surface_bet.header.icontext,
                         '#football', f'Svg Icon is not same as configured in cms')
        # Check svg background style if backend environment is not 'prod'
        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')
        # Check if the surface bet header title matches the expected title
        self.assertEqual(surface_bet.header.title.upper(), self.surface_bet['title'].upper(),
                         f'Actual title : "{surface_bet.header.title.upper()}" is not same as '
                         f'Expected title : "{self.surface_bet["title"].upper()}"')
        # Check if the surface bet content header matches the expected content header
        self.assertEqual(surface_bet.content_header.upper(),
                         self.surface_bet['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.surface_bet["contentHeader"].upper()}"')
        # Check if the surface bet content matches the expected content
        self.assertEqual(surface_bet.content.strip().upper(),
                         self.surface_bet['content'].strip().upper(),
                         f'Actual Content : "{surface_bet.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.surface_bet["content"].strip().upper()}"')

    def test_005_avalidate_the_surface_bet_content_headerbvalidate_the_surface_bet_contentcvalidate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: a)Validate the surface bet 'Content header'
        DESCRIPTION: b)Validate the surface bet 'Content'
        DESCRIPTION: C)Validate the SVG icon and SVG background
        EXPECTED: a)Content Header' should be displayed as per CMS config
        EXPECTED: b)Content' should be displayed as per CMS config.
        EXPECTED: c)SVG icon and SVG background should be displayed as per CMS config.
        """
    #     covered in test_004_validate_the_surface_bet_is_displayed_under_big_competition_world_cup

    def test_006_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        # covered in the test case as we are creating new time past time and all

    def test_007_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        # Update Surface bet Display dates to Past dates

        # Set the time format for formatting date and time strings
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        # Calculate start time by subtracting 8.5 hours from the current UTC time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-8.5)[:-3] + 'Z'
        # Calculate end time by subtracting 6.5 hours from the current UTC time
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-6.5)[:-3] + 'Z'
        # Update the surface bet's display dates in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        # Verify the surface bets on the front-end with the expectation of not finding the bet
        self.verify_surface_bets_on_fe(expected_result=False)

    def test_008_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # Update of Surface bet start_time to present for the present time and end_time to Future

        # Calculate the start time by subtracting 10 hours and adding 2 minutes from the current UTC time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-10, minutes=2)[:-3] + 'Z'
        # Calculate the end time by adding 10 hours from the current UTC time
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        # Update the surface bet's display dates in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time, displayTo=end_time)
        # Verify the surface bets on the front-end with the expectation of finding the bet
        self.verify_surface_bets_on_fe(expected_result=True)

    def test_009_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # Update of Surface bet start_time to future time and end_time to Future

        # Calculate the start time to be 9 hours ahead of the current UTC time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=9)[:-3] + 'Z'
        # Calculate the end time to be 10 hours ahead of the current UTC time
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        # Update the surface bet's display dates in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time, displayTo=end_time)
        # Verify the surface bets on the front-end with the expectation of not finding the bet
        self.verify_surface_bets_on_fe(expected_result=False)

        # Updation of Surface bet start_time to present for the present time and end_time to Future

        # Calculate the start time by subtracting 10 hours and 2 minutes from the current UTC time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-10, minutes=2)[:-3] + 'Z'
        # Calculate the end time to be 10 hours ahead of the current UTC time
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        # Update the surface bet's display dates in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time, displayTo=end_time)

    def test_010_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        # Get the surface bet object by verifying surface bets on the front-end
        surface_bet = self.verify_surface_bets_on_fe()
        # Click the bet button associated with the surface bet
        bet_button = surface_bet.bet_button
        bet_button.click()
        # Ensure that the bet button is selected
        self.assertTrue(bet_button.is_selected(), f'unable to select bet button')
        # Check the device type to determine the flow (mobile or not)
        if self.device_type == 'mobile':
            # For mobile devices:
            quick_bet = self.site.quick_bet_panel
            # Set the bet amount in the quick bet panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            # Place the bet by clicking the place bet button
            quick_bet.place_bet.click()
            # Wait for the bet receipt to be displayed
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            # Click the "reuse selection" button on the bet receipt
            quick_bet.bet_receipt.reuse_selection_button.click()
            # Ensure that the bet button is still selected after reusing the selection
            bet_button_status = wait_for_result(lambda: bet_button.is_selected(), expected_result=True, timeout=5,
                                                name='Waiting for BetButton to be selected')
            self.assertTrue(bet_button_status, f'bet button is not selected after clicking on reuse selection')
            # Open the betslip
            self.site.open_betslip()
        else:
            # For non-mobile devices:
            # Place a single bet using the defined method
            self.place_single_bet()
            # Check if the bet receipt is displayed
            self.check_bet_receipt_is_displayed()
            # Click the "reuse selection" button in the bet receipt footer
            self.site.bet_receipt.footer.reuse_selection_button.click()
        # Ensure that the bet button is still selected after reusing the selection
        bet_button_status = wait_for_result(lambda: bet_button.is_selected(), expected_result=True, timeout=5, name='Waiting for BetButton to be selected')
        self.assertTrue(bet_button_status, f'bet button is not selected after clicking on reuse selection')
        # Place a single bet again
        self.place_single_bet()
        # Check if the bet receipt is displayed
        self.check_bet_receipt_is_displayed()
        # Close the bet receipt
        self.site.close_betreceipt()

    def test_011_activatedeactivate_the_whole_surface_bet_module_on_big_competitions(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on big competitions
        EXPECTED: Surface bet should display on big competitions if it is activated
        EXPECTED: Surface bet should not display on big competitions if it is deactivated
        """
        # Check the module status and create a surface bet with active set to False
        self.check_module_status_and_create_surface_bet(active=False)
        # # Verify surface bets on the front-end with the expectation of not finding the bet
        self.verify_surface_bets_on_fe(expected_result=False)
        # # Check the module status and create a surface bet without specifying 'active'
        self.check_module_status_and_create_surface_bet()

    def test_012_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        # Generate modified content using a fake paragraph and append "modified by Surface bet"
        content = fake.paragraph() + "modified by Surface bet"
        # Update the content of the surface bet in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, content=content)
        # Verify surface bets on the front-end with the expectation of finding the bet
        surface_bet = self.verify_surface_bets_on_fe(expected_result=True)
        # Check if the displayed content on the front-end matches the modified content
        self.assertEqual(surface_bet.content.strip().upper(),
                         content.strip().upper(),
                         f'Actual Content : "{surface_bet.content.strip().upper()}" is not same as '
                         f'Expected Content : "{content.strip().upper()}"')

    def test_013_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # Delete the surface bet from the CMS configuration using its ID
        self.cms_config.delete_surface_bet(surface_bet_id=self.surface_bet_id)
        # Remove the deleted surface bet's ID from the list of created surface bets
        self.cms_config._created_surface_bets.remove(self.surface_bet_id)
        # Verify surface bets on the front-end with the expectation of not finding the deleted bet
        self.verify_surface_bets_on_fe(expected_result=False)

