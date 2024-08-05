import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './home.component';
import { MainDataResolver } from './cms-main-data.resolve';
import { FiveASideShowDownGuardService } from '@app/five-a-side-showdown/five-a-side-showdown-guard';

const homeRoutes: Routes = [
  {
    path: '',
    component: HomeComponent,
    resolve: {
      mainData: MainDataResolver
    },
    children: [
      {
        path: '',
        redirectTo: 'featured-modules',
        pathMatch: 'full'
      },
      {
        path: 'featured-modules',
        loadChildren: () => import('app/featured-tab/featured-tab.module').then(m => m.FeaturedTabModule)
      },
      {
        path: 'sports-pages/homepage',
        loadChildren: () => import('app/sports-pages/homepage/homepage.module').then(m => m.HomePageModule)
      },
      {
        path: 'sports-pages/event-hub',
        loadChildren: () => import('app/sports-pages/event-hub/event-hub.module').then(m => m.EventHubModule)
      },
      {
        path: 'sports-pages/sport-categories',
        loadChildren: () => import('app/sports-pages/sport-categories/sport-categories.module').then(m => m.SportCategoriesModule)
      },
      {
        path: 'football-coupon',
        loadChildren: () => import('app/football-coupon/football-coupon.module').then(m => m.FootballCouponModule)
      },
      {
        path: 'sports-pages/big-competition',
        loadChildren: () => import('app/sports-pages/big-competition/big-competition.module').then(m => m.BigCompetitionModule)
      },
      {
        path: 'sports-pages/olympics-pages',
        loadChildren: () => import('app/sports-pages/olympic-sports/olympics-sports.module').then(m => m.OlympicsModule)
      },
      {
        path: 'admin',
        loadChildren: () => import('app/admin/admin.module').then(m => m.AdminModule)
      },
      {
        path: 'banners/sport-banners',
        loadChildren: () => import('app/banners/sport-banners/sport.banners.module').then(m => m.SportBannersModule)
      },
      {
        path: 'banners/football-banners',
        loadChildren: () => import('app/banners/football-banners/football-banners.module').then(m => m.FootballBannersModule)
      },
      {
        path: 'banners/receipt/:type',
        loadChildren: () => import('app/banners/bet-receipt-banners/bet-receipt.module').then(m => m.BetReceiptModule)
      },
      {
        path: 'seo-pages',
        loadChildren: () => import('app/seo/seo.module').then(m => m.SeoModule)
      },
      {
        path: 'features',
        loadChildren: () => import('app/features/features.module').then(m => m.FeaturesModule)
      },
      {
        path: 'sso-page',
        loadChildren: () => import('app/sso/sso.module').then(m => m.SsoModule)
      },
      {
        path: 'system-configuration',
        loadChildren: () => import('app/system-configuration/system-configuration.module').then(m => m.SystemConfigurationModule)
      },
      {
        path: 'special-pages',
        loadChildren: () => import('app/special-pages/special-pages.module').then(m => m.SpecialPagesModule)
      },
      {
        path: 'static-blocks',
        loadChildren: () => import('app/static-blocks/static-blocks.module').then(m => m.StaticBlocksModule)
      },
      {
        path: 'edp-markets',
        loadChildren: () => import('app/edp-markets/edp-markets.module').then(m => m.EdpMarketsModule)
      },
      {
        path: 'racing-edp-markets',
        loadChildren: () => import('app/racing-edp-markets/racing-edp-markets.module').then(m => m.RacingEdpMarketsModule)
      },
      {
        path: 'leagues',
        loadChildren: () => import('app/leagues/leagues.module').then(m => m.LeaguesModule)
      },
      {
        path: 'dashboard',
        loadChildren: () => import('app/dashboard/dashboard.module').then(m => m.DashboardModule)
      },
      {
        path: 'promotions',
        loadChildren: () => import('app/promotions/promotions.module').then(m => m.PromotionsModule)
      },
      {
        path: 'widgets',
        loadChildren: () => import('app/widgets/widgets.module').then(m => m.WidgetsModule)
      },
      {
        path: 'countries-settings',
        loadChildren: () => import('app/countries/countries.module').then(m => m.CountriesModule)
      },
      {
        path: 'menu-configuration',
        loadChildren: () => import('app/menu-configuration/menu-configuration.module').then(m => m.MenuConfigurationModule)
      },
      {
        path: 'offers',
        loadChildren: () => import('app/offers/offers.module').then(m => m.OffersModule)
      },
      {
        path: 'maintenance',
        loadChildren: () => import('app/maintenance/maintenance.module').then(m => m.MaintenanceModule)
      },
      {
        path: 'module-ribbon-tabs',
        loadChildren: () => import('app/module-ribbon/module-ribbon.module').then(m => m.ModuleRibbonModule)
      },
      {
        path: 'odds-boost',
        loadChildren: () => import('app/odds-boost/odds-boost.module').then(m => m.OddsBoostModule)
      },
      {
        path: 'stat-content-info',
        loadChildren: () => import('app/stat-content-info/stat-content-info.module').then(m => m.StatContentInfoModule)
      },
      {
        path: 'yc/yc-leagues',
        loadChildren: () => import('app/your-call/your-call-leagues/your-call-leagues.module').then(m => m.YourCallLeaguesModule)
      },
      {
        path: 'yc/yc-markets',
        loadChildren: () => import('app/your-call/your-call-markets/your-call-markets.module').then(m => m.YourCallMarketsModule)
      },
      {
        path: 'yc/yc-static-blocks',
        loadChildren: () => import('app/your-call/your-call-static-blocks/your-call-static-blocks.module')
          .then(m => m.YourCallStaticBlocksModule)
      },
      {
        path: 'byb/byb-switchers',
        loadChildren: () => import('app/byb/byb-switchers/byb-switchers.module').then(m => m.BYBSwitchersModule)
      },

      {
        path: 'byb/byb-widget',
        loadChildren: () => import('app/byb/byb-widget/byb-widget.module').then(m => m.BybWidgetModule)
      },
      {
        path: 'byb/byb-markets',
        loadChildren: () => import('app/byb/byb-markets/byb-markets.module').then(m => m.BybMarketsModule)
      },
      {
        path: 'byb/5aSide',
        loadChildren: () => import('app/fiveASide/fiveASide.module').then(m => m.FiveASideModule)
      },
      {
        path: 'five-a-side-showdown',
        loadChildren: () => import('app/five-a-side-showdown/five-a-side-showdown.module').then(m => m.FiveASideShowdownModule),
        canActivate: [FiveASideShowDownGuardService]
      },
      {
        path: 'menus',
        loadChildren: () => import('app/menus/menus.module').then(m => m.MenusModule)
      },
      {
        path: 'payment-methods',
        loadChildren: () => import('app/payments/payments.module').then(m => m.PaymentsModule)
      },
      {
        path: 'lotto',
        loadChildren: () => import('app/lotto/lotto.module').then(m => m.LottoModule)
      },
      {
        path: 'quick-links',
        loadChildren: () => import('app/quick-links/quick-links.module').then(m => m.QuickLinksModule)
      },
      {
        path: 'stat-content-info',
        loadChildren: () => import('app/stat-content-info/stat-content-info.module').then(m => m.StatContentInfoModule)
      },
      {
        path: 'stream-and-bet',
        loadChildren: () => import('app/stream-and-bet/stream-and-bet.module').then(m => m.StreamAndBetModule)
      },
      {
        path: 'external-links',
        loadChildren: () => import('app/external-links/external-links.module').then(m => m.ExternalLinksModule)
      },
      {
        path: 'one-two-free/games',
        loadChildren: () => import('app/one-two-free/games/games.module').then(m => m.GamesModule)
      },
      {
        path: 'one-two-free/static-text',
        loadChildren: () => import('app/one-two-free/static-text/static-text.module').then(m => m.StaticTextOtfModule)
      },
      {
        path: 'one-two-free/qualification-rule',
        loadChildren: () => import('app/one-two-free/qualification-rule/qualification-rule.module').then(m => m.QualificationRuleModule)
      },
      {
        path: 'one-two-free/mybadge-detail',
        loadChildren: () => import('app/one-two-free/my-badges/my-badges.module').then(m => m.MyBadgesModule)
      },
      {
        path: 'one-two-free/otf-seasons',
        loadChildren: () => import('app/one-two-free/otf-seasons/otf-seasons.module').then(m => m.OtfSeasonsModule)
      },
      {
        path: 'one-two-free/otf-gamification',
        loadChildren: () => import('app/one-two-free/otf-gamification/otf-gamification.module').then(m => m.OtfGamificationModule)
      },
      {
        path: 'one-two-free/ios-app-toggle',
        loadChildren: () => import('app/one-two-free/ios-app-toggle/otf-ios-app-toggle.module').then(m => m.OtfIOSAppToggleModule)
      },
      {
        path: 'one-two-free/tab-name-configuration',
        loadChildren: () => import('app/one-two-free/tab-name-configuration/tab-name-configuration.module').then(m => m.TabNameConfigurationModule)
      },
      {
        path: 'on-boarding-guide',
        loadChildren: () => import('app/on-boarding-guide/on-boarding-guide.module').then(m => m.OnBoardingGuideModule)
      },
      {
        path: 'on-boarding-overlay',
        loadChildren: () => import('app/on-boarding-overlay/on-boarding-overlay.module').then(m => m.OnBoardingOverlayModule)
      },
      {
        path: 'betSharing',
        loadChildren: () => import('app/bet-sharing/bet-sharing.module').then(m => m.BetSharingModule)
      },
      {
        path: 'timeline/campaign',
        loadChildren: () => import('app/timeline/campaign/campaign.module').then(m => m.CampaignModule)
      },
      {
        path: 'timeline/system-config',
        loadChildren: () => import('app/timeline/system-config/system-config.module').then(m => m.SystemConfigModule)
      },
      {
        path: 'timeline/splash-page',
        loadChildren: () => import('app/timeline/splash-page/splash-page.module').then(m => m.SplashPageModule)
      },
      {
        path: 'question-engine/quiz',
        loadChildren: () => import('app/quiz/quiz-engine/quiz-engine.module').then(m => m.QuizEngineModule)
      },
      {
        path: 'question-engine/splash-pages',
        loadChildren: () => import('app/quiz/splash-page/splash-page.module').then(m => m.SplashPageModule)
      },
      {
        path: 'question-engine/quick-links',
        loadChildren: () => import('app/quiz/quick-links/quick-links.module').then(m => m.QuickLinksModule)
      },
      {
        path: 'question-engine/end-page',
        loadChildren: () => import('app/quiz/end-page/end-page.module').then(m => m.EndPageModule)
      },
      {
        path: 'timeline/template',
        loadChildren: () => import('app/timeline/template/template.module').then(m => m.TemplateModule)
      },
      {
        path: 'timeline/post',
        loadChildren: () => import('app/timeline/post/post.module').then(m => m.PostModule)
      },
      {
        path: 'question-engine/quiz-popup',
        loadChildren: () => import('app/quiz/quiz-popup/quiz-popup.module').then(m => m.QuizPopupModule)
      },
      {
        path: 'byb/asset-management',
        loadChildren: () => import('app/asset-management/assetManagement.module').then(m => m.AssetManagementModule)
      },
      {
        path: 'virtual-hub/virtual-sports',
        loadChildren: () => import('app/virtual-sports/virtual-sports.module').then(m => m.VirtualSportsModule)
      },
      {
        path: 'virtual-hub/top-sports',
        loadChildren: () => import('app/virtual-sports/top-sports/top-sports.module').then(m => m.TopSportsModule)
      },
      {
        path: 'secrets',
        loadChildren: () => import('app/secrets/secrets.module').then(m => m.SecretsModule)
      },
      {
        path: 'image-manager',
        loadChildren: () => import('app/image-manager/image-manager.module').then(m => m.ImageManagerModule)
      },
      {
        path: 'free-ride',
        loadChildren: () => import('app/free-ride/free-ride.module').then(m => m.FreeRideModule)
      },
      {
        path: 'lucky-dip',
        loadChildren: () => import('app/lucky-dip/lucky-dip.module').then(m => m.LuckyDipModule)
      },
      {
        path: 'arc-configurations',
        loadChildren: () => import('app/arc-configurations/arc-configurations.module').then(m => m.ArcConfigurationModule)
      },
      {
        path: 'statistics-links/league-links',
        loadChildren: () => import('app/statistics-links/league-links/league-links.module').then(m => m.LeagueLinksModule)
      },
      {
        path: 'statistics-links/market-links',
        loadChildren: () => import('app/statistics-links/market-links/market-links.module').then(m => m.MarketLinksModule)
      },
      {
        path: 'delete-segments',
        loadChildren: () => import('app/delete-segments/delete-segments.module').then(m => m.DeleteSegmentsModule)
      },
      {
        path: 'config-registry',
        loadChildren: () => import('app/config-registry/config-registry.module').then(m => m.ConfigRegistryModule)
      },
      {
        path: 'fanzones',
        loadChildren: () => import('app/fanzone/fanzone.module').then(m => m.FanzoneModule)
      },
      {
        path: 'network-indicator',
        loadChildren: () => import('app/network-indicator/network-indicator.module').then(m => m.NetworkIndicatorModule)
      },
      {
        path: 'betpack-market',
        loadChildren: () => import('app/betpack-market-place/betpack.module').then(m => m.BetPackModule)
      },
      {
        path: 'signposting',
        loadChildren: () => import('app/signposting/signposting.module').then(m => m.SignpostingModule)
      }, {
        path: 'bonus-suppression',
        loadChildren: () => import('app/bonus-suppression/bonus-suppression.module').then(m => m.BonusSuppressionModule)
      }, 
      {
        path: 'most-popular',
        loadChildren: () => import('app/popular-bets/popular-bets.module').then(m => m.PopularbetsModule)
      },
      {
        path: 'my-stable',
        loadChildren: () => import('app/mystable-configurations/mystable.module').then(m => m.MystableModule)
      },
      {
        path: 'rss-rewards',
        loadChildren: () => import('app/rss-rewards/rss-rewards.module').then(m => m.RssRewardsModule)
      },
      {
        path: 'my-bets',
        loadChildren: () => import('app/my-bets/my-bets.module').then(m => m.MyBetsModule)
      },
      {
        path: 'betslip',
        loadChildren: () => import('app/betslip/betslip.module').then(m => m.BetslipModule)
      },
    ]
  }
];

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(homeRoutes)
  ],
  exports: [
    RouterModule
  ],
  providers: [
    MainDataResolver,
    FiveASideShowDownGuardService
  ]
})
export class HomeRoutingModule { }
