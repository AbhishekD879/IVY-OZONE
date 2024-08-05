import { DeviceService } from '@core/services/device/device.service';
import { ISystemConfig } from '@core/services/cms/models';
import { of as observableOf } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { BonusSuppressionErrorDialogComponent } from './bonus-suppression-error-dialog.component';
import { REDIRECTION_URLS } from './bonus-suppression-error-dialog.constants';

describe('BonusSuppressionErrorDialogComponent', () => {
  let component: BonusSuppressionErrorDialogComponent;
  let device;
  let windowRef;
  let cmsService;

  const sysConfig: ISystemConfig = {
    BonusSupErrorMsg: {
      errorMsg: 'Permission Denied',
      url: '/'
    }
  };

  beforeEach(() => {
    device = DeviceService;
    windowRef = {
      nativeWindow: {
        document: {} as HTMLDocument,
        open: jasmine.createSpy('window.open')
      } as any
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(sysConfig))
    };
    component = new BonusSuppressionErrorDialogComponent(device, windowRef, cmsService);
  });

  describe('#getErrorMessage' , ()=> {
    it('getErrorMessage if CMS configured', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
        sysConfigModified['BonusSupErrorMsg'] = {
          errorMsg: 'Permission Denied',
          url: '/'
        };
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
          .and.returnValue(observableOf(sysConfigModified));
  
        component.getErrorMessage();
  
        expect(component.bonusSuppresionErrorMessage).toEqual('Permission Denied');
    });
    it('getErrorMessage if CMS not configured', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
        sysConfigModified['BonusSupErrorMsg'] = undefined
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
          .and.returnValue(observableOf(sysConfigModified));
  
        component.getErrorMessage();
  
        expect(component.bonusSuppresionErrorMessage).toEqual('User Permission Denied');
    });
  })

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call redirection to ladbrokes page #goToChatPage',() => {
      environment.brand = 'ladbrokes';
      component.goToChatPage();
      expect(windowRef.nativeWindow.open).toHaveBeenCalledWith(REDIRECTION_URLS.ladbrokes);
  })

  it('should call redirection to coral page #goToChatPage',() => {
    environment.brand = 'bma';
    component.goToChatPage();
    expect(windowRef.nativeWindow.open).toHaveBeenCalledWith(REDIRECTION_URLS.coral);
  })
});
