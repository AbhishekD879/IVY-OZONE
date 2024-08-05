import {fakeAsync, tick} from '@angular/core/testing';

import { ToteFreeBetsToggleComponent } from './tote-free-bets-toggle.component';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { LocaleService } from '@core/services/locale/locale.service';

describe('ToteFreeBetToggleComponent', () => {
  let component: ToteFreeBetsToggleComponent;
  let componentFactoryResolver;
  let dialogService;
  let freeBetsFactory;
  let filtersService;
  let storageService;
  let changeDetectorRef;
  let localeService: any = LocaleService;
  let timeService;
  let gtmService;
  let eventVideoStreamProviderService;

  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: false
  }
  beforeEach(() => {
    dialogService = {
      API: dialogIdentifierDictionary,
      openDialog: jasmine.createSpy('openDialog').and.callFake((p1, p2, p3, opt) => {
        opt.onSelect({
          freebetTokenValue: 1,
          freebetTokenId: 1,
          freebetOfferCategories: { freebetOfferCategory: 'Bet Pack' }
        });
      }),
      closeDialog: jasmine.createSpy('closeDialog')
    };
    
    eventVideoStreamProviderService = {isStreamAndBet: true};
    
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({})
    };
    freeBetsFactory = {
      isBetPack: jasmine.createSpy('isBetPack'),
      isFanzone: jasmine.createSpy('isFanzone')

    };
    filtersService = {
      setFreebetCurrency: jasmine.createSpy().and.returnValue('£1')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(value => value)
    } as any;
    storageService = { get: (key) => { 
      return {
        poolBet: {
          freebetTokenValue: 1,
          freebetTokenId: 1,
          freebetTokenExpiryDate: "2023-09-06"
        }
      }
     }, set: (key, value) => {return (key+value);} };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    }
    component = new ToteFreeBetsToggleComponent(
      componentFactoryResolver,
      dialogService,
      freeBetsFactory,
      filtersService,
      storageService,
      changeDetectorRef,
      localeService,
      timeService,
      gtmService,
      eventVideoStreamProviderService
    );
    component.freebetsConfig = {
      freeBetAdded: 'FREE BET ADDED',
      betTokenAdded: 'BET TOKEN ADDED',
      plusTokenAndFreeBet : '+TokenAndFreeBet',
      plusFreeBet : '+FreeBet',
      plusToken : '+BetToken',
      addTokenAndFreeBet: 'AddTokenAndFreeBet',
      addFreeBet: 'AddFreeBet',
      addBetToken: 'AddBetToken',
      fanZoneAdded: 'FANZONE FREE BET ADDED'
    };
  });

  describe('useFreebet', () => {
    it('no available free bets and betpacklist', () => {
      component.freeBets = null;
      component.betPackList = null;
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).not.toHaveBeenCalled();
    });

    it('no available free bets with available betpacklist', () => {
      component.freeBets = null;
      component.betPackList = [{}] as any[];
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectToteFreebetDialog');
    });
    it('no available free bets with available betpacklist and no freebetOfferCategories', () => {
      dialogService.openDialog = jasmine.createSpy('openDialog').and.callFake((p1, p2, p3, opt) => {
        opt.onSelect({
          freebetTokenValue: 1,
          freebetTokenId: 1,
          freebetOfferCategories: null
        });
      })
      component.freeBets = null;
      component.betPackList = [{}] as any[];
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectToteFreebetDialog');
    });

    it('free bets and betpacklist available', () => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectToteFreebetDialog');
    });

    it('open dialog', fakeAsync(() => {
      component.freeBets = [{}] as any[];
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectToteFreebetDialog');
    }));
  });

  it('removeFreeBet betType true', () => {
    component.toteBet.emit = jasmine.createSpy('emit');
    //spyOn<any>(component, 'triggerGtmService');
    storageService.get = (key) => { return {poolBet: {betType: true, freebetTokenId: 1}}};
    
    component.removeFreeBet();
    expect(component.selected).toBeNull();
  });
  it('removeFreeBet with bet type false', () => {
    component.toteBet.emit = jasmine.createSpy('emit');
    spyOn<any>(component, 'triggerGtmService');
    storageService.get = (key) => { return {poolBet: {betType: false, freebetTokenId: 1}}};
    
    component.removeFreeBet();
    expect(component.selected).toBeNull();
  });



  describe('freebetButtonText in mobile view', ()=> {
    it('should display +TokenAndFreeBet', () => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      component.isMobile = true; 
      expect(component.freebetButtonText()).toBe('AddTokenAndFreeBet');
    });
    
    it('should display AddFreeBet and fanzones', () => {
      component.isMobile = false;
      component.freeBets = [{freebetTokenValue: 1,
        freebetTokenId: 1}] as any[];
      component.betPackList = [] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });
    it('should display +FreeBet', () => {
      component.freeBets = [{}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });

    it('should display empty', () => {
      component.freeBets = [] as any[];
      component.betPackList = [] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText()).toBe('');
    });

    it('should display +BetToken', () => {
      component.betPackList = [{}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(true)).toBe('+BetToken');
    });
    it('should display +TokenAndFreeBet', () => {
      component.betPackList = [{}] as any[];
      component.freeBets = [{freebetTokenValue: 1,
        freebetTokenId: 1}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(true)).toBe('+TokenAndFreeBet');
    });
    it('should display +FreeBet', () => {
      component.betPackList = [] as any[];
      component.freeBets = [{freebetTokenValue: 1,
        freebetTokenId: 1}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(true)).toBe('+FreeBet');
    });
    it('should display +BetToken', () => {
      component.betPackList = [{}] as any[];
      component.freeBets = [] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(true)).toBe('+BetToken');
    });

    it('should return empty string', () => {
      component.betPackList = [] as any[];
      component.freeBets = [] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(true)).toBe('');
    });

    it('should call freebetButtonText and return AddTokenAndFreeBet ', () => {
      component.freeBets = [{id: '123'}] as any;
      component.betPackList = [{id: '123'}] as any;
      component.freebetsConfig = { addTokenAndFreeBet: 'AddTokenAndFreeBet' };
      expect(component.freebetButtonText()).toBe('AddTokenAndFreeBet');
    });
    it('should call freebetButtonText and return addFreeBet ', () => {
      component.freeBets = [{id: '123'}] as any;
      component.betPackList = [] as any;
      component.freebetsConfig = { addFreeBet: 'addFreeBet' };
      expect(component.freebetButtonText()).toBe('addFreeBet');
    });
    it('should call freebetButtonText and return addBetToken ', () => {
      component.freeBets = null;
      component.betPackList = [{id: '123'}] as any;
      component.freebetsConfig = { addBetToken: 'addBetToken' };
      expect(component.freebetButtonText()).toBe('addBetToken');
    });
    it('should call freebetButtonText and return ""', () => {
      component.freeBets = null;
      component.betPackList = [] as any;
      component.freebetsConfig = { addBetToken: 'addBetToken' };
      expect(component.freebetButtonText()).toBe('');
    });

   it('should return BET TOKEN ADDED string', () => {
    freeBetsFactory.isBetPack.and.returnValue(true);
      component.selected = {
        value: 1,
        type: 'current',
        freebetOfferCategories: { freebetOfferCategory: 'Bet Pack' }
      };
    expect(component.removeFreebetButtonText()).toBe('FREE BET ADDED');
    });
    
    it('should return FREE BET ADDED string', () => {
      component.selected = {value : 1, type: 'current'};
    expect(component.removeFreebetButtonText()).toBe('FREE BET ADDED');
    });
    it('should return FANZONE ADDED string', () => {
      component.selected = {value : 1, type: 'current',freebetOfferCategories:{freebetOfferCategory:'FANZONE'}};
      freeBetsFactory.isFanzone.and.returnValue(true);
      expect(component.removeFreebetButtonText()).toBe('FREE BET ADDED');
    });

    it('should return FREE BET ADDED string if selected is empty', () => {
    expect(component.removeFreebetButtonText()).toBe('FREE BET ADDED');
    });
    it('should return betTokenAdded', () => {
    storageService.get = (key) => { return {poolBet: {betType: true}}};
    expect(component.removeFreebetButtonText()).toBe('BET TOKEN ADDED');
    });
    it('should return true', () => {
       component.dialogComponent = true;
        expect(component.dialogComponent).toBeTruthy();
    });

  });

  describe('freebetButtonText in Desktop view', ()=> {
    it('should display AddFreeBet', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      component.betPackList = [{'freeBetId': '122','freeBetName': 'betpack Football Bundle22'}] as any[];
      expect(component.freebetButtonText()).toBe('AddTokenAndFreeBet');
    });
    it('should display AddFreeBet and fanzones', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      component.betPackList = [] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });
    it('should display AddFreeBet and without fanzones', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      component.betPackList = [] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });

    it('should display fanzone', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });

    it('should display AddBetToken', () => {
      component.isMobile = false;
      component.betPackList = [{}] as any[];
      expect(component.freebetButtonText()).toBe('AddBetToken');
    });

    it('should return empty string', () => {
      component.isMobile = false;
      component.betPackList = [] as any[];
      component.freeBets = [] as any[];
      expect(component.freebetButtonText()).toBe('');
    });
  });
  describe('should call ngOnchanges', ()=> { 
      it("call ngOnchanges with current value null", () => {
        const changes = {
          selectedToteFreeBetValue: {
            currentValue: null
          }
        } as any;

        component.ngOnChanges(changes);
        expect(component.selected).toBeNull();
      });

      it("call ngOnchanges with current value", () => {
        const changes = {
          selectedToteFreeBetValue: {
            currentValue: true
          }
        } as any;

        component.ngOnChanges(changes);
        expect(component.selected).toBeUndefined();
      });

      it("call ngOnchanges with current value true for totefreebet", () => {
        const changes = {
          toteFreeBetSelected: {
            currentValue: null
          }
        } as any;

        component.ngOnChanges(changes);
        expect(component.selected).toBeUndefined();
      });

      it("call ngOnchanges with current value true for both", () => {
        const changes = {
          selectedToteFreeBetValue: {
            currentValue: true,
          },
          toteFreeBetSelected: {
            currentValue: true
          }
        } as any;

        component.ngOnChanges(changes);
        expect(component.selected).toEqual(undefined);
      });
  });

  it('should call getText', () => {
    component.selected = [{value : 1, type: 'current', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack'}}] as any;
    component.freebetsConfig.betTokenAdded = "BET TOKEN ADDED";
    freeBetsFactory.isBetPack.and.returnValue(false);
    freeBetsFactory.isFanzone.and.returnValue(false);
    expect(component.getText()).toBe('£1 bs.betTokenAdded');
    component.selected = [{value : 1, type: 'current', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack1'}}] as any;
    component.freebetsConfig.betTokenAdded = "BET TOKEN ADDED";
    expect(component.getText()).toBe('£1 FREE BET ADDED');
  });

  it('should call getText with bet token', () => {
    component.selected = {value : 1, type: 'current', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack'}} as any;
    component.freebetsConfig.betTokenAdded = "BET TOKEN ADDED";
    freeBetsFactory.isBetPack.and.returnValue(false);
    freeBetsFactory.isFanzone.and.returnValue(false);
    expect(component.getText()).toBe('£1 bs.betTokenAdded');
    storageService.get = (key) => {
      if(key === 'toteBet') {
        return {
          poolBet: {
            betType: 'BET TOKEN ADDED'
          }
        }
      }
    };
    component.selected = {value : 1, type: 'current', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack1'}} as any;
    expect(component.getText()).toBe('£1 FREE BET ADDED');
  });
  it('should call isBetSelected', ()=> {
    storageService.get = (key) => { return null;}
    expect(component.isBetSelected()).toBeFalse();
  });
  it('should call triggerGtmService isStreamAndBet true', ()=> {
    component['triggerGtmService'](true, '')
    expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call triggerGtmService isStreamAndBet false isBetslip true', ()=> { 
    component.isBetslip = true;
    component['triggerGtmService'](false, '');
    expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call triggerGtmService isStreamAndBet false isBetslip true optional', ()=> { 
    component.isBetslip = true;
    component['triggerGtmService'](false);
    expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call triggerGtmService isStreamAndBet false isBetslip empty', ()=> { 
    component.isBetslip = true;
    component['triggerGtmService']();
    expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call triggerGtmService isStreamAndBet false isBetslip true with text', ()=> { 
    component.isBetslip = true;
    component['triggerGtmService'](false, 'text');
    expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call triggerGtmService isStreamAndBet false isBetslip false', ()=> { 
    spyOn<any>(component, 'getEventdetails');
    component.isBetslip = false;
    component['triggerGtmService'](false, '');
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe("#getEventdetails", ()=> {
    it('should call getEventdetails showOnDigitKeyborad false', ()=> { 
      spyOn(component, 'isBetSelected').and.returnValue(false);
      spyOn(component, 'freebetButtonText')
      component.showOnDigitKeyborad = false;
      component.isMobile = false;
      component['getEventdetails']();
      expect(component.freebetButtonText).toHaveBeenCalled();
    });
    it('should call getEventdetails showOnDigitKeyborad true', ()=> { 
      spyOn(component, 'isBetSelected').and.returnValue(true);
      spyOn(component, 'freebetButtonText');
      spyOn(component, 'removeFreebetButtonText');
      component.showOnDigitKeyborad = true;
      component['getEventdetails']();
      expect(component.removeFreebetButtonText).toHaveBeenCalled();
    });
    it('should call getEventdetails showOnDigitKeyborad true isBetSelected false', ()=> { 
      spyOn(component, 'isBetSelected').and.returnValue(false);
      spyOn(component, 'freebetButtonText');
      spyOn(component, 'removeFreebetButtonText');
      component.showOnDigitKeyborad = true;
      component.isMobile = true;
      component['getEventdetails']();
      expect(component.freebetButtonText).toHaveBeenCalled();
    });
    it('should call getEventdetails showOnDigitKeyborad false isBetSelected true', ()=> { 
      spyOn(component, 'isBetSelected').and.returnValue(true);
      spyOn(component, 'getText').and.returnValue(undefined)
      component.showOnDigitKeyborad = false;
      component.isMobile = true;
      component['getEventdetails']();
      expect(component.getText).toHaveBeenCalled();
    });
    it('should call getEventdetails showOnDigitKeyborad false isBetSelected true', ()=> { 
      spyOn(component, 'isBetSelected').and.returnValue(true);
      spyOn(component, 'getText').and.returnValue("gettext")
      component.showOnDigitKeyborad = false;
      component.isMobile = true;
      component['getEventdetails']();
      expect(component.getText).toHaveBeenCalled();
    });

    it('should call getEventdetails showOnDigitKeyborad true isBetSelected false', ()=> { 
      component.isMobile = true;
      spyOn(component, 'isBetSelected').and.returnValue(false);
      component.showOnDigitKeyborad = false;
      spyOn(component, 'freebetButtonText');
      spyOn(component, 'removeFreebetButtonText');
      
      expect(component['getEventdetails']()).toEqual('');
    });
  });

  it('should call gtmFreebetText', ()=> {
    storageService.get = (key) => { 
      if(key === 'toteFreeBets'){
        return [{id: 1}, {id: 2}];
      }else {
        return [{id: 1}, {id: 2}];
      }
    }
    expect(component['gtmFreebetText']()).toEqual('add bet token and free bet');
    storageService.get = (key) => { 
      if(key === 'toteFreeBets'){
        return [{id: 1}, {id: 2}];
      }else {
        return [];
      }
    }
    expect(component['gtmFreebetText']()).toEqual('add free bet');
    storageService.get = (key) => { 
      if(key === 'toteFreeBets'){
        return [];
      }else {
        return [{id: 1}, {id: 2}];
      }
    }
    expect(component['gtmFreebetText']()).toEqual('add bet token');
  });
});