import {DateRangeComponent} from './date.range.component';

describe('DateRangeComponent', () => {
  let component;

  beforeEach(() => {
    component = new DateRangeComponent();

    component.ngOnInit();
  });

  it('should init default Dates', () => {
    expect(component.startDate).toBeDefined();
    expect(component.endDate).toBeDefined();
    expect(component.minEndDate).toBeDefined();
    expect(component.maxStartDate).toBeDefined();
  });
});
