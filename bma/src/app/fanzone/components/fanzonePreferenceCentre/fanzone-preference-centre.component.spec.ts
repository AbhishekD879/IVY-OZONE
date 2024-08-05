import { FanzonePreferenceCentreAppComponent } from './fanzone-preference-centre.component';
import { PreferenceCentre, PreferenceCentreAllPreferencesSelected, PreferenceCentreSomePreferencesSelected, selectedFanzone } from '@app/fanzone/components/fanzonePreferenceCentre/mockData/fanzone-preference-centre.component.mock';
import { of, of as observableOf } from 'rxjs';
import { FanzonePreferenceDialogComponent } from '@app/lazy-modules/fanzone/components/fanzonePreferenceDialog/fanzone-preference-dialog.component';
import { FanzonePreferenceDialog } from '@app/fanzone/constants/fanzonePreferenceConstants';

describe('FanzonePreferenceCentreAppComponent', () => {
  let component: FanzonePreferenceCentreAppComponent,
      componentFactoryResolver, 
      dialogService,
      fanzoneSharedService, 
      router,
      fanzoneStorageService, 
      fanzonePreferenceDialogComponent,
      pubSubService,
      changeDetectorRef,
      WindowRefService,
      routingState,
      nativeBridge;
  const createSpyWithReturnedObservable = (spyName: string, observableOf1?: any) => {
    return jasmine.createSpy(spyName)
      .and.returnValue(observableOf(observableOf1 ? observableOf1 : null));
  };

  beforeEach(() => {
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(FanzonePreferenceDialogComponent)
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get')
    };
    router = {
      getCurrentNavigation: jasmine.createSpy('getCurrentNavigation')
    }
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => {return true}),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        FANZONE_TOGGLE_ON: 'FANZONE_TOGGLE_ON'
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    fanzoneSharedService = {
      saveTeamOnPlatformOne: jasmine.createSpy('saveTeamOnPlatformOne'),
      pushCachedEvents: jasmine.createSpy('pushCachedEvents'),
      getFanzoneInfo: jasmine.createSpy('getFanzoneInfo').and.returnValue({}),
      getFanzonePreferences: jasmine.createSpy('getFanzonePreferences').and.returnValue(of(PreferenceCentre)),
      isSubscribedToCustomTeam: jasmine.createSpy('isSubscribedToCustomTeam')
    };
    fanzonePreferenceDialogComponent = {
      name: 'fanzonePreferenceDialogComponent',
    };
    WindowRefService = {
      nativeWindow: {
        NativeBridge : { pushNotificationsEnabled: true,showNotificationSettings: jasmine.createSpy() },
        location: {
          pathname: 'testPath'
        }
      },
      document: {
        querySelectorAll: jasmine.createSpy().and.returnValue([])
      }
    } as any;
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('/now-next'),
    };
    component = new FanzonePreferenceCentreAppComponent(nativeBridge, componentFactoryResolver, dialogService,
      fanzoneSharedService, router, fanzoneStorageService, pubSubService, changeDetectorRef, WindowRefService,routingState);
    component.preferences = PreferenceCentre[0];
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', ()=> {
    component.getPreferences = jasmine.createSpy();
    component.switchToggleOn = jasmine.createSpy()
    component.ngOnInit();
    expect(component.getPreferences).toHaveBeenCalled();
    expect(component.switchToggleOn).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  })

  it('#pubsub on init', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: { data: PreferenceCentre[0]} } } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(selectedFanzone)));
    fanzoneSharedService.getFanzoneInfo = jasmine.createSpy('getFanzoneInfo').and.returnValue(selectedFanzone);
    component['updatePrefWithSelectTeam'] = jasmine.createSpy('');
    pubSubService.subscribe.and.callFake((p1, p2, cb) =>  cb(true));
    component.ngOnInit();
    expect(component['updatePrefWithSelectTeam']).toHaveBeenCalled();
  });
  
  it('#ngOnInit for pushNotificationsEnabled false', ()=> {
    WindowRefService.nativeWindow.NativeBridge.pushNotificationsEnabled = false;
    component.getPreferences = jasmine.createSpy();
    component.switchToggleOn = jasmine.createSpy()
    component.ngOnInit();
    expect(component.getPreferences).toHaveBeenCalled();
    expect(component.switchToggleOn).toHaveBeenCalled();
  })

  it('#switchToggleOn', () => {
    pubSubService.subscribe.and.callFake((p1, p2, cb) =>  cb(true));
    component.switchToggleOn();
    expect(pubSubService.subscribe).toHaveBeenCalled();
    expect(component.fanzoneSubscription).toBeTruthy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  }) 

  it('should get all selected preferences', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: { data: PreferenceCentre[0]} } } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(selectedFanzone)));
    fanzoneSharedService.getFanzoneInfo = jasmine.createSpy('getFanzoneInfo').and.returnValue(selectedFanzone)
    component.getPreferences();
    expect(fanzoneSharedService.getFanzoneInfo).toHaveBeenCalled();
    expect(component.preferences).toBe(PreferenceCentre[0]);
    expect(component.activatedPreferences).toEqual(["TEAM_NEWS", "PRE_MATCH"]);
  })

  it('should get all selected preferences when state is undefined', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: undefined } } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(selectedFanzone)));
    fanzoneSharedService.getFanzoneInfo = jasmine.createSpy('getFanzoneInfo').and.returnValue(selectedFanzone)
    component.getPreferences();
    expect(fanzoneSharedService.getFanzoneInfo).toHaveBeenCalled();
    expect(component.preferences).toBe(PreferenceCentre[0]);
  })

  it('should get all selected preferences when data is undefined ', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: {data: undefined} } } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(selectedFanzone)));
    fanzoneSharedService.getFanzoneInfo = jasmine.createSpy('getFanzoneInfo').and.returnValue(selectedFanzone)
    component.getPreferences();
    expect(fanzoneSharedService.getFanzoneInfo).toHaveBeenCalled();
    expect(component.preferences).toBe(PreferenceCentre[0]);
  })

  it('should get all selected preferences when extras is undefined', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: undefined } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify(selectedFanzone)));
    fanzoneSharedService.getFanzoneInfo = jasmine.createSpy('getFanzoneInfo').and.returnValue(selectedFanzone)
    component.getPreferences();
    expect(fanzoneSharedService.getFanzoneInfo).toHaveBeenCalled();
    expect(component.preferences).toBe(PreferenceCentre[0]);
  })

  it('should call on init to get preferences', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: { data: {}} } } as any);
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({});
    component.getPreferences();
    expect(component.preferences).toBe(PreferenceCentre[0]);
    expect(component.fanzoneSubscription).toBeFalsy();
  })

  it('should call on init to get preferences', () => {
    router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ extras: { state: { data: {}} } } as any);
    component.preferences = null;
    component.getPreferences();
    expect(fanzoneSharedService.getFanzonePreferences).toHaveBeenCalled();
    expect(component.preferences).toEqual(PreferenceCentre[0]);
  })

  it('call check if all Preferences are selected', ()=> {
    component.preferences = PreferenceCentreAllPreferencesSelected[0];
    const res = component.checkIfAllPreferencesSelected(); 
    expect(res).toBe(true);
  })

  it('call check if all Preferences are not selected', ()=> {
    component.preferences = PreferenceCentreSomePreferencesSelected[0];
    const res = component.checkIfAllPreferencesSelected();
    expect(res).toBe(false);
  })


  it('should activate all preferences on toggle all preference and ga tracking as show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/football'),
    
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.allPreferencesSwitch(true);
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle on', 'All','show your colors');
    expect(component.activatedPreferences).toEqual(["TEAM_NEWS", "PRE_MATCH", "KICK_OFF", "IN_PLAY", "HALF_TIME", "FULL_TIME", "POST_MATCH"]);
  })

  it('should activate all preferences on toggle all preference and ga tracking as fanzone', () => {
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.allPreferencesSwitch(true);
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle on', 'All','fanzone');
    expect(component.activatedPreferences).toEqual(["TEAM_NEWS", "PRE_MATCH", "KICK_OFF", "IN_PLAY", "HALF_TIME", "FULL_TIME", "POST_MATCH"]);
  })

  it('should deactivate all preferences on toggle all preferences and set ga tracking as show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/football'),

    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.allPreferencesSwitch(false);
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle off', 'All','show your colors');
    expect(component.activatedPreferences).toEqual([]);
  })

  it('should deactivate all preferences on toggle all preferences and set ga tracking as fanzone', () => {
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.allPreferencesSwitch(false);
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle off', 'All','fanzone');
    expect(component.activatedPreferences).toEqual([]);
  })

  it('should get active preferences on toggle off and set ga tacking as fanzone', () => {
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.preferenceSwitch(false, "POST_MATCH",'POST MATCH OFFERS' );
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle off', 'POST MATCH OFFERS','fanzone');
    expect(component.activatedPreferences).toEqual([]);
  })

  it('should get active preferences on toggle off and set ga tracking as show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/football'),
    
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.preferenceSwitch(false, "POST_MATCH",'POST MATCH OFFERS' );
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle off', 'POST MATCH OFFERS','show your colors');
    expect(component.activatedPreferences).toEqual([]);
  })

  it('should get active preferences on toggle on and set ga tracking as fanzone', () => {
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.preferenceSwitch(true, "POST_MATCH", 'POST MATCH OFFERS');
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle on', 'POST MATCH OFFERS','fanzone');
    expect(component.activatedPreferences).toEqual(["POST_MATCH"]);
  })

  it('should get active preferences on toggle on and set ga tracking as show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/football'),
    
    
    component.activatedPreferences = [];
    component.preferences = PreferenceCentre[0];
    component.preferenceSwitch(true, "POST_MATCH", 'POST MATCH OFFERS');
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('toggle on', 'POST MATCH OFFERS','show your colors');
    expect(component.activatedPreferences).toEqual(["POST_MATCH"]);
  })

  it('should set allPreferences toggle on', () => {
    component.activatedPreferences = ["TEAM_NEWS", "PRE_MATCH", "KICK_OFF", "IN_PLAY", "HALF_TIME", "FULL_TIME"];
    component.preferences = PreferenceCentreAllPreferencesSelected[0];
    component.preferenceSwitch(true, "POST_MATCH", 'POST MATCH OFFERS');
    expect(component.allPreferences).toBe(true);
  })

  it('should set allPreferences toggle off', () => {
    component.activatedPreferences = ["TEAM_NEWS", "PRE_MATCH", "KICK_OFF", "IN_PLAY", "HALF_TIME", "FULL_TIME"];
    component.preferences = PreferenceCentreSomePreferencesSelected[0];
    component.preferenceSwitch(true, "POST_MATCH", 'POST MATCH OFFERS');
    expect(component.allPreferences).toBe(false);
  })

  it('should submit preferences on click of submit and set ga tracking as fanzone', () => {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({url:'sport/football', teamName: 'FZ001'})));
    component.preferences = {url:'sport/football', teamName: 'FZ001'} as any;
    component.onSubmitPreference();
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('Submit', '', 'fanzone');
  })

  it('should submit preferences on click of submit and set ga tracking as show your colors', () => {
    routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue('/football'),
    
    
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({url:'sport/football', teamName: 'FZ001'})));
    component.preferences = {url:'sport/football', teamName: 'FZ001'} as any;
    component.onSubmitPreference();
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('Submit', '', 'show your colors');
  })

  it('should submit preferences on click of submit route to', () => {
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(JSON.parse(JSON.stringify({teamName:'arsenal'})));
    component.preferences = {teamName:'arsenal'} as any;
    component.onSubmitPreference();
    expect(fanzoneSharedService.pushCachedEvents).toHaveBeenCalledWith('Submit', '', 'fanzone');
  })


  it('should open dialog when fanzone is unsubscribed', () => {
    component.fanzoneSubscription = true;
    component.unsubcribeFanzone();
    expect(component.fanzoneSubscription).toBeFalsy();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      FanzonePreferenceDialog, FanzonePreferenceDialogComponent, true, jasmine.any(Object)
    );
  });

  it('should not open dialog when fanzone is unsubscribed', () => {
    component.fanzoneSubscription = false;
    component.unsubcribeFanzone();
    expect(component.fanzoneSubscription).toBeTruthy();
    expect(dialogService.openDialog).not.toHaveBeenCalledWith(
      FanzonePreferenceDialog, FanzonePreferenceDialogComponent, true, jasmine.any(Object)
    );
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(pubSubService.API.FANZONE_TOGGLE_ON);
  });
  
  it('should get preference title for generic team', () => {
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(true);
    expect(component.getTitleAndDescription('title')).toBe(PreferenceCentre[0].genericTeamNotificationTitle);
  });

  it('should get preference description for generic team', () => {
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(true);
    expect(component.getTitleAndDescription('description')).toBe(PreferenceCentre[0].genericTeamNotificationDescription);
  });

  it('should get preference title for other valid teams', () => {
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(false);
    expect(component.getTitleAndDescription('title')).toBe(PreferenceCentre[0].pushPreferenceCentreTitle);
  });

  it('should get preference description for other valid teams', () => {
    fanzoneSharedService.isSubscribedToCustomTeam.and.returnValue(false);
    expect(component.getTitleAndDescription('description')).toBe(PreferenceCentre[0].pcDescription);
  });
});
