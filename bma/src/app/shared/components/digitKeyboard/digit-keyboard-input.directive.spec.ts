import { DigitKeyboardInputDirective } from '@shared/components/digitKeyboard/digit-keyboard-input.directive';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('DigitKeyboardInputDirective', () => {
  let directive: DigitKeyboardInputDirective,
    pubSubService,
    deviceService,
    gtmService,
    domToolsService,
    rendererService,
    elementRef,
    windowRefService,
    coreToolsService,locale,betslipService,
    event;
  let element;

  beforeEach(() => {
    element = {
      style: {},
      appendChild: jasmine.createSpy(),
      querySelector: jasmine.createSpy(),
      querySelectorAll: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, fn) => { fn(''); }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync')
    };
    deviceService = {
      isMobileOnly: true,
      isIos: false,
      isWrapper: false
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    rendererService = {
      renderer: {
        setAttribute: jasmine.createSpy('setAttribute'),
        removeAttribute: jasmine.createSpy('removeAttribute'),
        removeClass: jasmine.createSpy('removeClass'),
        listen: jasmine.createSpy('listen'),
        addClass: jasmine.createSpy('addClass'),
        setProperty: jasmine.createSpy('setProperty')
      }
    };
    domToolsService = {
      isChild: jasmine.createSpy().and.returnValue(true),
      getOffset: jasmine.createSpy('getOffset').and.returnValue({}),
      getHeight: jasmine.createSpy('getHeight'),
      getScrollTop: jasmine.createSpy('getScrollTop'),
      closest: jasmine.createSpy('closest').and.returnValue(element)
    };
    elementRef = {
      nativeElement: {
        parentElement: {
          classList: {
            contains: jasmine.createSpy().and.returnValue(true)
          }
        },
        classList: {
          contains: jasmine.createSpy().and.returnValue(true)
        },
        id : '1'
      }
    };
    coreToolsService = {
      uuid: jasmine.createSpy().and.returnValue('xxxx-xxx-xxxx')
    };
    windowRefService = {
      nativeWindow: {
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy(),
        setTimeout: jasmine.createSpy()
      },
      document: {
        getElementById: jasmine.createSpy().and.returnValue(element),
        querySelector: jasmine.createSpy().and.returnValue(element),
        querySelectorAll: jasmine.createSpy().and.returnValue(element),
      }
    };
    event = {
      preventDefault: jasmine.createSpy(),
      stopPropagation: jasmine.createSpy(),
      target: {
        blur: jasmine.createSpy()
      }
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('TEST'),
    }
    betslipService={
      filterKyeBoardData:jasmine.createSpy('filterKyeBoardData'),
      betKeyboardData:['test']

    }
    directive = new DigitKeyboardInputDirective(
      pubSubService,
      deviceService,
      gtmService,
      domToolsService,
      rendererService,
      elementRef,
      windowRefService,
      coreToolsService,locale,betslipService
  );
  });

  it('should be instantiated', () => {
    expect(directive).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it(`'shouldInit' should be truthy if Not showOnDesktop and is isMobileOnly`, () => {
      directive.ngOnInit();

      expect(directive['shouldInit']).toBeTruthy();
    });

    it(`'shouldInit' should be falthy if Not showOnDesktop and is Not isMobileOnly`, () => {
      directive['isMobileOnly'] = false;

      directive.ngOnInit();

      expect(directive['shouldInit']).toBeFalsy();
    });

    it(`should 'shouldInit' be truthy if showOnDesktop`, () => {
      directive['showOnDesktop'] = true;

      directive.ngOnInit();

      expect(directive['shouldInit']).toBeTruthy();
    });

    it(`should return if 'shouldInit' is falthy`, () => {
      directive['isMobileOnly'] = false;

      directive.ngOnInit();

      expect(directive.hostType).toEqual('tel');
    });

    it('should set special flag on element', () => {
      directive.ngOnInit();

      expect(rendererService.renderer.setAttribute).toHaveBeenCalledWith(jasmine.any(Object), 'data-has-keyboard', 'true');
    });
  });

  it('should be ngOnInit', () => {
    directive.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  describe('onClickHandler', () => {
    it(`should return if 'shouldInit' is falthy`, () => {
      spyOn(directive as any, 'validateValue');

      directive.onClickHandler(event);

      expect(directive['validateValue']).not.toHaveBeenCalled();
    });

    it('should listen for clicks on parent container (subscribeOnMainElementTouchEvent)', () => {
      pubSubService.subscribe.and.stub();
      directive.ngOnInit();
      directive.ngAfterViewInit();
      directive.onClickHandler(event);
      expect(rendererService.renderer.listen).toHaveBeenCalledWith(element, 'click', jasmine.any(Function));
    });

    it('should close sideOutBetslip Balance DropDown', () => {
      directive['shouldInit'] = true;
      pubSubService.subscribe.and.stub();

      directive.onClickHandler(event);

      expect(pubSubService.publish).toHaveBeenCalledWith('BETSLIP_BALANCE_DROPDOWN_HIDE');
    });

    it('placeholder, stake', () => {
      directive['shouldInit'] = true;
      directive['mainElement'] = <any>{
        querySelectorAll: jasmine.createSpy().and.returnValue([{
          removeClass: jasmine.createSpy(),
          id: 'id',
          attributes: {'data-uuid': 'ABC-123'}
        }])
      };
      directive.onClickHandler(event);
      expect(rendererService.renderer.setAttribute).toHaveBeenCalled();
    });

    it('should publish BS_HIDE_FREEBET_TOOLTIP', () => {
      event.isTrusted = true;
      directive['shouldInit'] = true;
      directive.onClickHandler(event);
      expect(directive['stakeClickHandlerInProgressFlag']).toBeTruthy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.BS_HIDE_FREEBET_TOOLTIP);
    });
  });

  describe('ngOnChanges', () => {
    it(`should return if 'shouldInit' is falthy`, () => {
      spyOn(directive as any, 'whenViewReady').and.returnValue(() => {});

      directive.ngOnChanges({ disabled: true } as any);

      expect(directive['whenViewReady']).not.toHaveBeenCalled();
    });

    it(`should not return if 'shouldInit' is falthy`, () => {
      spyOn(directive as any, 'whenViewReady').and.returnValue(() => {});
      directive['shouldInit'] = true;

      directive.ngOnChanges({ disabled: true } as any);

      expect(directive['whenViewReady']).toHaveBeenCalled();
    });
  });

  describe('ngAfterViewInit', () => {
    it(`should return if 'shouldInit' is falthy`, () => {
      spyOn(directive['isInit'] as any, 'emit');

      directive.ngAfterViewInit();

      expect(directive['isInit'].emit).toHaveBeenCalledWith(false);
    });
  });

  describe('ngOnDestroy', () => {
    it(`should return if 'shouldInit' is falthy`, () => {
      spyOn(directive['isInit'] as any, 'emit');

      directive.ngOnDestroy();

      expect(directive['isInit'].emit).not.toHaveBeenCalled();
    });

    it(`should unsubscribe quikStateUuid`, () => {
      spyOn(directive['isInit'] as any, 'emit');
      directive['shouldInit'] = true;
      directive.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(`DigitKeyboardInputDirective-xxxx-xxx-xxxx`);
    });
  });

  describe('setFreeBetSelectedValue', () => {
    it('should set selected free bet field and emit freebetselected event', ()=>{
      spyOn(directive['freeBetSelected'] as any, 'emit');
      const event = {
        output: "free bet1",
        value: "1.00"
      };
      directive['setFreeBetSelectedValue'](event);
      expect(directive['freeBetSelected'].emit).toHaveBeenCalledWith(event);
    });
  });

  describe('disableKeyboard', () => {
    it(`disabled = true`, () => {
      directive['disableKeyboard'](true);
      expect(pubSubService.publish).toHaveBeenCalledWith('DIGIT_KEYBOARD_HIDDEN', directive.componentId);
    });

    it(`disabled = false`, () => {
      directive['disableKeyboard'](false);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('should validate value on quick-stake button pressed', () => {
    directive['validateValue'] = jasmine.createSpy('validateValue');
    directive.ngOnInit();

    expect(directive['isEdited']).toBeFalsy();
    expect(directive['validateValue']).toHaveBeenCalled();
  });

  afterEach(() => {
    directive = null;
  });

  describe('@whenViewReady', () => {
    it('should return function', () => {
      const cb = jasmine.createSpy('whenViewReadyCb');
      const res = directive['whenViewReady'](cb);
      expect(res).toEqual(jasmine.any(Function));
    });

    it('should call callback', fakeAsync(() => {
      const cb = jasmine.createSpy('whenViewReadyCb');
      directive['whenViewReady'](cb)();
      directive['viewReady$'].complete();
      tick();
      expect(cb).toHaveBeenCalled();
    }));
  });

  describe('@bindElements', () => {
    it('should bind elements', () => {
      directive['keyboardElement'] = null;
      directive['qsElement'] = null;
      directive['bindElements']();
      expect(directive['keyboardElement']).not.toBeNull();
      expect(directive['qsElement']).not.toBeNull();
    });
  });

  describe('@handleNumber', () => {
    it('should return if maxlength', () => {
      directive.ngModelChange.emit = jasmine.createSpy('emit');
      directive.maxLength = 5;
      directive['isEdited'] = true;
      directive['currentValueLength'] = 5;

      directive['handleNumber']('123123');
      expect(directive.ngModelChange.emit).not.toHaveBeenCalled();
    });
  });

  describe('@onKeyBoardPressHandler', () => {
    beforeEach(() => {
      directive['handleNumber'] = jasmine.createSpy('handleNumber');
    });
    it('should handle keyboard click for active input', () => {
      directive['onKeyBoardPressHandler']('9');

      expect(directive['handleNumber']).toHaveBeenCalledWith('9');
    });

    it('should not handle keyboard click for active input', () => {
      elementRef.nativeElement.parentElement.classList.contains.and.returnValue(false);
      elementRef.nativeElement.classList.contains.and.returnValue(false);

      directive['onKeyBoardPressHandler']('qb');

      expect(directive['handleNumber']).not.toHaveBeenCalledWith('qb');
    });

    it('should not handle keyboard click QB', () => {
      elementRef.nativeElement.parentElement.classList.contains.and.returnValue(true);
      elementRef.nativeElement.classList.contains.and.returnValue(true);
      directive['handleQDButton'] = jasmine.createSpy('handleQDButton');

      directive['onKeyBoardPressHandler']('qb');

      expect(directive['handleQDButton']).toHaveBeenCalledWith('qb');
    });

    it('should not handle keyboard click enter', () => {
      elementRef.nativeElement.parentElement.classList.contains.and.returnValue(false);
      elementRef.nativeElement.classList.contains.and.returnValue(true);
      directive['handleEnter'] = jasmine.createSpy('handleEnter');

      directive['onKeyBoardPressHandler']('enter');

      expect(directive['handleEnter']).toHaveBeenCalledWith('enter');
    });

    it('should not handle keyboard click delete', () => {
      elementRef.nativeElement.parentElement.classList.contains.and.returnValue(true);
      elementRef.nativeElement.classList.contains.and.returnValue(false);
      directive['handleDelete'] = jasmine.createSpy('handleDelete');

      directive['onKeyBoardPressHandler']('delete');

      expect(directive['handleDelete']).toHaveBeenCalledWith('delete');
    });

    it('should not handle keyboard click dot', () => {
      elementRef.nativeElement.parentElement.classList.contains.and.returnValue(true);
      elementRef.nativeElement.classList.contains.and.returnValue(false);
      directive['handleDot'] = jasmine.createSpy('handleDot');

      directive['onKeyBoardPressHandler']('.');

      expect(directive['handleDot']).toHaveBeenCalledWith('.');
    });
  });

  describe('@onCloseHandler', () => {
    it('should not close keyboard if click was on quick stakes buttons', () => {
      elementRef.nativeElement = { test: 'test' };
      directive['onCloseHandler'](event);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_HIDDEN, 123);
      expect(pubSubService.unsubscribe).not.toHaveBeenCalledWith();
    });

    it('should close keyboard if click was on quick stakes buttons', () => {
      directive.componentId = '123';
      directive['uuid'] = '321';
      elementRef.nativeElement = { test: 'test' };
      domToolsService.isChild.and.returnValue(false);
      directive['onCloseHandler'](event);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_HIDDEN, '123');
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('321');
    });
    it('should not close keyboard when clickHandler in progress', () => {
      elementRef.nativeElement = { test: 'test' };
      directive['stakeClickHandlerInProgressFlag'] = true;
      directive['onCloseHandler'](event);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_HIDDEN, 123);
      expect(pubSubService.unsubscribe).not.toHaveBeenCalledWith();
    });
    it('should not close keyboard when clickHandler in progress and element is not found', () => {
      elementRef.nativeElement = { test: 'test' };
      windowRefService.document.querySelector.and.returnValue(null);
      directive['stakeClickHandlerInProgressFlag'] = true;
      directive['onCloseHandler'](event);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_HIDDEN, 123);
      expect(pubSubService.unsubscribe).not.toHaveBeenCalledWith();
    });
    it('should not close keyboard when clickHandler not in progress', () => {
      directive.componentId = '123';
      directive['uuid'] = '321';
      elementRef.nativeElement = { test: 'test' };
      domToolsService.isChild.and.returnValue(false);
      elementRef.nativeElement = { test: 'test' };
      directive['stakeClickHandlerInProgressFlag'] = false;
      directive['onCloseHandler'](event);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_HIDDEN, '123');
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('321');
    });
  });

  describe('subscribeToEvent', () => {
    let onKeyBoardPressHandlerSpy;
    beforeEach(() => {
      onKeyBoardPressHandlerSpy = spyOn<any>(directive, 'onKeyBoardPressHandler');
      spyOn<any>(directive, 'autoScrollToStakeField');
    });

    it('should publish DIGIT_KEYBOARD_SHOWN sync call iOS Wrapper', () => {
      directive['deviceService'].isIos = true;
      directive['deviceService'].isWrapper = true;
      directive['subscribeToEvent']();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_SHOWN, jasmine.any(Array), false);
    });

    it('should publish DIGIT_KEYBOARD_SHOWN async not Wrapper', () => {
      directive['deviceService'].isIos = true;
      directive['deviceService'].isWrapper = false;
      directive['subscribeToEvent']();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_SHOWN, jasmine.any(Array), true);
    });

    it('should publish DIGIT_KEYBOARD_SHOWN async not iOS', () => {
      directive['deviceService'].isIos = false;
      directive['deviceService'].isWrapper = true;
      directive['subscribeToEvent']();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_SHOWN, jasmine.any(Array), true);
    });

    it('should publish DIGIT_KEYBOARD_SHOWN async sync not iOS Wrapper', () => {
      directive['deviceService'].isIos = false;
      directive['deviceService'].isWrapper = false;
      directive['subscribeToEvent']();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DIGIT_KEYBOARD_SHOWN, jasmine.any(Array), true);
    });

    it('should publish FREEBETS_BY_SELECTION', () => {
      directive['subscribeToEvent']();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.FREEBETS_BY_SELECTION, jasmine.any(Array));
    });

    it('should subscribe to FREEBET_SELECTED_EVENT', () => {
      const setFreeBetSelectedValue = spyOn<any>(directive, 'setFreeBetSelectedValue');
      directive['subscribeToEvent']();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('DigitKeyboardInputDirective-xxxx-xxx-xxxx', 
      pubSubService.API.DIGIT_KEYBOARD_KEY_PRESSED, onKeyBoardPressHandlerSpy);
      expect(pubSubService.subscribe).toHaveBeenCalledWith('DigitKeyboardInputDirective-xxxx-xxx-xxxx', 
      pubSubService.API.FREEBET_SELECTED_EVENT, setFreeBetSelectedValue);
    });

    it('should scroll to field after timeout', fakeAsync(() => {
      directive['subscribeToEvent']();

      expect(directive['autoScrollToStakeField']).not.toHaveBeenCalled();

      tick(100);

      expect(directive['autoScrollToStakeField']).toHaveBeenCalled();
    }));
  });

  it('should handleDelete', () => {
    directive['currentValue'] = '400.00';
    directive['currentValueLength'] = 6;
    directive['handleDelete']('delete');
    expect(pubSubService.publishSync).toHaveBeenCalledWith('DIGIT_KEYBOARD_DEC_DOT_PRESSED', ['400.0', 'delete']);
  });

  it('should resetPlaceholder', () => {
    directive['resetPlaceholder']();
    expect(rendererService.renderer.setAttribute).toHaveBeenCalledWith(jasmine.any(Object), 'placeholder', 'Stake');
  });

  it('should not set placeholder for cvv input', () => {
    elementRef.nativeElement = { id: 'QDCVV2' };

    directive['resetPlaceholder']();
    expect(rendererService.renderer.setAttribute).not.toHaveBeenCalledWith(jasmine.any(Object), 'placeholder', 'Stake');
  });

  it('should not set placeholder for cvv input', () => {
    elementRef.nativeElement = { id: 'QDAmount' };

    directive['resetPlaceholder']();
    expect(rendererService.renderer.setAttribute).not.toHaveBeenCalledWith(jasmine.any(Object), 'placeholder', 'Stake');
  });

  it('should handle enter click(hide keyboard)', () => {
    directive['newValue'] = '0';
    directive.componentId = '1';

    directive['handleEnter']('1');

    expect(pubSubService.publish).toHaveBeenCalledWith('DIGIT_KEYBOARD_DEC_DOT_PRESSED', ['0', '1']);
    expect(pubSubService.publish).toHaveBeenCalledTimes(2);
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  describe('autoScrollToStakeField', () => {
    beforeEach(() => {
      directive['bsSelectionsElement'] = {} as any;
    });

    it('should not set property if there is no keyboard offset', () => {
      domToolsService.getOffset.and.returnValue(false);

      directive['autoScrollToStakeField']();

      expect(rendererService.renderer.setProperty).not.toHaveBeenCalled();
    });

    it('should not set property if there is no keyboard offset', () => {
      const keyboardElement = 'keyboard' as any;

      directive['keyboardElement'] = keyboardElement;
      domToolsService.getOffset.and.callFake(el => {
        return {
          top: el === keyboardElement ? 120 : 100
        };
      });
      domToolsService.getHeight.and.returnValue(10);

      directive['autoScrollToStakeField']();

      expect(rendererService.renderer.setProperty).not.toHaveBeenCalled();
    });

    it('should not set property if there is no bsSelectionsElement', () => {
      const keyboardElement = 'keyboard' as any;

      directive['keyboardElement'] = keyboardElement;
      domToolsService.getOffset.and.callFake(el => {
        return {
          top: el === keyboardElement ? 110 : 100
        };
      });
      domToolsService.getHeight.and.returnValue(10);
      directive['bsSelectionsElement'] = null;

      directive['autoScrollToStakeField']();

      expect(rendererService.renderer.setProperty).not.toHaveBeenCalled();
    });

    it('should set property if there is bsSelectionsElement', () => {
      const keyboardElement = 'keyboard' as any;
      const bsSelectionsScrollTop = 5;
      const bsStakeClosestHeight = 10;

      directive['keyboardElement'] = keyboardElement;
      domToolsService.getOffset.and.callFake(el => {
        return {
          top: el === keyboardElement ? 110 : 100
        };
      });
      domToolsService.getHeight.and.returnValue(bsStakeClosestHeight);
      domToolsService.getScrollTop.and.returnValue(bsSelectionsScrollTop);
      domToolsService.getHeight.and.returnValue(bsStakeClosestHeight);

      directive['autoScrollToStakeField']();

      expect(rendererService.renderer.setProperty).toHaveBeenCalledWith(directive['bsSelectionsElement'], 'scrollTop', 15);
    });

    it('should not set property if there is no bsTotalWrapper', () => {
      const keyboardElement = 'keyboard' as any;
      windowRefService.document.querySelector.and.returnValue(null);
      directive['bsSelectionsElement'] = { } as any;
      domToolsService.getScrollTop.and.returnValue(5);
      directive['keyboardElement'] = keyboardElement;
      domToolsService.getOffset.and.callFake(el => {
        return {
          top: el === keyboardElement ? 110 : 100
        };
      });
      domToolsService.getHeight.and.returnValue(10);

      directive['autoScrollToStakeField']();
      expect(rendererService.renderer.setProperty).toHaveBeenCalledWith(directive['bsSelectionsElement'], 'scrollTop', 5);
    });
  });

  it('clearActiveElement', () => {
    directive['mainElement'] = <any>{
      querySelectorAll: jasmine.createSpy().and.returnValue([{
        removeClass: jasmine.createSpy(),
        id: 'QDAmount',
        attributes: {'data-uuid': 'ABC-123'}        
      }])
    };
    elementRef.nativeElement.id = 'QDAmount';
    directive['depositPlaceholder'] = '1';

    directive['clearActiveElement']();

    expect(rendererService.renderer.setAttribute).toHaveBeenCalledWith(jasmine.any(Object), 'placeholder', '1');
    expect(rendererService.renderer.removeAttribute).toHaveBeenCalledWith(jasmine.any(Object), 'data-uuid');
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  it('restorePlaceholder', () => {
    elementRef.nativeElement.id = 'QDAmount';
    directive['depositPlaceholder'] = '1';

    directive['restorePlaceholder']();

    expect(rendererService.renderer.setAttribute).toHaveBeenCalledWith(elementRef.nativeElement, 'placeholder', '1');
  });

  it('validateValue', () => {
    directive['renderValue'] = jasmine.createSpy();
    directive.ngModel = '12';
    directive.ngModelChange.emit = jasmine.createSpy();

    directive['validateValue']();

    expect(directive.ngModelChange.emit).toHaveBeenCalledWith('12.00');
    expect(directive['renderValue']).toHaveBeenCalledWith(directive.ngModel);
  });

  it('allInputsValueToFixed', () => {
    directive['bsSelectionsElement'] = <any>{
      querySelectorAll: jasmine.createSpy().and.returnValue([{
        removeClass: jasmine.createSpy(),
        id: 'id',
        value: '123'
      }])
    };
    directive['allInputsValueToFixed']();
    expect(rendererService.renderer.setAttribute).toHaveBeenCalledWith(jasmine.any(Object), 'value', '123.00');
  });

  it('handleDot', () => {

    directive['handleDot']('.');
    expect(directive['isEdited']).toEqual(true);
  });

  it('handleDot', () => {
    directive['currentValue'] = '2';
    directive['isEdited'] = true;
    directive['handleDot']('1');
    expect(directive['newValue']).toEqual('2.');
  });


  it('handleQDButton coral', () => {
    directive['eventAction'] = 'quick deposit';
    directive['handleQDButton']('1');

    expect(directive['isEdited']).toEqual(false);
  });
  it('handleQDButton coral', () => {
    directive['eventAction'] = 'quick deposit';
    directive['handleQDButton']('1.01');
    expect(directive['isEdited']).toEqual(false);
  });
  it('handleQDButton lads', () => {
    directive['eventAction'] = 'quick deposit';
    directive['isBrandLadbrokes']=true;
    directive['handleQDButton']('1');

    expect(directive['isEdited']).toEqual(false);
  });
  it('handleQDButton new value', () => {
    directive['eventAction'] = 'quick deposit';
    directive['newValue ']='10.001';
    directive['handleQDButton']('1');

    expect(directive['isEdited']).toEqual(false);
  });
    it('handleQDButton current value greater than 1', () => {
    directive['eventAction'] = 'quick deposit';
    directive['currentValue']='10.001';
    directive['handleQDButton']('1');

    expect(directive['isEdited']).toEqual(false);
  });
      it('handleQDButton new value less than 1', () => {
    directive['eventAction'] = 'quick deposit';
    directive['currentValue']='10';
    directive['handleQDButton']('1');

    expect(directive['isEdited']).toEqual(false);
  });

});
