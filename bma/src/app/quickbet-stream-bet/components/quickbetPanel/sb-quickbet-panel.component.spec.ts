import { SbQuickbetPanelComponent } from '@app/quickbet-stream-bet/components/quickbetPanel/sb-quickbet-panel.component';
import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';
import { SbQbReceiptData } from '@app/quickbet/services/quickbetService/quickbet.service';
import { Subject } from 'rxjs';
describe('SbQuickbetPanelComponent', () => {
  let component: SbQuickbetPanelComponent;
  let rendererService;
  let pubsub;
  let userService;
  let locale;
  let quickbetDepositService;
  let device;
  let infoDialog;
  let quickbetService;
  let quickbetDataProviderService;
  let quickbetNotificationService;
  let cmsService;
  let windowRefService;
  let domToolsService;
  let router;
  let quickbetUpdateService;
  let changeDetectorRef;
  let arcUserService;
  let nativeBridgeService;
  let serviceClosureService;
  let yourCallMarketService;
  let dialogService;
  let sessionStorageService;
  let user;
  let filtersService;
  let gtmService;
  let quickDepositIframeService;
  let BetReceiptService;

  beforeEach(() => {
    locale = {
        getString: jasmine.createSpy().and.returnValue(''),
      };

    quickbetService = {
      qbReceiptDataSubj: new Subject<SbQbReceiptData>(),
      quickBetOnOverlayCloseSubj: new Subject<string>()
    };

    filtersService = {
      filterAddScore: {},
      filterPlayerName: {}
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new SbQuickbetPanelComponent(
    rendererService,
    pubsub,
    userService,
    locale,
    quickbetDepositService,
    device,
    infoDialog,
    quickbetService,
    quickbetDataProviderService,
    quickbetNotificationService,
    cmsService,
    windowRefService,
    domToolsService,
    router,
    quickbetUpdateService,
    changeDetectorRef,
    arcUserService,
    nativeBridgeService,
    serviceClosureService,
    yourCallMarketService,
    dialogService,
    sessionStorageService,
    user,
    filtersService, 
    gtmService,
    quickDepositIframeService,
    BetReceiptService
    );
  });

  describe('#SbQuickbetPanelComponent', () => {
    it('ngOnInit is called, with stake value', () => {
      spyOn(QuickbetPanelComponent.prototype, 'ngOnInit');
      component.market = {outcomes: [{id: '123'} as any]} as any;
      component.selection = {outcomeId: '123'} as any;
      component.ngOnInit();
      quickbetService.qbReceiptDataSubj.next({stake: '123', returns: '2500', freeBetData: {}});
      expect(component.outcome).toEqual({id: '123'} as any)
    });

    it('ngOnInit is called, with returns value', () => {
      spyOn(QuickbetPanelComponent.prototype, 'ngOnInit');
      component.market = {outcomes: [{id: '123'} as any]} as any;
      component.selection = {outcomeId: '123'} as any;
      component.ngOnInit();
      quickbetService.qbReceiptDataSubj.next({returns: '2500', freeBetData: {}});
      expect(component.outcome).toEqual({id: '123'} as any)
    });

    it('ngOnInit is called, with odds value', () => {
      spyOn(QuickbetPanelComponent.prototype, 'ngOnInit');
      component.market = {outcomes: [{id: '123'} as any]} as any;
      component.selection = {outcomeId: '123'} as any;
      component.ngOnInit();
      quickbetService.qbReceiptDataSubj.next({odds: '2.5', freeBetData: {}});
      expect(component.outcome).toEqual({id: '123'} as any)
    });

    it('closePanel is called', () => {
      spyOn(QuickbetPanelComponent.prototype, 'closePanel');
      component.closePanel();
      expect(QuickbetPanelComponent.prototype.closePanel).toHaveBeenCalled();
    });
  
    it('filterAddScore is called', () => {
      const filterAddScoreSpy = spyOn(filtersService, 'filterAddScore');
      component.filterAddScore('Match Betting', 'US');
      expect(filterAddScoreSpy).toHaveBeenCalled();
    });

    it('filterPlayerName is called', () => {
      const filterPlayerNameSpy = spyOn(filtersService, 'filterPlayerName');
      component.filterPlayerName('Novak');
      expect(filterPlayerNameSpy).toHaveBeenCalled();
    });

  });

});

