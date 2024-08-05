import { ReceiptCreateComponent } from './receipt-create.component';

describe('ReceiptCreateComponent', () => {
  let component: ReceiptCreateComponent;
  let dialogRef;
  let brandService;
  let router;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};
    router = { url: '1/2/3/4' };

    component = new ReceiptCreateComponent(dialogRef, brandService, router);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.type).toBeDefined();
    expect(component.banner).toBeDefined();
  });
});
