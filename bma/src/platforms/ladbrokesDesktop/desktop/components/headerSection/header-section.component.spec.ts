import { of  } from 'rxjs';
import { HeaderSectionComponent } from './header-section.component';
import { IHeaderSubMenu } from '@core/services/cms/models';
import { fakeAsync, tick } from '@angular/core/testing';
import { FANZONECONFIG } from './mockdata/header-section.component.mock';

describe('LDHeaderSectionComponent', () => {
  let component: HeaderSectionComponent;
  let headerSubMenu: IHeaderSubMenu[];

  const fanzoneConfig = FANZONECONFIG
  let cmsService, filtersService,
    germanSupportService, navigationService, user, pubsub, changeDetectorRef, fanzoneStorageService,
    bonusSuppressionService;

  beforeEach(() => {
    headerSubMenu = [{
      disabled: false,
      lang: 'lang',
      linkTitle: 'linkTitle',
      linkTitle_brand: 'linkTitle_brand',
      sortOrder: 0,
      targetUri: 'targetUri',
      inApp: false,
      id: 'id',
      brand: 'brand',
      createdBy: 'createdBy',
      createdAt: 'createdAt',
      updatedBy: 'updatedBy',
      updatedAt: 'updatedAt',
      updatedByUserName: 'updatedByUserName',
      createdByUserName: 'createdByUserName',
      target: 'target',
      targetUriCopy: 'targetUriCopy',
      sportName: 'sportName',
      relUri: false,
      svgId: 'svgId',
    },
    {
      disabled: false,
      lang: 'lang',
      linkTitle: '1-2-Free',
      linkTitle_brand: 'linkTitle_brand',
      sortOrder: 0,
      targetUri: 'targetUri',
      inApp: false,
      id: 'id',
      brand: 'brand',
      createdBy: 'createdBy',
      createdAt: 'createdAt',
      updatedBy: 'updatedBy',
      updatedAt: 'updatedAt',
      updatedByUserName: 'updatedByUserName',
      createdByUserName: 'createdByUserName',
      target: 'target',
      targetUriCopy: 'targetUriCopy',
      sportName: 'sportName',
      relUri: false,
      svgId: 'svgId',
    }];

    cmsService = {
      getHeaderSubMenu: jasmine.createSpy('getHeaderSubMenu').and.returnValue(of(headerSubMenu)),
      getFanzone: jasmine.createSpy('getFanzone').and.returnValue(of(fanzoneConfig)),
      isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true)),
    } as any;

    filtersService = {
      filterLink: jasmine.createSpy('filterLink').and.returnValue('lorem'),
    } as any;

    germanSupportService = {
      toggleItemsList: jasmine.createSpy('toggleItemsList').and.returnValue(headerSubMenu),
    };

    navigationService = {
      doRedirect: jasmine.createSpy('doRedirect'),
      sendToGTM: jasmine.createSpy('sendToGTM'),
      trackGTMEvent: jasmine.createSpy('trackGTMEvent'),
      openUrl: jasmine.createSpy('openUrl')
    } as any;

    user = {
      username: 'abc',
      status: true,
    };
    
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    }

    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName, channel, cb) => cb()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
      },
    } as any;

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    } as any;

    fanzoneStorageService = {
      get: jasmine.createSpy()
    }

    component = new HeaderSectionComponent(
      filtersService,
      cmsService,
      user,
      pubsub,
      germanSupportService,
      navigationService,
      changeDetectorRef,
      fanzoneStorageService,
      bonusSuppressionService
    );
  });

  describe('#ngOnInit', () => {
    it('should execute ngOnInit, and headerSubMenuIsExists should be truthy', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(germanSupportService.toggleItemsList).toHaveBeenCalledWith(headerSubMenu, 'filterRestrictedSports');
      expect(component.headerSubLinks).toEqual(headerSubMenu);
      expect(component.headerSubMenuIsExists).toBeTruthy();

      expect(pubsub.subscribe).toHaveBeenCalledWith('HeaderSectionComponent',
        [component['pubsub'].API.SESSION_LOGIN, component['pubsub'].API.SESSION_LOGOUT], jasmine.any(Function));
    }));

    it('should execute ngOnInit, and headerSubMenuIsExists should be falsy', fakeAsync(() => {
      germanSupportService.toggleItemsList.and.returnValue(of([]));
      expect(component.headerSubMenuIsExists).toBeFalsy();
    }));

  });

  it('#ngOnDestroy, should call unsubscribe', () => {
    component['unsubscribe'].next = jasmine.createSpy();
    component['unsubscribe'].complete = jasmine.createSpy();
    component.ngOnDestroy();

    expect(component['pubsub'].unsubscribe).toHaveBeenCalled();
    expect(component['unsubscribe'].next).toHaveBeenCalled();
    expect(component['unsubscribe'].complete).toHaveBeenCalled();
  });

  it('should filter headerdata', () => {
    component.fanzone = {
      active: true,
      fanzoneConfiguration: {
        sportsRibbon: true
      }
    } as any
    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({ teamName: 'Manchester',teamId:'fz00' }),
      set: jasmine.createSpy('set')
    };
    component['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'Manchester',teamId:'fz00'});
    spyOn<any>(component, 'filterLinks');
    germanSupportService.toggleItemsList.and.returnValue( [{targetUri: '/fanzone'},{targetUri: '/test'}] as any);
    component['filterHeaderData']();
    expect(component.headerSubLinks[0].disabled).toBeFalsy();
    expect(component.headerSubLinks[0].targetUri).toBe('/fanzone/vacation');
  });

  describe('getToURL', () => {
    it('should delegate url opening to service (inApp)', () => {
      component.goToURL('', true, '');

      expect(navigationService.openUrl).toHaveBeenCalledWith('', true);
    });

    it('should delegate url opening to service', () => {
      component.goToURL('foo', false, '');

      expect(navigationService.openUrl).toHaveBeenCalledWith('foo', false);
    });

    it('should delegate tracking to service (default action)', () => {
      component.goToURL('', true, 'title');

      expect(navigationService.trackGTMEvent).toHaveBeenCalledWith('header', 'title');
    });

    it('should delegate tracking to service (custom action)', () => {
      component.goToURL('', true, 'title', 'main');

      expect(navigationService.trackGTMEvent).toHaveBeenCalledWith('main', 'title');
    });
  });

  it('#trackByLink, should return link title', () => {
    expect(component.trackByLink(headerSubMenu[0])).toEqual(headerSubMenu[0].linkTitle);
  });

  it('#filterLinks, should set correct link', () => {
    component.headerSubLinks = [{} as any];

    component['filterLinks']();
    expect(component.headerSubLinks[0].targetUri).toBe(undefined);

    component.headerSubLinks = headerSubMenu;
    component.headerSubMenuIsExists = true;
    component['filterLinks']();
    expect(component.headerSubLinks[0].targetUri).toBe('lorem');
  });

  describe('#filterHeaderBasedOnRgyellow, should filterout headerlinks based on rgYellow status',() =>{
    it('filterHeaderBasedOnRgyellow should filter out links with rgYellow true', () =>{
      component.headerSubLinks = headerSubMenu;
      component.filterHeaderBasedOnRgyellow();
      expect(component.headerSubLinks).toEqual(headerSubMenu);
    })
  })
});
