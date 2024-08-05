import logging

import crlat_swagger_cms.swagger_client.api as client

_logger = logging.getLogger('behave_logger')


def data_cleanup(context, scenario):
    userdata = context.config.userdata
    modules = userdata.get('module_to_remove', {})
    if modules.items():
        for name, ids in modules.items():

            # Featured
            if name == 'HomeModuleApi':
                home_module_api = client.HomeModuleApi(context.api_client)
                [home_module_api.delete_home_module_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # SportQuickLink
            if name == 'SportQuickLinkApi':
                quick_link_api = client.SportQuickLinkApi(context.api_client)
                [quick_link_api.sport_quick_link_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
                try:
                    quick_link_api.sport_quick_link_by_id(id=userdata['quick_link_1'])
                    quick_link_api.sport_quick_link_by_id(id=userdata['quick_link_2'])
                    _logger.info(
                        f'Removing data from userdata for scenario: "{scenario.name}" '
                        f'with ids: "{userdata["quick_link_1"]}" and "{userdata["quick_link_2"]}"')
                except KeyError:
                    pass

            # HighlightCarousel
            if name == 'HighlightCarouselApi':
                highlight_carousel_api = client.HighlightCarouselApi(context.api_client)
                [highlight_carousel_api.delete_highlight_carousel_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
                try:
                    highlight_carousel_api.delete_highlight_carousel_by_id(id=userdata['highlight_carousel_module_1'])
                    highlight_carousel_api.delete_highlight_carousel_by_id(id=userdata['highlight_carousel_module_2'])
                    _logger.info(
                        f'Removing data from userdata for scenario: "{scenario.name}" '
                        f'with ids: "{userdata["highlight_carousel_module_1"]}" '
                        f'and "{userdata["highlight_carousel_module_2"]}"')
                except KeyError:
                    pass

            # SurfaceBet
            if name == 'SurfaceBetApi':
                surface_bets_api = client.SurfaceBetApi(context.api_client)
                [surface_bets_api.delete_surface_bet_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
                try:
                    surface_bets_api.delete_surface_bet_by_id(id=userdata['surface_bets_module_1'])
                    surface_bets_api.delete_surface_bet_by_id(id=userdata['surface_bets_module_2'])
                    _logger.info(
                        f'Removing data from userdata for scenario: "{scenario.name}" '
                        f'with ids: "{userdata["surface_bets_module_1"]}" and "{userdata["surface_bets_module_2"]}"')
                except KeyError:
                    pass

            # Promotion
            if name == 'PromotionApi':
                promotion_api = client.PromotionApi(context.api_client)
                [promotion_api.promotion_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # EventHub
            if name == 'EventHubApi':
                event_hub_api = client.EventHubApi(context.api_client)
                [event_hub_api.event_hub_delete_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
                try:
                    event_hub_api.event_hub_delete_by_id(id=userdata['event_hub_1'])
                    event_hub_api.event_hub_delete_by_id(id=userdata['event_hub_2'])
                    _logger.info(
                        f'Removing data from userdata for scenario: "{scenario.name}" '
                        f'with ids: "{userdata["event_hub_1"]}" and "{userdata["event_hub_2"]}"')
                except KeyError:
                    pass

            # CMS 1-2 Free Games
            if name == 'GameApi':
                one_two_free_api = client.GameApi(context.api_client)
                [one_two_free_api.game_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
            if name == 'StaticTextOtfApi':
                static_text_otf_api = client.StaticTextOtfApi(context.api_client)
                [static_text_otf_api.static_text_otf_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
            if name == 'TeamKitApi':
                team_kit_api = client.TeamKitApi(context.api_client)
                [team_kit_api.delete_team_kit_by_id(id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Configuration and Structure
            if name == 'ConfigurationApi':
                conf_module_api = client.ConfigurationApi(context.api_client)
                brand = userdata.get('brand', 'bma')
                [conf_module_api.configuration_brand_element_by_brand(brand=brand, element_id=item) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
            if name == 'StructureApi':
                conf_module_api = client.StructureApi(context.api_client)
                [conf_module_api.delete_element(id=item, element_name=context.structure_element_name) for item in ids]
                _logger.info(
                    f'Removing data from userdata for scenario: "{scenario.name}" '
                    f'with ids: "{ids}" and element_name: "{context.structure_element_name}"')

            # ModuleRibbonTab
            if name == 'ModuleRibbonTabApi':
                module_ribbon_api = client.ModuleRibbonTabApi(context.api_client)
                [module_ribbon_api.module_ribbon_tab_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
                try:
                    module_ribbon_api.module_ribbon_tab_by_id(id=userdata['module_ribbon_tab_1'])
                    module_ribbon_api.module_ribbon_tab_by_id(id=userdata['module_ribbon_tab_2'])
                    _logger.info(
                        f'Removing data from userdata for scenario: "{scenario.name}" '
                        f'with ids: "{userdata["module_ribbon_tab_1"]}" and "{userdata["module_ribbon_tab_2"]}"')
                except KeyError:
                    pass

            # SportModule
            if name == 'SportModuleApi':
                conf_module_api = client.SportModuleApi(context.api_client)
                [conf_module_api.sport_module_delete_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Competition
            if name == 'CompetitionApi':
                competition_api = client.CompetitionApi(context.api_client)
                [competition_api.competition_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # NavigationPoint
            if name == 'NavigationPointApi':
                navigation_api = client.NavigationPointApi(context.api_client)
                [navigation_api.navigation_point_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Sport Category
            if name == 'SportCategoryApi':
                sport_category_api = client.SportCategoryApi(context.api_client)
                [sport_category_api.sport_category_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Seo page
            if name == 'SeoPageApi':
                seo_api = client.SeoPageApi(context.api_client)
                [seo_api.seo_page_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Sso page
            if name == 'SsoPageApi':
                sso_api = client.SsoPageApi(context.api_client)
                [sso_api.sso_page_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Offer module
            if name == 'OfferModuleApi':
                offer_module_api = client.OfferModuleApi(context.api_client)
                [offer_module_api.offer_module_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Offer
            if name == 'OfferApi':
                offer_api = client.OfferApi(context.api_client)
                [offer_api.offer_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Olympic Sports
            if name == 'SportOlympicSportsApi':
                olympic_sports_api = client.SportOlympicSportsApi(context.api_client)
                [olympic_sports_api.sport_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # Connect Menu
            if name == 'ConnectMenuApi':
                connect_menu_api = client.ConnectMenuApi(context.api_client)
                [connect_menu_api.connect_menu_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # CMS Users, Admins
            if name == 'UserApi':
                user_api = client.UserApi(context.api_client)
                [user_api.user_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # CMS Leagues
            if name == 'LeagueApi':
                league_api = client.LeagueApi(context.api_client)
                [league_api.league_by_id(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')

            # CMS EDP market
            if name == 'EdpMarketApi':
                edp_market_api = client.EdpMarketApi(context.api_client)
                [edp_market_api.edp_market_by_id_with_http_info(id=item) for item in ids]
                _logger.info(f'Removing data from userdata for scenario: "{scenario.name}" with ids: "{ids}"')
