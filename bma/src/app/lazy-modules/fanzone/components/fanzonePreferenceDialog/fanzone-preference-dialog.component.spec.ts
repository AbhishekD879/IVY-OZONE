import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { PreferenceCentre } from '@ladbrokesMobile/fanzone/components/fanzonePreferenceCentre/mockData/fanzone-preference-center.component.mock';
import { FanzonePreferenceDialogComponent } from './fanzone-preference-dialog.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('FanzonePreferenceDialogComponent', () => {
  let component: FanzonePreferenceDialogComponent, device, fanzoneSharedService, router, storageService, windowRef, pubsub, routingState;
  beforeEach(() => {
    device = { isAndroid: true };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get').and.returnValue({teamId:'123',teamName:'arsenal'}),
      remove: jasmine.createSpy('remove')
    };
    fanzoneSharedService = {
      saveTeamOnPlatformOne: jasmine.createSpy('saveTeamOnPlatformOne'),
      deleteFanzonePreferences: jasmine.createSpy('deleteFanzonePreferences'),
      pushCachedEvents: jasmine.createSpy('pushCachedEvents'),
      resignFanzone: jasmine.createSpy('resignFanzone')
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: {
        NativeBridge : { showNotificationSettings: jasmine.createSpy() },
        location: {
          pathname: 'testPath'
        }
      }
    } as any;
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('/')
    }
    component = new FanzonePreferenceDialogComponent(
      device, 
      fanzoneSharedService,
      router, 
      storageService, 
      windowRef,
      pubsub,
      routingState
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should open dialog with params', () => {
    const openSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'open');
    const params = PreferenceCentre[0];
    AbstractDialogComponent.prototype.setParams(params);
    component.open();
    expect(component.params).toEqual(params);
    expect(openSpy).toHaveBeenCalled();
  })

  

  it('close dialog on exit click', () => {
    const closeDialogSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'closeDialog');
    const params = PreferenceCentre[0];
    AbstractDialogComponent.prototype.setParams(params);
    component.exitDialog();
    expect(pubsub.publish).toHaveBeenCalled();
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('no thanks', '', 'show your colors' );
    expect(closeDialogSpy).toHaveBeenCalled();
  })

  it('navigate to football page if previous url is show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/show-your-colours')
    
    const closeDialogSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'closeDialog');
    const params = PreferenceCentre[0];
    AbstractDialogComponent.prototype.setParams(params);
    component.exitDialog();
    expect(router.navigate).toHaveBeenCalledWith(['/sport/football']);
    expect(closeDialogSpy).toHaveBeenCalled();
  })

  it('should call showNotificationSettings', () => {
    const closeDialogSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'closeDialog');
    component.savePreferences();

    expect(closeDialogSpy).toHaveBeenCalled();
    expect(windowRef.nativeWindow.NativeBridge.showNotificationSettings).toHaveBeenCalled();
  })

  it('should not call showNotificationSettings, navigate to fanzone page ', ()=>{
    const closeDialogSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'closeDialog');
    windowRef.nativeWindow.NativeBridge.pushNotificationsEnabled = true;
    component.savePreferences();

    expect(windowRef.nativeWindow.NativeBridge.showNotificationSettings).toHaveBeenCalled();
  })

  it('should route to fanzone', () => {
    const closeDialogSpy = spyOn(FanzonePreferenceDialogComponent.prototype['__proto__'], 'closeDialog');
    component.params = {routeToFz: true, teamName:'arsenal'} as any;
    windowRef.nativeWindow.NativeBridge.pushNotificationsEnabled = true;

    component.savePreferences();
    expect(windowRef.nativeWindow.NativeBridge.showNotificationSettings).toHaveBeenCalled();
  })
});
