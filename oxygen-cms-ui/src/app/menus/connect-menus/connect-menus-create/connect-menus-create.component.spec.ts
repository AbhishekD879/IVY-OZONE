import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ConnectMenusCreateComponent } from './connect-menus-create.component';

describe('ConnectMenusCreateComponent', () => {
  let component: ConnectMenusCreateComponent;
  let dialogRef;
  let brandService;
  let apiClientService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};
    apiClientService = {
      connectMenu: jasmine.createSpy('connectMenu').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: {}
        }))
      })
    };

    component = new ConnectMenusCreateComponent(dialogRef, brandService, apiClientService);
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();

    tick();

    expect(apiClientService.connectMenu).toHaveBeenCalled();
    expect(component.connectMenus).toBeDefined();
    expect(component.connectMenu).toBeDefined();
    expect(component.form).toBeDefined();
  }));
});
