import { of as observableOf, of } from 'rxjs';

import { SeoStaticBlockComponent } from '@lazy-modules/seoStaticBlock/components/seo-static-block.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SeoStaticBlockComponent', () => {
  let component: SeoStaticBlockComponent,
    pubSub,
    domSanitizer,
    seoAutomatedTagsService,
    rendererService,
    elementRef,
    domToolsService,
    windowRef,
    changeDetectorRef,
    deviceService,
    router;

  beforeEach(() => {
    domSanitizer = {
      sanitize: () => 'safeString',
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('sanitized')
    };
    pubSub = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync'),
      API: pubSubApi
    };
    seoAutomatedTagsService = {
      getPage: jasmine.createSpy('getPage').and.returnValue(of({}))
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(jasmine.any(Function))
      }
    };
    elementRef = {
      nativeElement : {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({}),
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{}])
        }])
      }
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      toggleVisibility: jasmine.createSpy('toggleVisibility')
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };
    deviceService = {};
    router = {
      events: {
        pipe: jasmine.createSpy('subscribe'),
        subscribe: jasmine.createSpy('subscribe'),
        url: '/'
      }
    };

    component = new SeoStaticBlockComponent(
      domSanitizer,
      pubSub,
      seoAutomatedTagsService,
      rendererService,
      elementRef,
      domToolsService,
      windowRef,
      changeDetectorRef,
      deviceService,
      router
    );
  });

  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      component['subscribeToRouterEvents'] = jasmine.createSpy();
      component['updateDOM'] = jasmine.createSpy('updateDOM').and.callThrough();
      component['addListeners'] = jasmine.createSpy('addListeners').and.callThrough();
      component.ngOnInit();

      expect(seoAutomatedTagsService.getPage).toHaveBeenCalled();
      expect(pubSub.subscribe).toHaveBeenCalledWith(
        'seoStaticBlockComponent',
        pubSub.API.SEO_DATA_UPDATED,
        component['updateDOM']
      );
      expect(component['addListeners']).toHaveBeenCalled();
    });

    it('isExpanded false, isDesktop is false', () => {
      component['subscribeToRouterEvents'] = jasmine.createSpy();
      component.isExpanded = false;
      deviceService.isDesktop = false;

      component.ngOnInit();

      expect(component.isExpanded).toEqual(false);
    });

    it('isExpanded true, isDesktop is true', () => {
      component['subscribeToRouterEvents'] = jasmine.createSpy();
      component.isExpanded = false;
      deviceService.isDesktop = true;

      component.ngOnInit();

      expect(component.isExpanded).toEqual(true);
    });
  });

  it('ngOnDestroy', () => {
    component['routeChangeSuccessHandler'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['routeChangeSuccessHandler'].unsubscribe).toHaveBeenCalled();
    expect(pubSub.unsubscribe).toHaveBeenCalledWith('seoStaticBlockComponent');
    expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
  });

  it('subscribeToRouterEvents', fakeAsync(() => {
    router.events = observableOf(new NavigationEnd(0, '', ''));
    component['subscribeToRouterEvents']();

    tick();

    expect(component.seoStaticBlockContent).toBeFalsy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  }));
  
  describe('@updateDOM', () => {
    let data;

    beforeEach(() => {
      data = {
        staticBlock: 'staticBlock'
      };
      component['addListeners'] = jasmine.createSpy('addListeners').and.callThrough();
    });

    it('should add static block content', () => {
      component['updateDOM'](data);

      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith(data.staticBlock);
    });

    it('should not add static block content', () => {
      data.staticBlock = '';

      component['updateDOM'](data);

      expect(domSanitizer.bypassSecurityTrustHtml).not.toHaveBeenCalled();
    });
    it('should get default title if staticBlockTitle is empty', () => {
      data.staticBlockTitle = '';
      component['updateDOM'](data);
      expect(component.seoPageTitleBlock).toBe('SPORTS BETTING ONLINE');
    });

    it('should get default title if staticBlockTitle is not empty', () => {
      data.staticBlockTitle = 'SeoConfigured';
      component['updateDOM'](data);
      expect(component.seoPageTitleBlock).toBe('SeoConfigured');
    });

    afterEach(() => {
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
      expect(component['addListeners']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(1);
    });
  });

  describe('@addListeners', () => {
    it('should add listener to handle expand/collapse panel', () => {
      rendererService.renderer.listen.and.callFake((a, b, cb) => {
        cb();
      });
      component['addListeners']();

      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.page-container');
      expect(rendererService.renderer.listen).toHaveBeenCalled();
      expect(domToolsService.toggleClass).toHaveBeenCalled();
      expect(domToolsService.toggleVisibility).toHaveBeenCalled();
    });
  });
});
