import { fakeAsync, tick,flush } from '@angular/core/testing';
import { DigitKeyboardComponent } from './digit-keyboard.component';
import { IFreebetToken } from '@root/app/bpp/services/bppProviders/bpp-providers.model';
import environment from '@environment/oxygenEnvConfig';
describe('DigitKeyboardComponent', () => {
  let component: DigitKeyboardComponent;
  let pubSubService;
  let coreToolsService;
   let changeDetectorRef;
  let locale;
  let storageService;
  let toteBetslipService;
  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy(),
      publishSync: jasmine.createSpy(),
      API: {
        DIGIT_KEYBOARD_DEC_DOT_PRESSED: 'DIGIT_KEYBOARD_DEC_DOT_PRESSED',
        DIGIT_KEYBOARD_SHOWN: 'DIGIT_KEYBOARD_SHOWN',
        DIGIT_KEYBOARD_HIDDEN: 'DIGIT_KEYBOARD_HIDDEN',
        DIGIT_KEYBOARD_KEY_PRESSED: 'DIGIT_KEYBOARD_KEY_PRESSED',
        FREEBET_SELECTED_EVENT: 'FREEBET_SELECTED_EVENT',
        ODDS_BOOST_UNSET_FREEBETS: 'ODDS_BOOST_UNSET_FREEBETS',

      }
    };

    coreToolsService = {
      uuid: jasmine.createSpy().and.returnValue('xxxx-xxx-xxxx')
    };

    toteBetslipService = {
      getFreeBetsConfig: () => { return 'getFreeBetsConfig'}
    }
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    // userService = {
    //   status: false
    // };
    locale = {
      getString: jasmine.createSpy('').and.returnValue('Ladbrokes'),
      toLowerCase: jasmine.createSpy()
    };
    storageService = {
      get: jasmine.createSpy('get')
    }
    component = new DigitKeyboardComponent(
      pubSubService,
      coreToolsService,
      changeDetectorRef,
      locale,
      storageService,
      toteBetslipService
    );
  });

 

  it('should execute ngOnInit', () => {
    environment.brand = 'ladbrokes';
    storageService.get.and.returnValue({poolBet: {}});
    component.ngOnInit();
    expect(component['locale'].getString).toHaveBeenCalled();
    
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.isDecimalButtonEnabled).toEqual(true);
    expect(component.isDecimalPointPressed).toEqual(false);
    expect(component.isKeyboardShown).toEqual(false);
    expect(component.isQuickDepositButtonsShown).toEqual(false);
    expect(component.quickDepositButtons).toEqual([]);
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit', () => {
      component['setLabels'] = jasmine.createSpy();
      storageService.get.and.returnValue({poolBet: {freebetTokenId: 1}});
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(6);

      expect(component['setLabels']).toHaveBeenCalled();
    });

    it('should set hideKeyboardFlag based on input', () => {
      component.hideKeyboardFlag = false;
      storageService.get.and.returnValue({poolBet: {freebetTokenId: 1}});
      component.ngOnInit();

      expect(component.hideKeyboardFlag).toBeFalsy();
    });

    it('should set hideKeyboardFlag with default value', () => {
      storageService.get.and.returnValue({poolBet: {freebetTokenId: 1}});
      component.ngOnInit();

      expect(component.hideKeyboardFlag).toBeTruthy();
    });

    it('should set hideKeyboardFlag with storage value', () => {
      spyOn(component, 'checkIfToteFreebetAdded');
      storageService.get = (key) => {
        if(key === 'toteFreeBets') {
          return [
            {freebetTokenId: 1}
          ]
        } else if(key === 'toteBetPacks') {
          return [
            {freebetTokenId: 1}
          ]
        }
      };
      component.ngOnInit();

      expect(component.checkIfToteFreebetAdded).toHaveBeenCalled();
      storageService.get = (key) => {
        if(key === 'toteFreeBets') {
          return []
        } else if(key === 'toteBetPacks') {
          return [
            {freebetTokenId: 1}
          ]
        }
      };
      component.ngOnInit();

      expect(component.checkIfToteFreebetAdded).toHaveBeenCalled();
    });

    it('should checkIfToteFreebetAdded with data', () => {
      // spyOn(component, 'reAssignSelectedToteFreeBetObj');
      let toteBet = {
        poolBet: {}
      };
       let toteFreeBets = [{freebetTokenId: 1},{freebetTokenId: 2}];
       let toteBetPacks =  [{freebetTokenId: 1}];
      component.checkIfToteFreebetAdded(toteBet, toteFreeBets, toteBetPacks);
      expect(component.selectedToteFreeBetObj).toBeUndefined();

      toteBet = {
        poolBet: {freebetTokenId: 1}
      };
      component.checkIfToteFreebetAdded(toteBet, toteFreeBets, toteBetPacks);
      expect(component.selectedToteFreeBetObj.length).toEqual(1);
      toteBet = {
        poolBet: {freebetTokenId: 2}
      };
      toteFreeBets = [{freebetTokenId: 1},{freebetTokenId: 12}];
      toteBetPacks =  [{freebetTokenId: 2}];
      component.checkIfToteFreebetAdded(toteBet, toteFreeBets, toteBetPacks);
      expect(component.selectedToteFreeBetObj.length).toEqual(1);
    });
  });

  describe('#ngOnChanges', () => {
    it('should call ngOnChanges', () => {
      component['setLabels'] = jasmine.createSpy();
      component.currency = 'Kr';
      component.ngOnChanges();

      expect(component['setLabels']).toHaveBeenCalled();
    });
  });

  describe('#setLabels', () => {
    it('setLabels with KR', () => {
      component['getLabelData'] = jasmine.createSpy();

      component.currency = 'Kr';
      component['setLabels']();

      expect(component['getLabelData']).toHaveBeenCalledWith([50, 100, 500, 1000] );
    });
  });

  describe('#ngOnDestroy', () => {
    it('should call ngOnDestroy', () => {
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('DigitKeyboardComponent-xxxx-xxx-xxxx');
    });
  });

  describe('#onButtonClickHandler', () => {
    it('should call onButtonClickHandler', () => {
      const event = {
        target: {
          dataset: {
            value: '1'
          }
        },
        stopPropagation: jasmine.createSpy('stopPropagation')
        
      };
      const clickTransition= spyOn(component,'clickTransition')
      component.onButtonClickHandler((event as any));

      expect(pubSubService.publishSync).toHaveBeenCalledWith('DIGIT_KEYBOARD_KEY_PRESSED', '1');
      expect(clickTransition).toHaveBeenCalled();

    });
  });

  describe('#onButtonClickHandler', () => {
    it('should call onButtonClickHandler and isDecimalPointPressed', () => {
      component.isDecimalPointPressed = false;
      component.isDecimalButtonEnabled = true;

      const event = {
        target: {
          dataset: {
            value: '.'
          }
        },
        stopPropagation: jasmine.createSpy('stopPropagation')
      };
      const clickTransition= spyOn(component,'clickTransition')

      component.onButtonClickHandler((event as any));
      expect(component.isDecimalPointPressed).toEqual(true);

      expect(pubSubService.publishSync).toHaveBeenCalledWith('DIGIT_KEYBOARD_KEY_PRESSED', '.');
    });
  });
  describe('#onButtonClickHandler', () => {
    it('should call onButtonClickHandler and qb pressed', () => {
      component.isDecimalPointPressed = false;
      component.isDecimalButtonEnabled = true;

      const event = {
        target: {
          dataset: {
            value: '.'
          }
        },
        stopPropagation: jasmine.createSpy('stopPropagation')
      };
      const clickTransition= spyOn(component,'clickTransition')

      component.onButtonClickHandler((event as any),'qb');
      expect(component.isDecimalPointPressed).toEqual(true);

      expect(pubSubService.publishSync).toHaveBeenCalledWith('DIGIT_KEYBOARD_KEY_PRESSED', '.');
    });
  });

  describe('#onButtonClickHandler', () => {
    it('should call onButtonClickHandler and return if isDecimalButtonEnabled is true', () => {
      component.isDecimalButtonEnabled = false;

      const event = {
        target: {
          dataset: {
            value: '.'
          }
        },
        stopPropagation: jasmine.createSpy('stopPropagation')
      };
      component.onButtonClickHandler((event as any));

      expect(pubSubService.publishSync).not.toHaveBeenCalled();
    });
  });

  describe('#setFreeBetList', () => {
    it('should set selected bet and free bet list', () => {
      const freebetsList: IFreebetToken[] = [{'freebetTokenValue': '1.00'}] as any;
      const selectedFreeBet = {'freebetTokenValue': '1.00'} as any;
      const freebetsConfig = {'header': 'Freebets available'} as any;
      const isBoostEnabled = true;
      const isSelectionBoosted = true;
      const canBoostSelection = true;
      const betPackList:IFreebetToken[] = [{'freebetTokenValue': '1.00'}] as any;
      const fanzoneList:IFreebetToken[] = [{'freebetTokenValue': '1.00'}] as any;
      component.triggeredFromToteBets = true;
      component.setFreeBetList(freebetsList, selectedFreeBet, freebetsConfig, isBoostEnabled, isSelectionBoosted, canBoostSelection,betPackList,fanzoneList);
      expect(component.availableFreeBets).toEqual(freebetsList);
      expect(component.selected).toEqual(selectedFreeBet);
    });
  });

  describe('#onFreebetChange', () => {
    it('should set selected free bet and emit the event', () => {
      const event = {
        output: 'freebet',
        value: {'tokenValue': '1.00'}  as any
      };
      component.onFreebetChange((event as any));
      expect(component.selected).toEqual(event.value);
      expect(pubSubService.publishSync).toHaveBeenCalledWith('FREEBET_SELECTED_EVENT', event);
    });
  });

  describe('#onToteFreebetChange', () => {
    it('should set selected free bet and emit the event', () => {
      const event = {
        output: 'freebet',
        value: undefined  as any
      };
      component.triggeredFromToteBets = true;
      component.onToteFreebetChange((event as any));
      expect(component.selected).toEqual(event.value);
      expect(pubSubService.publishSync).toHaveBeenCalledWith('FREEBET_SELECTED_EVENT', event);
      expect(component.triggeredFromToteBets).toBeTruthy()
    });
  });

  describe('#getLabelData (logged Out)', () => {
    it('should getLabelData', () => {
      component['currency'] = '$';
      const values = [1, 3, 5, 7];
      expect(component['getLabelData'](values)[2]).toEqual(jasmine.objectContaining({
        label: '+$5',
        value: 'qb-5'
      }));
    });

    it('should getLabelData (loggedIn)', () => {
      component['userService'] = <any>{ status: true };
      component['currency'] = '$';

      const values = [1, 3, 5, 7];
      expect(component['getLabelData'](values)[2]).toEqual(jasmine.objectContaining({
        label: '+$5',
        value: 'qb-5'
      }));
    });
  });

  describe('hideKeyboard', () => {
    let notifyEmitter;
    const componentId = '123';

    beforeEach(() => {
      notifyEmitter = jasmine.createSpy('notifyEmitter');

      component['componentId'] = componentId;
      component.keyboardHidden.subscribe(notifyEmitter);
    });

    it('should not handle close if keyboard was not shown', fakeAsync(() => {
      component['isKeyboardShown'] = false;
      component['hideKeyboard'](componentId);
      tick();

      expect(notifyEmitter).not.toHaveBeenCalled();
    }));

    it('should not handle close if passed id is not equal as component\'s id', fakeAsync(() => {
      component['isKeyboardShown'] = true;
      component['hideKeyboard']('12');
      tick();

      expect(notifyEmitter).not.toHaveBeenCalled();
    }));

    it('should handle close if passed id is equal as component\'s id and keyboard was shown', fakeAsync(() => {
      component['isDecimalButtonEnabled'] = false;
      component['isDecimalPointPressed'] = true;
      component['isKeyboardShown'] = true;
      component['hideKeyboard'](componentId);
      tick();

      expect(notifyEmitter).toHaveBeenCalled();
      expect(component['isDecimalButtonEnabled']).toBeTruthy();
      expect(component['isDecimalPointPressed']).toBeFalsy();
      expect(component['isKeyboardShown']).toBeFalsy();
    }));
  });

  describe('showKeyboard', () => {
    let notifyEmitter;
    const componentId = '123';

    beforeEach(() => {
      notifyEmitter = jasmine.createSpy('notifyEmitter');

      component['componentId'] = componentId;
      component.keyboardShown.subscribe(notifyEmitter);
    });

    it('should not handle if passed id is not equal as component\'s id', fakeAsync(() => {
      component['showKeyboard'](false, false, ['1','2','3','4'],'12');
      tick();

      expect(notifyEmitter).not.toHaveBeenCalled();
    }));

    it('should handle if passed id is equal as component\'s id', fakeAsync(() => {
      const decimalButton = false;
      const quickDepositButton = false;
      const quickStakeItems = [1,2,3,4];


      component['isDecimalButtonEnabled'] = true;
      component['isQuickDepositButtonsShown'] = true;
      component['isDecimalPointPressed'] = true;
      component['isKeyboardShown'] = false;
      component['showKeyboard'](decimalButton, quickDepositButton,quickStakeItems, componentId);
      tick();

      expect(notifyEmitter).toHaveBeenCalled();
      expect(component['isDecimalButtonEnabled']).toBeFalsy();
      expect(component['isQuickDepositButtonsShown']).toBeFalsy();
      expect(component['isKeyboardShown']).toBeTruthy();
      expect(component['isDecimalPointPressed']).toBeFalsy();
    }));
  });

  describe('#updateDecimalPointState', () => {
    it('updateDecimalPointState', () => {
      component.isDecimalPointPressed = undefined;
      component['updateDecimalPointState']('', '');
      expect(component.isDecimalPointPressed).toEqual(undefined);
    });

    it('updateDecimalPointState true', () => {
      component.isDecimalPointPressed = undefined;
      component['updateDecimalPointState']('1', '.');
      expect(component.isDecimalPointPressed).toEqual(true);
    });
  });
  describe('#clickTransition', () => {
    it('clickTransition', fakeAsync(() => {
      const el = document.createElement('div');
      el.setAttribute('class', 'dk-key-one');
      document.body.append(el)
      component.clickTransition('one');
      component.isBrandLadbrokes = false;
      component.clickTransition('one');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
    it('clickTransition qb', fakeAsync(() => {
      const el = document.createElement('div');
      el.setAttribute('class', 'dk-key-qb');
      document.body.append(el)
      component.clickTransition('qb');
      component.isBrandLadbrokes = false;
      component.clickTransition('qb');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
    it('clickTransition lads', fakeAsync(() => {
      const el = document.createElement('div');
      el.setAttribute('class', 'dk-key-one');
      document.body.append(el);
      component.isBrandLadbrokes = true;
      component.clickTransition('one');
      component.isBrandLadbrokes = false;
      component.clickTransition('one');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
    it('clickTransition lads qb', fakeAsync(() => {
      const el = document.createElement('div');
      el.setAttribute('class', 'dk-key-qb');
      document.body.append(el);
      component.isBrandLadbrokes = true;
      component.clickTransition('qb');
      component.isBrandLadbrokes = false;
      component.clickTransition('qb');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
  });

  it('setToteFreebetConfig', () => {
    expect(component['setToteFreebetConfig']()).toEqual('getFreeBetsConfig');
  });
  
});
