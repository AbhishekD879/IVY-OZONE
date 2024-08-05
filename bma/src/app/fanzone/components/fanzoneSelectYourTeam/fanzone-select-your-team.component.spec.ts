import { fakeAsync, tick } from '@angular/core/testing';
import { TEAM_COLOR } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveasdie-crest-image.mock';
import { of, of as observableOf } from 'rxjs';

import { FanzoneSelectYourTeamAppComponent } from '@app/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { SHOW_YOUR_COLORS } from '@app/fanzone/constants/fanzoneconstants';
import { FANZONE_ASSET, FANZONE_NO_TEAM_DATA_PRE_LOGIN, FANZONE_SYT_POPUP_EXCEEDED, FANZONE_TEAM_DETAIL, FANZONE_TEAM_DETAILS, FANZONE_TEAM_DATA_PRE_LOGIN, SPECIAL_PAGESDATA, NO_SUPPORT_TO_TEAM_PRE_LOGIN } from '@app/fanzone/mockdata/fanzone-select-your-team.component.mock';

describe('FanzoneSelectYourTeamAppComponent', () => { 
  let component: FanzoneSelectYourTeamAppComponent,
    componentFactoryResolver,
    cmsService,
    deviceService,
    dialogService,
    fanzoneSharedService,
    fanzoneSelectYourTeamDialogComponent,
    gtmService,
    localeService,
    pubSubService,
    route,
    routingState,
    storageService,
    successfulLoginHandler,
    userService,
    windowRef,
    timeService,
    changeDetectorRef,
    fanzoneStorageService;
  const fanzoneDetails = FANZONE_TEAM_DETAILS;
  const fanzoneSycDetails = SPECIAL_PAGESDATA;
  const createSpyWithReturnedObservable = (spyName: string, observableOf1?: any) => {
    return jasmine.createSpy(spyName)
      .and.returnValue(observableOf(observableOf1 ? observableOf1 : null));
  }; 

  beforeEach(() => {
    fanzoneSelectYourTeamDialogComponent = {
      name: 'NoSupport2AnyTeam',
      ctaSecondaryBtnClick: jasmine.createSpy('')
    };
    cmsService = {
      getFanzone: createSpyWithReturnedObservable('getAllFanzoneDetails', fanzoneDetails),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of([TEAM_COLOR])),
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(fanzoneSelectYourTeamDialogComponent)
    };
    deviceService = {};
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    fanzoneSharedService = {
      getSpecialPagesDataCollection: jasmine.createSpy('specialPagesData').and.returnValue(of(fanzoneSycDetails))
    }
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, listeners, handler) => {
        if (listeners === 'SESSION_LOGIN' || listeners === 'SUCCESSFUL_LOGIN') {
          successfulLoginHandler = handler;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        OPEN_LOGIN_DIALOG: 'OPEN_LOGIN_DIALOG'
      }
    } as any;
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get')
    };
    userService = {
      status: true,
      isUserLoggedIn: jasmine.createSpy('isUserLoggedIn')
    };
    windowRef = {
      nativeWindow: {
        setItem: jasmine.createSpy('setItem'),
        getItem: jasmine.createSpy('getItem').and.returnValue(true)
      }
    };
    timeService = {
      daysDifference: jasmine.createSpy('')
    }
    createComponent();
  });

  function createComponent() {
    component = new FanzoneSelectYourTeamAppComponent(
      cmsService as any,
      componentFactoryResolver as any,
      deviceService as any,
      dialogService as any,
      fanzoneSharedService as any,
      gtmService as any,
      localeService as any,
      pubSubService as any,
      route as any,
      routingState as any,
      storageService as any,
      userService as any,
      timeService as any,
      changeDetectorRef as any,
      fanzoneStorageService as any
    );
  }

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#OnInit', () => {
    it('should set component isLoggedIn properties to true', () => {
      component.getPopupData = jasmine.createSpy();
      component.ngOnInit();
      expect(component.iDonotSupportAnyTeam).toBeDefined();
      expect(component.isUserLoggedIn).toBeTrue();
      expect(component.getPopupData).toHaveBeenCalled();
    });

    it('Asset and team data should be not empty', () => {
      cmsService.getFanzone = createSpyWithReturnedObservable('getFanzoneDetails', []);
      cmsService.getTeamsColors = createSpyWithReturnedObservable('getTeamsColors', []);
      component.ngOnInit();
      expect(component.fanzoneData).toBeDefined();
      expect(component.fanzoneData).toEqual([]);
    });

    it('#getTeamDetails', ()=> {
      component.fanzoneData = FANZONE_TEAM_DETAILS;
      component.onTeamSelection = jasmine.createSpy();
      component.getTeamDetails('Everton');
      expect(component.onTeamSelection).toHaveBeenCalledWith(FANZONE_TEAM_DETAILS[0], 0);
    })

    it('should open modal with selected team  post login', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(FANZONE_TEAM_DATA_PRE_LOGIN)));
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (Array.isArray(b) && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
          cb();
        }
      });
      component.getTeamDetails = jasmine.createSpy();
      component['isUserLoggedIn'] = true;
      component.ngOnInit();
      tick();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.ctrlName, [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGIN], jasmine.any(Function)
      );
      expect(component.isUserLoggedIn).toBeTrue();
      expect(fanzoneStorageService.get).toHaveBeenCalled();
      expect(component.getTeamDetails).toHaveBeenCalledWith(FANZONE_TEAM_DATA_PRE_LOGIN.tempTeam.teamName);
    }));

    it('should highlight previous selected team', () => {
      component.teamJourneyAlreadyFinished = jasmine.createSpy('teamJourneyAlreadyFinished');
      fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue(JSON.parse(JSON.stringify(FANZONE_SYT_POPUP_EXCEEDED)));
      component['isUserLoggedIn'] = true;
      component.getPopupData();
      expect(component.teamJourneyAlreadyFinished).toHaveBeenCalled();
    })

    it('should highlight previous selected team if user subscribed to custom team', () => {
      fanzoneStorageService.get = jasmine.createSpy('FanzoneSYTPopup').and.returnValue(JSON.parse(JSON.stringify(NO_SUPPORT_TO_TEAM_PRE_LOGIN)));
      component['isUserLoggedIn'] = true;
      component.getPopupData();
      expect(component.noTeamSupport).toBeTruthy();
    })

    it('should get the index of previous selected team', () => {
      component.fanzoneData = [FANZONE_TEAM_DETAIL];
      component.teamJourneyAlreadyFinished("3");
      expect(component.currentlyClickedCardIndex).toEqual(0);
    })

    it('should open modal with i dont support post login', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(FANZONE_NO_TEAM_DATA_PRE_LOGIN)));
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (Array.isArray(b) && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
          cb();
        }
      });
      component.onNoTeamSupportSelection = jasmine.createSpy();
      component.ngOnInit();
      tick();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.ctrlName, [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGIN], jasmine.any(Function)
      );
      expect(component.isUserLoggedIn).toBeTrue();
      expect(fanzoneStorageService.get).toHaveBeenCalled();
      expect(component.customTeam).toEqual(FANZONE_NO_TEAM_DATA_PRE_LOGIN.tempTeam.teamName);
      expect(component.onNoTeamSupportSelection).toHaveBeenCalled();
    }));
  })

  it('ga tracking object should be pushed to data layer', fakeAsync(() => {
    component['fanzonePopupData'] = fanzoneSycDetails[0];
    component.pushCachedEvents = jasmine.createSpy('cachedEvents');
    component.pushCachedEvents(SHOW_YOUR_COLORS.GTA.DE_SELECT, SHOW_YOUR_COLORS.GTA.I_DONT_SUPPORT);
    tick();
    expect(component.pushCachedEvents).toHaveBeenCalledWith(SHOW_YOUR_COLORS.GTA.DE_SELECT, SHOW_YOUR_COLORS.GTA.I_DONT_SUPPORT);
  }))

  it('ga tracking object pushed to gtm service', () => {
    component['pushCachedEvents'](SHOW_YOUR_COLORS.GTA.DE_SELECT, SHOW_YOUR_COLORS.GTA.I_DONT_SUPPORT);
    const dataLayer = { event: SHOW_YOUR_COLORS.GTA.TRACK_EVENT, eventAction: SHOW_YOUR_COLORS.GTA.DE_SELECT, eventCategory: SHOW_YOUR_COLORS.GTA.SHOW_UR_COLORS, eventLabel: SHOW_YOUR_COLORS.GTA.I_DONT_SUPPORT }
    expect(gtmService.push).toHaveBeenCalledWith(dataLayer.event, dataLayer);
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('#ngOnDestroy', () => {
    it('called on component destroy', () => {
      component['ctrlName'] = 'Fanzone';
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['ctrlName']);
    });
  });


  it('should call through when user selects i donot support any team ', fakeAsync(() => {
    deviceService.isDesktop = jasmine.createSpy('isDesktop').and.returnValue(false);
    component['fanzonePopupData'] = fanzoneSycDetails[0];
    component.pushCachedEvents = jasmine.createSpy();
    component.onNoTeamSupportSelection('GenericTeam');
    tick();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    expect(component.pushCachedEvents).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      SHOW_YOUR_COLORS.DIALOG_NAME.NO_SUPPORT_TO_TEAM, fanzoneSelectYourTeamDialogComponent, true, jasmine.any(Object)
    );
  }));

  it('#getTimePeriodChangeMessage', ()=>{
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({"subscriptionDate": "2022-04-28T10:44:02Z"})));
    component.fanzonePopupData = {daysToChangeTeam: 35} as any;
    timeService.daysDifference.and.returnValue(32);
  })

  it('should call through when user selects i donot support any team  when user not logged in from promotions page', fakeAsync(() => {
    userService.status = jasmine.createSpy('status').and.returnValue(false);
    deviceService.isDesktop = jasmine.createSpy('isDesktop').and.returnValue(true);
    component['isUserLoggedIn'] = false;
    component['fanzonePopupData'] = fanzoneSycDetails[0];
    component.pushCachedEvents = jasmine.createSpy();
    component.onNoTeamSupportSelection('GenericTeam');
    tick();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    expect(component.pushCachedEvents).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      SHOW_YOUR_COLORS.DIALOG_NAME.NO_SUPPORT_TO_TEAM, fanzoneSelectYourTeamDialogComponent, true, jasmine.any(Object)
    );
  }));

  it('should call through when user selects a team when there is temp team', fakeAsync(() => {
    component['fanzonePopupData'] = fanzoneSycDetails[0];
    component.pushCachedEvents = jasmine.createSpy();
    component.getPopupDescriptionForDesktop = jasmine.createSpy();
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({tempTeam: {id:'7yx5dqhhphyvfisohikodajhv', teamname:'Bentford'}})));
    component.onTeamSelection(fanzoneDetails[0], 1);
    expect(component.currentlyClickedCardIndex).toBe(1);
    tick();
    expect(fanzoneStorageService.set).toHaveBeenCalled();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    expect(component.pushCachedEvents).toHaveBeenCalled();
    expect(component.getPopupDescriptionForDesktop).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      SHOW_YOUR_COLORS.DIALOG_NAME.TEAM_CONFIRMATION, fanzoneSelectYourTeamDialogComponent, true, jasmine.any(Object)
    );
  }));

  it('should call through when user selects a team', fakeAsync(() => {
    component['fanzonePopupData'] = fanzoneSycDetails[0];
    component.pushCachedEvents = jasmine.createSpy();
    component.getPopupDescriptionForDesktop = jasmine.createSpy();
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({"subscriptionDate": "2022-04-28T10:44:02Z"})));
    component.onTeamSelection(fanzoneDetails[0], 1);
    expect(component.currentlyClickedCardIndex).toBe(1);
    tick();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    expect(component.pushCachedEvents).toHaveBeenCalled();
    expect(component.getPopupDescriptionForDesktop).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      SHOW_YOUR_COLORS.DIALOG_NAME.TEAM_CONFIRMATION, fanzoneSelectYourTeamDialogComponent, true, jasmine.any(Object)
    );
  }));

  it('should open modal with selected team  post login', fakeAsync(() => {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(FANZONE_NO_TEAM_DATA_PRE_LOGIN)));
    pubSubService.subscribe.and.callFake((a, b, cb) => {
      if (Array.isArray(b) && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
        cb();
      }
    });
    component.teamJourneyAlreadyFinished = jasmine.createSpy();
    component.checkIfUserLoginFirstTime = jasmine.createSpy().and.returnValue(true);
    component['getPreLoginInfo'] = jasmine.createSpy();
    component['isUserLoggedIn'] = true;
    component.ngOnInit();
    tick();
    expect(component.checkIfUserLoginFirstTime).toHaveBeenCalled();
    expect(component['getPreLoginInfo']).toHaveBeenCalled();
    expect(component.teamJourneyAlreadyFinished).toHaveBeenCalled();
  }));
  it('getPopupDescriptionForDesktop',() => {
    const value = "By CONFIRMING that you are a supporter of <span class='font-weight-bold'>Arsenal</span> you will not be able to change your team for another <span class='font-weight-bold'>30</span> days. On the next screen you can tell us which FANZONE notifications you want to receive";
    const res = component.getPopupDescriptionForDesktop(fanzoneSycDetails[0].sycConfirmMsgMobile,'Arsenal', 30);
    expect(res).toEqual(value);
  })

  it('checkIfUserLoginFirstTime', ()=>{
    storageService.get = jasmine.createSpy('USER').and.returnValue(JSON.parse(JSON.stringify({firstLogin:true})));
    const res = component.checkIfUserLoginFirstTime();
    expect(res).toBe(true);
  })

  it('checkIfUserLoginFirstTime', ()=>{
    storageService.get = jasmine.createSpy('USER').and.returnValue(JSON.parse(JSON.stringify({firstLogin:false})));
    const res = component.checkIfUserLoginFirstTime();
    expect(res).toBe(false);
  })

  describe("Should check for assets", () => {
    it("check if asset exists and add to team", () => {
      component.fanzoneData = [FANZONE_TEAM_DETAIL];
      component.colorsData = [FANZONE_ASSET];
      component.getAssetData();
      expect(component.fanzoneData[0].asset).toEqual(component.colorsData[0]);
    });
  });

  describe('should update popup information when user not logged in', () => {
    beforeEach(() => {
      userService = {
        status: true
      };
    })

    it('should call getMessageUserLogin method', () => {
      component['isUserLoggedIn'] = true;
      const result = component.getMessageUserLogin('message1', 'message2');
      expect(result).toBe('message1');
    });

    it('should call getMessageUserLoginDevice method when device is not desktop', () => {
      deviceService.isDesktop = false;
      component['isUserLoggedIn'] = true;
      const result = component.getMessageUserLoginDevice('message1', 'message2', 'message3');
      expect(result).toBe('message2');
    });

    it('should call getMessageUserLoginDevice method when device is desktop', () => {
      deviceService.isDesktop = true;
      component['isUserLoggedIn'] = true;
      const result = component.getMessageUserLoginDevice('message1', 'message2', 'message3');
      expect(result).toBe('message1');
    })
  })


  describe('should update popup information when user not logged in', () => {
    beforeEach(() => {
      userService = {
        status: false
      };
    })

    it('should call private method', () => {
      component['isUserLoggedIn'] = false;
      const result = component.getMessageUserLogin('message1', 'message2');
      expect(result).toBe('message2');
    });
  })

});
