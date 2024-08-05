import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BetslipDigitKeyboardDirective } from './betslip-digit-keyboard.directive';

describe('BetslipDigitKeyboardDirective', () => {
  let directive: BetslipDigitKeyboardDirective;

  let pubSubService;
  let windowRefService;
  let rendererService;
  let dkComponent;

  beforeEach(() => {
    pubSubService = {
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callThrough(),
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy().and.returnValue({
          offsetHeight: 10
        })
      },
      nativeWindow: {
        innerHeight: 100
      }
    };
    rendererService = {
      renderer: {
        removeAttribute: jasmine.createSpy(),
        setStyle: jasmine.createSpy()
      }
    };
    dkComponent = <any>{
      enterKey: '',
      keyboardKeys: [''],
      quickStakeKeys: ['']
    };

    directive = new BetslipDigitKeyboardDirective(
      pubSubService,
      windowRefService,
      rendererService,
      dkComponent
    );
  });

  describe('ngAfterViewInit', () => {
    it('should init keys', () => {
      directive.ngAfterViewInit();
      expect(directive['enterKey']).toEqual(<any>'');
      expect(directive['keyboardKeys']).toEqual(<any>['']);
      expect(directive['quickStakeKeys']).toEqual(<any>['']);
    });

    it('should not init keys', () => {
      directive['dkComponent'] = null;
      directive.ngAfterViewInit();
      expect(directive['enterKey']).toBeUndefined();
      expect(directive['keyboardKeys']).toBeUndefined();
      expect(directive['quickStakeKeys']).toBeUndefined();
    });
  });

  it('ngOnDestroy', () => {
    directive.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('betslipDigitKeyboardDirective');
  });

  describe('ngOnInit', () => {
    it('should subscribe to keyboard events', () => {
      directive.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'betslipDigitKeyboardDirective',
        pubSubApi.DIGIT_KEYBOARD_SHOWN,
        jasmine.anything()
      );
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'betslipDigitKeyboardDirective',
        pubSubApi.DIGIT_KEYBOARD_HIDDEN,
        jasmine.anything()
      );
    });

    it('should not subscribe to keyboard events', () => {
      directive['dkComponent'] = null;
      directive.ngOnInit();
      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });
  });

  it('clearInlineStyle', () => {
    directive['clearInlineStyle'](<any>{
      nativeElement: {}
    });

    expect(rendererService.renderer.removeAttribute).toHaveBeenCalledWith({}, 'style');
  });

  it('getBsElementsHeight', () => {
    expect(directive['getBsElementsHeight']()).toEqual(50);

    windowRefService.document.querySelector.and.returnValue(null);
    expect(directive['getBsElementsHeight']()).toEqual(0);
  });

  it('setElementHeight', () => {
    directive['setElementHeight'](50, <any>{
      nativeElement: {}
    });
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'height', '50px');
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'line-height', '50px');
  });

  it('hideKeyboard', () => {
    directive.ngAfterViewInit();
    directive['enterKey'] = <any>{
      nativeElement: {}
    };
    directive['hideKeyboard']();
    expect(rendererService.renderer.removeAttribute).toHaveBeenCalledTimes(3);
  });

  describe('showKeyboard', () => {
    it('should not set element height (window height lower than allowed height)', () => {
      windowRefService.nativeWindow.innerHeight = 700;
      directive['showKeyboard'](true, true);
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });

    it('should not set element height (no available height)', () => {
      windowRefService.document.querySelector.and.returnValue({ offsetHeight: -50 });
      directive['showKeyboard'](false, false);
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });

    it('should not set element height (no elements)', () => {
      directive['enterKey'] = null;
      directive['keyboardKeys'] = null;
      directive['quickStakeKeys'] = null;
      directive['showKeyboard'](false, false);
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });

    it('should set elements height', () => {
      directive['enterKey'] = {} as any;
      directive['keyboardKeys'] = [{}] as any;
      directive['quickStakeKeys'] = [{}] as any;
      directive['showKeyboard'](true, true);
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(6);
    });
  });
});
