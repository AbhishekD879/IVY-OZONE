import {OddsBoostService} from './odds-boost.service';
import {Injectable} from '@angular/core';
import {HttpBackend, HttpClient} from '@angular/common/http';
import 'rxjs/add/operator/map';

import {BrandService} from '../brand.service';
import {UserService} from './user.service';
import {BrandConfigService} from './brandConfig.service';
import {StaticBlocksService} from './staticBlocks.service';
import { FanzoneService } from '@app/client/private/services/http/fanzone.service';
import {PublicApiService} from './publicApi.service';
import {LoginService} from './login.service';
import {PromotionsService} from './promotions.service';
import {PromotionsSectionsService} from './promotions-sections.service';
import { PromotionsNavigationsService } from '@app/client/private/services/http/promotions-navigations.service';
import { PromotionsLeaderboardService } from '@app/client/private/services/http/promotions-leaderboard.service';
import {OffersService} from './offers.service';
import {OfferModulesService} from './offer-modules.service';
import {environment} from '@environment/environment';
import {SportCategoriesService} from './sportCategory.service';
import {MaintenanceService} from './maintenance.service';
import {FootballCouponService} from '@app/football-coupon/services/footballCoupon.service';
import {SeoPageService} from './seo.service';
import {OlympicsPageService} from './olympics.service';
import {WidgetsService} from './widgets.service';
import {DashboardService} from './dashboard.service';
import {SsoPagesService} from './sso.service';
import {LeagueService} from './league.service';
import {BannersService} from './banners.service';
import {Football3dBannersService} from './footballBanner.service';
import {BetReceiptMobileBannerService} from './betReceiptMobileBanner.service';
import {BetReceiptTabletBannerService} from './betReceiptTabletBanner.service';
import {CountriesService} from './countries.service';
import {ModuleRibbonService} from './moduleRibbon.service';
import {EdpMarketsService} from './edpMarkets.service';
import {RacingEdpMarketsService} from './racingEDPMarkets.service';
import {BrandsService} from './brands.service';
import {BrandMenuesService} from './brandMenus.service';
import {FeaturedTabModulesService} from './featuredTabModules.service';
import {YourCallLeaguesService} from './yourCallLeagues.service';
import {YourCallMarketsService} from './yourCallMarkets.service';
import {YourCallStaticBlocksService} from './yourCallStaticBlocks.service';
import {HeaderMenuService} from './menu/headerMenu.service';
import {HeaderSubMenuService} from './menu/headerSubMenu.service';
import {ConnectMenuService} from './menu/connectMenu.service';
import {RightMenuService} from './menu/rightMenu.service';
import {BankingMenuService} from './menu/bankingMenu.service';
import {UserMenuService} from './menu/userMenus.service';
import {SportCategoryService} from './menu/sportCategory.service';
import {FeatureService} from './feature.service';
import {FooterLogoService} from './menu/footerLogo.service';
import {FooterMenuService} from './menu/footerMenu.service';
import {TopGameService} from './menu/topGame.service';
import {BottomMenuService} from './menu/bottomMenu.service';
import {DesktopQuickLinkService} from './quick-links/desktopQuickLink.service';
import {HrQuickLinksService} from './quick-links/hrQuickLinks.service';
import {NavigationPointsService} from './quick-links/navigationPoints.service';
import { ExtraNavigationPointsService } from './quick-links/extraNavigationPoints.service';
import {CompetitionsService} from './competitions.service';
import {CompetitionTabsService} from './competitionTabs.service';
import {CompetitionSubTabsService} from './competitionSubTabs.service';
import {CompetitionModulesService} from './competitionModules.service';
import {CompetitionParticipantsService} from './competitionParticipants.service';
import {TinymceService} from './tinymce.service';
import {PaymentMethodsService} from './paymentMethods.service';
import {BYBSwitchersService} from './bybSwitchers.service';
import {BybMarketsService} from './bybMarkets.service';
import {StreamAndBetService} from './streamAndBet.service';
import {ExternalLinkService} from './externalLink.service';
import {HeaderContactMenuService} from './menu/headerContactMenu.service';
import {HomepageService} from './homepage.service';
import {SportsQuickLinksService} from './quick-links/sportsQuickLinks.service';
import {GamesService} from './games.service';
import {EventsService} from './gamesEvent.service';
import {StaticTextOtfService} from './staticTextOtf.service';
import {SportsHighlightCarouselsService} from './sportsHighlightCarousels.service';
import {MarketSelectorService} from '@app/football-coupon/services/marketSelector.service';
import {OnBoardingGuideService} from '@app/client/private/services/http/onBoardingGuide.service';
import {TeamKitService} from '@app/client/private/services/http/teamKit.service';
import {SportsSurfaceBetsService} from './sportsSurfaceBets.service';
import {EventHubService} from '@app/client/private/services/http/eventHub.service';
import {SportTabService} from '@app/client/private/services/http/sportTabs.service';
import {QualificationRuleService} from '@app/client/private/services/http/qualificationRuleService';
import {OtfIosAppToggleService} from '@app/client/private/services/http/otf-ios-app-toggle.service';
import {QuizService} from '@app/client/private/services/http/quiz.service';
import {SplashPageService} from '@app/client/private/services/http/splash-page.service';
import {QEQuickLinksService} from '@app/client/private/services/http/qeQuickLinks.service';
import {EndPageService} from '@app/client/private/services/http/end-page.service';
import {TimelineTemplateService} from '@app/client/private/services/http/timelineTemplate.service';
import {CampaignService} from '@app/client/private/services/http/campaign.service';
import {TimelinePostService} from '@app/client/private/services/http/timeline-post.service';
import {TimelineConfigService} from '@app/client/private/services/http/timeline-config.service';
import {TimelineSplashPageConfigService} from '@app/client/private/services/http/timeline-splash-page-config.service';
import {TimelineSpotlightService} from '@app/client/private/services/http/timeline-spotlight.service';

