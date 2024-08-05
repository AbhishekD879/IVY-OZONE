import { Injectable } from '@angular/core';
import { LAZY_MODULES_MODULE, OTHER_MODULES } from './module.constants';

@Injectable({ providedIn: 'root' })
export class LazyComponentLoader {

        lazyLoadedModule: string;
        private readonly LAZY_MODULES: string[] = LAZY_MODULES_MODULE;
        private readonly OTHER_MODULES: string[] = OTHER_MODULES;
        constructor() { }

        /* eslint-disable */
        getModule(lazyLoadedModule: string): Promise<any> {
                if (this.LAZY_MODULES.includes(lazyLoadedModule)) {
                        return this.loadLazyModules(lazyLoadedModule);
                } else if (this.OTHER_MODULES.includes(lazyLoadedModule)) {
                        return this.loadOtherModules(lazyLoadedModule);
                } else {
                        return Promise.reject('Not a known module!');
                }
        }

        /**
         * To Load Lazy Modules by Path
         * @param {string} module
         * @returns {Promise<any}
         */
        private loadLazyModules(module: string): Promise<any> {
                switch (module) {
                        case '@lazy-modules-module/racingFeatured/racing-featured.module':
                                return import('@lazy-modules-module/racingFeatured/racing-featured.module');
                        case '@lazy-modules-module/competitionsSportTab/competitionsSportTab.module':
                                return import('@lazy-modules-module/competitionsSportTab/competitionsSportTab.module');
                        case '@lazy-modules-module/forecastTricast/forecastTricast.module':
                                return import('@lazy-modules-module/forecastTricast/forecastTricast.module');
                        case '@lazy-modules-module/eventVideoStream/event-video-stream.module':
                                return import('@lazy-modules-module/eventVideoStream/event-video-stream.module');
                        case '@lazy-modules-module/sortByOptions/sort-by-options.module':
                                return import('@lazy-modules-module/sortByOptions/sort-by-options.module');
                        case '@lazy-modules-module/superButton/super-button.module':
                                return import('@lazy-modules-module/superButton/super-button.module');
                        case '@lazy-modules-module/devLog/dev-log.module':
                                return import('@lazy-modules-module/devLog/dev-log.module');
                        case '@lazy-modules-module/rpg/rpg.module':
                                return import('@lazy-modules-module/rpg/rpg.module');
                        case '@lazy-modules-module/quiz/quiz-dialog.module':
                                return import('@lazy-modules-module/quiz/quiz-dialog.module');
                        case '@lazy-modules-module/receiptHeader/receipt-header.module':
                                return import('@lazy-modules-module/receiptHeader/receipt-header.module');
                        case '@lazy-modules-module/bpmpFreeTokens/bpmp-tokens.module':
                                return import('@lazy-modules-module/bpmpFreeTokens/bpmp-tokens.module');
                        case '@lazy-modules-module/betpackOnboarding/betpack-onboarding.module':
                                return import('@lazy-modules-module/betpackOnboarding/betpack-onboarding.module');
                        case '@lazy-modules-module/betRadarProvider/bet-radar.module':
                                return import('@lazy-modules-module/betRadarProvider/bet-radar.module');
                        case '@lazy-modules-module/runnerSpotlight/runner-spotlight.module':
                                return import('@lazy-modules-module/runnerSpotlight/runner-spotlight.module');
                        case '@lazy-modules-module/banners/banners.module':
                                return import('@lazy-modules-module/banners/banners.module');
                        case '@lazy-modules-module/market-description/market-description.module':
                                return import('@lazy-modules-module/market-description/market-description.module');
                        case '@lazy-modules-module/racingPostVerdict/racing-post-verdict.module':
                                return import('@lazy-modules-module/racingPostVerdict/racing-post-verdict.module');
                        case '@lazy-modules-module/racingPostTip/racing-post-tip.module':
                                return import('@lazy-modules-module/racingPostTip/racing-post-tip.module');
                        case '@lazy-modules-module/nextRacesToBetslip/nextraces-to-betslip.module':
                                return import('@lazy-modules-module/nextRacesToBetslip/nextraces-to-betslip.module');
                        case '@lazy-modules-module/competitionFilters/competitionFilters.module':
                                return import('@lazy-modules-module/competitionFilters/competitionFilters.module');
                        case '@lazy-modules-module/fiveASideShowDown/fiveaside-entry-confirmation.module':
                                return import('@lazy-modules-module/fiveASideShowDown/fiveaside-entry-confirmation.module');
                        case '@lazy-modules-module/timeline/timeline.module':
                                return import('@lazy-modules-module/timeline/timeline.module');
                        case '@lazy-modules-module/racingMyBets/racing-mybets.module':
                                return import('@lazy-modules-module/racingMyBets/racing-mybets.module');
                        case '@lazy-modules-module/maxpayOutErrorContainer/maxpayout-error-container.module':
                                return import('@lazy-modules-module/maxpayOutErrorContainer/maxpayout-error-container.module');
                        case '@lazy-modules-module/listTemplate/list-template.module':
                                return import('@lazy-modules-module/listTemplate/list-template.module');
                        case '@lazy-modules-module/customFlagFiltertoggle/custom-flag-filter-toggle.module':
                                return import('@lazy-modules-module/customFlagFiltertoggle/custom-flag-filter-toggle.module');  
                        case '@lazy-modules-module/multiMarketTemplate/multi-market-template.module':
                                return import('@lazy-modules-module/multiMarketTemplate/multi-market-template.module');
                        case '@lazy-modules-module/nextRaces/next-races.module':
                                return import('@lazy-modules-module/nextRaces/next-races.module');        
                        case '@lazy-modules-module/freeRide/freeRide.module':
                                return import('@lazy-modules-module/freeRide/free-ride.module');
                        case '@lazy-modules-module/floating-ihr-msg/floating-ihr-msg.module':
                                return import('@lazy-modules-module/floating-ihr-msg/floating-ihr-msg.module');
                        case '@lazy-modules-module/racingStatus/racing-status.module':
                                return import('@lazy-modules-module/racingStatus/racing-status.module');
                        case '@lazy-modules-module/racesMeetingsOverlay/racing-meetings.module': 
                                return import('@lazy-modules-module/racesMeetingsOverlay/racing-meetings.module');
                        case '@lazy-modules-module/fanzone/fanzone-shared.module':
                                return import('@lazy-modules-module/fanzone/fanzone-shared.module');
                        case '@lazy-modules-module/couponsModule/coupons.module':
                                return import('@lazy-modules-module/couponsModule/coupons.module');
                        case '@lazy-modules-module/raceCard/race-card-content.module':
                                return import('@lazy-modules-module/raceCard/race-card-content.module');
                        case '@lazy-modules-module/footerMenu/footer-menu.module':
                                return import('@lazy-modules-module/footerMenu/footer-menu.module');
                        case '@lazy-modules-module/coupon-stat-widget/coupon-stat-widget.module':
                                return import('@lazy-modules-module/coupon-stat-widget/coupon-stat-widget.module');
                        case '@lazy-modules-module/InplayHRHeader/inplay-hr-header.module':
                                return import('@lazy-modules-module/InplayHRHeader/inplay-hr-header.module');
                        case '@lazy-modules-module/InPlaySportTab/in-play-sport-tab.module':
                                return import('@lazy-modules-module/InPlaySportTab/in-play-sport-tab.module');
                        case '@lazy-modules-module/racingEventModel/racing-event-model.module':
                                return import('@lazy-modules-module/racingEventModel/racing-event-model.module');
                        case '@lazy-modules-module/raceMarket/race-market.module':
                                return import('@lazy-modules-module/raceMarket/race-market.module');
                        case '@lazy-modules-module/onBoardingTutorial/firstBetPlacement/first-bet-placement.module':
                                return import('@lazy-modules-module/onBoardingTutorial/firstBetPlacement/first-bet-placement.module')
                        case '@lazy-modules-module/racingFullResults/racing-full-results.module':
                                return import('@app/lazy-modules/racingFullResults/racing-full-results.module');
                        case '@lazy-modules-module/extraPlaceSignposting/extra-place-signposting.module':
                                return import('@lazy-modules-module/extraPlaceSignposting/extra-place-signposting.module');
                        case '@lazy-modules-module/raceCardInplay/race-card-inplay.module':
                                return import('@lazy-modules-module/raceCardInplay/race-card-inplay.module');     
                        case '@lazy-modules-module/twoUpSignpostingBlurbMsg/twoup-signposting-blurbmsg.module':
                                return import('@lazy-modules-module/twoUpSignpostingBlurbMsg/twoup-signposting-blurbmsg.module');
                        case '@lazy-modules-module/signposting/signposting.module':
                                return import('@lazy-modules-module/signposting/signposting.module');
                        case '@lazy-modules-module/lazyNextRacesTab/lazyNextRacesTab.module':
                                return import('@lazy-modules-module/lazyNextRacesTab/lazyNextRacesTab.module');
                        case '@lazy-modules-module/bet-share-image-card/bet-share-image-card.module':
                                return import('@lazy-modules-module/bet-share-image-card/bet-share-image-card.module');
                        case '@lazy-modules-module/lottoBetSlip/lotto-betslip.module':
                                return import('@lazy-modules-module/lottoBetSlip/lotto-betslip.module');                                
                        case '@lazy-modules-module/statisticalContentInformation/statistical-content-information.module':
                              return import('@lazy-modules-module/statisticalContentInformation/statistical-content-information.module');     
                        case '@lazy-modules-module/luckyDip/luckyDip.module':
                                return import('@lazy-modules-module/luckyDip/lucky-dip.module');
                        case '@lazy-modules-module/stream-bet-tutorial-pop-up/stream-bet-tutorial-pop-up.module':
                                return import('@lazy-modules-module/stream-bet-tutorial-pop-up/stream-bet-tutorial-pop-up.module');
                        case '@lazy-modules-module/eventQuickSwitch/quick-switch.module':
                                return import('@lazy-modules-module/eventQuickSwitch/quick-switch.module');
                        case '@lazy-modules-module/sidebar/sidebar.module':
                                return import('@lazy-modules-module/sidebar/sidebar.module');
                        case '@lazy-modules-module/carouselMenu/carousel-menu.module':
                                return import('@lazy-modules-module/carouselMenu/carousel-menu.module');
                        case '@lazy-modules-module/quickLinks/quick-links.module':
                                return import('@lazy-modules-module/quickLinks/quick-links.module');
                        case '@lazy-modules-module/promoLeaderboard/promo-leaderboard.module':
                                return import('@lazy-modules-module/promoLeaderBoard/promo-leaderboard.module');
                        case '@lazy-modules-module/home-screen/home-screen.module':
                                return import('@lazy-modules-module/home-screen/home-screen.module');
                        case '@lazy-modules-module/profit-indicator/profit-indicator.module':
                                return import('@lazy-modules-module/profit-indicator/profit-indicator.module');
                        case '@lazy-modules-module/virtualEntryPointBanner/virtual-entry-point-banner.module':
                                return import('@lazy-modules-module/virtualEntryPointBanner/virtual-entry-point-banner.module');
                }
        }

