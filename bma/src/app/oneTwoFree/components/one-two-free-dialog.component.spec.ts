import { OneTwoFreeDialogComponent } from './one-two-free-dialog.component';
import { of } from 'rxjs';

describe('OneTwoFreeDialogComponent', () => {
  let component: OneTwoFreeDialogComponent;
  let deviceService;
  let pubSubService;
  let cmsService;
  let serviceClosureService;
  let elementRef;
  let changeDetectorRef;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        id: 'elementId'
      }
    };

    changeDetectorRef = {};

    deviceService = {
      isMobile: true
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: 'TOGGLE_MOBILE_HEADER_FOOTER'
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({ F2PERRORS: 'F2PError' }))
    };

    component = new OneTwoFreeDialogComponent(
      elementRef as any,
      changeDetectorRef as any,
      deviceService as any,
      pubSubService as any,
      cmsService,
      serviceClosureService
    );

    component.modal = <any>{
      open: jasmine.createSpy()
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  

  it('should hide footer & header', () => {
    deviceService.isMobile = true;
    component.ngOnInit();
    expect(pubSubService.publish).toHaveBeenCalledWith(
      pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, false
    );
  });

  it('shouldn`t hide footer & header', () => {
    deviceService.isMobile = false;
    component.ngOnInit();
    expect(pubSubService.publish).toHaveBeenCalledWith(
      pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, true
    );
  });

  it('shouldn`t open modal dialog', () => {
    deviceService.isMobile = false;
    component.ngOnInit();
    expect(component.modal.open).not.toHaveBeenCalled();
  });

  it('shouldn`t open modal dialog', () => {
    deviceService.isMobile = false;
    component.ngOnInit();
    expect(component.closeOnOutsideClick).toBe(true);
  });

  it('should show footer & header', () => {
    component.ngOnDestroy();
    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should show footer & header', () => {
    cmsService.getSystemConfig.and.returnValue(of({ undefined }))
    const component1 = new OneTwoFreeDialogComponent(
      elementRef as any,
      changeDetectorRef as any,
      deviceService as any,
      pubSubService as any,
      cmsService,
      serviceClosureService
    );
    expect(component1).toBeTruthy();
  });

});