import {QuizPopupService} from '@app/client/private/services/http/quizPopup.service';
import {FiveASideService} from '@app/client/private/services/http/fiveASide.service';
import {GamingSubMenuService} from './gaming-submenu.service';
import {AssetManagementService} from '@app/client/private/services/http/assetManagement.service';
import {VirtualSportsService} from '@app/client/private/services/http/virtualSports.service';
import {VirtualSportsChildsService} from '@app/client/private/services/http/virtualSportsChilds.service';
import { SecretsService } from '@app/client/private/services/http/secrets.service';
import { ContestManagerService } from '@app/client/private/services/http/contestManager.service';
import { FAQService } from '@app/client/private/services/http/faq.service';
import { TermsAndConditionsService } from '@app/client/private/services/http/termsAndConditions.service';
import { welcomeOverlayService } from '@app/client/private/services/http/welcomeOverlay.Service';
import { EuroLoyaltyService } from '@app/client/private/services/http/euroLoyalty.service';
import { FreerideService } from '@app/client/private/services/http/freeride.service';
import { LuckyDipService } from '@app/client/private/services/http/lucky-dip.service';
import { SegmentManagerService } from '@app/client/private/services/http/segment-manager.service';
import { AutoseoService } from '@app/client/private/services/http/autoseo.service';
import { ARCConfigService } from '@app/client/private/services/http/arcConfig.service';
import { OtfSeasonBadgesService } from '@app/client/private/services/http/otfSeasonBadges.service';
import { LeagueLinksService } from './league-links.service';
import { MarketLinksService } from './market-links.service';
import { ConfigRegistryService } from '@app/client/private/services/http/config-registry.service';
import { networkIndicatorService } from './networkIndicator.service';
import { couponStatWidgetService } from './couponStatWidget.service';
import { BetPackMarketService } from './bet-pack-market.service';
import { OnboardBetpackService } from './onboard-betpack.service';
import { firstBetPlacementService } from './firstBetPlacement.service';
import { BetSharingAPIService } from '@app/bet-sharing/bet-sharing.api.service';
import { LottosService } from './lottos.service';
import { FreebetSignpostingService } from './freebet-signposting.service';
import { VirtualHubTopSportsService } from './virtual-hub-top-sports.service';
import {StatContentInfoService } from './statContentInfo.service';
import { BonusSuppressionService } from '@app/client/private/services/http/bonusSuppression.service';
import { PopularBetsApiService } from './popular-bets.api.service';
import { Router } from '@angular/router';
import { MyStableService } from '@app/client/private/services/http/my-stable.service';
import { RssRewardsService } from './rss-rewards.service';
import { MyBetsService } from '@root/app/my-bets/my-bets.service';
import { CouponMarketMappingService } from '@root/app/football-coupon/services/couponMarketMapping.service';
import { SportsNextEventCarouselsService } from './sportsNextEventCarousels.service';
import { ForYouService } from '@app/sports-pages/sport-categories/insights/for-you/for-you-personalized/for-you.service';
import { BybWidgetService } from '@root/app/byb/byb-widget/BYB-Widget/byb-widget.service';
import { PopularAccasWidgetService } from './popular-accas-widget.service';
import { BetSlipService } from './betslip.service';

