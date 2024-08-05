
import { TabAddComponent } from './tab-add.component';

describe('TabAddComponent', () => {
  let component: TabAddComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {
      brand: 'CORAL'
    };
    brandService = {};

    component = new TabAddComponent(dialogRef, brandService);
    component.ngOnInit();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
