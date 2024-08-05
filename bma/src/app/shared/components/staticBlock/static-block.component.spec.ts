import { StaticBlockComponent } from '@shared/components/staticBlock/static-block.component';
import { IStaticBlock } from '@core/services/cms/models';
import { of as observableOf, throwError } from 'rxjs';

describe('StaticBlockComponent', () => {
  let cmsService,
    locale,
    storageService,
    elementRef,
    domToolsService,
    rendererService,
    domSanitizer,
    router,
    windowRef,
    changeDetectorRef,
    component: StaticBlockComponent;

  beforeEach(() => {
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(observableOf({})),
      parseContent: jasmine.createSpy('parseContent')
    };
    locale = {
      getLocale: jasmine.createSpy('getLocale').and.returnValue('')
    };
    storageService = {
      get: jasmine.createSpy('get')
    };
    elementRef = {
      nativeElement: {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{}])
        }])
      }
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      toggleVisibility: jasmine.createSpy('toggleVisibility')
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
        listen: jasmine.createSpy('listen').and.returnValue(jasmine.any(Function))
      }
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn())
      }
    } as any;
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new StaticBlockComponent(
      cmsService,
      locale,
      storageService,
      elementRef,
      domToolsService,
      rendererService,
      domSanitizer,
      router,
      windowRef,
      changeDetectorRef
    );
    component.service = 'service';
    component.params = '';
    component.expand = false;
    component.removeContainer = false;
    component.loader = false;
    component.cmsContent = {} as IStaticBlock;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.state.loading).toBe(true);
    expect(component.state.error).toBe(false);
    expect(component.isUsedFromWidget).toBe(false);
  });

  it('setHtml: should parse html content for acca insurance text', () => {
    component.service = 'acca-notification';
    component['setHtml']({ htmlMarkup: 'htmlMarkup'} as IStaticBlock);

    expect(cmsService.parseContent).toHaveBeenCalledWith('htmlMarkup', '');
  });

  describe('ngOnInit', () => {
    it('should hide spinner if there is cmsContent', () => {
      component.cmsContent = { htmlMarkup: 'htmlMarkup'} as any;
      component.ngOnInit();
      expect(component.state.loading).toEqual(false);
    });

    it('no cmsContent content', () => {
      component.cmsContent = undefined;
      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('service', '');
      expect(component.state.loading).toEqual(false);
      expect(component.cmsContent).toEqual({} as any);
    });

    it('cmsContent content', () => {
      const cmsContent = { htmlMarkup: 'htmlMarkup' } as any;

      cmsService.getStaticBlock = jasmine.createSpy('getStaticBlock').and.returnValue(observableOf(cmsContent));
      component.cmsContent = undefined;
      component['setHtml'] = jasmine.createSpy('setHtml').and.callThrough();

      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('service', '');
      expect(component.state.loading).toEqual(false);
      expect(component.cmsContent).toEqual(cmsContent);
      expect(component['setHtml']).toHaveBeenCalledWith(cmsContent);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('fail case', () => {
      component.cmsContent = undefined;
      cmsService.getStaticBlock.and.returnValue(throwError('error'));
      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('service', '');
      expect(component.state.error).toBeTruthy();
    });

    it('no cmsContent content, loading = true ', () => {
      spyOn(console, 'warn');
      component.service = '';
      component.cmsContent = undefined;

      component.ngOnInit();

      expect(cmsService.getStaticBlock).not.toHaveBeenCalled();
      expect(component.state.loading).toEqual(true);
      expect(console.warn).toHaveBeenCalledWith('Incorrect usage of staticBlock directive.');
    });
  });

  describe('@replaceHref', () => {
    it('should return empty string', () => {
      expect(component.replaceHref(undefined)).toEqual('');
    });

    it('should replace href with data-routerlink', () => {
      const inputHtml = '<a href="../some-url"></a>';
      const result = '<a data-routerlink="some-url"></a>';

      expect(component.replaceHref(inputHtml)).toEqual(result);
    });
  });

  describe('@checkRedirect', () => {
    let event;

    beforeEach(() => {
      event = {
        target: {
          dataset: {
            routerlink: 'routerlink'
          }
        }
      } as any;
    });

    it('should redirect', () => {
      component.checkRedirect(event);

      expect(router.navigateByUrl).toHaveBeenCalledWith(event.target.dataset.routerlink);
    });

    it('should not redirect', () => {
      event.target.dataset.routerlink = '';
      component.checkRedirect(event);

      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });
  });

  describe('@setHtml', () => {
    beforeEach(() => {
      rendererService.renderer.listen.and.callFake((a, b, cb) => {
        cb();
      });
    });

    it('bronzeLevel = true', () => {
      component['bronzeLevel'] = true;

      component['setHtml']({} as any);

      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.normalMail, .normalTel');
      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.bronzeLevelTel, .bronzeLevelMail');
      expect(rendererService.renderer.addClass).toHaveBeenCalledTimes(1);
    });

    it('silverGoldPlatinumLevel = true', () => {
      component['silverGoldPlatinumLevel'] = true;

      component['setHtml']({} as any);

      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.normalMail, .normalTel');
      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.silverGoldPlatinumLevelTel, .silverGoldPlatinumLevelMail');
      expect(rendererService.renderer.addClass).toHaveBeenCalledTimes(1);
    });

    afterEach(() => {
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 500);
      expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('.page-container');
      expect(rendererService.renderer.listen).toHaveBeenCalled();
      expect(domToolsService.toggleClass).toHaveBeenCalled();
      expect(domToolsService.toggleVisibility).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      spyOn(component as any, 'setHtml').and.callThrough();
    });

    it('should set html', () => {
      component.cmsContent = { htmlMarkup: 'html' } as any;
      component.ngOnChanges({ cmsContent: { currentValue: { htmlMarkup: 'html' } } } as any);
      expect(component['setHtml']).toHaveBeenCalled();
    });

    it('should not set html', () => {
      component.cmsContent = null;
      component.ngOnChanges({} as any);
      expect(component['setHtml']).not.toHaveBeenCalled();
    });
  });
});
