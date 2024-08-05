import { of as observableOf } from 'rxjs';
import { PromoLabelsComponent } from './promo-labels.component';

describe('PromoLabelsComponent', () => {
  let component, cmsService;

  beforeEach(() => {
    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(observableOf(true))
    };

    createComponent();
  });

  function createComponent() {
    component = new PromoLabelsComponent(cmsService);
    component.ngOnInit();
  }

  describe('promoLabels', () => {
    it('should create', () => {
      expect(component).toBeTruthy();
    });

    it('should set isCashoutAvailable', () => {
      component.cashoutValue = '50';
      expect(component.isCashoutAvailable).toBeTruthy();
    });

    it('should generate Promo Labels array', () => {
      component.event = {
        id: '8208340',
        categoryName: 'Horse Racing',
        className: 'Horse Racing - Live',
        drilldownTagNames: 'EVFLAG_EPR',
        markets: [
          {
            eachWayFactorDen: 5,
            eachWayFactorNum: 1,
            id: '137767829',
            isEachWayAvailable: true,
            isGpAvailable: false,
            isLpAvailable: false,
            isSpAvailable: true,
            marketStatusCode: 'A',
            name: 'Win or Each Way',
            drilldownTagNames: 'MKTFLAG_EPR'
          }
        ]
      } as any;
      component.marketId = '137767829';
      component.ngOnInit();
      expect(component.promoLabels).toEqual([{
        name: 'extraPlace',
        eventFlag: 'EVFLAG_EPR',
        marketFlag: 'MKTFLAG_EPR',
        id: '#extra-place-icon'
      }]);
    });

    it('should generate Promo Labels empty array', () => {
      component.event = { id: '8208340', markets: [] } as any;
      component.ngOnInit();
      expect(component.promoLabels).toEqual([]);
    });

    it('should add acca insurance label', () => {
      component.accaInsurance = true;
      component.ngOnInit();
      expect(component.promoLabels.length).toEqual(1);
      expect(component.promoLabels[0]).toEqual(jasmine.objectContaining({
        name: 'accaInsurance',
        id: '#acca-insurance'
      }));
    });

    it('should not show cashout label for quickbet', () => {
      component.mode = 'quickbetslip';
      component.ngOnInit();
      expect(component.isQuickbet).toBeTruthy();
    });

    it('should show cashout label', () => {
      component.mode = 'betslip';
      component.ngOnInit();
      expect(component.isQuickbet).toBeFalsy();
    });

    it('should set cashout label to true', () => {
      component.mode = undefined;
      component.ngOnInit();
      expect(component.isQuickbet).toBeFalsy();
    });

    it('should trackByIndex', () => {
      expect(component.trackByIndex(1)).toEqual(1);
    });
  });

  it('should not generate Promo Labels if !isPromoSignpostingEnabled', () => {
    cmsService.getToggleStatus = jasmine.createSpy('getToggleStatus').and.returnValue(observableOf(false));
    createComponent();

    component.accaInsurance = true;
    component.ngOnInit();
    expect(component.isPromoSignpostingEnabled).toEqual(false);
    expect(component.promoLabels.length).toEqual(0);
  });
});
