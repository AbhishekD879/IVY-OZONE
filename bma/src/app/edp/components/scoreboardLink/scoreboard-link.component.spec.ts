import { ScoreboardLinkComponent } from '@edp/components/scoreboardLink/scoreboard-link.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('ScoreboardLinkComponent', () => {
  let component: ScoreboardLinkComponent;
  let optaScoreboardOverlayService;
  let pubSubService;


  beforeEach(() => {
    optaScoreboardOverlayService = {
      showOverlay: jasmine.createSpy('showOverlay'),
      setOverlayData: jasmine.createSpy('setOverlayData'),
      initOverlay: jasmine.createSpy('initOverlay')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
    };

    component = new ScoreboardLinkComponent(
      optaScoreboardOverlayService,
      pubSubService
    );

  });

  describe('showStats', () => {
    it('should showStats', () => {
      component.event = { id: 10589591, categoryId: '16', typeId: 442, name: 'Everton v Manchester United FC'} as any;
      component.market = { name: 'Both Teams to Score'} as any;
      const optaLink = {marketOptaLink: {overlayKey: 'overlay-key', tabKey: 'tab-key'}} as any;
      component.showStats(optaLink);
      expect(optaScoreboardOverlayService.initOverlay).toHaveBeenCalled();
      expect(optaScoreboardOverlayService.setOverlayData).toHaveBeenCalledWith({
        overlayKey: 'overlay-key', matchId: '10589591', tabKey: 'tab-key'
      });

      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'in-line stats',
        eventAction: 'view statistics',
        eventLabel: 'Both Teams to Score',
        categoryID: '16',
        typeID: '442',
        eventID: '10589591'
      }]);
      expect(optaScoreboardOverlayService.showOverlay).toHaveBeenCalled();
    });
  });

});
