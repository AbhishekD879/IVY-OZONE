import { SbQuickbetReceiptComponent } from './sb-quickbet-receipt.component';
import { LadbrokesQuickbetReceiptComponent as QuickbetReceiptComponent } from '@ladbrokesMobile/quickbet/components/quickbetReceipt/quickbet-receipt.component';
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
  let germanSupportService;
  let freeRideHelperService;
  
  
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
        germanSupportService,
        freeRideHelperService,
        bonusSuppressionService
    );
  });

  describe('#SbQuickbetReceiptComponent', () => {
    it('ngOnInit is called', () => {
      QuickbetReceiptComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      spyOn(component, 'onQuickbetEvent');
      component.betReceipt = {receipt: {id: '123'}};
      component.ngOnInit();
      quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      expect(component.receiptId).toBe('123');
    });
  });

});
