import { of, throwError } from 'rxjs';
import { PayTableComponent } from '@app/five-a-side-showdown/components/pay-table/pay-table.component';
import { PAY_TABLE_DATA } from '@app/five-a-side-showdown/components/pay-table/pay-table.component.mock';

describe('PayTableComponent', () => {
  let component: PayTableComponent;
  let dialogService;
  let contestManagerService;
  let apiClientService;
  let globalLoaderService;
  let payTableMock;
  let errorService;

  beforeEach(() => {
    payTableMock = PAY_TABLE_DATA.slice();
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(PAY_TABLE_DATA[1]);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    contestManagerService = {
      payTableData: {} as any,
      getAllPrizesByContest: jasmine.createSpy('getAllPrizesByContest').and.returnValue(of({ body: payTableMock})),
      addPrizeById: jasmine.createSpy('addPrizeById').and.returnValue(of({body: payTableMock[0]})),
      uploadPrizeSvgImage: jasmine.createSpy('uploadPrizeSvgImage').and.returnValue(of({body: payTableMock[0]})),
      getPrizeById: jasmine.createSpy('getPrizeById').and.returnValue(of({body: payTableMock[1]})),
      removePrize: jasmine.createSpy('removePrize').and.returnValue(of(void 0)),
      editPrizeById: jasmine.createSpy('editPrizeById').and.returnValue(of({body: payTableMock[2]}))
    };
    apiClientService = {
      contestManagerService: () => contestManagerService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    component = new PayTableComponent(dialogService,
      apiClientService, globalLoaderService, errorService);
    component.prizesChanged = {
      emit: jasmine.createSpy('emit')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOninit', () => {
    it('should initialize data in ngOnInit(case: succcess)', () => {
      component.ngOnInit();
      expect(component.payTable).not.toBeNull();
      expect(component.isLoading).toBe(false);
    });
    it('should initialize data in ngOnInit(case: error)', () => {
      contestManagerService.getAllPrizesByContest.and.returnValue(throwError({error: '401'}));
      component.ngOnInit();
      expect(component.payTable.length).toBe(0);
      expect(component.isLoading).toBe(false);
    });
  });

  describe('#addPrize', () => {
    it('should update paytable whenever prize is added(case: success)', () => {
      spyOn(component as any, 'removeSvgFile');
      component.payTable = [];
      component.addPrize();
      expect(component.payTable.length).toBe(1);
    });
    it('should update paytable whenever prize is added(case: failure)', () => {
      spyOn(component as any, 'removeSvgFile');
      contestManagerService.addPrizeById.and.returnValue(throwError({error: '401'}));
      component.payTable = [];
      component.addPrize();
      expect(component.payTable.length).toBe(0);
    });
  });

  describe('#editPrize', () => {
    it('should update paytable whenever prize is edited(Case: Success)', () => {
      const mockPay = PAY_TABLE_DATA.slice() as any;
      spyOn(component as any, 'removeSvgFile');
      component.payTable = mockPay;
      component.editPrize(mockPay[1]);
      expect(component.payTable[1].type).toBe('Cash');
    });
    it('should update paytable whenever prize is edited(Case: Failure)', () => {
      contestManagerService.editPrizeById.and.returnValue(throwError({error: '401'}));
      const mockPay = PAY_TABLE_DATA.slice() as any;
      spyOn(component as any, 'removeSvgFile');
      component.payTable = mockPay;
      component.editPrize(mockPay[1]);
      expect(component.payTable[1].type).toBe('Ticket');
    });
  });

  describe('#removePrize', () => {
    it('should update paytable whenever prize is removed(case: Success)', () => {
      const payMock = PAY_TABLE_DATA.slice() as any;
      component.payTable = payMock;
      const mockLength = component.payTable.length;
      component.removePrize(payMock[1]);
      expect(component.payTable.length).toBe(mockLength-1);
    });
    it('should update paytable whenever prize is removed(case: Failure)', () => {
      contestManagerService.removePrize.and.returnValue(throwError({error: '401'}));
      const payMock = PAY_TABLE_DATA.slice() as any;
      component.payTable = payMock;
      const mockLength = component.payTable.length;
      component.removePrize(payMock[1]);
      expect(component.payTable.length).toBe(mockLength);
    });
  });

  describe('#removeSvgFile', () => {
    it('should set icon/signposting null, if originalName does not exist', () => {
      const prizeData = {
        icon: {
          originalname: ''
        },
        signPosting: {
          originalname: ''
        }
      } as any;
      component['removeSvgFile'](prizeData);
      expect(prizeData.icon).toBeNull();
    });
    it('should not set icon/signposting null, if originalName exist', () => {
      const prizeData = {
        icon: {
          originalname: 'original'
        },
        signPosting: {
          originalname: 'original'
        }
      } as any;
      component['removeSvgFile'](prizeData);
      expect(prizeData.icon).not.toBeNull();
    });
    it('should not set icon/signposting null, if icon/signposting is null', () => {
      const prizeData = {
        icon: null,
        signPosting: null
      } as any;
      component['removeSvgFile'](prizeData);
      expect(prizeData.icon).toBeNull();
    });
  });
});
