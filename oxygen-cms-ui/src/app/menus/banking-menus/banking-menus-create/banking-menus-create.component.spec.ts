import { BankingMenusCreateComponent } from './banking-menus-create.component';

describe('BankingMenusCreateComponent', () => {
  let component: BankingMenusCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new BankingMenusCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.bankingMenu).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
