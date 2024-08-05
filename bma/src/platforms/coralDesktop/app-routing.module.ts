import { LocationStrategy, PathLocationStrategy } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoggedInGuard } from '@coreModule/guards/logged-in-guard.service';
import { ContactUsComponent } from '@bmaModule/components/contactUs/contact-us.component';
import { NotFoundComponent } from '@bmaModule/components/404/404.component';
import { MaintenanceComponent } from '@sharedModule/components/maintenance/maintenance.component';
import { IRetailConfig } from '@coreModule/services/cms/models/system-config';
import { IRouteData } from '@coreModule/models/route-data.model';
import { StaticComponent } from '@bmaModule/components/static/static.component';
import { LazyRouteGuard } from '@coreModule/guards/lazy-route-guard.service';
import { routeData } from '@frontend/vanilla/core';
import { VANILLA_LAZY_ROUTES } from '@frontend/loaders/routes';
import { RootComponent } from '@coralDesktop/app.component';
import { ROOT_APP_ROUTES } from '@vanillaInitModule/root-routes.definitions';

import { routes as SbRoutes } from '@sbModule/sb-routing.module';
import { routes as RacingRoutes } from '@coralDesktop/racing/racing-routing.module';
import { routes as OlympicsRoutes } from '@olympicsModule/olympics-route.module';
import { routes as BetFinderRoutes } from '@betFinderModule/betfinder-routing.module';

import { LogoutResolver } from '@vanillaInitModule/services/logout/logout.service';
import { DesktopHomeComponent } from '@coralDesktop/bma/components/home/home.component';
import { ProductSwitchResolver } from '@app/host-app/product-switch.resolver';
import { DepositRedirectGuard } from '@coreModule/guards/deposit-redirect.guard';
import { SignUpRouteGuard } from '@core/guards/sign-up-guard.service';
import { MaintenanceGuard, MaintenanceResolver } from '@core/guards/maintenance-guard.service';
import { DesktopLiveStreamWrapperComponent } from '@coralDesktop/bma/components/liveStream/live-stream-wrapper.component';
import { NotFoundPageGuard } from '@core/guards/not-found-page-guard.service';
import { BetPackAuthGuard } from '@app/betpackMarket/guard/betpack-auth-guard.service';
import { BetPackReviewAuthGuard } from '@app/betpackMarket/guard/betpack-review-auth-guard.service';
import { RgyCheckGuard, RgyMatchGuard } from '@core/guards/rgy-check.guard';
import { rgyellow } from '@bma/constants/rg-yellow.constant';

