import { FooterMenusCreateComponent } from './footer-menus-create.component';
import { FormControl, FormGroup } from '@angular/forms';
import { FooterMenu } from '@app/client/private/models';

describe('FooterMenusCreateComponent', () => {
  let component: FooterMenusCreateComponent;
  let dialogRef;
  let brandService;
  beforeEach(() => {
    dialogRef = { close: jasmine.createSpy('dialogRef.close') };
    brandService = {};

    component = new FooterMenusCreateComponent(dialogRef, brandService);
    component.footerMenu = { linkTitle: '', targetUri: '' } as FooterMenu;
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.footerMenu).toBeDefined();
    expect(component.form).toBeDefined();
  });

  describe('#getfooterMenu', () => {
    it('should return same value of entered data in form', () => {
      component.form = new FormGroup({
        linkTitle: new FormControl('ladbrokes'),
        targetUri: new FormControl('coral')
      });
      component.getFooterMenu();
      expect(component.footerMenu.linkTitle).toEqual('ladbrokes');
      expect(component.footerMenu.targetUri).toEqual('coral');
    });
    it('if the form is empty it should return undefined', () => {
      component.form = new FormGroup({});
      component.getFooterMenu();
      expect(component.footerMenu.linkTitle).toBeUndefined();
      expect(component.footerMenu.targetUri).toBeUndefined();
    });
    it('should return value and if nothing is given for targetUri it should return null', () => {
      component.form = new FormGroup({
        linkTitle: new FormControl('ladbrokes'),
        targetUri: new FormControl(null)
      });
      component.getFooterMenu();
      expect(component.footerMenu.linkTitle).toBe('ladbrokes');
      expect(component.footerMenu.targetUri).toBeNull();
    });
  });

  it('closeDialog should call close()', () => {
    spyOn(component, 'closeDialog').and.callFake(function () {
      return dialogRef.close();
    });
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
