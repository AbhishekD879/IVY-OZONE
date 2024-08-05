import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { Notification_DATA, Notification_DATA_PC_FALSE } from './mockData/fanzone-notification.component.mock'
import { FanzoneNotificationComponent } from './fanzone-notification.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('FanzoneNotificationComponent', () => {
  let component: FanzoneNotificationComponent;
  let device;
  let windowRef;
  let router;
  let fanzoneSharedService;
  let fanzoneStorageService;
  let pubsub;
  let element;

  beforeEach(() => {

    device = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    fanzoneSharedService = {
      deleteFanzonePreferences: jasmine.createSpy('deletePref'),
      pushCachedEvents: jasmine.createSpy('pushCachedEvents'),
      getFanzoneInfo: jasmine.createSpy('getFanzoneInfo').and.returnValue({teamName: 'Arsenal FC'}),
      resignFanzone: jasmine.createSpy('resignFanzone'),
      isSubscribedToCustomTeam: jasmine.createSpy('isSubscribedToCustomTeam')
    }
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    fanzoneStorageService = {
      remove: jasmine.createSpy('remove'),
      get: jasmine.createSpy('get')
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    }
    element = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };

    component = new FanzoneNotificationComponent(
      device,
      windowRef,
      router,
      pubsub,
      fanzoneSharedService,
      fanzoneStorageService,
      element
    );
  });

  it('Handle onToggleChange method', () => {
    component.onToggleChange(false);
    expect(component.initialState).toEqual(false);
  });

  it('to turn on fanzone toggle on click outside notification popup', ()=>{
    element.nativeElement.contains.and.returnValue(false);
    const event = { target: { tagName: 'target '} } as any;
    component.clickOutside(event);
    expect(pubsub.publish).toHaveBeenCalled();
  })
  
  it('to not turn on fanzone toggle on click outside notification popup', ()=>{
    element.nativeElement.contains.and.returnValue(true);
    const event = { target: { tagName: 'target '} } as any;
    component.clickOutside(event);
    expect(pubsub.publish).not.toHaveBeenCalled();
  })
  
  it('should open dialog', () => {

    const openSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'open');
    const params = Notification_DATA;
    AbstractDialogComponent.prototype.setParams(params);

    component.open();

    expect(openSpy).toHaveBeenCalled();
  });

  it('should call resign fanzone method', () =>{
    const closeDialogSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'closeDialog');
    component.popUp = false;
    component.confirm();
    expect(fanzoneSharedService.resignFanzone).toHaveBeenCalled();
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('should not call resign fanzone method', () =>{
    const closeDialogSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'closeDialog');
    component.notificationData = Notification_DATA_PC_FALSE;
    component.popUp = true;
    component.confirm();
    expect(fanzoneSharedService.resignFanzone).not.toHaveBeenCalled();
    expect(closeDialogSpy).not.toHaveBeenCalled();
  });

  it('should close dialog', fakeAsync(() => {
    component.notificationData = {showToggle: false}
    fanzoneStorageService.get = jasmine.createSpy('fanzone-previous-url').and.returnValue(JSON.parse(JSON.stringify('sport/football')));
    const closeDialogSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'closeDialog');
    component.close();
    tick(200);
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component.popUp).toEqual(true);
    expect(component.initialState).toEqual(true);
    expect(router.navigate).toHaveBeenCalled();
  }));

  it('should close dialog from promotions', fakeAsync(() => {
    component.notificationData = {showToggle: false}
    fanzoneStorageService.get = jasmine.createSpy('fanzone-previous-url').and.returnValue('');
    const closeDialogSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'closeDialog');
    component.close();
    tick(200);
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component.popUp).toEqual(true);
    expect(component.initialState).toEqual(true);
    expect(router.navigate).toHaveBeenCalled();
  }));
  
  it('should close dialog but not route', () =>{
    component.notificationData = {showToggle: true}
    const closeDialogSpy = spyOn(FanzoneNotificationComponent.prototype['__proto__'], 'closeDialog');
    component.close();
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(component.popUp).toEqual(true);
    expect(component.initialState).toEqual(true);
  });

  it('should get notification title for generic team', () => {
    component.notificationData = Notification_DATA;
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(true);
    expect(component.getTitleAndDescription('title')).toBe(Notification_DATA.genericTeamNotificationTitle);
  });

  it('should get notification description for generic team', () => {
    component.notificationData = Notification_DATA;
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(true);
    expect(component.getTitleAndDescription('description')).toBe(Notification_DATA.genericTeamNotificationDescription);
  });

  it('should get notification title for other valid teams', () => {
    component.notificationData = Notification_DATA;
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(false);
    expect(component.getTitleAndDescription('title')).toBe(Notification_DATA.notificationPopupTitle);
  });

  it('should get notification description for other valid teams', () => {
    component.notificationData = Notification_DATA;
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(false);
    expect(component.getTitleAndDescription('description')).toBe(Notification_DATA.notificationDescriptionDesktop);
  });
});