const appRoutes: Routes = [
  {
    path: '',
    component: RootComponent,
    data: {
      ...routeData({ allowAnonymous: true }),
      product: 'host',
      segment: 'main'
    },
    runGuardsAndResolvers: 'always',
    resolve: {
      __p: ProductSwitchResolver
    },
    children: [
      {
        path: 'en',
        data: {
          segment: 'vanilla'
        },
        children: [
          ...VANILLA_LAZY_ROUTES,
          ...ROOT_APP_ROUTES,
          {
            path: '**',
            redirectTo: '/'
          }
        ]
      },
      ...SbRoutes,
      ...RacingRoutes,
      ...OlympicsRoutes,
      ...BetFinderRoutes,
      {
        path: '',
        component: DesktopHomeComponent,
        data: {
          segment: 'home'
        },
        children: [
          {
            path: '',
            pathMatch: 'full',
            loadChildren: () => import('@featuredModule/featured.module').then(m => m.FeaturedModule),
            data: {
              segment: 'home'
            }
          }
        ]
      }, {
        path: 'live-stream',
        component: DesktopLiveStreamWrapperComponent,
        data: {
          segment: 'liveStream'
        }
      }, {
        path: 'az-sports',
        data: {
          segment: 'azSports'
        },
        loadChildren: () => import('@lazy-modules/aToZMenu/aToZ-sports-page.module').then(m => m.LazyAToZSportPageModule)
      }, {
        path: 'logout',
        component: DesktopHomeComponent,
        resolve: {
          logout: LogoutResolver
        },
        data: {
          segment: 'logout'
        }
      }, {
        path: 'settings',
        loadChildren: () => import('@bma/components/userSettings/user-settings.module').then(m => m.UserSettingsModule),
        canActivate: [LoggedInGuard],
        runGuardsAndResolvers: 'always',
        data: {
          segment: 'settings'
        }
      }, {
        path: 'contact-us',
        component: ContactUsComponent,
        data: {
          segment: 'contactUs'
        }
      }, {
        path: 'static/:static-block',
        component: StaticComponent,
        data: {
          segment: 'static'
        }
      }, {
        path: 'freebets',
        loadChildren: () => import('@freebetsModule/freebets.module').then(m => m.FreebetsModule),
        canActivate: [LoggedInGuard],
        data: {
          segment: 'freebets'
        }
      }, {
        path: '404',
        component: NotFoundComponent,
        data: {
          segment: '404'
        }
      }, {
        path: 'under-maintenance',
        component: MaintenanceComponent,
        resolve: { data: MaintenanceResolver },
        canDeactivate: [MaintenanceGuard]
      }, {
        path: 'deposit',
        component: DesktopHomeComponent,
        canActivate: [DepositRedirectGuard]
      },
      // Modules lazy loaded by routes
      // Yourcall
      {
        path: 'yourcall-lazy-load',
        loadChildren: () => import('@yourCallModule/your-call.module').then(m => m.YourCallModule)
      },
      {
        path: 'tote-information',
        redirectTo: 'tote/information'
      }, {
        path: 'tote',
        loadChildren: () => import('@toteModule/tote.module').then(m => m.ToteModule)
      }, {
        path: 'virtual-sports',
        loadChildren: () => import('@coralDesktop/vsbr/vsbr.module').then(m => m.VsbrModule)
      }, {
        path: 'in-play',
        loadChildren: () => import('@inplayModule/inplay.module').then(m => m.InplayModule),
        data: {
          preload: true
        }
      }, {
        path: 'byb-module',
        loadChildren: () => import('@bybHistoryModule/byb-history.module').then(m => m.LazyBybHistoryModule),
        canActivate: [ LazyRouteGuard ]
      }, {
        path: 'betslip/add/:outcomeId',
        loadChildren: () => import('@betslipModule/betslip.module').then(m => m.BetslipModule)
      }, {
        path: 'betslip/unavailable',
        loadChildren: () => import('@betslipModule/betslip.module').then(m => m.BetslipModule)
      },
      {
        path: 'competitions/:sport/:className/:typeName',
        data: {
          segment: 'competitionTypeEvents'
        },
        loadChildren: () => import('@lazy-modules-module/competitionsSportTab/competitionsSportTab.module')
                              .then(m => m.CompetitionsTabModule)
      },
      {
        path: 'competition-filters',
        loadChildren: () => import('@lazy-modules-module/competitionFilters/competitionFilters.module')
                              .then(m => m.CompetitionFiltersModule)
      },
      // Odds Boost module lazy loading
      {
        path: 'superbooster',
        loadChildren: () => import('@oddsBoostModule/odds-boost.module').then(m => m.OddsBoostModule)
      },
      // Bet History module lazy loading
      {
        path: 'cashout',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      },
      {
        path: 'forecast-tricast-lazy-load',
        loadChildren: () => import('@lazy-modules-module/forecastTricast/forecastTricast.module').then(m => m.ForecastTricastModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'event-video-stream-lazy-load',
        loadChildren: () => import('@lazy-modules-module/eventVideoStream/event-video-stream.module')
                              .then(m => m.LazyEventVideoStreamModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'market-description-lazy-load',
        loadChildren: () => import('@lazy-modules-module/market-description/market-description.module')
                              .then(m => m.MarketDescriptionModule),
        canActivate: [LazyRouteGuard]
      },
      // Bet radar lazy loading
      {
        path: 'bet-radar-lazy-load',
        loadChildren: () => import('@lazy-modules-module/betRadarProvider/bet-radar.module').then(m => m.BetRadarCoralModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'racing-post-verdict-lazy-load',
        loadChildren: () => import('@lazy-modules-module/racingPostVerdict/racing-post-verdict.module')
                                  .then(m => m.RacingPostVerdictModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Receipt header lazy loading
      {
        path: 'receipt-header-lazy-load',
        loadChildren: () => import('@lazy-modules-module/receiptHeader/receipt-header.module').then(m => m.ReceiptHeaderModule),
        canActivate: [ LazyRouteGuard ]
      },
      // bet receipt bpmp tokens lazy load
      {
        path: 'bet-receipt-bpmp-tokens-lazy-load',
        loadChildren: () => import('@lazy-modules/bpmpFreeTokens/bpmp-tokens.module').then(m => m.BpmpFreeBetTokensModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Racing Post lazy loading
      {
       path: 'racing-post-lazy-load',
       loadChildren: () => import('@lazy-modules-module/racingPostTip/racing-post-tip.module').then(m => m.RacingPostTipModule),
       canActivate: [ LazyRouteGuard ]
      },
      // Next Race for Betslip lazy loading
      {
        path: 'next-races-lazy-load',
        loadChildren: () => import('@lazy-modules-module/nextRacesToBetslip/nextraces-to-betslip.module')
                                    .then(m => m.NextRacesToBetslipModule),
        canActivate: [ LazyRouteGuard ]
       },
      // Runner-spotlight lazy loading
      {
        path: 'runner-spotlight-lazy-load',
        loadChildren: () => import('@lazy-modules-module/runnerSpotlight/runner-spotlight.module').then(m => m.RunnerSpotlightModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: 'open-bets',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, {
        path: 'bet-history',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, {
        path: 'in-shop-bets',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      },
      // Betslip module lazy loading
      {
        path: 'voucher-code',
        loadChildren: () => import('@betslipModule/betslip.module').then(m => m.BetslipModule)
        },
      // Lotto module lazy loading
      // {
      //   path: 'lotto-results',
      //   redirectTo: 'lotto/results'
      // }, 
      {
        path: 'lotto',
        loadChildren: () => import('@lottoModule/lotto.module').then(m => m.LottoModule)
      },
      {
        path: 'big-competition',
        loadChildren: () => import('@bigCompetitionsModule/big-competitions.module').then(m => m.BigCompetitionsModule)
      },
      // Retail module lazy loading
      {
        path: 'retail',
        /* below 2 lines added for grid decommision in sports book*/
        redirectTo:'/shop-locator',
        pathMatch:'full',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'menu'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'betbundle-market',
        canActivate: [BetPackAuthGuard, RgyCheckGuard],
        data: {moduleName: rgyellow.BET_BUNDLES},
        loadChildren: () => import('@betpackModule/betpack-market.module').then(m => m.BetpackMarketModule),
      },
      {
        path: 'betbundle-review',
        canActivate: [BetPackReviewAuthGuard],
        loadChildren: () => import('@betpackReviewModule/betpack-review.module').then(m => m.BetpackReviewModule),
      },
      {
        path: 'retail-upgrade',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'upgrade'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'bet-filter',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'bet-filter/:child',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'bet-filter/:child/:child',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'bet-tracker',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'shopBetTracker'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'shop-locator',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'shopLocator'
        } as IRouteData<IRetailConfig>
      },
      // Quickbet
      {
        path: 'quickbet-lazy-load',
        loadChildren: () => import('@quickbetModule/quickbet.module').then(m => m.QuickbetModule),
        canActivate: [LazyRouteGuard]
      },
      // Quick Deposit
      {
        path: 'quick-deposit-lazy-load',
        loadChildren: () => import('@quickDepositModule/quick-deposit.module').then(m => m.QuickDepositModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'promotions',
        loadChildren: () => import('@promotionsModule/promotions.module').then(m => m.PromotionsModule),
        data: {
          path: 'promotions/retail',
          feature: 'promotions',
          moduleName: rgyellow.PROMOTIONS
        },
        canMatch: [RgyMatchGuard],
        canActivate: [RgyCheckGuard]
      },
     // ShowDown Module (TO-DO New Feature will be enabled in future)
      // {
      //   path: '5-a-side',
      //   loadChildren: () => import('@fiveASideShowDownModule/fiveASideShowDown.module').then(m => m.FiveASideShowDownModule)
      // },
      // Euro  Program
      {
        path: 'matchday-rewards',
        loadChildren: () => import('@euroModule/euro.module').then(m => m.EuroModule),
      },
      // EDP
      {
        path: 'edp-lazy-load',
        loadChildren: () => import('@edpModule/edp.module').then(m => m.EdpModule),
        canActivate: [LazyRouteGuard]
      },
      // Banners Module
      {
        path: 'banners-section',
        loadChildren: () => import('@lazy-modules-module/banners/banners.module').then(m => m.BannersModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: 'signup',
        canActivate: [SignUpRouteGuard],
        children: []
      },
      // Correct4
      {
        path: 'footballsuperseries',
        loadChildren: () => import('@questionEngine/question-engine.module').then(m => m.QuestionEngineModule),
        data: {
          segment: 'question-engine',
          moduleName: rgyellow.FOOTBALL_SUPER_SERIES
        },
        canMatch: [RgyMatchGuard]
      },
      // Other Question Engine versions
      {
        path: 'qe/:sourceId',
        loadChildren: () => import('@questionEngine/question-engine.module').then(m => m.QuestionEngineModule),
        data: {
          segment: 'question-engine'
        }
      },
      {
        path: 'seoStaticBlock-lazy-load',
        loadChildren: () => import('@lazy-modules/seoStaticBlock/seo-static-block.module').then(m => m.SeoStaticBlockModule),
        canActivate: [ LazyRouteGuard ]
      },
      // MaxPayoutError Component
      {
        path: 'maxpayout-error-container',
        loadChildren: () => import('@lazy-modules-module/maxpayOutErrorContainer/maxpayout-error-container.module')
        .then(m => m.MaxpayoutErrorContainerModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'extra-place-signposting',
        loadChildren: () => import('@lazy-modules-module/extraPlaceSignposting/extra-place-signposting.module')
        .then(m => m.ExtraPlaceSignpostingModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: '**',
        component: NotFoundComponent,
        canActivate: [ NotFoundPageGuard ]
      }
    ]
  }];

@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes,
      {
    useHash: false,
    paramsInheritanceStrategy: 'always',
    onSameUrlNavigation: 'reload',
    // enableTracing: true  // <-- debugging purposes only
}
    )
  ],
  exports: [
    RouterModule
  ],
  declarations: [],
  providers: [
    { provide: LocationStrategy, useClass: PathLocationStrategy }
  ]
})
export class AppRoutingModule { }