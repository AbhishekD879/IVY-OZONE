import {AddStaticBlockComponent} from './add-static-block.component';

describe('AddStaticBlockComponent', () => {
  let component: AddStaticBlockComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };
    component = new AddStaticBlockComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();
  });

  it('should define newStaticBlock', () => {
    expect(component.newStaticBlock).toBeDefined();
    expect(component.newStaticBlock.brand).toEqual(brandService.brand);
  });
});
