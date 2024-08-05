import { VisIframeDimensionsDirective } from './vis-iframe-dimensions.directive';

describe('VisIframeDimensionsDirective', () => {
  let directive: VisIframeDimensionsDirective;
  let elementRef;
  let rendererService;
  let windowRef;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue('iframe'),
        parentNode: {
          offsetWidth: 375
        }
      }
    };
    rendererService = {
      renderer: {
        setStyle: jasmine.createSpy('setStyle'),
        listen: jasmine.createSpy('listen')
      }
    };

    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };

    directive = new VisIframeDimensionsDirective(windowRef, elementRef, rendererService);
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it(`should set height = 0 to container`, () => {
      directive.ngOnInit();

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(directive['container'], 'height', '0');
      expect(directive.dimensionMultiplier).toEqual(0.625);
    });

    it(`should set listener on iframe 'load'`, () => {
      directive.visType = 'castro';
      directive.ngOnInit();

      expect(rendererService.renderer.listen['calls'].argsFor(0)).toEqual([directive['iframe'], 'load', jasmine.any(Function)]);
      expect(directive.dimensionMultiplier).toEqual(0.29);
    });

    it(`should set listener on nativeWindow 'orientationchange'`, () => {
      directive.ngOnInit();

      expect(rendererService.renderer.listen['calls'].argsFor(2))
        .toEqual([windowRef.nativeWindow, 'orientationchange', jasmine.any(Function)]);
    });

    afterEach(() => {
      expect(directive['container']).toEqual(elementRef.nativeElement);
      expect(directive['iframe'] as any).toEqual('iframe');
      expect(directive['delta']).toEqual(null);
    });
  });

  describe('resizeFrame', () => {
    beforeEach(() => {
      directive['iframe'] = {} as any;
      directive['container'] = {} as any;
      directive.dimensionMultiplier = 1;
    });

    it('should resize with 0 delta', () => {
      directive['resizeFrame']();

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'width', '375px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '375px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '375px');
    });

    it('should resize with delta equal 1', () => {
      directive.visDelta = 1;
      directive['resizeFrame']();

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'width', '375px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '376px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '376px');
    });

    it('should resize without offset width', () => {
      elementRef.nativeElement.parentNode.offsetWidth = 0;
      directive['resizeFrame']();

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'width', '0px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '100%px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '100%px');
    });

    afterEach(() => {
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
  });

  it('onResizeBind', () => {
    directive['onResizeBind']();
    expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 700);
  });

  it('ngOnDestroy', () => {
    directive['loadHandler'] = () => {
    };
    directive['resizeHandler'] = () => {
    };
    directive['orientationChangeHandler'] = () => {
    };
    directive['ngOnDestroy']();
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(directive['container'], 'height', '0');
  });
});
