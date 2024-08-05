import { SbQuickbetReceiptComponent } from '@app/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component';
import { QuickbetReceiptComponent } from '@app/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { SbQbReceiptData } from '@app/quickbet/services/quickbetService/quickbet.service';
import { Subject } from 'rxjs';

describe('SbQuickbetReceiptComponent', () => {
  let component: SbQuickbetReceiptComponent;
  let user;
  let filtersService;
  let quickbetService;
  let nativeBridge;
  let window;
  let pubSubService;
  let http;
  let storageService;
  let racingPostTipService;
  let cmsService;
  let fiveASideEntryConfirmationService;
  let fiveASideContestSelectionService;
  let freeBetsService;
  let gtmService;
  let maxPayOutErrorService;
  let locale;
  let firstBetGAService;
  let sessionStorage;
  let betReuseService;
  let bonusSuppressionService;
  
  
  beforeEach(() => {
    locale = {
        getString: jasmine.createSpy().and.returnValue(''),
      };

    quickbetService = {
      qbReceiptDataSubj: new Subject<SbQbReceiptData>(),

      quickBetOnOverlayCloseSubj: new Subject<string>(),
    };

    component = new SbQuickbetReceiptComponent(
        user,
        filtersService,
        quickbetService,
        nativeBridge,
        window,
        pubSubService,
        http,
        storageService,
        racingPostTipService,
        cmsService,
        fiveASideEntryConfirmationService,
        fiveASideContestSelectionService,
        freeBetsService,
        gtmService,
        maxPayOutErrorService,
        locale,
        firstBetGAService,
        betReuseService,
        sessionStorage,
        bonusSuppressionService
    );
  });

  describe('#SbQuickbetReceiptComponent', () => {
    it('ngOnInit is called', () => {
      spyOn(component, 'onQuickbetEvent');
      spyOn(QuickbetReceiptComponent.prototype, 'ngOnInit');
      component.betReceipt = {receipt: {id: '123'}};
      component.ngOnInit();
      quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      expect(component.receiptId).toBe('123');
    });
  });

});
