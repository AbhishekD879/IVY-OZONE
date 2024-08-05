import { fakeAsync } from '@angular/core/testing';
import { LottoBetReceiptComponent } from './lotto-bet-receipt.component';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { of as observableOf } from 'rxjs';

describe('LottoBetReceiptComponent', () => {
  let component: LottoBetReceiptComponent;
  let userService;
  let nativeBridge;
  let betReceiptService;
  let cmsService;

  beforeEach(fakeAsync(() => {

    userService = {
      currencySymbol: '$',
    }
    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(observableOf({
        svg: 'svg',
        svgId: 'svgId'
      }))
    };
    betReceiptService = {
      setToggleSwitchId: () => { },
    }
    createComp();
  }));

  function createComp() {
    component = new LottoBetReceiptComponent(
      userService,
      nativeBridge,
      betReceiptService,
      cmsService
    )
  }

  it('should create', () => {
    expect(component).toBeDefined();
  });


  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.setToggleSwitchId).toEqual(jasmine.any(Function));
  });

  it('should call ngOnInit()', () => {
    component.ngOnInit();
    expect(component).toBeDefined();
  });

  it('should call ngOnInit()', () => {
    cmsService.getItemSvg = jasmine.createSpy().and.returnValue(observableOf({
      svg: 'svg',
      svgId: undefined
    }));
    component.ngOnInit();
    expect(component).toBeDefined();
  });

  it('should call onExpandSummary() on expandsummary true', () => {
    component.lottobetslipData = [{} as any, { expanded: true }];
    component.onExpandSummary(1);
    expect(component.lottobetslipData[1].expanded).toBeFalsy();
  });

  it('should call onExpandSummary() on expandsummary false', () => {
    component.lottobetslipData = [{} as any, { expanded: false }];
    component.onExpandSummary(1);
    expect(component.lottobetslipData[1].expanded).toBeTruthy();
  });


  it('trackById should return joined string', () => {
    const index: number = 11;
    const betslipStake: any = { id: '22' };
    const result = component.trackById(index, betslipStake);
    expect(result).toEqual('22_11');
  });

  it('trackByDrawId should return joined string', () => {
    const index: number = 15;
    const betslipStake: any = { id: '42' };
    const result = component.trackByDrawId(index, betslipStake);
    expect(result).toEqual('42_15');
  });

  it('it should call getSelectionNumbers()', () => {
    const leg = [{ lotteryLeg: { picks: "27|40|43" }, documentId: "1" }]
    const values = component.getSelectionNumbers(leg);
    expect(values).toEqual(['27', '40', '43']);
  });
  it('it should call getSelectionNumbers()', () => {
    const leg = undefined;
    const values = component.getSelectionNumbers(leg);
    expect(values).toBeUndefined();
  });

  describe('#toggleWinAlerts', () => {
    it('should call toggleWinAlerts method and emit winAlertsToggleChanged', () => {
      component.winAlertsToggleChanged.emit = jasmine.createSpy('winAlertsToggleChanged.emit');

      component.toggleWinAlerts({} as any, true);

      expect(component.winAlertsToggleChanged.emit).toHaveBeenCalledWith({
        receipt: {} as IBetDetail,
        state: true
      });
    });
  });

});
