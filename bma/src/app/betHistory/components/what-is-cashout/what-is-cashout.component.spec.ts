import { WhatIsCashoutComponent } from './what-is-cashout.component';

describe('WhatIsCashoutComponent', () => {
  let component: WhatIsCashoutComponent;

  let device;
  let infoDialog;
  let dialogService;
  let componentFactoryResolver;

  beforeEach(() => {
    device = {
      isOnline: jasmine.createSpy().and.returnValue(true)
    };
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy()
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);

    component = new WhatIsCashoutComponent(
      device,
      infoDialog,
      dialogService,
      componentFactoryResolver
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('openWhatIsCashOut: no internet', () => {
    component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
    component.openWhatIsCashOut();
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(1);
    expect(dialogService.openDialog).not.toHaveBeenCalled();
  });

  it('should create', () => {
    component.openWhatIsCashOut();
    expect(infoDialog.openConnectionLostPopup).not.toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalled();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalled();
  });
});
