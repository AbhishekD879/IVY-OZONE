import { AbstractDialogComponent } from "@app/shared/components/oxygenDialogs/abstract-dialog";
import { FanzoneSycDialogComponent } from "@lazy-modules/fanzone/components/fanzoneSycDialog/fanzone-syc-dialog.component";
import { specialPagesData as sycData } from "@lazy-modules/fanzone/mockData/fanzone-shared.mock"
import { of } from "rxjs";

describe('FanzoneSycDialogComponent', () => {
  let component: FanzoneSycDialogComponent;
  let device;
  let windowRef;
  let userService;
  let fanzoneStorageService;
  let router;
  let timeService;
  let gtmService;
  let fanzoneSharedService;

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

    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({}),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove')
    };

    userService = {
      username: 'ukmigct_qa3237'
    };

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    timeService = {
      getHydraDaysDifference: jasmine.createSpy('getHydraDaysDifference').and.returnValue(10),
    };
    fanzoneSharedService = {
      addDaysToCurrentDate: jasmine.createSpy('addDaysToCurrentDate'),
      appendToStorage: jasmine.createSpy('appendToStorage'),
      addDaysToDate: jasmine.createSpy(),
      checkIfTeamIsRelegated: jasmine.createSpy('checkIfTeamIsRelegated').and.returnValue(of(false)),
      isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false))
    }
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new FanzoneSycDialogComponent(
      device,
      windowRef,
      fanzoneStorageService,
      userService,
      router,
      timeService,
      gtmService,
      fanzoneSharedService
    );
    component.dialog = {
      open : jasmine.createSpy('open'),
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };

    component.userKey = 'setDate-ukmigct_qa3237'
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('FanzoneSycDialogComponent', () => {

    it('should open dialog if user data in storage is empty ', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.getUserData = jasmine.createSpy();
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({});
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(openSpy).toHaveBeenCalled();
      expect(component.fanzonePopupData).toEqual(params);
    });

    it('should open dialog when remindLater time is exceeded', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneSharedService.addDaysToDate.and.returnValue('2022-05-07T13:20:00.834Z')
      fanzoneStorageService.get.and.returnValue({ teamId:'FZ001', teamName:'customTeam', "subscriptionDate": "2022-04-07T13:20:00.834Z" })
      timeService.getHydraDaysDifference.and.returnValue(of(35));
      component.open();
      expect(component.subscriptionTime).toBe(parseInt(sycData[0].remindLaterHideDays));
      expect(openSpy).toHaveBeenCalled();
    });

    it('should calculate showSYCPopup on for opening dialog when custom team is selected', () => {
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneSharedService.addDaysToDate.and.returnValue('2022-05-07T13:20:00.834Z')
      fanzoneStorageService.get.and.returnValue({ teamId:'agjsdeejendjfj', teamName:'customTeam', subscriptionDate: '2022-04-07T13:20:00.834Z' })
      component.open();
      expect(component.subscriptionTime).not.toBe(sycData[0].daysToChangeTeam);
    });

    it('should calculate showSYCPopup on for opening dialog ', () => {
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ teamId:'FZ001', teamName:'Arsenal', subscriptionDate: '2022-04-07T13:20:00.834Z' })
      component.open();
      expect(component.subscriptionTime).toBe(parseInt(sycData[0].remindLaterHideDays));
    });

    it('should open dialog when isFanzoneExists is false', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({isFanzoneExists:false, teamId: 'Arsenal FC'});
      timeService.getHydraDaysDifference.and.returnValue(of(35));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open dialog when showSYCPopupOn time exceeds', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({"showSYCPopupOn":'2022-05-26T08:38:28.807Z'});
      timeService.getHydraDaysDifference.and.returnValue(of(5));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open dialog when isResignedUser is true', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({isResignedUser:true, teamLastUpdatedAt: '2022-02-14T08:44:11.329Z'})
      timeService.getHydraDaysDifference.and.returnValue(of(31));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open dialog when when there\'s no previous selection', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({})
      timeService.getHydraDaysDifference.and.returnValue(of(-0.2));
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should open dialog if user is resigned and remind me later days exceeeded and days of subscribtion exceeds 30d', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isResignedUser: true, subscriptionDate: '2022-05-26T08:38:28.807Z', isFanzoneExists: false })
      timeService.getHydraDaysDifference.and.returnValue(of(30));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open dialog if user is resigned and remind me later days not exceeeded or days of subscribtion not exceeds 30d', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isResignedUser: true, subscriptionDate: '2022-04-26T08:38:28.807Z', isFanzoneExists: false })
      timeService.getHydraDaysDifference.and.returnValue(of(-.2));
      component.open();

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open dialog if user is resigned and remind me later days exceeeded and days of subscribtion exceeds 30d', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isResignedUser: true, subscriptionDate: '2022-04-26T08:38:28.807Z', isFanzoneExists: false })
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('when a team is relegated', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneSharedService.checkIfTeamIsRelegated.and.returnValue(of(true));
      fanzoneStorageService.get.and.returnValue({ "teamId":"235gd56378334bhfd","showSYCPopupOn":'2022-05-26T08:38:28.807Z', isResignedUser: true, subscriptionDate: '2022-04-26T08:38:28.807Z', isFanzoneExists: false })
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('should open dialog when resigned from 21st team', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({isResignedUser:true, isCustomResignedUser: true, teamLastUpdatedAt: '2022-02-14T08:44:11.329Z'});
      component.open();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open syc dialog when resigned from 21st team and clicked on either dont show me again / remind me later', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({isResignedUser:true, isCustomResignedUser: true, teamLastUpdatedAt: '2022-02-14T08:44:11.329Z', showSYCPopupOn: '2022-02-14T08:44:11.329Z'});
      component.open();
      expect(openSpy).not.toHaveBeenCalled();
    });

    it('fetchRelegatedTeamInfo', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const fzStorage = { "teamId":"235gd56378334bhfd","showSYCPopupOn":'2022-05-26T08:38:28.807Z', isResignedUser: true, subscriptionDate: '2022-04-26T08:38:28.807Z', isFanzoneExists: false }
      fanzoneStorageService.get.and.returnValue(fzStorage);
      fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
      component.fetchRelegatedTeamInfo(fzStorage);
      expect(gtmService.push).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
    })

    it('fetchRelegatedTeamInfo when days season start date not reached', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      const fzStorage = {isFanzoneTeamRelegated: true, showRelegatedPopupOn: 'test'}
      fanzoneStorageService.get.and.returnValue(fzStorage);
      fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
      component.fetchRelegatedTeamInfo(fzStorage);
      expect(gtmService.push).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
    })

    it('fetchRelegatedTeamInfo when days season start date reached', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      timeService.getHydraDaysDifference.and.returnValue(of(-1));
      const fzStorage = {isFanzoneTeamRelegated: true, showRelegatedPopupOn: 'test'}
      fanzoneStorageService.get.and.returnValue(fzStorage);
      fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
      component.fetchRelegatedTeamInfo(fzStorage);
      expect(gtmService.push).not.toHaveBeenCalled();
      expect(openSpy).not.toHaveBeenCalled();
    })

    it('should not open dialog if user is new and remind me later days exceeeded', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isFanzoneExists: false, isResignedUser: false })
      timeService.getHydraDaysDifference.and.returnValue(of(30));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open dialog if user is new and remind me later days not exceeeded', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isFanzoneExists: false, isResignedUser: false })
      timeService.getHydraDaysDifference.and.returnValue(of(-2));
      component.open();

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open dialog if user is new and remind me later days exceeeded', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ "showSYCPopupOn":'2022-05-26T08:38:28.807Z', isFanzoneExists: false, isResignedUser: false })
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open dialog if user has selected remind me later until new season starts/no. of days completed', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ 'remindMeLater': true, 'setDate-ukmigct_qa3237': '2022-02-14T08:44:11.329Z' })

      component.open();

      expect(openSpy).not.toHaveBeenCalled();
    });
    
    it('should not open dialog if user has selected dont show me again after new season starts', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ 'DontShowMeAgain': true, 'setDate-ukmigct_qa3237': '2022-02-14T08:44:11.329Z' })

      component.open();

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should not open dialog if user has selected remind me later until new season starts/no. of days completed', () => {

      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneStorageService.get.and.returnValue({ 'remindMeLater': true, 'setDate-ukmigct_qa3237': '2022-02-14T08:44:11.329Z' })

      component.open();

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open dialog if user team is relegated ', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.getUserData = jasmine.createSpy();
      fanzoneSharedService.checkIfTeamIsRelegated.and.returnValue(of(true));
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({isFanzoneTeamRelegated: true, showRelegatedPopupOn: 'test'});
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(gtmService.push).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open dialog if user team is relegated for specified days', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.getUserData = jasmine.createSpy();
      fanzoneSharedService.checkIfTeamIsRelegated.and.returnValue(of(true));
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({isFanzoneTeamRelegated: true, showRelegatedPopupOn: 'test'});
      timeService.getHydraDaysDifference.and.returnValue(of(-10));
      component.open();

      expect(openSpy).toHaveBeenCalled();
    });

    it('should not open dialog if fanzone config is disabled', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      fanzoneSharedService.checkIfTeamIsRelegated.and.returnValue(of(true));
      fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(true));
      component.open();
      
      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open dialog if new user ', () => {
      const openSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'open');
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.getUserData = jasmine.createSpy();
      fanzoneSharedService.checkIfTeamIsRelegated.and.returnValue(of(true));
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({});
      timeService.getHydraDaysDifference.and.returnValue(of(2));
      component.open();

      expect(gtmService.push).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
    });


    it('should set boolean values of isImInClicked flag as per button clicked 1  ', () => {
      const closeDialogSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'closeDialog');
      component.checkDialogButtonClick('I M IN');

      expect(component.isImInClicked).toEqual(true);
      expect(router.navigate).toHaveBeenCalled();
      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should return storage data when called getUserData', () => {
      fanzoneStorageService.get.and.returnValue({ 'DontShowMeAgain': true, 'setDate-ukmigct_qa3237': '2022-02-14T08:44:11.329Z' })
      const res = component.getUserData();
      expect(res).toBeTruthy();
    })

    it('should return {} when called getUserData', () => {
      fanzoneStorageService.get.and.returnValue({})
      const res = component.getUserData();
      expect(res).toEqual({});
    })

    it('should set boolean values of isRemindMeLaterClicked flag as per button clicked ', () => {
      const closeDialogSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'closeDialog');
      // component.getDateDifference = jasmine.createSpy();
      component.checkDialogButtonClick('Remind Me Later');

      expect(component.isRemindMeLaterClicked).toBe(true);
      // expect(component.getDateDifference).toHaveBeenCalled();
      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should set boolean values of isDontShowMeAgainClicked flag as per button clicked ', () => {
      const closeDialogSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'closeDialog');
      component.checkDialogButtonClick('Dont show me this again');

      expect(component.isDontShowMeAgainClicked).toBeTruthy();
      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should set boolean values as false if user is not logged in ', () => {
      userService.username = null;
      const closeDialogSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'closeDialog');
      component.closeSYCDialog();

      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should set boolean values of isImInClicked flag as per button clicked 2 ', () => {
      const closeDialogSpy = spyOn(FanzoneSycDialogComponent.prototype['__proto__'], 'closeDialog');
      component.checkDialogButtonClick('test');

      expect(component.isImInClicked).toEqual(false);
      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should return data from storage ', () => {
      const userData = component.getUserData();

      expect(userData).toEqual({});
    });

    it('should return data from storage ', () => {
      fanzoneStorageService.get.and.returnValue(null);
      const userData = component.getUserData();

      expect(userData).toEqual({});
    });

    it('should close dialog and update date to storage on click of remind me later', ()=>{
      userService.username = 'ukmigct_qa3237';
      component.isRemindMeLaterClicked = true;
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.closeSYCDialog();
      expect(fanzoneSharedService.addDaysToCurrentDate).toHaveBeenCalled();
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    })

    it('should close dialog and update date to storage on click of dont show me again', ()=>{
      userService.username = 'ukmigct_qa3237';
      component.isDontShowMeAgainClicked = true;
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.closeSYCDialog();
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    })

    it('should close dialog and update date to storage on click of i\'m in', ()=>{
      userService.username = 'ukmigct_qa3237';
      component.isImInClicked = true;
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.closeSYCDialog();
      expect(router.navigate).toHaveBeenCalled();
    })

    it('should close relegated dialog and update date to storage on click of remind me later', ()=>{
      userService.username = 'ukmigct_qa3237';
      component.isRemindMeLaterClicked = true;
      component.isRelegated = true;
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.closeSYCDialog();
      expect(fanzoneSharedService.addDaysToCurrentDate).toHaveBeenCalled();
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    })

    it('should close relegated dialog and update date to storage on click of dont show me again', ()=>{
      userService.username = 'ukmigct_qa3237';
      component.isDontShowMeAgainClicked = true;
      component.isRelegated = true;
      const params = sycData[0];
      AbstractDialogComponent.prototype.setParams(params);
      component.closeSYCDialog();
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    })
  });
});
