import { CreatePaymentComponent } from './create-payment.component';

describe('CreatePaymentComponent', () => {
  let component: CreatePaymentComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'brandMockedName'
    };

    component = new CreatePaymentComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.payment).toBeDefined();
  });
});
