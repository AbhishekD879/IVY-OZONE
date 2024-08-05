import { YcStaticBlocksCreateComponent } from './yc-static-blocks-create.component';

describe('YcStaticBlocksCreateComponent', () => {
  let component: YcStaticBlocksCreateComponent, dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };
    component = new YcStaticBlocksCreateComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();

  });

  it('should define yourCallStaticBlock', () => {
    expect(component.yourCallStaticBlock).toBeDefined();
  });
});
