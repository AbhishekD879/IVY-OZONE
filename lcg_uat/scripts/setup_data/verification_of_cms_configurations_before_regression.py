import sys
from crlat_cms_client.request import CMSAPIRequest

class Check_CMS_Configurations():
    def __init__(self, env, brand):
        self.__class__._cms_request = None
        self.__class__._cms_config = None
        from crlat_cms_client.cms_client import CMSClient
        self.brand = brand
        self._cms_config = CMSClient(env=env, brand=brand)
        self._cms_request = CMSAPIRequest()

    def verification_of_all_sports_footer_menu(self):
        """
        DESCRIPTION: Load CMS application and Navigate to Footer Menus under Menus section
        EXPECTED: 'All Sports' footer menu is available
        """
        try:
            footer_menus = self._cms_config.get_initial_data().get('footerMenu')
            all_footer_menus = [footer_menu.get('linkTitle') for footer_menu in footer_menus]
            if 'All Sports' in all_footer_menus:
                return "\033[32m✔ 'All Sports' footer menu is configured in CMS.... Verification of all sports footer menu is successful..\033[0m"
            else:
                return "\033[31mX 'All Sports' footer menu is not configured in CMS.... Verification of all sports footer menu is failed...Manually configure 'All Sports' footer menu in CMS.\033[0m""]]"
        except BaseException as e:
            return f"\033[31mX An error occurred during the verification of 'All Sports' footer menu in CMS: {str(e)}\033[0m"

    def check_offer_module_configured(self, offer_modules):
        """
        DESCRIPTION: Load CMS application and Navigate to Offer Modules under Offers section
        EXPECTED: offer modules are available
        """
        try:
            all_cms_offer_modules = self._cms_config.get_offer_modules()
            cms_offer_modules = [module.get('name') for module in all_cms_offer_modules]
            offer_modules_not_created = [offer_module for offer_module in offer_modules if
                                         offer_module not in cms_offer_modules]
            return f"\033[31mX Verification of Offer Modules in CMS is failed...{offer_modules} Offer Modules are configured in CMS...Verify existing offer Modules are linked to offers\033[0m" if offer_modules_not_created != offer_modules else f"\033[32m✔ Offer Modules {offer_modules} not configured in CMS. Verification of Offer Modules configuration is successful\033[0m"
        except BaseException as e:
            return f"\033[31mX An error occurred during the offer module check in CMS: {str(e)}\033[0m"

    def verify_5a_side_added_in_sport_categories(self) -> str:
        """
        DESCRIPTION: Load CMS application and Navigate to Sports
        EXPECTED: 5-A Side is available
        """
        try:
            if self.brand != "bma":
                sport_categories = self._cms_config.get_sport_categories()
                for sport_category in sport_categories:
                    if sport_category.get('imageTitle') == "5-A Side" and sport_category.get('disabled') == False and sport_category.get('showInAZ') == True and sport_category.get('inApp') == True:
                        return "\033[32m✔ 5-A Side is configured in CMS.... Verification of 5-A Side is successful\033[0m"""
                return "\033[31mX 5-A Side is not configured in CMS.... Verification of 5-A Side is failed...Manually configure 5-A Side in CMS\033[0m"
            else:
                return f"\033[33m✔ Verification of '5-A Side' Sports Category configuration is not applicable for {self.brand} brand"
        except BaseException as e:
            return f"\033[31mX An error occurred during the verification of '5-A Side' Sports Category in CMS: {str(e)}\033[0m"

    def verify_lobby_added_in_header_submenus(self) -> str:
        """
        DESCRIPTION: Load CMS application and Navigate to Header Submenus under Menus section
        EXPECTED: LOBBY is available
        """
        try:
            if self.brand != "bma":
                header_submenus = self._cms_config.get_header_submenus()
                for header_submenu in header_submenus:
                    if header_submenu.get('linkTitle') == "LOBBY" and header_submenu.get('disabled') == False and header_submenu.get('inApp') == True:
                        return "\033[32m✔ 'LOBBY' Header Submenu is configured in cms...Verification of LOBBY Header Submenu configuration is successful\033[0m"
                return "\033[31mX 'LOBBY' Header Submenu is not configured in cms...Verification of LOBBY Header Submenu configuration is failed...Manually configure 'LOBBY' Header Submenu in CMS\033[0m""]]"
            else:
                return f"\033[33m✔ Verification of LOBBY Header Submenu configuration is not applicable for {self.brand} brand"
        except BaseException as e:
            return f"\033[31X mAn error occurred during the verification of LOBBY Header Submenu configuration in CMS: {str(e)}\033[0m"

    def verify_bet_builder_module_ribbon_tab_is_available(self):
        """
        DESCRIPTION: Load CMS application and Navigate to Module Ribbon Tab
        EXPECTED: Bet Builder/Build Your Bet is available
        """
        try:
            path = 'module-ribbon-tab/brand/%s/segment/Universal' % self.brand
            module_ribbon_tabs = self._cms_request.get(path)
            cms_module_ribbon_tabs = []
            module_ribbon_tab_name = None
            for module_ribbon_tab in module_ribbon_tabs:
                if self.brand != "bma":
                    module_ribbon_tab_name = "Bet Builder"
                    if module_ribbon_tab['title'] == module_ribbon_tab_name and module_ribbon_tab['internalId'] == "tab-bet-builder" and module_ribbon_tab['visible'] == True and module_ribbon_tab['devices']['android'] == True and module_ribbon_tab['devices']['ios'] == True and module_ribbon_tab['devices']['wp'] == True:
                        cms_module_ribbon_tabs.append(module_ribbon_tab['title'])
                else:
                    module_ribbon_tab_name = "Build Your Bet"
                    if module_ribbon_tab['title'] == module_ribbon_tab_name and module_ribbon_tab['internalId'] == "tab-build-your-bet" and  module_ribbon_tab['visible'] ==  True and module_ribbon_tab['devices']['android'] == True and module_ribbon_tab['devices']['ios'] == True and module_ribbon_tab['devices']['wp'] == True:
                        cms_module_ribbon_tabs.append(module_ribbon_tab['title'])
            if len(cms_module_ribbon_tabs) == 0:
                return f"\033[31mX Verification of {module_ribbon_tab_name} module ribbon tab is failed...{module_ribbon_tab_name} module ribbon tab is not configured in CMS...Manually configure {module_ribbon_tab_name} module ribbon tab\033[0m"
            else:
                return f"\033[32m✔ {module_ribbon_tab_name} module ribbon tab is configured in CMS...Verification of {module_ribbon_tab_name} module ribbon tab is successful\033[0m"
        except BaseException as e:
            return f"\033[31mX Exception occurred while Verifing module ribbon tab: {str(e)}"

    def verify_odds_boost_is_enabled(self):
        """
        DESCRIPTION: Load CMS application and naviagte to Odds Boost
        EXPECTED: Active checkbox is enabled
        """
        path = 'odds-boost/%s' % self.brand
        odds_boost = self._cms_request.get(path)
        if not odds_boost['enabled']:
            self._cms_config.update_odds_boost_config(enabled=True)
        odds_boost = self._cms_request.get(path)
        if odds_boost['enabled']:
            return f"\033[32m✔ Odds Boost is enabled in CMS...Verification of Odds Boost enabled in CMS is successful\033[0m"
        else:
            return f"\033[31mX Odds Boost is not enabled in CMS...Verification of Odds Boost enabled in CMS is failed\033[0,"

    def delete_quizs_created_through_scripts(self):
        try:
            self._cms_config.delete_quizes_created_by_automation_scripts()
            res = "\033[32m✔ Quizs Deleted Successfully...\033[0m"
        except:
            res = "\033[31mX Unable to delete quizs....\033[0m""]]"
        return res


