import { BannersCreateComponent } from './banners-create.component';

describe('BannersCreateComponent', () => {
  let component: BannersCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new BannersCreateComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.banner).toBeDefined();
  });
});
