import { CustomerVariantsSelectComponent } from './customer-variants-select.component';

describe('CustomerVariantsSelectComponent', () => {
  let component;

  beforeEach(() => {
    component = new CustomerVariantsSelectComponent();
  });

  it('should not init properties if no options', () => {
    component.ngOnInit();
    expect(component.showToCustomerVariants).not.toBeDefined();
  });

  it('should init properties if options present', () => {
    component.optionsType = 'loggedIn';

    component.ngOnInit();

    expect(component.showToCustomerVariants).toBeDefined();
    expect(component.variantsEnum).toBeDefined();
  });
});
