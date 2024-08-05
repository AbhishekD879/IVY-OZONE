import { LazyComponentLoader } from '@core/services/lazyComponentFactory/lazy-component.loader';

describe('LazyComponentFactory -', () => {
  let service: LazyComponentLoader;

  beforeEach(() => {
    service = new LazyComponentLoader();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('@getModule (Lazy-Modules)', () => {
    it('should return racing-featured.module', () => {
      const response = service.getModule('@lazy-modules-module/racingFeatured/racing-featured.module');
      expect(response).not.toBe(null);
    });
    it('should return competitionsSportTab.module', () => {
        const response = service.getModule('@lazy-modules-module/competitionsSportTab/competitionsSportTab.module');
        expect(response).not.toBe(null);
    });
    it('should return forecastTricast.module', () => {
        const response = service.getModule('@lazy-modules-module/forecastTricast/forecastTricast.module');
        expect(response).not.toBe(null);
    });
    it('should return event-video-stream.module', () => {
        const response = service.getModule('@lazy-modules-module/eventVideoStream/event-video-stream.module');
        expect(response).not.toBe(null);
    });
    it('should return sort-by-options.module', () => {
        const response = service.getModule('@lazy-modules-module/sortByOptions/sort-by-options.module');
        expect(response).not.toBe(null);
    });
    it('should return super-button.module', () => {
        const response = service.getModule('@lazy-modules-module/superButton/super-button.module');
        expect(response).not.toBe(null);
    });
    it('should return dev-log.module', () => {
        const response = service.getModule('@lazy-modules-module/devLog/dev-log.module');
        expect(response).not.toBe(null);
    });
    it('should return rpg.module', () => {
        const response = service.getModule('@lazy-modules-module/rpg/rpg.module');
        expect(response).not.toBe(null);
    });
    it('should return quiz-dialog.module', () => {
        const response = service.getModule('@lazy-modules-module/quiz/quiz-dialog.module');
        expect(response).not.toBe(null);
    });
    it('should return receipt-header.module', () => {
        const response = service.getModule('@lazy-modules-module/receiptHeader/receipt-header.module');
        expect(response).not.toBe(null);
    });
    it('should return bpmp-tokens.module', () => {
        const response = service.getModule('@lazy-modules-module/bpmpFreeTokens/bpmp-tokens.module');
        expect(response).not.toBe(null);
    });
    it('should return bet-radar.module', () => {
        const response = service.getModule('@lazy-modules-module/betRadarProvider/bet-radar.module');
        expect(response).not.toBe(null);
    });
    it('should return runner-spotlight.module', () => {
        const response = service.getModule('@lazy-modules-module/runnerSpotlight/runner-spotlight.module');
        expect(response).not.toBe(null);
    });
    it('should return banners.module', () => {
        const response = service.getModule('@lazy-modules-module/banners/banners.module');
        expect(response).not.toBe(null);
    });
    it('should return market-description.module', () => {
        const response = service.getModule('@lazy-modules-module/market-description/market-description.module');
        expect(response).not.toBe(null);
    });
    it('should return racing-post-verdict.module', () => {
        const response = service.getModule('@lazy-modules-module/racingPostVerdict/racing-post-verdict.module');
        expect(response).not.toBe(null);
    });
    it('should return racing post tip.module', () => {
        const response = service.getModule('@lazy-modules-module/racingPostTip/racing-post-tip.module');
        expect(response).not.toBe(null);
    });
    it('should return next races to betslip', () => {
        const response = service.getModule('@lazy-modules-module/nextRacesToBetslip/nextraces-to-betslip.module');
        expect(response).not.toBe(null);
    });
    it('should return banners.module', () => {
        const response = service.getModule('@lazy-modules-module/banners/banners.module');
        expect(response).not.toBe(null);
    });
    it('should return fiveASide-entry-confirmation', () => {
        const response = service.getModule('@lazy-modules-module/fiveASideShowDown/fiveaside-entry-confirmation.module');
        expect(response).not.toBe(null);
    });
    it('should return timeline.module', () => {
        const response = service.getModule('@lazy-modules-module/timeline/timeline.module');
        expect(response).not.toBe(null);
    });
    it('should return az-sports-page.module', () => {
        const response = service.getModule('@lazy-modules-module/aToZMenu/az-sports-page.module');
        expect(response).not.toBe(null);
    });
    it('should return maxpayout-error-container', () => {
        const response = service.getModule('@lazy-modules-module/maxpayOutErrorContainer/maxpayout-error-container.module');
        expect(response).not.toBe(null);
    });
    it('should return list-template.module', () => {
        const response = service.getModule('@lazy-modules-module/listTemplate/list-template.module');
        expect(response).not.toBe(null);
      });
    it('should return competitionFilters Module', () => {
        const response = service.getModule('@lazy-modules-module/competitionFilters/competitionFilters.module');
        expect(response).not.toBe(null);
    });
    it('should return freeRide Module', () => {
        const response = service.getModule('@lazy-modules-module/freeRide/freeRide.module');
        expect(response).not.toBe(null);
    });
    it('should return meetingOverlay Module', () => {
        const response = service.getModule('@lazy-modules-module/racesMeetingsOverlay/racing-meetings.module');
        expect(response).not.toBe(null);
    });
    it('should return lazyNextRacesTab Module', () => {
        const response = service.getModule('@lazy-modules-module/lazyNextRacesTab/lazyNextRacesTab.module');
        expect(response).not.toBe(null);
    });
    it('should return profit-indicator Module', () => {
        const response = service.getModule('@lazy-modules-module/profit-indicator/profit-indicator.module');
        expect(response).not.toBe(null);
      });
    it('should return stream-bet-tutorial-pop-up.module', () => {
        const response = service.getModule('@lazy-modules-module/stream-bet-tutorial-pop-up/stream-bet-tutorial-pop-up.module');
        expect(response).not.toBe(null);
    });
    it('should return quick-switch.module', () => {
        const response = service.getModule('@lazy-modules-module/eventQuickSwitch/quick-switch.module');
        expect(response).not.toBe(null);
    });
});

  describe('@getModule (Other-Modules)', () => {
    it('should return translation.module', () => {
      const response = service.getModule('@lazy-modules/locale/translation.module');
      expect(response).not.toBe(null);
    });
    it('should return stats.module', () => {
        const response = service.getModule('@app/stats/stats.module');
        expect(response).not.toBe(null);
    });
    it('should return uk-tote.module', () => {
        const response = service.getModule('@uktote-lazy-load/uk-tote.module');
        expect(response).not.toBe(null);
    });
    it('should return gaming-overlay.module', () => {
        const response = service.getModule('@lazy-modules/gamingOverlay/gaming-overlay.module');
        expect(response).not.toBe(null);
    });
    it('should return your-call.module', () => {
        const response = service.getModule('@yourCallModule/your-call.module');
        expect(response).not.toBe(null);
    });
    it('should return odds-boost.module', () => {
        const response = service.getModule('@oddsBoostModule/odds-boost.module');
        expect(response).not.toBe(null);
    });
    it('should return racing.module', () => {
        const response = service.getModule('@racingModule/racing.module');
        expect(response).not.toBe(null);
    });
    it('should return retail.module', () => {
        const response = service.getModule('@retail-lazy-load/retail.module');
        expect(response).not.toBe(null);
    });
    it('should return bet-history.module', () => {
        const response = service.getModule('@betHistoryModule/bet-history.module');
        expect(response).not.toBe(null);
    });
    it('should return featured.module', () => {
        const response = service.getModule('@featuredModule/featured.module');
        expect(response).not.toBe(null);
    });
    it('should return tote.module', () => {
        const response = service.getModule('@toteModule/tote.module');
        expect(response).not.toBe(null);
    });
    it('should return betslip.module', () => {
        const response = service.getModule('@betslipModule/betslip.module');
        expect(response).not.toBe(null);
    });
    it('should return quickbet.module', () => {
        const response = service.getModule('@quickbetModule/quickbet.module');
        expect(response).not.toBe(null);
    });
    it('should return edp.module', () => {
        const response = service.getModule('@edpModule/edp.module');
        expect(response).not.toBe(null);
    });
    it('should return inplay.module', () => {
        const response = service.getModule('@inplayModule/inplay.module');
        expect(response).not.toBe(null);
    });
    it('should return freebets.module', () => {
        const response = service.getModule('@freebetsModule/freebets.module');
        expect(response).not.toBe(null);
    });
    it('should return quick-deposit.module', () => {
        const response = service.getModule('@quickDepositModule/quick-deposit.module');
        expect(response).not.toBe(null);
    });
    it('should return seo-static-block.module', () => {
        const response = service.getModule('@lazy-modules/seoStaticBlock/seo-static-block.module');
        expect(response).not.toBe(null);
    });
    it('should return market-selector.module', () => {
        const response = service.getModule('@sharedModule/components/marketSelector/market-selector.module');
        expect(response).not.toBe(null);
    });
    it('should return byb-history.module', () => {
        const response = service.getModule('@bybHistoryModule/byb-history.module');
        expect(response).not.toBe(null);
    });

    it('should return right-column.module', () => {
        const response = service.getModule('@rightColumnModule/right-column.module');
        expect(response).not.toBe(null);
    });

    it('should return specials-sport-tab.module', () => {
      const response = service.getModule('@specialsModule/specials-sport-tab.module');
      expect(response).not.toBe(null);
    });

    it('should return odds-card-highligt-carousel.module', () => {
        // eslint-disable-next-line max-len
        const response = service.getModule('@sharedModule/components/oddsCard/oddsCardHightlightCarousel/odds-card-highligt-carousel.module');
        expect(response).not.toBe(null);
    });

    it('should return casino-my-bets-integration.module', () => {
        const response = service.getModule('@lazy-modules-module/casinoMyBetsIntegration/casino-my-bets-integration.module');
        expect(response).not.toBe(null);
    });

    it('should return racing-event-model.module', () => {
        const response = service.getModule('@lazy-modules-module/racingEventModel/racing-event-model.module');
        expect(response).not.toBe(null);
    });
    it('should return network-indicator.module', () => {
        const response = service.getModule('@lazy-modules/networkIndicator/network-indicator.module');
        expect(response).not.toBe(null);
    });
    it('should return sb-quickbet.module', () => {
        const response = service.getModule('@quickbetStreamBetModule/sb-quickbet.module');
        expect(response).not.toBe(null);
    });

  });

  xit('should not return module if it does not exist', () => {
    const response = service.getModule('tstModule');
    expect(response).toEqual(jasmine.any(Promise));
  });
  
});