@Injectable()
export class ApiClientService {

  private domain: string;
  private publicApiDomain: string;
  private brand: string;

  constructor(private http: HttpClient, private brandService: BrandService, private httpBackend: HttpBackend, private router: Router) {
    this.domain = environment.apiUrl;
    this.publicApiDomain = environment.publicApiUrl;
    this.brand = this.brandService.brand;
  }

  /**
   * creates service instance
   * @returns fanzoneService instance
   */
  public fanzoneService(): FanzoneService {
    return new FanzoneService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public paymentMethods(): PaymentMethodsService {
    return new PaymentMethodsService(this.http, this.domain, this.brand);
  }

  public user(): UserService {
    return new UserService(this.http, this.domain, this.brand);
  }

  public brandConfig(): BrandConfigService {
    return new BrandConfigService(this.http, this.domain, this.brand);
  }

  public bannersService(): BannersService {
    return new BannersService(this.http, this.domain, this.brand);
  }

  public footballBannersService(): Football3dBannersService {
    return new Football3dBannersService(this.http, this.domain, this.brand);
  }

  public promotionsService(): PromotionsService {
    return new PromotionsService(this.http, this.domain, this.brand);
  }

  public promotionsSectionsService(): PromotionsSectionsService {
    return new PromotionsSectionsService(this.http, this.domain, this.brand);
  }

  public promotionsNavigationsService(): PromotionsNavigationsService {
    return new PromotionsNavigationsService(this.http, this.domain, this.brand);
  }

  public promotionLeaderboardService(): PromotionsLeaderboardService {
    return new PromotionsLeaderboardService(this.http, this.domain, this.brand);
  }

  public seoPageService(): SeoPageService {
    return new SeoPageService(this.http, this.domain, this.brand);
  }

  public olympicsPageService(): OlympicsPageService {
    return new OlympicsPageService(this.http, this.domain, this.brand);
  }

  public ssoPagesService(): SsoPagesService {
    return new SsoPagesService(this.http, this.domain, this.brand);
  }

  public widgetsService(): WidgetsService {
    return new WidgetsService(this.http, this.domain, this.brand);
  }

  public sportCategoriesService(): SportCategoriesService {
    return new SportCategoriesService(this.http, this.domain, this.brand);
  }

  public publicApi(): PublicApiService {
    return new PublicApiService(this.http, this.publicApiDomain, this.brand);
  }

  public authorisation(): LoginService {
    return new LoginService(this.http, this.domain, this.brand);
  }

  public staticBlocks(): StaticBlocksService {
    return new StaticBlocksService(this.http, this.domain, this.brand);
  }

  public secrets(): SecretsService {
    return new SecretsService(this.http, this.domain, this.brand);
  }

  public tinymceService(): TinymceService {
    return new TinymceService(this.http, this.domain, this.brand);
  }

  public maintenance(): MaintenanceService {
    return new MaintenanceService(this.http, this.domain, this.brand);
  }

  public footballCoupon(): FootballCouponService {
    return new FootballCouponService(this.http, this.domain, this.brand);
  }

  public marketSelector(): MarketSelectorService {
    return new MarketSelectorService(this.http, this.domain, this.brand);
  }

  public couponMarketMapping(): CouponMarketMappingService {
    return new CouponMarketMappingService(this.http, this.domain, this.brand);
  }

  public dashboard(): DashboardService {
    return new DashboardService(this.http, this.domain, this.brand);
  }

  public league(): LeagueService {
    return new LeagueService(this.http, this.domain, this.brand);
  }

  public brands(): BrandsService {
    return new BrandsService(this.http, this.domain, this.brand);
  }

  public betReceiptMobileBanner(): BetReceiptMobileBannerService {
    return new BetReceiptMobileBannerService(this.http, this.domain, this.brand);
  }

  public betReceiptTabletBanner(): BetReceiptTabletBannerService {
    return new BetReceiptTabletBannerService(this.http, this.domain, this.brand);
  }

  public country(): CountriesService {
    return new CountriesService(this.http, this.domain, this.brand);
  }

  public moduleRibbonTab(): ModuleRibbonService {
    return new ModuleRibbonService(this.http, this.domain, this.brand);
  }

  public oddsBoost(): OddsBoostService {
    return new OddsBoostService(this.http, this.domain, this.brand);
  }

  public euroLoyalty(): EuroLoyaltyService {
    return new EuroLoyaltyService(this.http, this.domain, this.brand);
  }

  public arcConfig(): ARCConfigService {
    return new ARCConfigService(this.http, this.domain, this.brand);
  }

  public edp(): EdpMarketsService {
    return new EdpMarketsService(this.http, this.domain, this.brand);
  }

  public racingEdp(): RacingEdpMarketsService {
    return new RacingEdpMarketsService(this.http, this.domain, this.brand);
  }

  public featuredTabModules(): FeaturedTabModulesService {
    return new FeaturedTabModulesService(this.http, this.domain, this.brand);
  }

  public offersService() {
    return new OffersService(this.http, this.domain, this.brand);
  }

  public offerModulesService() {
    return new OfferModulesService(this.http, this.domain, this.brand);
  }

  public menues(): BrandMenuesService {
    return new BrandMenuesService(this.http, this.domain, this.brand);
  }

  public yourCallLeagues(): YourCallLeaguesService {
    return new YourCallLeaguesService(this.http, this.domain, this.brand);
  }

  public yourCallMarkets(): YourCallMarketsService {
    return new YourCallMarketsService(this.http, this.domain, this.brand);
  }

  public yourCallStaticBlocks(): YourCallStaticBlocksService {
    return new YourCallStaticBlocksService(this.http, this.domain, this.brand);
  }

  public fiveASideFormations(): FiveASideService {
    return new FiveASideService(this.http, this.domain, this.brand);
  }

  public assetManagements(): AssetManagementService {
    return new AssetManagementService(this.http, this.domain, this.brand);
  }

  public headerMenu(): HeaderMenuService {
    return new HeaderMenuService(this.http, this.domain, this.brand);
  }

  public headerSubMenu(): HeaderSubMenuService {
    return new HeaderSubMenuService(this.http, this.domain, this.brand);
  }

  public connectMenu(): ConnectMenuService {
    return new ConnectMenuService(this.http, this.domain, this.brand);
  }

  public rightMenu(): RightMenuService {
    return new RightMenuService(this.http, this.domain, this.brand);
  }

  public bankingMenu(): BankingMenuService {
    return new BankingMenuService(this.http, this.domain, this.brand);
  }

  public userMenu(): UserMenuService {
    return new UserMenuService(this.http, this.domain, this.brand);
  }

  public sportCategory(): SportCategoryService {
    return new SportCategoryService(this.http, this.domain, this.brand);
  }

  public feature(): FeatureService {
    return new FeatureService(this.http, this.domain, this.brand);
  }

  public footerLogo(): FooterLogoService {
    return new FooterLogoService(this.http, this.domain, this.brand);
  }

  public footerMenu(): FooterMenuService {
    return new FooterMenuService(this.http, this.domain, this.brand);
  }

  public topGame(): TopGameService {
    return new TopGameService(this.http, this.domain, this.brand);
  }

  public bottomMenu(): BottomMenuService {
    return new BottomMenuService(this.http, this.domain, this.brand);
  }

  public desktopQuickLink(): DesktopQuickLinkService {
    return new DesktopQuickLinkService(this.http, this.domain, this.brand);
  }

  public hrQuickLink(): HrQuickLinksService {
    return new HrQuickLinksService(this.http, this.domain, this.brand);
  }

  public sportsQuickLink(): SportsQuickLinksService {
    return new SportsQuickLinksService(this.http, this.domain, this.brand);
  }

  public sportsHighlightCarousel(): SportsHighlightCarouselsService {
    return new SportsHighlightCarouselsService(this.http, this.domain, this.brand);
  }

  public sportsNextEventCarousel(): SportsNextEventCarouselsService {
    return new SportsNextEventCarouselsService(this.http, this.domain, this.brand);
  }

  public sportsSurfaceBets(): SportsSurfaceBetsService {
    return new SportsSurfaceBetsService(this.http, this.domain, this.brand);
  }

  public sportCategoryService(): SportCategoriesService {
    return new SportCategoriesService(this.http, this.domain, this.brand);
  }

  public navigationPoints(): NavigationPointsService {
    return new NavigationPointsService(this.http, this.domain, this.brand);
  }

  public extraNavigationPoints():ExtraNavigationPointsService {
    return new ExtraNavigationPointsService(this.http, this.domain, this.brand);
  }

  public competitions(): CompetitionsService {
    return new CompetitionsService(this.http, this.domain, this.brand);
  }

  public competitionTabs(): CompetitionTabsService {
    return new CompetitionTabsService(this.http, this.domain, this.brand);
  }

  public competitionSubTabs(): CompetitionSubTabsService {
    return new CompetitionSubTabsService(this.http, this.domain, this.brand);
  }

  public competitionModules(): CompetitionModulesService {
    return new CompetitionModulesService(this.http, this.domain, this.brand);
  }

  public competitionParticipants(): CompetitionParticipantsService {
    return new CompetitionParticipantsService(this.http, this.domain, this.brand);
  }

  public bybSwitchers(): BYBSwitchersService {
    return new BYBSwitchersService(this.http, this.domain, this.brand);
  }

  public bybMarkets(): BybMarketsService {
    return new BybMarketsService(this.http, this.domain, this.brand);
  }

  public bybWidgetService(): BybWidgetService {
    return new BybWidgetService(this.http, this.domain, this.brand);
  }

  public streamAndBets(): StreamAndBetService {
    return new StreamAndBetService(this.http, this.domain, this.brand);
  }

  public externalLinks(): ExternalLinkService {
    return new ExternalLinkService(this.http, this.domain, this.brand);
  }

  public headerContactMenu(): HeaderContactMenuService {
    return new HeaderContactMenuService(this.http, this.domain, this.brand);
  }

  public homepages(): HomepageService {
    return new HomepageService(this.http, this.domain, this.brand);
  }

  public eventHub(): EventHubService {
    return new EventHubService(this.http, this.domain, this.brand);
  }

  public contestManagerService(): ContestManagerService {
    return new ContestManagerService(this.http, this.domain, this.brand);
  }

  public statContentInfoService(): StatContentInfoService{
    return new StatContentInfoService(this.http, this.domain, this.brand);
  }

  /**
   * To trigger terms condition service without default interceptor
   * @returns {TermsAndConditionsService}
   */
  public termsConditionService(): TermsAndConditionsService {
    return new TermsAndConditionsService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  /**
   * To trigger welcome overlay service without default interceptor
   * @returns {TermsAndConditionsService}
   */
   public welcomeOverlayService(): welcomeOverlayService {
    return new welcomeOverlayService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public couponStatWidgetService(): couponStatWidgetService {
    return new couponStatWidgetService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  /**
   * To trigger firstBetPlacement  service
   * @returns {firstBetPlacementService}
   */
  public firstBetPlacementService(): firstBetPlacementService {
    return new firstBetPlacementService(new HttpClient(this.httpBackend), this.domain, this.brand)
  }

  /**
   * To trigger network Indicator service without default interceptor
   * @returns {TermsAndConditionsService}
   */
   public networkIndicatorService(): networkIndicatorService {
    return new networkIndicatorService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  /**
    * To trigger betSharingAPI  service
    * @returns {betSharingApiService}
    */
  public betSharingApiService(): BetSharingAPIService {
    return new BetSharingAPIService(new HttpClient(this.httpBackend), this.domain, this.brand)
}
  /**
  * To trigger forYouService  service
  * @returns {ForYouService}
  */
  public forYouService(): ForYouService {
    return new ForYouService(new HttpClient(this.httpBackend), this.domain, this.brand)
  }
  /**

  /**
   * To trigger faq service
   * @returns {FAQService}
   */
  public faqService(): FAQService {
    return new FAQService(this.http, this.domain, this.brand);
  }

  public gamesService() {
    return new GamesService(this.http, this.domain, this.brand);
  }

  /**
   * To trigger OtfSeasonBadges Service
   * @returns {OtfSeasonBadgesService}
   */
  public otfSeasonBadgeService() {
    return new OtfSeasonBadgesService(this.http, this.domain, this.brand);
  }

  public quizService() {
    return new QuizService(this.http, this.domain, this.brand);
  }

  public eventsService(): EventsService {
    return new EventsService(this.http, this.domain, this.brand);
  }

  public staticTextOtfService() {
    return new StaticTextOtfService(this.http, this.domain, this.brand);
  }

  public qualificationRuleService() {
    return new QualificationRuleService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public quizPopupService() {
    return new QuizPopupService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public onBoardingGuide(): OnBoardingGuideService {
    return new OnBoardingGuideService(this.http, this.domain, this.brand);
  }

  public teamKitService(): TeamKitService {
    return new TeamKitService(this.http, this.domain, this.brand);
  }

  public sportTabService(): SportTabService {
    return new SportTabService(this.http, this.domain, this.brand);
  }

  public otfIOSAppToggleService() {
    return new OtfIosAppToggleService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public splashPageService(): SplashPageService {
    return new SplashPageService(this.http, this.domain, this.brand);
  }

  public qeQuickLinksService(): QEQuickLinksService {
    return new QEQuickLinksService(this.http, this.domain, this.brand);
  }

  public endPageService(): EndPageService {
    return new EndPageService(this.http, this.domain, this.brand);
  }

  public timelineTemplate(): TimelineTemplateService {
    return new TimelineTemplateService(this.http, this.domain, this.brand);
  }

  public campaignService(): CampaignService {
    return new CampaignService(this.http, this.domain, this.brand);
  }

  public postService(): TimelinePostService {
    return new TimelinePostService(this.http, this.domain, this.brand);
  }

  public timelineConfigService(): TimelineConfigService {
    return new TimelineConfigService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public timelineSplashConfigService(): TimelineConfigService {
    return new TimelineSplashPageConfigService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public gamaingSubMenuService(): GamingSubMenuService {
    return new GamingSubMenuService(this.http, this.domain, this.brand);
  }

  public virtualSportsService(): VirtualSportsService {
    return new VirtualSportsService(this.http, this.domain, this.brand);
  }

  public virtualSportsChildsService(): VirtualSportsChildsService {
    return new VirtualSportsChildsService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public lottosService(): LottosService{
    return new LottosService(this.http, this.domain, this.brand)
  }

  public timelineSpotlightService(): TimelineSpotlightService {
    return new TimelineSpotlightService(new HttpClient(this.httpBackend), this.domain, this.brand);
  }

  public freeRideService(): FreerideService {
    return new FreerideService(this.http, this.domain, this.brand);
  }

  public luckyDipService(): LuckyDipService {
    return new LuckyDipService(this.http, this.domain, this.brand);
  }

  /**
   * creates service instance
   * @returns segmentManagerService instance
   */
  public segmentMethods(): SegmentManagerService {
    return new SegmentManagerService(this.http, this.domain, this.brand);
  }

  /**
   * @returns new AutoseoService instance
   */
  public autoseoPageService(): AutoseoService {
    return new AutoseoService(this.http, this.domain, this.brand);
  }

  public statiscticsLeagueLinks(): LeagueLinksService {
    return new LeagueLinksService(this.http, this.domain, this.brand);
  }

  public statiscticsMarketLinks(): MarketLinksService {
    return new MarketLinksService(this.http, this.domain, this.brand);
  }
  public configRegistryService(): ConfigRegistryService {
    return new ConfigRegistryService(this.http, this.domain, this.brand);
  }
  /**
 * @returns new BetPackService instance
 */
  public betpackService(): BetPackMarketService {
    return new BetPackMarketService(this.http, this.domain, this.brand);
  }

  public onboardbetpackService(): OnboardBetpackService {
    return new OnboardBetpackService(this.http, this.domain, this.brand);
  }

  public freebetSignpostingService(): FreebetSignpostingService {
    return new FreebetSignpostingService(this.http, this.domain, this.brand);
  }

  public virtualHubTopSportsService(): VirtualHubTopSportsService {
    return new VirtualHubTopSportsService(this.http, this.domain, this.brand);
  }

  public bonusSuppressionService(): BonusSuppressionService {
    return new BonusSuppressionService(this.http, this.domain, this.brand);
  }

  /**
  * To trigger popularBetsApi  service
  * @returns {PopularBetsApiService}
  */
  public popularBetsApiService(): PopularBetsApiService {
    return new PopularBetsApiService(new HttpClient(this.httpBackend), this.domain, this.brand, this.router)
  }
  public myStableService(): MyStableService {
    return new MyStableService(this.http, this.domain, this.brand);
  }


  public rssRewards(): RssRewardsService {
    return new RssRewardsService(this.http, this.domain, this.brand);
  }
  public MyBetsService(): MyBetsService {
    return new MyBetsService(this.http, this.domain, this.brand);
  }

  /**
  * To trigger popularBetsApi  service
  * @returns {PopularBetsApiService}
  */
  public popularAccasWidgetService(): PopularAccasWidgetService {
    return new PopularAccasWidgetService(new HttpClient(this.httpBackend), this.domain, this.brand)
  }

  public betslipService(): BetSlipService{
    return new BetSlipService(this.http, this.domain, this.brand)
  }
}
