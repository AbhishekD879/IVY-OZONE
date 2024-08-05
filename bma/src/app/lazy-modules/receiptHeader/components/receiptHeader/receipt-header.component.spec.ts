import { ReceiptHeaderComponent } from '@lazy-modules/receiptHeader/components/receiptHeader/receipt-header.component';

describe('ReceiptHeaderComponent', () => {

  let component: ReceiptHeaderComponent;

  const timeService = {
    formatByPattern: jasmine.createSpy().and.returnValue('123')
  } as any;
  
  beforeEach(() => {
    component = new ReceiptHeaderComponent(timeService);
  });

  describe('#ngOnInit', () => {
    it('should set betTime', () => {
      component.betDate = '12/31/2019';
      component.ngOnInit();

      expect(timeService.formatByPattern).toHaveBeenCalledWith(jasmine.any(Date), 'dd/MM/yyyy, HH:mm');
      expect(component.betTime).toEqual(jasmine.any(String));
    });
    it('should not set betTime', () => {
      component.betDate = undefined;
      component.ngOnInit();

      expect(component.betTime).not.toBeDefined();
    });
  });
});
