import {DateAndTimeComponent} from './date.time.component';

describe('DateAndTimeComponent', () => {
  let component;

  beforeEach(() => {
    component = new DateAndTimeComponent();

    component.ngOnInit();
  });

  it('should init date', () => {
    expect(component.chosenDate).toBeDefined();
  });
});
