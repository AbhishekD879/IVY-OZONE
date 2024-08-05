import { AddExternalLinkComponent } from './add-external-link.component';

describe('AddExternalLinkComponent', () => {
  let component: AddExternalLinkComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new AddExternalLinkComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.newExternalLink).toBeDefined();
  });
});
