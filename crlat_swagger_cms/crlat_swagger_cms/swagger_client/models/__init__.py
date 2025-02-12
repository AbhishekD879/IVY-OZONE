# coding: utf-8

# flake8: noqa
"""
    Oxygen CMS REST API

    CMS Private API (Used by CMS UI)   # noqa: E501

    OpenAPI spec version: 82.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from crlat_swagger_cms.swagger_client.models.app_update import AppUpdate
from crlat_swagger_cms.swagger_client.models.app_update2 import AppUpdate2
from crlat_swagger_cms.swagger_client.models.banking_menu import BankingMenu
from crlat_swagger_cms.swagger_client.models.banking_menu2 import BankingMenu2
from crlat_swagger_cms.swagger_client.models.banner import Banner
from crlat_swagger_cms.swagger_client.models.banner2 import Banner2
from crlat_swagger_cms.swagger_client.models.bet_receipt_banner import BetReceiptBanner
from crlat_swagger_cms.swagger_client.models.bet_receipt_banner2 import BetReceiptBanner2
from crlat_swagger_cms.swagger_client.models.bet_receipt_banner_tablet import BetReceiptBannerTablet
from crlat_swagger_cms.swagger_client.models.bet_receipt_banner_tablet2 import BetReceiptBannerTablet2
from crlat_swagger_cms.swagger_client.models.bottom_menu import BottomMenu
from crlat_swagger_cms.swagger_client.models.bottom_menu2 import BottomMenu2
from crlat_swagger_cms.swagger_client.models.brand import Brand
from crlat_swagger_cms.swagger_client.models.brand2 import Brand2
from crlat_swagger_cms.swagger_client.models.brand79 import Brand79
from crlat_swagger_cms.swagger_client.models.brand792 import Brand792
from crlat_swagger_cms.swagger_client.models.competition import Competition
from crlat_swagger_cms.swagger_client.models.competition2 import Competition2
from crlat_swagger_cms.swagger_client.models.competition_module import CompetitionModule
from crlat_swagger_cms.swagger_client.models.competition_module2 import CompetitionModule2
from crlat_swagger_cms.swagger_client.models.competition_participant import CompetitionParticipant
from crlat_swagger_cms.swagger_client.models.competition_participant2 import CompetitionParticipant2
from crlat_swagger_cms.swagger_client.models.competition_sub_tab import CompetitionSubTab
from crlat_swagger_cms.swagger_client.models.competition_sub_tab2 import CompetitionSubTab2
from crlat_swagger_cms.swagger_client.models.competition_tab import CompetitionTab
from crlat_swagger_cms.swagger_client.models.competition_tab2 import CompetitionTab2
from crlat_swagger_cms.swagger_client.models.configuration import Configuration
from crlat_swagger_cms.swagger_client.models.configuration2 import Configuration2
from crlat_swagger_cms.swagger_client.models.configuration_item import ConfigurationItem
from crlat_swagger_cms.swagger_client.models.configuration_item2 import ConfigurationItem2
from crlat_swagger_cms.swagger_client.models.connect_menu import ConnectMenu
from crlat_swagger_cms.swagger_client.models.connect_menu2 import ConnectMenu2
from crlat_swagger_cms.swagger_client.models.country import Country
from crlat_swagger_cms.swagger_client.models.country2 import Country2
from crlat_swagger_cms.swagger_client.models.dashboard import Dashboard
from crlat_swagger_cms.swagger_client.models.dashboard2 import Dashboard2
from crlat_swagger_cms.swagger_client.models.desktop_quick_link import DesktopQuickLink
from crlat_swagger_cms.swagger_client.models.desktop_quick_link2 import DesktopQuickLink2
from crlat_swagger_cms.swagger_client.models.edp_market import EdpMarket
from crlat_swagger_cms.swagger_client.models.edp_market2 import EdpMarket2
from crlat_swagger_cms.swagger_client.models.error import Error
from crlat_swagger_cms.swagger_client.models.external_link import ExternalLink
from crlat_swagger_cms.swagger_client.models.external_link2 import ExternalLink2
from crlat_swagger_cms.swagger_client.models.feature import Feature
from crlat_swagger_cms.swagger_client.models.feature2 import Feature2
from crlat_swagger_cms.swagger_client.models.featured_events_type import FeaturedEventsType
from crlat_swagger_cms.swagger_client.models.featured_events_type2 import FeaturedEventsType2
from crlat_swagger_cms.swagger_client.models.football3_d_banner import Football3DBanner
from crlat_swagger_cms.swagger_client.models.football3_d_banner2 import Football3DBanner2
from crlat_swagger_cms.swagger_client.models.footer_logo import FooterLogo
from crlat_swagger_cms.swagger_client.models.footer_logo2 import FooterLogo2
from crlat_swagger_cms.swagger_client.models.footer_menu import FooterMenu
from crlat_swagger_cms.swagger_client.models.footer_menu2 import FooterMenu2
from crlat_swagger_cms.swagger_client.models.gallery import Gallery
from crlat_swagger_cms.swagger_client.models.gallery2 import Gallery2
from crlat_swagger_cms.swagger_client.models.hr_quick_link import HRQuickLink
from crlat_swagger_cms.swagger_client.models.hr_quick_link2 import HRQuickLink2
from crlat_swagger_cms.swagger_client.models.header_contact_menu import HeaderContactMenu
from crlat_swagger_cms.swagger_client.models.header_contact_menu2 import HeaderContactMenu2
from crlat_swagger_cms.swagger_client.models.header_menu import HeaderMenu
from crlat_swagger_cms.swagger_client.models.header_menu2 import HeaderMenu2
from crlat_swagger_cms.swagger_client.models.header_sub_menu import HeaderSubMenu
from crlat_swagger_cms.swagger_client.models.header_sub_menu2 import HeaderSubMenu2
from crlat_swagger_cms.swagger_client.models.home_module import HomeModule
from crlat_swagger_cms.swagger_client.models.home_module2 import HomeModule2
from crlat_swagger_cms.swagger_client.models.league import League
from crlat_swagger_cms.swagger_client.models.league2 import League2
from crlat_swagger_cms.swagger_client.models.left_menu import LeftMenu
from crlat_swagger_cms.swagger_client.models.left_menu2 import LeftMenu2
from crlat_swagger_cms.swagger_client.models.login import Login
from crlat_swagger_cms.swagger_client.models.maintenance_page import MaintenancePage
from crlat_swagger_cms.swagger_client.models.maintenance_page2 import MaintenancePage2
from crlat_swagger_cms.swagger_client.models.module_ribbon_tab import ModuleRibbonTab
from crlat_swagger_cms.swagger_client.models.module_ribbon_tab2 import ModuleRibbonTab2
from crlat_swagger_cms.swagger_client.models.navigation_point import NavigationPoint
from crlat_swagger_cms.swagger_client.models.navigation_point2 import NavigationPoint2
from crlat_swagger_cms.swagger_client.models.offer import Offer
from crlat_swagger_cms.swagger_client.models.offer2 import Offer2
from crlat_swagger_cms.swagger_client.models.offer_module import OfferModule
from crlat_swagger_cms.swagger_client.models.offer_module2 import OfferModule2
from crlat_swagger_cms.swagger_client.models.ordering import Ordering
from crlat_swagger_cms.swagger_client.models.ordering2 import Ordering2
from crlat_swagger_cms.swagger_client.models.post import Post
from crlat_swagger_cms.swagger_client.models.post2 import Post2
from crlat_swagger_cms.swagger_client.models.promotion import Promotion
from crlat_swagger_cms.swagger_client.models.promotion2 import Promotion2
from crlat_swagger_cms.swagger_client.models.promotion_section import PromotionSection
from crlat_swagger_cms.swagger_client.models.promotion_section2 import PromotionSection2
from crlat_swagger_cms.swagger_client.models.quick_link import QuickLink
from crlat_swagger_cms.swagger_client.models.quick_link2 import QuickLink2
from crlat_swagger_cms.swagger_client.models.right_menu import RightMenu
from crlat_swagger_cms.swagger_client.models.right_menu2 import RightMenu2
from crlat_swagger_cms.swagger_client.models.seo_page import SeoPage
from crlat_swagger_cms.swagger_client.models.seo_page2 import SeoPage2
from crlat_swagger_cms.swagger_client.models.simple_module import SimpleModule
from crlat_swagger_cms.swagger_client.models.simple_module2 import SimpleModule2
from crlat_swagger_cms.swagger_client.models.site_serve_event_dto import SiteServeEventDto
from crlat_swagger_cms.swagger_client.models.site_serve_event_validation_result_dto import SiteServeEventValidationResultDto
from crlat_swagger_cms.swagger_client.models.site_serve_event_validation_result_dto2 import SiteServeEventValidationResultDto2
from crlat_swagger_cms.swagger_client.models.site_serve_knockout_event_dto import SiteServeKnockoutEventDto
from crlat_swagger_cms.swagger_client.models.site_serve_market_dto import SiteServeMarketDto
from crlat_swagger_cms.swagger_client.models.site_serve_minimal_event_dto import SiteServeMinimalEventDto
from crlat_swagger_cms.swagger_client.models.sport import Sport
from crlat_swagger_cms.swagger_client.models.sport2 import Sport2
from crlat_swagger_cms.swagger_client.models.sport_category import SportCategory
from crlat_swagger_cms.swagger_client.models.sport_category2 import SportCategory2
from crlat_swagger_cms.swagger_client.models.sport_quick_link import SportQuickLink
from crlat_swagger_cms.swagger_client.models.sport_quick_link2 import SportQuickLink2
from crlat_swagger_cms.swagger_client.models.sports_featured_tab import SportsFeaturedTab
from crlat_swagger_cms.swagger_client.models.sports_featured_tab2 import SportsFeaturedTab2
from crlat_swagger_cms.swagger_client.models.stats_competition_season import StatsCompetitionSeason
from crlat_swagger_cms.swagger_client.models.token_request import TokenRequest
from crlat_swagger_cms.swagger_client.models.token_response import TokenResponse
from crlat_swagger_cms.swagger_client.models.token_response2 import TokenResponse2
from crlat_swagger_cms.swagger_client.models.static_text_otf_dto import StaticTextOtfDto