def main():
    env_dict = {'beta': 'hlv0', 'stg2': 'stg0', 'prod': 'prd0', 'qa2': 'tst0'}
    args = sys.argv[1:]
    if len(args) > 0:
        env = env_dict.get(args[0])
        brand = args[1]
    else:
        brand = 'bma'  # ladbrokes, bma
        env = env_dict.get("beta")  # beta, stg2, prd0, tst0, qa2
    check_config = Check_CMS_Configurations(env=env, brand=brand)
    expected_offer_modules = ['offer with no vip C28055', 'offer with vip_less_X C28055', 'offer with vip_X C28055',
                              'offer with vip_greater_X C28055',
                              'offer with no vip C28056', 'offer with vip_less_X C28056', 'offer with vip_X C28056',
                              'offer with vip_greater_X C28056',
                              'offer with no vip C28057', 'offer with vip_less_X C28057', 'offer with vip_X C28057',
                              'offer with vip_greater_X C28057']
    app = 'coral' if(brand == 'bma') else brand
    result = f"""
    \033[34m********** Verification of CMS configurations for {app} ************\033[0m
        {check_config.verification_of_all_sports_footer_menu()}           
        {check_config.check_offer_module_configured(expected_offer_modules)}
        {check_config.verify_5a_side_added_in_sport_categories()}
        {check_config.verify_lobby_added_in_header_submenus()}
        {check_config.verify_bet_builder_module_ribbon_tab_is_available()}
        {check_config.verify_odds_boost_is_enabled()}
        {check_config.delete_quizs_created_through_scripts()}
        """
    print(result)


if __name__ == '__main__':
    main()

"""
To run the script through Terminal follow the below steps
    1. Navigate to the directory where the script is present
        Ex: scripts/setup_data
    2. Execute the script using the below command
        python <script_name>.py <env> <brand>
        
"""
