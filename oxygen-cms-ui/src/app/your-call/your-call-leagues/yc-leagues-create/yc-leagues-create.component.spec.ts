import { YcLeaguesCreateComponent } from './yc-leagues-create.component';

describe('YcLeaguesCreateComponent', () => {
  let component: YcLeaguesCreateComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };
    component = new YcLeaguesCreateComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();
  });

  it('should define newLeague', () => {
    expect(component.newLeague).toBeDefined();
    expect(component.newLeague.brand).toEqual(brandService.brand);
  });
});
