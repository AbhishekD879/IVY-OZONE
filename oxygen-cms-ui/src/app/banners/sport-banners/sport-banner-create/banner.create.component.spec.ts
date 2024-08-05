import { BannerCreateComponent } from './banner.create.component';

describe('BannerCreateComponent', () => {
  let component: BannerCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new BannerCreateComponent(
      {}, dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.newBanner).toBeDefined();
  });
});
