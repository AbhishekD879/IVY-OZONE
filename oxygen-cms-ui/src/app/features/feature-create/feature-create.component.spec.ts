import { FeatureCreateComponent } from './feature-create.component';

describe('FeatureCreateComponent', () => {
  let component: FeatureCreateComponent;
  let brandService;
  let dialogRef;

  beforeEach(() => {
    brandService = {};
    dialogRef = {};

    component = new FeatureCreateComponent(
      brandService, dialogRef
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.feature).toBeDefined();
  });
});
