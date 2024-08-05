import { BetItemComponent } from './bet-item.component';

describe('BetItemComponent', () => {
  let component: BetItemComponent;

  beforeEach(() => {
    component = new BetItemComponent();
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.expanded).toBeFalsy();
  });
});
