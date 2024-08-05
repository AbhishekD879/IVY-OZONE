import { YcMarketsCreateComponent } from './yc-markets-create.component';

describe('YcMarketsCreateComponent', () => {
  let component: YcMarketsCreateComponent, dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };
    component = new YcMarketsCreateComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();
  });

  it('should define newMarket', () => {
    expect(component.newMarket).toBeDefined();
    expect(component.newMarket.brand).toEqual(brandService.brand);
  });
});
