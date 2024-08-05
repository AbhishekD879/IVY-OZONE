import { LocationStrategy, PathLocationStrategy } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { routeData } from '@frontend/vanilla/core';
import { VANILLA_LAZY_ROUTES } from '@frontend/loaders/routes';
import { RootComponent } from '@coralMobile/app.component';
import { routes as SbRoutes } from '@sb/sb-routing.module';
import { routes as FavouritesRoutes } from '@app/favourites/favourites-routing.module';
import { HomeComponent } from '@bmaModule/components/home/home.component';
import { FeaturedTabGuard } from '@core/guards/featured-tab-guard.service';
import { EventhubTabGuard } from '@core/guards/eventhub-tab-guard.service';
import { BuildYourBetHomeComponent } from '@sb/components/buildYourBetHome/build-your-bet-home.component';
import { InplayHomeTabComponent } from '@bma/components/inlayHomeTab/inplay-home-tab.component';
import { PrivateMarketsTabComponent } from '@sb/components/privateMarketsTab/private-markets-tab.component';
import { LoggedInGuard } from '@core/guards/logged-in-guard.service';
import { PrivateMarketsGuard } from '@core/guards/private-markets-guard.service';
import { ContactUsComponent } from '@bma/components/contactUs/contact-us.component';
import { StaticComponent } from '@bma/components/static/static.component';
import { NotFoundComponent } from '@bma/components/404/404.component';
import { MaintenanceComponent } from '@shared/components/maintenance/maintenance.component';
import { IRouteData } from '@core/models/route-data.model';
import { IRetailConfig } from '@core/services/cms/models/system-config';
import { LazyRouteGuard } from '@core/guards/lazy-route-guard.service';
import { LogoutResolver } from '@vanillaInitModule/services/logout/logout.service';
import { ROOT_APP_ROUTES } from '@vanillaInitModule/root-routes.definitions';
import { ProductSwitchResolver } from '@app/host-app/product-switch.resolver';
import { DepositRedirectGuard } from '@coreModule/guards/deposit-redirect.guard';
import { SignUpRouteGuard } from '@core/guards/sign-up-guard.service';
import { MaintenanceGuard, MaintenanceResolver } from '@core/guards/maintenance-guard.service';
import { LiveStreamWrapperComponent } from '@bma/components/liveStream/live-stream-wrapper.component';
import { NotFoundPageGuard } from '@core/guards/not-found-page-guard.service';
import { RgyCheckGuard, RgyMatchGuard } from '@core/guards/rgy-check.guard';
import { rgyellow } from '@bma/constants/rg-yellow.constant';
import { BetPackAuthGuard } from '@app/betpackMarket/guard/betpack-auth-guard.service';
import { BetPackReviewAuthGuard } from '@app/betpackMarket/guard/betpack-review-auth-guard.service';

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
      ...FavouritesRoutes,
      {
        path: '',
        component: HomeComponent,
        data: {
          segment: 'home'
        },
        children: [
          {
            path: '',
            pathMatch: 'full',
            loadChildren: () => import('@featuredModule/featured.module').then(m => m.FeaturedModule),
            canActivate: [FeaturedTabGuard],
            data: {
              preload: true
            }
          }
        ]
      },
      {
        path: 'home',
        component: HomeComponent,
        data: {
          segment: 'home'
        },
        children: [
          {
            path: '',
            pathMatch: 'full',
            redirectTo: 'featured'
          },
          {
            path: 'featured',
            loadChildren: () => import('@featuredModule/featured.module').then(m => m.FeaturedModule),
            data: {
              segment: 'featured'
            }
          },
          {
            path: 'eventhub/:hubIndex',
            loadChildren: () => import('@featuredModule/featured.module').then(m => m.FeaturedModule),
            canActivate: [EventhubTabGuard],
            data: {
              segment: 'featured'
            }
          },
          {
            path: 'buildyourbet',
            component: BuildYourBetHomeComponent,
            data: {
              segment: 'buildYourBet'
            }
          },
          {
            path: 'coupons',
            loadChildren: () => import('@lazy-modules/couponsListHomeTab/coupons-list-home-tab.module')
                                  .then(m => m.LazyCouponsListHomeTabModule)
          },
          {
            path: 'in-play',
            component: InplayHomeTabComponent,
            data: {
              segment: 'inPlay'
            }
          },
          {
            path: 'multiples',
            loadChildren: () => import('@lazy-modules/enhancedMultiplesTab/enhanced-multiples-tab.module').then(m => m.LazyEnhancedMultiplesTabModule),
            data: {
              segment: 'multiples'
            }
          },
          {
            path: 'live-stream',
            component: LiveStreamWrapperComponent,
            data: {
              segment: 'liveStream'
            }
          },
          {
            path: 'private-markets',
            component: PrivateMarketsTabComponent,
            canActivate: [LoggedInGuard, PrivateMarketsGuard],
            data: {
              segment: 'privateMarkets'
            }
          },
          {
            path: 'next-races',
            data: {
              segment: 'nextRaces'
            },
            loadChildren: () => import('@lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module').then(m => m.LazyNextRacesTabModule)
          }
        ]
      }, {
        path: 'live-stream',
        component: LiveStreamWrapperComponent,
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
        component: HomeComponent,
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
        component: HomeComponent,
        canActivate: [DepositRedirectGuard]
      },
      // Modules lazy loaded by routes
      {
        path: 'tote-information',
        redirectTo: 'tote/information'
      }, {
        path: 'tote',
        loadChildren: () => import('@toteModule/tote.module').then(m => m.ToteModule)
      }, {
        path: 'bet-finder',
        loadChildren: () => import('@betFinderModule/betfinder.module').then(m => m.BetFinderModule)
      }, {
        path: 'virtual-sports',
        loadChildren: () => import('@app/vsbr/vsbr.module').then(m => m.VsbrModule)
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
      // Betslip module lazy loading
      {
        path: 'voucher-code',
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
      {
        path: 'cashout',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, {
        path: 'open-bets',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, {
        path: 'bet-history',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, {
        path: 'in-shop-bets',
        loadChildren: () => import('@betHistoryModule/bet-history.module').then(m => m.BetHistoryModule)
      }, 
      // {
      //   path: 'lotto-results',
      //   redirectTo: 'lotto/results'
      // },
      {
        path: 'lotto',
        loadChildren: () => import('@lottoModule/lotto.module').then(m => m.LottoModule)
      }, {
        path: 'big-competition',
        loadChildren: () => import('@app/bigCompetitions/big-competitions.module').then(m => m.BigCompetitionsModule)
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
        path: 'shop-locator',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'shopLocator'
        } as IRouteData<IRetailConfig>
      },
      // Racing lazy loading
      {
        path: 'horse-racing',
        loadChildren: () => import('@racing/horseracing.module').then(m => m.HorseracingModule)
      },
      {
        path: 'greyhound-racing',
        loadChildren: () => import('@racing/greyhound.module').then(m => m.GreyhoundModule)
      },
      // EDP
      {
        path: 'edp-lazy-load',
        loadChildren: () => import('@edpModule/edp.module').then(m => m.EdpModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Banners Module
      {
        path: 'banners-section',
        loadChildren: () => import('@lazy-modules-module/banners/banners.module').then(m => m.BannersModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: 'market-description-lazy-load',
        loadChildren: () => import('@lazy-modules-module/market-description/market-description.module')
                              .then(m => m.MarketDescriptionModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'fiveAside-entry-confirmation-lazy-load',
        loadChildren: () => import('@lazy-modules-module/fiveASideShowDown/fiveaside-entry-confirmation.module')
          .then(m => m.FiveASideEntryConfirmationModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: 'odds-card-highlight-carousel-lazy-load',
        loadChildren: () => import('@sharedModule/components/oddsCard/oddsCardHightlightCarousel/odds-card-highligt-carousel.module')
          .then(m => m.OddsCardHighlightCarouselModule),
        canActivate: [LazyRouteGuard],
        data: {
          preload: true
        }
      },
      // Sport (SB) lazy loading
      {
        path: 'sport',
        loadChildren: () => import('@sbModule/sport/sport.module').then(m => m.LazySportModule)
      },

      // Event (SB) lazy loading
      {
        path: 'event',
        loadChildren: () => import('@sbModule/event/event.module').then(m => m.LazyEventModule)
      },

      // Coupons lazy loading
      {
        path: 'coupons',
        loadChildren: () => import('@lazy-modules/couponsPage/coupons-page.module').then(m => m.LazyCouponsPageModule)
      },

      // Olympics lazy loading
      {
        path: 'olympics',
        loadChildren: () => import('@olympicsModule/olympics.module').then(m => m.OlympicsModule)
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
      // Bet radar lazy loading
      {
        path: 'bet-radar-lazy-load',
        loadChildren: () => import('@lazy-modules-module/betRadarProvider/bet-radar.module').then(m => m.BetRadarCoralModule),
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
      // bet pack onboarding
      {
        path: 'bet-pack-onboarding-lazy-load',
        loadChildren: () => import('@lazy-modules/betpackOnboarding/betpack-onboarding.module').then(m => m.BetpackOnBoardingModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Signposting lazy loading
      {
        path: 'signposting-lazy-load',
        loadChildren: () => import('@lazy-modules/signposting/signposting.module').then(m => m.SignpostingModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Racing-Post-Verdict lazy loading
      {
        path: 'racing-post-verdict-lazy-load',
        loadChildren: () => import('@lazy-modules-module/racingPostVerdict/racing-post-verdict.module')
                                  .then(m => m.RacingPostVerdictModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Racing Post lazy loading
      {
        path: 'racing-post-lazy-load',
        loadChildren: () => import('@lazy-modules-module/racingPostTip/racing-post-tip.module')
          .then(m => m.RacingPostTipModule),
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
        path:'market-selector',
        loadChildren: () => import('@sharedModule/components/marketSelector/market-selector.module').then(m => m.MarketSelectorModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path:'market-selector',
        loadChildren:() => import('@sharedModule/components/marketSelector/market-selector.module').then(m => m.MarketSelectorModule),
        canActivate: [LazyRouteGuard]
      },
      // Quickbet
      {
        path: 'quickbet-lazy-load',
        loadChildren: () => import('@quickbetModule/quickbet.module').then(m => m.QuickbetModule),
        canActivate: [ LazyRouteGuard ]
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
      {
        // path: 'euro',
        path: 'matchday-rewards',
        loadChildren: () => import('@euroModule/euro.module').then(m => m.EuroModule),
      },
      {
        path: 'signup',
        canActivate: [ SignUpRouteGuard ],
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
        canMatch: [RgyMatchGuard],
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
        path: 'module-ribbon-lazy-load',
        loadChildren: () => import('@sharedModule/components/moduleRibbon/module-ribbon.module')
          .then(m => m.RibbonModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: '**',
        component: NotFoundComponent,
        canActivate: [ NotFoundPageGuard ]
      }
    ]
  }
];

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
export class AppRoutingModule {}
