import { JackpotReceiptPageComponent } from './jackpot-receipt-page.component';

describe('JackpotReceiptPageComponent', () => {
  let component: JackpotReceiptPageComponent;
  let jackpotReceiptPageService: any;
  let sbFiltersService: any;
  let filtersService: any;
  let gtmService: any;
  let localeService: any;
  let router: any;

  beforeEach(() => {
    jackpotReceiptPageService = {
      get getReceiptData() {
        return '';
      },
      get localeService() {
        return '';
      },
      get getTotalStake() {
        return '';
      },
      get getTotalLines() {
        return '';
      },
      get getBetReceiptNumber() {
        return '';
      }
    };

    sbFiltersService = jasmine.createSpyObj('sbFiltersService', ['outcomeMinorCodeName']);
    filtersService = jasmine.createSpyObj('filtersService', ['setCurrency']);
    gtmService = jasmine.createSpyObj('gtmService', ['push']);
    localeService = jasmine.createSpyObj('localeService', ['getString']);
    router = jasmine.createSpyObj('router', ['navigate']);

    component = new JackpotReceiptPageComponent(
      jackpotReceiptPageService,
      sbFiltersService,
      filtersService,
      gtmService,
      localeService,
      router
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should set properties and call correct method', () => {
      spyOnProperty(jackpotReceiptPageService, 'getReceiptData').and.returnValue([1]);
      spyOnProperty(jackpotReceiptPageService, 'getTotalStake').and.returnValue(2);
      spyOnProperty(jackpotReceiptPageService, 'getTotalLines').and.returnValue(3);
      spyOnProperty(jackpotReceiptPageService, 'getBetReceiptNumber').and.returnValue(4);

      component.ngOnInit();

      expect(component['receiptData'] as any).toEqual([1]);
      expect(component['totalStake'] as any).toEqual(2);
      expect(component['totalLines'] as any).toEqual(3);
      expect(component['betReceiptNumber'] as any).toEqual(4);
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('should call goToPage method', () => {
      spyOn(component, 'goToPage');
      spyOnProperty(jackpotReceiptPageService, 'getReceiptData').and.returnValue([]);

      component.ngOnInit();

      expect(component['goToPage']).toHaveBeenCalled();
    });
  });

  it('goToPage should call navigate method with correct params', () => {
    component.goToPage();

    expect(router.navigate).toHaveBeenCalledWith(['sport', 'football', 'jackpot']);
  });

  it('sortOutcomes should return sorted array', () => {
    expect(component.sortOutcomes([
      {outcomeMeaningMinorCode: 2, name: 'first'},
      {outcomeMeaningMinorCode: 3, name: 'second'}
    ] as any)[0].name).toEqual('first');
  });

  it('setButtonText should call methods and return service result', () => {
    localeService.getString.and.returnValue(2);

    expect(component.setButtonText('text') as any).toEqual(2);
    expect(sbFiltersService.outcomeMinorCodeName).toHaveBeenCalledWith('text');
  });

  describe('setCurrency', () => {
    const value = 2.2222;

    it('should call setCurrency method with non fixed value', () => {
      component.setCurrency(value);

      expect(filtersService.setCurrency).toHaveBeenCalledWith(value, '£');
    });

    it('should call setCurrency method with fixed value', () => {
      component.setCurrency(value, true);
      expect(filtersService.setCurrency).toHaveBeenCalledWith('2.22', '£');
    });
  });
});
