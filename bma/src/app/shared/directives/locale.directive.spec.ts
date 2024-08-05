import { LocaleDirective } from '@shared/directives/locale.directive';
import { fakeAsync, tick } from '@angular/core/testing';
import { BehaviorSubject } from 'rxjs';

describe('LocaleDirective', () => {
  let directive: LocaleDirective;
  let rendererService;
  let element;
  let localeService;
  beforeEach(() => {
    rendererService = {
      renderer: {
        setProperty: jasmine.createSpy('setProperty')
      }
    };
    element = {
      nativeElement: {}
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(str => str),
      isTranslationModuleLoaded: {
        value: true
      }
    };
  });

  it('should create an instance', () => {
    directive = new LocaleDirective(rendererService, element, localeService);

    expect(directive).toBeTruthy();
  });

  it('should create an instance', () => {
    directive = new LocaleDirective(rendererService, element, localeService);

    expect(directive).toBeTruthy();
  });

  it('ngOnInit', () => {
    directive = new LocaleDirective(rendererService, element, localeService);
    spyOn(directive, 'render');
    directive.ngOnInit();

    expect(directive.render).toHaveBeenCalled();
  });

  it('ngOnChanges', () => {
    directive = new LocaleDirective(rendererService, element, localeService);
    spyOn(directive, 'render');
    directive.ngOnChanges();

    expect(directive.render).toHaveBeenCalled();
  });

  it('render', () => {
    directive = new LocaleDirective(rendererService, element, localeService);
    directive.i18n = 'some.property';
    directive.render();

    expect(localeService.getString).toHaveBeenCalledWith(directive.i18n, directive.i18nArgs);
    expect(rendererService.renderer.setProperty).toHaveBeenCalledWith(element.nativeElement, 'innerHTML', directive.i18n);
  });

  it('should not re-render on subject error', fakeAsync(() => {
    localeService.isTranslationModuleLoaded = new BehaviorSubject(false);
    directive = new LocaleDirective(rendererService, element, localeService);
    spyOn(directive, 'render');
    localeService.isTranslationModuleLoaded.error();

    tick();

    expect(directive.render).not.toHaveBeenCalled();
  }));

  it('should re-render on subject complete', fakeAsync(() => {
    localeService.isTranslationModuleLoaded = new BehaviorSubject(false);
    directive = new LocaleDirective(rendererService, element, localeService);
    spyOn(directive, 'render');
    localeService.isTranslationModuleLoaded.complete();

    tick();

    expect(directive.render).toHaveBeenCalled();
  }));

  it('should not subscribe on loading translation subject', () => {
    localeService.isTranslationModuleLoaded = {
      value: true,
      subscribe: jasmine.createSpy()
    };
    directive = new LocaleDirective(rendererService, element, localeService);

    expect(localeService.isTranslationModuleLoaded.subscribe).not.toHaveBeenCalled();
  });

  it('should subscribe on loading translation subject', () => {
    localeService.isTranslationModuleLoaded = {
      value: false,
      subscribe: jasmine.createSpy()
    };
    directive = new LocaleDirective(rendererService, element, localeService);

    expect(localeService.isTranslationModuleLoaded.subscribe).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(str => str),
      isTranslationModuleLoaded: {
        value: false,
        subscribe: () => ({ unsubscribe: jasmine.createSpy() })
      }
    };
    directive = new LocaleDirective(rendererService, element, localeService);
    directive.ngOnDestroy();

    expect(directive['translationModuleLoadedSub'].unsubscribe).toHaveBeenCalled();
  });
});
