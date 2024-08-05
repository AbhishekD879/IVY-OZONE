import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { SHOW_YOUR_COLORS } from '@app/fanzone/constants/fanzoneconstants';
import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { FANZONE_SYT_POPUP_NO_SUPPORT, NO_SUPPORT_TO_TEAM_POST_LOGIN, NO_SUPPORT_TO_TEAM_PRE_LOGIN, SUPPORT_TO_TEAM_POST_LOGIN, SUPPORT_TO_TEAM_PRE_LOGIN, THANKYOU_POPUP_DATA } from '@app/fanzone/mockdata/fanzone-select-your-team.component.mock';
import { FanzoneSelectYourTeamDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneSelectYourTeamDialog/fanzone-select-your-team-dialog.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';
import { Subject } from 'rxjs/internal/Subject';

describe('FanzoneSelectYourTeamDialogComponent', () => {
  let component: FanzoneSelectYourTeamDialogComponent, 
      dialogService,
      deviceService,
      gtmService,
      pubsubReg,
      pubSubService,
      router,
      fanzoneStorageService,
      timeService,
      userService,
      changeDetectorRef,
      vanillaApiService,
      fanzoneSharedService,
      windowRef,
      fanzoneHelperService;
  const noSupportToTeamPreLogin = NO_SUPPORT_TO_TEAM_PRE_LOGIN;
  const noSupportToTeamPostLogin = NO_SUPPORT_TO_TEAM_POST_LOGIN;
  const selectedTeamDataPreLogin = SUPPORT_TO_TEAM_PRE_LOGIN;
  const selectedTeamDataPostLogin = SUPPORT_TO_TEAM_POST_LOGIN;
  const thankYouPopupData = THANKYOU_POPUP_DATA;
  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    deviceService = { isMobile: true };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    fanzoneSharedService = {
      appendToStorage: jasmine.createSpy('appendToStorage'),
      addDaysToCurrentDate: jasmine.createSpy('addDaysToCurrentDate'),
      saveTeamOnPlatformOne: jasmine.createSpy('saveTeamOnPlatformOne').and.returnValue({}),
      getFanzoneRouteName : jasmine.createSpy('getFanzoneRouteName ').and.returnValue('club')
    }
    pubsubReg = {};
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish').and.callFake((channel, args) => {
        pubsubReg[channel] && pubsubReg[channel](args);
      })
    }
    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      url: '/show-your-colours'
    };
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get')
    };
    timeService = {
      getHydraDaysDifference: jasmine.createSpy('getHydraDaysDifference').and.returnValue(observableOf({
          'timestamp': 1642393233124,
          'x-forward-for': '103.115.128.202'
      }))
    };
    userService = {
      username: 'ukmigct_gm',
      status: true
    };
    windowRef = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearInterval: jasmine.createSpy('clearInterval'),
      }
    };
    fanzoneHelperService = {
      fanzoneTeamUpdate: new Subject<any>(),
      selectedFanzoneUpdate: {
        subscribe: jasmine.createSpy('')
      },
      checkIfTeamIsRelegated: jasmine.createSpy('checkIfTeamIsRelegated').and.returnValue(observableOf(false))
    }
    component = new FanzoneSelectYourTeamDialogComponent(
      deviceService,
      gtmService,
      fanzoneSharedService,
      pubSubService,
      router,
      fanzoneStorageService,
      timeService,
      userService,
      windowRef,
      changeDetectorRef,
      fanzoneHelperService
    );
    component.dialog = {
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('open', () => {
    it('should open respective popup(i.e., i dont support any team/ team when fzDataAvailable is true', () => {
      component.changeOfTeamValidation = jasmine.createSpy('changeOfTeamValidation');
      const params = { teamId:'FZ001', teamName: 'everton' };
      userService.status = true;
      fanzoneHelperService.fzDataAvailable = true;
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(component.changeOfTeamValidation).toHaveBeenCalled();
    });
    
    it('should open respective popup(i.e., i dont support any team/ team when fzDataAvailable is false but fz storage exists', () => {
      component.changeOfTeamValidation = jasmine.createSpy('changeOfTeamValidation');
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{teamId:'FZ001'},"subscriptionDate": "2022-04-28T10:44:02Z"})));
      const params = { teamId:'FZ001', teamName: 'everton' };
      userService.status = true;
      fanzoneHelperService.fzDataAvailable = false;
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(component.changeOfTeamValidation).toHaveBeenCalled();
    });

    it('should open respective popup(i.e., i dont support any team/ team', () => {
      const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{teamId:'FZ001'},"subscriptionDate": "2022-04-28T10:44:02Z"})));
      userService.status = false;
      const params = { teteamId:'FZ001', teamName: 'everton' };
      fanzoneHelperService.checkIfTeamIsRelegated.and.returnValue(observableOf(false));
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open respective popup(i.e., when fanzone team is relegated', () => {
      const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{teamId:'FZ001'},"subscriptionDate": "2022-04-28T10:44:02Z"})));
      userService.status = true;
      fanzoneHelperService.fzDataAvailable = false;
      const params = { teteamId:'FZ001', teamName: 'everton' };
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneHelperService.checkIfTeamIsRelegated.and.returnValue(observableOf(true));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open popup if user is unsubscribed from custom team and again subscribed to custom team', () => {
      const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({isResignedUser:true, subscriptionDate:'2023-07-26T10:26:54Z', isFanzoneExists:false, isCustomResignedUser: true})));
      userService.status = true;
      fanzoneHelperService.fzDataAvailable = false;
      const params = { teteamId:'FZ001', teamName: 'everton' };
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneHelperService.checkIfTeamIsRelegated.and.returnValue(observableOf(false));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });
  });

  it('should close the dialog when user selects Select Different Team ', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.ctaPrimaryBtnClick('SELECT DIFFERENT TEAM');
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('ga tracking object should be pushed to data layer', () => {
    component.pushCachedEvents = jasmine.createSpy();
    component.pushCachedEvents('login', 'Arsenal');
    expect(component.pushCachedEvents).toHaveBeenCalled();
  });

  it('should close the dialog when user selects Exit ', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.ctaPrimaryBtnClick('EXIT');
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('should trigger keyup event when cusotm team value exists', () => {
    const event = { target: { value: 'Everton' } };
    component.setCustomTeamName(event as any);
    expect(component.customTeamName).toEqual('Everton');
    expect(component.customTeamNameError).toBe(false);
  });

  it('should produce error on trigger keyup event when user submits', () => {
    const event = { target: { value: '' } };
    component.setCustomTeamName(event as any);
    expect(component.customTeamName).toEqual('');
    expect(component.customTeamNameError).toBe(true);
  });

  it('should show thank you popup on selection of i donot support any team tile', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.ctaSecondaryBtnClick(noSupportToTeamPostLogin, 'EXIT');
    component['thankYouPopup'] = true;
    expect(component.customTeamNameError).toBeFalse();
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('should route to football home page on exit', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.customTeamNameError = false;
    component.thankYouPopup = true;
    component.fanzonePopupData = thankYouPopupData;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{teamId:'FZ001', teamName:'Generic'},"subscriptionDate": "2022-04-28T10:44:02Z"})));
    fanzoneSharedService.getFanzoneRouteName = jasmine.createSpy('fanzoneSharedService.getFanzoneRouteNam').and.returnValue('now-next');
    component.interval = 10;
    component.ctaSecondaryBtnClick(thankYouPopupData, 'EXIT');
    expect(windowRef.nativeWindow.setInterval).toHaveBeenCalled();
    expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalled();
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('should route to football home page on exit when route is unavailable', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.customTeamNameError = false;
    component.thankYouPopup = true;
    component.fanzonePopupData = thankYouPopupData;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{teamId:'FZ001', teamName:'Generic'},"subscriptionDate": "2022-04-28T10:44:02Z"})));
    fanzoneSharedService.getFanzoneRouteName = jasmine.createSpy('fanzoneSharedService.getFanzoneRouteNam').and.returnValue(undefined);
    component.interval = 1;
    component.ctaSecondaryBtnClick(thankYouPopupData, 'EXIT');
    expect(windowRef.nativeWindow.setInterval).toHaveBeenCalled();
    expect(windowRef.nativeWindow.clearInterval).not.toHaveBeenCalled();
    expect(router.navigateByUrl).not.toHaveBeenCalled();
    expect(closeDialogSpy).not.toHaveBeenCalled();
  });

  it('should not route to football home page on exit if team is selected', () => {
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.customTeamNameError = false;
    component.thankYouPopup = true;
    component.fanzonePopupData = {};
    component.ctaSecondaryBtnClick({}, 'EXIT');
    expect(router.navigate).not.toHaveBeenCalled();
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('should open a confirm popup pre login on team selection', () => {
    component.customTeamName = '';
    const params = { selectedTeamDataPreLogin };
    AbstractDialogComponent.prototype.setParams(params);
    component['fanzonePopupData'] = selectedTeamDataPreLogin;
    component.ctaSecondaryBtnClick(selectedTeamDataPreLogin, SHOW_YOUR_COLORS.CTA_BUTTONS.LOGIN);
    expect(fanzoneSharedService.appendToStorage).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'Fanzone' });
  });

  it('should open a confirm popup pre login on no team', () => {
    component.customTeamName = 'arsenal';
    const params = { noSupportToTeamPreLogin };
    AbstractDialogComponent.prototype.setParams(params);
    component['fanzonePopupData'] = noSupportToTeamPreLogin;
    component.ctaSecondaryBtnClick(noSupportToTeamPreLogin, SHOW_YOUR_COLORS.CTA_BUTTONS.LOGIN);
    expect(fanzoneSharedService.appendToStorage).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'Fanzone' });
  });

  it('should open a confirm popup post login', () => {
    component.customTeamName = '';
    component.ctaSecondaryBtnClick(noSupportToTeamPreLogin, SHOW_YOUR_COLORS.CTA_BUTTONS.LOGIN);
    component.noSupportToTeam(noSupportToTeamPreLogin);
    expect(component.customTeamNameError).toBeTrue();
  });

  it("#userSelectionDaysExceeded days exceeded", ()=> {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    timeService.getHydraDaysDifference.and.returnValue(observableOf(35));
    const res = component.userSelectionDaysExceeded();
    res.subscribe(data => {
      expect(data).toBe(true);
    })
    
  });

  it("#userSelectionDaysExceeded days not exceeded", ()=> {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    timeService.getHydraDaysDifference.and.returnValue(observableOf(5));
    const res = component.userSelectionDaysExceeded();
    res.subscribe(data => {
      expect(data).toBe(false);
    })
  });

  it('#noSupportToTeam', ()=> {
    component.customTeamName = ''
    component.checkIfTeamNameEntered = jasmine.createSpy('checkIfTeamNameEntered').and.returnValue(false);
    component.savePreferences = jasmine.createSpy('');
    component.noSupportToTeam(noSupportToTeamPostLogin);
    expect(component.thankYouPopup).toBe(true);
    expect(component.fanzonePopupData).toBe(component.thankYouPopupData);
    expect(component.savePreferences).toHaveBeenCalled();
  });

  it('#noSupportToTeam when no team entered', ()=> {
    component.customTeamName = ''
    component.checkIfTeamNameEntered = jasmine.createSpy('checkIfTeamNameEntered').and.returnValue(true);
    component.savePreferences = jasmine.createSpy('');
    component.noSupportToTeam(noSupportToTeamPostLogin);
    expect(component.customTeamNameError).toBe(true);
  });

  it('#ctaSecondaryBtnClick exit', () => {
    component.thankYouPopup = false;
    const closeDialogSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'closeDialog');
    component.ctaSecondaryBtnClick({},'EXIT');
    expect(closeDialogSpy).toHaveBeenCalled();
  });

  it('#onTeamSelectionConfirmation confirm', () => {
    component.savePreferences = jasmine.createSpy('');
    component.ctaSecondaryBtnClick(selectedTeamDataPostLogin,'CONFIRM');
    expect(component.savePreferences).toHaveBeenCalled();
  });

  it('#onNoTeamSelectionConfirmation confirm', () => {
    component.noSupportToTeam = jasmine.createSpy('');
    component.ctaSecondaryBtnClick(noSupportToTeamPostLogin,'CONFIRM');
    expect(component.noSupportToTeam).toHaveBeenCalled();
  });

  it('#checkIfTeamNameEntered when custom team not entered', () => {
    component.customTeamName  = '';
    const res = component.checkIfTeamNameEntered('FZ001');
    expect(res).toBe(true)
  });

  it('#checkIfTeamNameEntered when team entered', () => {
    component.customTeamName  = '';
    const res = component.checkIfTeamNameEntered('1c8m2ko0wxq1asfkuykurdr0y');
    expect(res).toBe(false)
  });

  it('#checkIfTeamNameEntered when custom team entered', () => {
    component.customTeamName  = 'arsenal';
    const res = component.checkIfTeamNameEntered('FZ001');
    expect(res).toBe(false);
  });

  it('#savePreferences', () => {
    component.savePreferences(selectedTeamDataPostLogin);
    expect(fanzoneSharedService.saveTeamOnPlatformOne).toHaveBeenCalled();
  });

  it('getUserData to return proper data', fakeAsync(() => {
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue(JSON.parse(JSON.stringify(FANZONE_SYT_POPUP_NO_SUPPORT)));
    component.storageKey = 'FanzoneSYTPopup';
    const userData = component.getUserData();
    tick();
    expect(userData).toEqual(JSON.parse(JSON.stringify(FANZONE_SYT_POPUP_NO_SUPPORT)));
  }));

  it('getUserData to return empty response', fakeAsync(() => {
    const userData = component.getUserData();
    tick();
    expect(userData).toEqual({});
  }));

  it('should display changeOfTeamValidation error message when a team is already selected and time has not elapsed', () => {
    const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    const params = selectedTeamDataPostLogin;
    AbstractDialogComponent.prototype.setParams(params);
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.changeOfTeamValidation = jasmine.createSpy('');
    component.userSelectionDaysExceeded = jasmine.createSpy('userSelectionDaysExceeded').and.returnValue(false);
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"1c8m2ko0wxq1asfkuykurdr0y","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(observableOf(16));
    component.open();
    expect(openSpy).not.toHaveBeenCalled();
    expect(component.changeOfTeamValidation).toHaveBeenCalled();
  });
  
  it('should not display changeOfTeamValidation error message when user is not logged in', () => {
    const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    const params = selectedTeamDataPostLogin;
    AbstractDialogComponent.prototype.setParams(params);
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.changeOfTeamValidation = jasmine.createSpy('');
    userService.status = false
    component.userSelectionDaysExceeded = jasmine.createSpy('userSelectionDaysExceeded').and.returnValue(false);
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"1c8m2ko0wxq1asfkuykurdr0y","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(observableOf(16));
    component.open();
    expect(openSpy).toHaveBeenCalled();
    expect(component.changeOfTeamValidation).not.toHaveBeenCalled();
  });

  
  it('should not display changeOfTeamValidation error message when a team is already selected and time has  elapsed 1 ', () => {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.changeOfTeamValidation = jasmine.createSpy('');
    component.userSelectionDaysExceeded = jasmine.createSpy('userSelectionDaysExceeded').and.returnValue(true);
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"1c8m2ko0wxq1asfkuykurdr0y","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(31);
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).not.toBe(true);
    expect(component.fanzonePopupData).not.toBe(component.daysNotCompletedPopupData);
  });

  it('should not display changeOfTeamValidation error message when a team is already selected and time has  elapsed 2', () => {
    component.fanzonePopupData = noSupportToTeamPostLogin;
    component.changeOfTeamValidation = jasmine.createSpy('');
    component.userSelectionDaysExceeded = jasmine.createSpy('userSelectionDaysExceeded').and.returnValue(true);
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"FZ001","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(32);
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).not.toBe(true);
    expect(component.fanzonePopupData).not.toBe(component.daysNotCompletedPopupData);
  });

  it('#onResign/new user', ()=>{
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    component.changeOfTeamValidation = jasmine.createSpy('changeOfTeamValidation');
    fanzoneHelperService.selectedFanzoneUpdate.subscribe = jasmine.createSpy('selectedFanzoneUpdate').and.callFake(cb => cb && cb(true));
    component.open();  
    expect(component.changeOfTeamValidation).toHaveBeenCalled();
  });

  it('#onResign/new user', ()=>{
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    component.changeOfTeamValidation = jasmine.createSpy('changeOfTeamValidation');
    fanzoneHelperService.fanzoneTeamUpdate.subscribe = jasmine.createSpy('fanzoneTeamUpdate').and.callFake(cb => cb && cb(true));
    component.open();  
    expect(component.changeOfTeamValidation).toHaveBeenCalled();
  });

  it('changeOfTeamValidation', ()=> {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    userService.status = false;
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage').and.returnValue(observableOf('timePer'));
    component.userSelectionDaysExceeded = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf(false));
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).toBe(false);
  });

  it('changeOfTeamValidation', ()=> {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    userService.status = false;
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).toBe(false);
    expect(openSpy).toHaveBeenCalled();
  });

  it('#getTimePeriodChangeMessage', ()=>{
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({"subscriptionDate": "2022-04-28T10:44:02Z"})));
    component.fanzonePopupData = {daysToChangeTeam: 35} as any;
    timeService.getHydraDaysDifference.and.returnValue(observableOf(32));
    const res = component.getTimePeriodChangeMessage('You signed up​  less than 30 days ago you will need to​ wait until the ${days} days expire to change your team.​', '${days}');
    res.subscribe(rs => {
      expect(rs).toBe("You signed up​  less than 30 days ago you will need to​ wait until the <span class='font-weight-bold'>3</span> days expire to change your team.​");
    })
    
  });

  it('#fzValidation', ()=> {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({"subscriptionDate": "2022-04-28T10:44:02Z"})));
    const res = component.fzValidation();
    expect(res).toBe(true);
  });

  it('#fzValidation', ()=> {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam:{},"subscriptionDate": "2022-04-28T10:44:02Z"})));
    const res = component.fzValidation();
    expect(res).toBe(false);
  });

  it('#fzValidation', ()=> {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({})));
    const res = component.fzValidation();
    expect(res).toBe(false);
  });
  it('#changeOfTeamValidation selected a team 3', () => {
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage');
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"FZ001","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    component.fanzonePopupData = noSupportToTeamPostLogin;
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).not.toBe(true);
    expect(component.fanzonePopupData).not.toBe(component.daysNotCompletedPopupData);
  });

  it('#changeOfTeamValidation selected a team before', () => {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    timeService.getHydraDaysDifference.and.returnValue(observableOf(32));
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage').and.returnValue(observableOf('timePer'));
    component.userSelectionDaysExceeded = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf(false));
    userService.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({ "teamId":"1c8m2ko0wxq1asfkuykurdr0y","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).toBe(true);
    expect(component.fanzonePopupData).toBeDefined();
  });

  it('should not display changeOfTeamValidation error message when a team is already selected and time has  elapsed now 3', () => {
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage');
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    fanzoneHelperService.fanzoneTeamUpdate.subscribe = jasmine.createSpy('fanzoneTeamUpdate').and.callFake(cb => cb && cb(true));
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage').and.returnValue(observableOf('timePer'));
    component.userSelectionDaysExceeded = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf(false));
    userService.status = true;
    fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue({ "teamId":"1c8m2ko0wxq1asfkuykurdr0y","teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(12);
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).toBe(true); 
    expect(component.fanzonePopupData).toBeDefined()
  });

  it('#changeOfTeamValidation selected a team before for resigned user', () => {
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage');
    spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage').and.returnValue(observableOf('timePer'));
    component.userSelectionDaysExceeded = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf(false));
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({ isResignedUser: true,"teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(32);
    component.changeOfTeamValidation();
    expect(component.thankYouPopup).toBe(true);
    expect(component.fanzonePopupData).toBe(component.daysNotCompletedPopupData);
  });

  it('#changeOfTeamValidation selected a team before for resigned user', () => {
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage');
    const openSpy = spyOn(FanzoneSelectYourTeamDialogComponent.prototype['__proto__'], 'open');
    component.fanzonePopupData = selectedTeamDataPostLogin;
    component.getTimePeriodChangeMessage = jasmine.createSpy('getTimePeriodChangeMessage').and.returnValue(observableOf('timePer'));
    component.userSelectionDaysExceeded = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf(true));
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({ isResignedUser: true,"teamName":"Crystal Palace", "isFanzoneExits": true,"subscriptionDate":"2022-04-07T13:20:01Z" });
    timeService.getHydraDaysDifference.and.returnValue(12);
    component.changeOfTeamValidation();
    expect(openSpy).toHaveBeenCalled();
  });

  it('#getChangeOfTeamTitle actual team', () => {
    const res = component.getChangeOfTeamTitle('1c8m2ko0wxq1asfkuykurdr0y', 'ARSENAL');
    expect(res).toBe('CHANGE TEAM');
  });

  it('#getChangeOfTeamTitle custom team', () => {
    const res = component.getChangeOfTeamTitle('FZ001', 'ARSENAL');
    expect(res).toBe('ARSENAL');
  });

});
