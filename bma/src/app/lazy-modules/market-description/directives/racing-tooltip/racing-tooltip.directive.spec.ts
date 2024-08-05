import { RacingTooltipDirective } from './racing-tooltip.directive';

describe('RacingTooltipDirective', () => {
  let directive: RacingTooltipDirective,
   element,
   rendererService,
   resolver,
   vcr,
   locale,
   storageService,
   gtmService;

  beforeEach(() => {
    element = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };

    rendererService = {
      renderer: {
        createText: jasmine.createSpy('renderer.createText')
      }
    };

    resolver = {
      resolveComponentFactory: jasmine.createSpy('resolver.resolveComponentFactory')
    };

    vcr = {
      createComponent: jasmine.createSpy('vcr.createComponent')
    };

    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('welcome')
    };

    storageService = {
        get: jasmine.createSpy('get').and.returnValue(true),
        set: jasmine.createSpy('set')
    } as any;

    directive = new RacingTooltipDirective(
      element,
      rendererService,
      resolver,
      vcr,
      locale,
      storageService,
      gtmService
    );
  });

  describe('#ngOnInit', () => {
    it('should call display tooltip', () => {
      directive.isTooltipSeen.emit = jasmine.createSpy('modelChangeHandler.emit');
      spyOn(directive as any, 'validateTooltip').and.returnValue(true);
      spyOn(directive as any, 'displayTooltip');

      directive.ngOnInit();
      expect(directive.displayTooltip).toHaveBeenCalled();
    });
    it('should not call display tooltip', () => {
      directive.isTooltipSeen.emit = jasmine.createSpy('modelChangeHandler.emit');
      spyOn(directive as any, 'validateTooltip').and.returnValue(false);
      spyOn(directive as any, 'displayTooltip');

      directive.ngOnInit();
      expect(directive.displayTooltip).not.toHaveBeenCalled();
    });
  });

  describe('#generateNgContent', () => {
    it('should proceed based on the type', () => {
      directive.racingTooltip = 'test tooltip';
      directive.generateNgContent();
      expect(locale.getString).toHaveBeenCalledWith('app.tooltip.test tooltip', undefined);
      expect(rendererService.renderer.createText).toHaveBeenCalled();
    });
    it('should not proceed based on the type', () => {
      directive.racingTooltip = {} as any;
      directive.generateNgContent();
      expect(locale.getString).not.toHaveBeenCalled();
    });
  });

  it('ngOnDestroy', () => {
    spyOn(directive, 'destroy');
    directive.ngOnDestroy();

    expect(directive.destroy).toHaveBeenCalled();
  });

  it('displayTooltip', () => {
    directive.displayTooltip();

    expect(resolver.resolveComponentFactory).toHaveBeenCalled();
    expect(vcr.createComponent).toHaveBeenCalled();
  });

  describe('#validateTooltip', () => {
    it('should show tooltip if the condition satisfy', () => {
      const marketContainer = {
        clientWidth: 22
      } as HTMLElement;
      spyOn(directive as any, 'getInnerWidth').and.returnValue(25);
      spyOn(directive as any, 'showHideToolTip').and.returnValue(true);
      const response = directive['validateTooltip'](marketContainer);
      expect(response).toBe(true);
    });
    it('should not show tooltip if both the conditions does not satisfy', () => {
      const marketContainer = null;
      spyOn(directive as any, 'getInnerWidth').and.returnValue(25);
      spyOn(directive as any, 'showHideToolTip').and.returnValue(true);
      const response = directive['validateTooltip'](marketContainer);
      expect(response).toBe(undefined);
    });
    it('should not show tooltip if only one condition satisfy', () => {
      const marketContainer = {
        clientWidth: 22
      } as HTMLElement;
      spyOn(directive as any, 'getInnerWidth').and.returnValue(21);
      spyOn(directive as any, 'showHideToolTip').and.returnValue(true);
      const response = directive['validateTooltip'](marketContainer);
      expect(response).toBe(undefined);
    });
  });

  describe('#getInnerWidth', () => {
    it('should return scroll width if marketContainer exists', () => {
      const marketContainer = {
        children: [{
          scrollWidth: 25
        }]
      } as any;
      const response = directive['getInnerWidth'](marketContainer);
      expect(response).toBe(25);
    });
    it('should return scroll width 0 if marketContainer does not exists', () => {
      const marketContainer = null;
      const response = directive['getInnerWidth'](marketContainer);
      expect(response).toBe(0);
    });
  });

  describe('#showHideToolTip', () => {
    it('should return true if tooltip is not present in local storage', () => {
      storageService.get.and.returnValue(null);
      const response = directive['showHideToolTip']();
      expect(response).toBe(true);
    });
    it('should return false if tooltip is present in local storage', () => {
      const response = directive['showHideToolTip']();
      expect(response).toBe(false);
    });
  });
});
