import { RetailPageComponent } from '@app/retail/components/retailPage/retail-page.component';

describe('RetailPageComponent', () => {
  let component;

  beforeEach(() => {
    component = new RetailPageComponent();
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.showRetailMenu).toBeTruthy();
  });
});
