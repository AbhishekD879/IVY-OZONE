import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FanzoneSharedComponent } from '@lazy-modules/fanzone/components/fanzone-shared.component';
import { specialPagesData } from '@lazy-modules/fanzone/mockData/fanzone-shared.mock';
import { fakeAsync, tick } from '@angular/core/testing';

describe('FanzoneSharedComponent', () => {
  let component: FanzoneSharedComponent;
  let fanzoneSharedService;
  let pubsubService;
  let dialogService;
  let userService;
  let windowRefService;
  let componentFactoryResolver;
  let fanzoneHelperService

  beforeEach(() => {
    fanzoneSharedService = {
      getSpecialPagesDataCollection: jasmine.createSpy('getSpecialPagesDataCollection').and.returnValue(of(specialPagesData)),
      isEnableFanzone: true,
      isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true))
    };

    pubsubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({ data: [1] });
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);

    userService = {
      username: 'username'
    };
    windowRefService = {
      nativeWindow: {
        location: {
          href: 'location_href',
          pathname: '/sport/football'
        }
      }
    };

    fanzoneHelperService = {
      fanzoneTeamUpdate: {
        subscribe: jasmine.createSpy('fanzoneTeamUpdate').and.callFake(cb => cb && cb(true))
      },
      checkIfTeamIsRelegated: jasmine.createSpy('checkIfTeamIsRelegated').and.returnValue(of(true))
    };
    componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);

    createComponent();
  });

  function createComponent() {
    component = new FanzoneSharedComponent(fanzoneSharedService, pubsubService, dialogService, userService,windowRefService,componentFactoryResolver, fanzoneHelperService);
  }

  it('should create fanzone shared component ', () => {
    expect(component).toBeTruthy();
  });

  it('should get special pages data ', () => {
    component.ngOnInit();

    expect(component.sycData).toEqual(specialPagesData);
  });

  it('should get special pages data on SUCCESSFUL_LOGIN', () => {
    pubsubService.subscribe = jasmine.createSpy('pubSubService.subscribe')
                .and.callFake((filename: string, b: string, callback: Function) => {
                    if (b.length && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
                      fanzoneHelperService.fanzoneTeamUpdate.subscribe = jasmine.createSpy('fanzoneTeamUpdate').and.callFake(() => {
                        callback(component.getSycData());
                        expect(component.sycData).toEqual(specialPagesData);
                      })  
                    }
                });
    component.ngOnInit();
  });

  it('set fanzone enabled as true when home page on login', fakeAsync(() => {
    pubsubService.subscribe.and.callFake((a, b, cb) => {
      component.getSycData = jasmine.createSpy('');
      if (b.length && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
        cb();
        expect(component.getSycData).toHaveBeenCalled();
      }
    });
    component.ngOnInit();
    tick();
    expect(pubsubService.subscribe).toHaveBeenCalledWith(
      component.channelName, [pubsubService.API.SESSION_LOGIN, pubsubService.API.SUCCESSFUL_LOGIN], jasmine.any(Function)
    ); 
  }));

  it('should get special pages data on SUCCESSFUL_LOGIN 2', () => {
    pubsubService.subscribe = jasmine.createSpy('pubSubService.subscribe')
                .and.callFake((filename: string, b: string, callback: Function) => {
                    if (b.length && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
                      callback(component.getSycData());
                      expect(component.sycData).toEqual(specialPagesData);
                    }
                });
    component.ngOnInit();
  });

  it('should open dialog if football page and user logged in',()=>{
    windowRefService.nativeWindow.location.href = 'https://sports.ladbrokes/sport/football/matches';
    userService.username = 'test';
    fanzoneHelperService.isEnableFanzone = true;
    fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
    component.ngOnInit();  

    expect(dialogService.openDialog).toHaveBeenCalled();
  });

  it('should open dialog if football page and user logged in',()=>{
    windowRefService.nativeWindow.location.pathname = '/sport/football';
    userService.username = 'test';
    fanzoneHelperService.isEnableFanzone = true;
    fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
    component.ngOnInit();  

    expect(dialogService.openDialog).toHaveBeenCalled();
  });

  it('should open dialog if football page and user logged in',()=>{
    windowRefService.nativeWindow.location.pathname = '/sport/football/competitions';
    userService.username = 'test';
    fanzoneHelperService.isEnableFanzone = true;
    fanzoneSharedService.isFanzoneConfigDisabled.and.returnValue(of(false));
    component.ngOnInit();  

    expect(dialogService.openDialog).not.toHaveBeenCalled();
  });

  it('should not open dialog if not football page and user logged in',()=>{
    windowRefService.nativeWindow.location.href = 'https://sports.ladbrokes/home';
    userService.username = 'test';

    component.ngOnInit();
 
    expect(dialogService.openDialog).not.toHaveBeenCalled();
  });

  it('should not open dialog if  football page and user not logged in',()=>{
    windowRefService.nativeWindow.location.href = 'https://sports.ladbrokes/football';
    userService.username = null;

    component.ngOnInit();

    expect(dialogService.openDialog).not.toHaveBeenCalled();
  });

  it('should not open dialog if  not football page and user not logged in',()=>{
    windowRefService.nativeWindow.location.href = 'https://sports.ladbrokes/home';
    userService.username = null;

    component.ngOnInit();

    expect(dialogService.openDialog).not.toHaveBeenCalled();
  });

  it('#ngOnDestroy should call pubSubService.unsubscribe', () => {
    const controllerIdentifier = 'fanzoneSharedHome';
    component['channelName'] = controllerIdentifier;

    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith(controllerIdentifier);
  });
});
