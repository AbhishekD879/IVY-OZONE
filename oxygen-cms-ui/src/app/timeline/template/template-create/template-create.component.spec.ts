import { TemplateCreateComponent } from './template-create.component';

describe('TemplateCreateComponent', () => {
  let component: TemplateCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};
    component = new TemplateCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.template).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
