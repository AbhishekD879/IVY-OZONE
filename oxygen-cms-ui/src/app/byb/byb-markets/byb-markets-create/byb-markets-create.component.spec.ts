import { BybMarketsCreateComponent } from './byb-markets-create.component';

describe('BybMarketsCreateComponent', () => {
  let component: BybMarketsCreateComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {};

    component = new BybMarketsCreateComponent(dialogRef);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.form).toBeDefined();
  });
});