        /**
         * To Load Other Modules
         * @param {string} module
         * @returns {Promise<any>}
         */
        private loadOtherModules(module: string): Promise<any> {
                switch (module) {
                        case '@lazy-modules/locale/translation.module':
                                return import('@lazy-modules/locale/translation.module');
                        case '@app/stats/stats.module':
                                return import('@app/stats/stats.module');
                        case '@uktote-lazy-load/uk-tote.module':
                                return import('@uktote-lazy-load/uk-tote.module');
                        case '@lazy-modules/gamingOverlay/gaming-overlay.module':
                                return import('@lazy-modules/gamingOverlay/gaming-overlay.module');
                        case '@yourCallModule/your-call.module':
                                return import('@yourCallModule/your-call.module');
                        case '@oddsBoostModule/odds-boost.module':
                                return import('@oddsBoostModule/odds-boost.module');
                        case '@racingModule/racing.module':
                                return import('@racingModule/racing.module');
                        case '@retail-lazy-load/retail.module':
                                return import('@retail-lazy-load/retail.module');
                        case '@betHistoryModule/bet-history.module':
                                return import('@betHistoryModule/bet-history.module');
                        case '@featuredModule/featured.module':
                                return import('@featuredModule/featured.module');
                        case '@toteModule/tote.module':
                                return import('@toteModule/tote.module');
                        case '@betslipModule/betslip.module':
                                return import('@betslipModule/betslip.module');
                        case '@quickbetModule/quickbet.module':
                                return import('@quickbetModule/quickbet.module');
                        case '@quickbetStreamBetModule/sb-quickbet.module':
                                return import('@quickbetStreamBetModule/sb-quickbet.module');
                        case '@edpModule/edp.module':
                                return import('@edpModule/edp.module');
                        case '@inplayModule/inplay.module':
                                return import('@inplayModule/inplay.module');
                        case '@freebetsModule/freebets.module':
                                return import('@freebetsModule/freebets.module');
                        case '@quickDepositModule/quick-deposit.module':
                                return import('@quickDepositModule/quick-deposit.module');
                        case '@lazy-modules/seoStaticBlock/seo-static-block.module':
                                return import('@lazy-modules/seoStaticBlock/seo-static-block.module');
                        case '@sharedModule/components/marketSelector/market-selector.module':
                                return import('@sharedModule/components/marketSelector/market-selector.module');
                        case '@bybHistoryModule/byb-history.module':
                                return import('@bybHistoryModule/byb-history.module');
                        case '@rightColumnModule/right-column.module':
                                return import('@rightColumnModule/right-column.module');
                        case '@specialsModule/specials-sport-tab.module':
                                return import('@specialsModule/specials-sport-tab.module');
                        case '@sharedModule/components/oddsCard/oddsCardHightlightCarousel/odds-card-highligt-carousel.module':
                                return import('@sharedModule/components/oddsCard/oddsCardHightlightCarousel/odds-card-highligt-carousel.module');
                        case '@lazy-modules-module/lazyPromotionIcons/lazy-promotion-icons.module':
                                return import('@lazy-modules-module/lazyPromotionIcons/lazy-promotion-icons.module');
                        case '@lazy-modules-module/casinoMyBetsIntegration/casino-my-bets-integration.module':
                                return import('@lazy-modules-module/casinoMyBetsIntegration/casino-my-bets-integration.module');
                        case '@betpackModule/betpack-market.module':
                                return import('@betpackModule/betpack-market.module');
                        case '@lazy-modules/networkIndicator/network-indicator.module':
                                return import('@lazy-modules/networkIndicator/network-indicator.module');
                        case '@sharedModule/components/moduleRibbon/module-ribbon.module':
                                return import('@sharedModule/components/moduleRibbon/module-ribbon.module');
                        case '@inPlayLiveStream/inplay-live-stream.module':
                                return import('@inPlayLiveStream/inplay-live-stream.module');
                        // case '@couponsModule/coupons.module':
                        //         return import('@couponsModule/coupons.module');
                }
        }
}
