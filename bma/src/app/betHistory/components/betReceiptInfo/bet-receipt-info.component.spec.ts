import { BetReceiptInfoComponent } from './bet-receipt-info.component';

describe('BetReceiptInfoComponent', () => {
  let timeService;
  let component: BetReceiptInfoComponent;

  beforeEach(() => {
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern'),
      getLocalDateFromString: jasmine.createSpy('getLocalDateFromString')
    };

    component = new BetReceiptInfoComponent(
      timeService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(timeService.formatByPattern).toHaveBeenCalledTimes(1);
    expect(timeService.getLocalDateFromString).toHaveBeenCalledTimes(1);
  });
});
