import {SportCategoriesCreateComponent} from './sport-categories-create.component';

describe('SportCategoriesCreateComponent', () => {
  let component: SportCategoriesCreateComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    },
    brandService = {
      brand: 'coral'
    };
    component = new SportCategoriesCreateComponent(
      dialogRef, brandService
    );

    component.ngOnInit();
  });

  it('should define sportCategory', () => {
    expect(component.sportCategory).toBeDefined();
    expect(component.sportCategory.brand).toEqual(brandService.brand);
  });
});
