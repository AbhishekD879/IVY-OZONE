import { LocationStrategy, PathLocationStrategy } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from '@bma/components/home/home.component';
import { LoggedInGuard } from '@core/guards/logged-in-guard.service';
import { BuildYourBetHomeComponent } from '@sb/components/buildYourBetHome/build-your-bet-home.component';
import { PrivateMarketsTabComponent } from '@ladbrokesMobile/sb/components/privateMarketsTab/private-markets-tab.component';
import { NotFoundComponent } from '@bma/components/404/404.component';
import { MaintenanceComponent } from '@shared/components/maintenance/maintenance.component';
import { IRouteData } from '@app/core/models/route-data.model';
import { ILadbrokesRetailConfig } from '@ladbrokesMobile/core/services/cms/models/system-config';
import { FeaturedTabGuard } from '@core/guards/featured-tab-guard.service';
import { PrivateMarketsGuard } from '@core/guards/private-markets-guard.service';
import { ContactUsComponent } from '@bma/components/contactUs/contact-us.component';
import { SignUpRouteGuard } from '@core/guards/sign-up-guard.service';
import { LogoutResolver } from '@app/vanillaInit/services/logout/logout.service';
import { GermanSupportGuard } from '@app/core/guards/german-support-guard.service';
import { StaticComponent } from '@bma/components/static/static.component';
import { LazyRouteGuard } from '@core/guards/lazy-route-guard.service';
import { EventhubTabGuard } from '@core/guards/eventhub-tab-guard.service';
import { RootComponent } from '@ladbrokesMobile/app.component';
import { ProductSwitchResolver } from '@app/host-app/product-switch.resolver';
import { routeData } from '@frontend/vanilla/core';
import { VANILLA_LAZY_ROUTES } from '@frontend/loaders/routes';
import { ROOT_APP_ROUTES } from '@app/vanillaInit/root-routes.definitions';
import { routes as SbRoutes } from '@ladbrokesMobile/sb/sb-routing.module';
import { routes as FavouritesRoutes } from '@app/favourites/favourites-routing.module';
import { MaintenanceGuard, MaintenanceResolver } from '@core/guards/maintenance-guard.service';
import { DepositRedirectGuard } from '@coreModule/guards/deposit-redirect.guard';
import { NotFoundPageGuard } from '@core/guards/not-found-page-guard.service';
import { IRetailConfig } from '@core/services/cms/models/system-config';
import { FanzoneAuthGuard } from '@app/fanzone/guards/fanzone-auth-guard.service';
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
            canActivate: [FeaturedTabGuard]
          }
        ]
      }, {
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
            loadChildren: () => import('@ladbrokesMobile/featured/featured.module').then(m => m.FeaturedModule),
            canActivate: [EventhubTabGuard],
            data: {
              segment: 'featured'
            }
          },
          {
            path: 'betbuilder',
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
            loadChildren: () => import('@bma/components/inlayHomeTab/inplay-home-tab.module').then(m => m.InplayHomeTabModule),
            data: {
              segment: 'inPlay'
            }
          }, {
            path: 'byb-module',
            loadChildren: () => import('@bybHistoryModule/byb-history.module').then(m => m.LazyBybHistoryModule),
            canActivate: [ LazyRouteGuard ]
          }, {
            path: 'multiples',
            // eslint-disable-next-line max-len
            loadChildren: () => import('@lazy-modules-module/enhancedMultiplesTab/enhanced-multiples-tab.module').then(m => m.LazyEnhancedMultiplesTabModule),
            data: {
              segment: 'multiples'
            }
          }, {
            path: 'live-stream',
            loadChildren: () => import('@bma/components/liveStream/live-stream-wrapper.component.module').then(m => m.LiveStreamWrapperModule),
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
            canActivate: [GermanSupportGuard],
            data: {
              segment: 'nextRaces'
            },
            loadChildren: () => import('@ladbrokesMobile/lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module')
            .then(m => m.LazyNextRacesTabModule)
          }
        ]
      }, {
        path: 'live-stream',
        loadChildren: () => import('@bma/components/liveStream/live-stream-wrapper.component.module').then(m => m.LiveStreamWrapperModule),
        data: {
          segment: 'liveStream'
        }
      }, {
        path: 'az-sports',
        data: {
          segment: 'azSports'
        },
        loadChildren: () => import('@lazy-modules-module/aToZMenu/aToZ-sports-page.module').then(m => m.LazyAToZSportPageModule)
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
        loadChildren: () => import('@ladbrokesMobile/bma/components/userSettings/user-settings.module')
        .then(m => m.LadbrokesUserSettingsModule),
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
        canActivate: [GermanSupportGuard],
        children: []
      }, {
        path: 'tote',
        canActivate: [GermanSupportGuard],
        loadChildren: () => import('@toteModule/tote.module').then(m => m.ToteModule)
      }, {
        path: 'bet-finder',
        canActivate: [GermanSupportGuard],
        loadChildren: () => import('@betFinderModule/betfinder.module').then(m => m.BetFinderModule),
        data: {
          feature: 'raceBetFinder'
        } as IRouteData<ILadbrokesRetailConfig>
      }, {
        path: 'virtual-sports',
        loadChildren: () => import('@ladbrokesMobile/vsbr/vsbr.module').then(m => m.VsbrModule)
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

      // Odds Boost module lazy loading
      {
        path: 'oddsboost',
        loadChildren: () => import('@oddsBoostModule/odds-boost.module').then(m => m.OddsBoostModule)
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
      {
        path: 'signup',
        canActivate: [ SignUpRouteGuard ],
        children: []
      }, {
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
      //  canActivate: [GermanSupportGuard],
      //  children: []
      // }, 
      {
        path: 'lotto',
        canActivate: [GermanSupportGuard],
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
        path: 'retail-upgrade',
        loadChildren: () => import('@retailModule/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'upgrade'
        } as IRouteData<IRetailConfig>
      },
      {
        path: 'bet-filter',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<ILadbrokesRetailConfig>
      },
      {
        path: 'bet-filter/:child',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<ILadbrokesRetailConfig>
      },
      {
        path: 'bet-filter/:child/:child',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'footballFilter'
        } as IRouteData<ILadbrokesRetailConfig>
      },
      {
        path: 'bet-filter',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'digitalCoupons'
        } as IRouteData<ILadbrokesRetailConfig>
      },
      {
        path: 'digital-coupons',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'digitalCoupons'
        } as IRouteData<ILadbrokesRetailConfig>
      },
      {
        path: 'saved-betcodes',
        loadChildren: () => import('@retail-lazy-load/retail.module').then(m => m.RetailModule),
        data: {
          feature: 'savedBetCodes'
        } as IRouteData<ILadbrokesRetailConfig>
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
      // Racing lazy loading
      {
        path: 'horse-racing',
        loadChildren: () => import('@racingModule/horseracing.module').then(m => m.HorseracingModule),
        canActivate: [GermanSupportGuard]
      },
      {
        path: 'greyhound-racing',
        loadChildren: () => import('@racingModule/greyhound.module').then(m => m.GreyhoundModule),
        canActivate: [GermanSupportGuard]
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
      // Quickbet
      {
        path: 'quickbet-lazy-load',
        loadChildren: () => import('@quickbetModule/quickbet.module').then(m => m.QuickbetModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Yourcall
      {
        path: 'yourcall-lazy-load',
        loadChildren: () => import('@yourCallModule/your-call.module').then(m => m.YourCallModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Quick Deposit
      {
        path: 'quick-deposit-lazy-load',
        loadChildren: () => import('@quickDepositModule/quick-deposit.module').then(m => m.QuickDepositModule),
        canActivate: [ LazyRouteGuard ]
      },
      {
        path: 'fanzone',
        loadChildren: () => import('@ladbrokesMobile/fanzone/fanzone.module').then(m => m.FanzoneModule),
        canActivate: [FanzoneAuthGuard]
      },
      // Sport (SB) lazy loading
      {
        path: 'sport',
        loadChildren: () => import('@sbModule/sport/sport.module').then(m => m.LazySportModule)
      },

      // Event (SB) lazy loading
      {
        path: 'event',
        loadChildren: () => import('@sb/event/event.module').then(m => m.LazyEventModule)
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
      // Bet radar lazy loading
      {
        path: 'bet-radar-lazy-load',
        loadChildren: () => import('@lazy-modules-module/betRadarProvider/bet-radar.module').then(m => m.BetRadarLadbrokesModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Receipt header lazy loading
      {
        path: 'receipt-header-lazy-load',
        loadChildren: () => import('@lazy-modules-module/receiptHeader/receipt-header.module').then(m => m.ReceiptHeaderModule),
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
      // Racing-Post-Verdict lazy loading
      {
        path: 'racing-post-verdict-lazy-load',
        loadChildren: () => import('@lazy-modules-module/racingPostVerdict/racing-post-verdict.module')
                                  .then(m => m.RacingPostVerdictModule),
        canActivate: [LazyRouteGuard]
      },
      // Runner-spotlight lazy loading
      {
        path: 'runner-spotlight-lazy-load',
        loadChildren: () => import('@lazy-modules-module/runnerSpotlight/runner-spotlight.module').then(m => m.RunnerSpotlightModule),
        canActivate: [LazyRouteGuard]
      },
      // Market Selector
      {
        path:'market-selector',
        loadChildren: () => import('@sharedModule/components/marketSelector/market-selector.module').then(m => m.MarketSelectorModule),
        canActivate: [LazyRouteGuard]
      },
      {
        path: 'forecast-tricast-lazy-load',
        loadChildren: () => import('@lazy-modules-module/forecastTricast/forecastTricast.module').then(m => m.ForecastTricastModule),
        canActivate: [ LazyRouteGuard ]
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
      {
        path: 'event-video-stream-lazy-load',
        loadChildren: () => import('@lazy-modules-module/eventVideoStream/event-video-stream.module')
        .then(m => m.LazyEventVideoStreamModule),
        canActivate: [ LazyRouteGuard ]
      },
      // Freebets lazy loading
      {
        path: 'freebets-lazy-load',
        loadChildren: () => import('@freebetsModule/freebets.module').then(m => m.FreebetsModule),
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
      // ShowDown Module (New Feature)
      {
        path: '5-a-side',
        loadChildren: () => import('@fiveASideShowDownModule/fiveASideShowDown.module').then(m => m.FiveASideShowDownModule),
        data: {
          feature: 'show-down'
        }
      },
      {
        path: 'matchday-rewards',
        loadChildren: () => import('@euroModule/euro.module').then(m => m.EuroModule),
      },
      {
        path: '1-2-free',
        pathMatch: 'full',
        loadChildren: () => import('@app/oneTwoFree/one-two-free.module').then(m => m.OneTwoFreeModule),
        data: {
          segment: '1-2-free',
          moduleName: rgyellow.ONE_TWO_FREE
        },
        canMatch: [RgyMatchGuard]
      },
      {
        path: 'qe/:sourceId',
        loadChildren: () => import('@ladbrokesMobile/questionEngine/question-engine.module').then(m => m.QuestionEngineModule),
        data: {
          segment: 'question-engine'
        }
      },
      // Timeline
      {
        path: 'timeline-lazy-load',
        loadChildren: () => import('@lazy-modules-module/timeline/timeline.module')
        .then(m => m.TimelineModule),
        canActivate: [ LazyRouteGuard ]
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
export class AppRoutingModule { }
