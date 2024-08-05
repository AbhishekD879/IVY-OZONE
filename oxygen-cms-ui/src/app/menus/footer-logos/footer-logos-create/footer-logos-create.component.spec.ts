import { FooterLogosCreateComponent } from './footer-logos-create.component';

describe('FooterLogosCreateComponent', () => {
  let component: FooterLogosCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new FooterLogosCreateComponent(
      dialogRef,
      brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.footerLogo).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
