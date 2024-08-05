import { of as observableOf, of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { HeaderSectionComponent } from './header-section.component';
import { IHeaderSubMenu } from '@core/services/cms/models';

describe('CDHeaderSectionComponent', () => {
  let component: HeaderSectionComponent;

  const headerSubMenu: IHeaderSubMenu[] = [{
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
  },{
    disabled: false,
    id: "5f199427c9e77c00012b94b9",
    inApp: true,
    linkTitle: "Racing Super Serie",
    targetUri: "https://racingsuperseries.coral.co.uk/en",
    lang: 'lang',
    linkTitle_brand: 'linkTitle_brand',
    sortOrder: 0,
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

  const cmsService = {
    getHeaderSubMenu: () => observableOf(headerSubMenu),
    getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
  } as any;

  const filtersService = {
    filterLink: jasmine.createSpy('filterLink').and.returnValue(headerSubMenu[0].targetUri),
  } as any;

  const navigationService = {
    doRedirect: jasmine.createSpy('doRedirect'),
    sendToGTM: jasmine.createSpy('doRedirect'),
    openUrl: jasmine.createSpy('openUrl'),
    trackGTMEvent: jasmine.createSpy('trackGTMEvent')
  } as any;

  const pubsub = {
    subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName, channel, cb) => cb()),
    unsubscribe: jasmine.createSpy('unsubscribe'),
    API: {
      SESSION_LOGIN: 'SESSION_LOGIN',
      SESSION_LOGOUT: 'SESSION_LOGOUT',
    },
  } as any;

  const changeDetectorRef = {
    detectChanges: jasmine.createSpy('detectChanges'),
  } as any;

  const bonusSuppressionService = {
    checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
  } as any;

  beforeEach(() => {

    component = new HeaderSectionComponent(
      filtersService,
      cmsService,
      navigationService,
      pubsub,
      changeDetectorRef,
      bonusSuppressionService
    );

  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should execute ngOnInit, and headerSubMenuIsExists should be truthy', fakeAsync(() => {
      component['filterLinks'] = jasmine.createSpy('filterLinks');
      component['filterHeaderBasedOnRgyellow'] = jasmine.createSpy('filterHeaderBasedOnRgyellow');
      component.ngOnInit();

      component['cmsService'].getHeaderSubMenu()
      .subscribe((data: IHeaderSubMenu[]) => {
        expect(data).toEqual(headerSubMenu);
        tick(10);
        expect(component['filterLinks']).toHaveBeenCalled();
        expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
      });

      component['pubsub']
      .subscribe('HeaderSectionComponent',
        [component['pubsub'].API.SESSION_LOGIN, component['pubsub'].API.SESSION_LOGOUT], () => {
          expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
          expect(component['filterHeaderBasedOnRgyellow']).toHaveBeenCalled();
        });
        tick(10);
      expect(component.headerSubLinks).toEqual(headerSubMenu);
      expect(component.headerSubMenuIsExists).toBeTruthy();
    }));

    it('should execute ngOnInit, and headerSubMenuIsExists should be falsy', () => {
      component['cmsService'] = {
        getHeaderSubMenu: () => observableOf([]),
        getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
      } as any;
      component.ngOnInit();

      expect(component.headerSubMenuIsExists).toBeFalsy();
    });

  });

  it('#ngOnDestroy, should call unsubscribe', () => {
    component['unsubscribe'].next = jasmine.createSpy();
    component['unsubscribe'].complete = jasmine.createSpy();
    component.ngOnDestroy();

    expect(component['pubsub'].unsubscribe).toHaveBeenCalled();
    expect(component['unsubscribe'].next).toHaveBeenCalled();
    expect(component['unsubscribe'].complete).toHaveBeenCalled();
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

  it('#filterLinks, should set correct link', () => {
    component.headerSubLinks = [{} as any];

    component['filterLinks']();
    expect(component.headerSubLinks[0].targetUri).toBe(undefined);

    component.headerSubLinks = headerSubMenu;
    component.headerSubMenuIsExists = true;
    component['filterLinks']();
    expect(component.headerSubLinks[0].targetUri).toBe('targetUri');
  });

  describe('#filterHeaderBasedOnRgyellow, should filterout headerlinks based on rgYellow status',() =>{
    it('filterHeaderBasedOnRgyellow should filter out links with rgYellow true', () =>{
      component.headerSubLinks = headerSubMenu;
      component.filterHeaderBasedOnRgyellow();
      expect(component.headerSubLinks).toEqual(headerSubMenu);
    })
  });
});

