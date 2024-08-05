import { BetslipReceiptSubheaderComponent } from '@betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component';

describe('BetslipReceiptSubheaderComponent', () => {

  let component: BetslipReceiptSubheaderComponent;

  const localeService = {
    getString: jasmine.createSpy().and.returnValue('123')
  } as any;
  beforeEach(() => {
    component = new BetslipReceiptSubheaderComponent(localeService);
  });

  describe('#ngOnInit', () => {
    it('should set betTime', () => {
      component.counter = 228;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalled();
      expect(component['title']).toEqual('123');
      expect(component.betsCounterText).toEqual('123: (228)');
    });
  });
});
