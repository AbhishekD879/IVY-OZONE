import { fakeAsync, tick } from '@angular/core/testing';

import { FreeBetToggleComponent } from './free-bet-toggle.component';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';

describe('FreeBetToggleComponent', () => {
  let dialogService;
  let componentFactoryResolver;
  let component: FreeBetToggleComponent;
  let resolvedDialogComponent;
  let filtersService;
  let deviceService;
  let freeBetsFactory;
  let gtmService;
  let changeDetectorRef;
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
        opt.onSelect();
      }),
      closeDialog: jasmine.createSpy('closeDialog')
    };
    deviceService = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType)
    };
    resolvedDialogComponent = {
      name: dialogService.API.selectFreeBetDialog
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(resolvedDialogComponent)
    };
    freeBetsFactory = {
      isBetPack: jasmine.createSpy('isBetPack'),
      isFanzone: jasmine.createSpy('isFanzone')

    };
    filtersService = {
      setFreebetCurrency: jasmine.createSpy().and.returnValue('£1')
    };
    gtmService = { push: jasmine.createSpy('push') };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    eventVideoStreamProviderService = {
      isStreamAndBet: true
    };
    component = new FreeBetToggleComponent(
      dialogService,
      componentFactoryResolver,
      filtersService,
      deviceService,
      freeBetsFactory,
      gtmService,
      changeDetectorRef,
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
    it('no available free bets', () => {
      component.freeBets = null;
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).not.toHaveBeenCalled();
    });

    it('no available free bets, selection is disabled', () => {
      component.freeBets = null;
      component.selection = {disabled: true} as any;
      component.useFreeBet();
      expect(componentFactoryResolver.resolveComponentFactory).not.toHaveBeenCalled();
    });

    it('open dialog', fakeAsync(() => {
      component.freeBets = [{}] as any[];
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));

    it('open dialog with freeBets and betPacks#1', fakeAsync(() => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));

    it('open dialog with only betPacks#2', fakeAsync(() => {
      component.freeBets = null;
      component.betPackList = [{}] as any[];
      component.fanzoneList = null;
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));

    it('open dialog with betpacks', fakeAsync(() => {
      component.betPackList = [{}] as any[];
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));
    it('open dialog with betpacks', fakeAsync(() => {
      component.fanzoneList = [{}] as any[];
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));
    it('open dialog with fanzone', fakeAsync(() => {
      component.fanzoneList = [{}] as any[];
      component.selection = {disabled: false} as any;
      component.useFreeBet();
      tick();
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'selectFreeBetDialog', resolvedDialogComponent, true, jasmine.any(Object)
      );
      expect(dialogService.closeDialog).toHaveBeenCalledWith('selectFreeBetDialog');
    }));
  });

  it('removeFreeBet', () => {
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: false} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).toHaveBeenCalledWith(null);
  });

  it('removeFreeBet and selection is disabled', () => {
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: true} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).not.toHaveBeenCalledWith(null);
  });
  it('removeFreeBet and selection is disabled in case of SnB', () => {
    freeBetsFactory.isBetPack.and.returnValue(true);
    component.isStreamAndBet = true;
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: false, freeBetOfferCategory: 'bet pack'} as any;
    component.selected = {freeBetOfferCategories: {freebetOfferCategory: 'bet pack'}} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).toHaveBeenCalledWith(null);
  });
  it('removeFreeBet and selection is disabled in case of SnB#1', () => {
    freeBetsFactory.isBetPack.and.returnValue(true);
    component.isStreamAndBet = true;
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: false, freeBetOfferCategory: 'bet pack'} as any;
    component.selected = {freeBetOfferCategories: {}} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).toHaveBeenCalledWith(null);
  });
  it('removeFreeBet and selection is disabled in case of SnB#2', () => {
    freeBetsFactory.isBetPack.and.returnValue(true);
    component.isStreamAndBet = true;
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: false} as any;
    component.selected = {freeBetOfferCategories: {freebetOfferCategory: 'bet pack'}} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).toHaveBeenCalledWith(null);
  });
  it('removeFreeBet and selection is disabled in case of SnB#3', () => {
    freeBetsFactory.isBetPack.and.returnValue(false);
    component.isStreamAndBet = true;
    component.selectedChange.emit = jasmine.createSpy('emit');
    component.selection = {disabled: false} as any;
    component.selected = {freeBetOfferCategories: {freebetOfferCategory: 'bet pack1'}} as any;
    component.removeFreeBet();
    expect(component.selectedChange.emit).toHaveBeenCalledWith(null);
  });

  

  it('should return freebet value', ()=> {
    freeBetsFactory.isBetPack.and.returnValue(false);
    freeBetsFactory.isFanzone.and.returnValue(false);
    component.selected = {value : 1, type: 'current'};
    expect(component.value).toEqual('£1 FREE BET ADDED');
  });
  it('should return fanzone value', ()=> {
    freeBetsFactory.isBetPack.and.returnValue(false);
    freeBetsFactory.isFanzone.and.returnValue(true);
    component.selected = {value : 1, type: 'current', freeBetOfferCategories: {freebetOfferCategory: 'FANZONE'}};
    expect(component.value).toEqual('£1 FANZONE FREE BET ADDED');
  });
  it('should return bettoken value', ()=> {
    freeBetsFactory.isBetPack.and.returnValue(true);
    freeBetsFactory.isFanzone.and.returnValue(false);
    component.selected = {value : 1, type: 'current', freeBetOfferCategories: {freebetOfferCategory: 'Bet Pack'}};
    expect(component.value).toEqual('£1 BET TOKEN ADDED');
  });

  describe('freebetButtonText in mobile view', ()=> {
    it('should display +TokenAndFreeBet', () => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(component.isMobile)).toBe('+TokenAndFreeBet');
    });
    it('should display AddFreeBet and fanzones', () => {
      component.isMobile = false;
      component.freeBets = [] as any[];
      component.betPackList = [] as any[];
      component.fanzoneList = [{'freeBetId': '122',
      'freeBetName': 'Fazone Football Bundle22','freebetOfferCategories': {
        'freebetOfferCategory':'Fanzone'},}] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });
    it('should display +FreeBet', () => {
      component.freeBets = [{}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(component.isMobile)).toBe('+FreeBet');
    });

    it('should display empty', () => {
      component.freeBets = [] as any[];
      component.betPackList = [] as any[];
      component.fanzoneList = [] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(component.isMobile)).toBe('');
    });

    it('should display +BetToken', () => {
      component.betPackList = [{}] as any[];
      component.isMobile = true;
      expect(component.freebetButtonText(component.isMobile)).toBe('+BetToken');
    });

    it('should return empty string', () => {
      component.betPackList = [] as any[];
      component.freeBets = [] as any[];
      expect(component.freebetButtonText()).toBe('');
    });

   it('should return BET TOKEN ADDED string', () => {
    freeBetsFactory.isBetPack.and.returnValue(true);
      component.selected = {
        value: 1,
        type: 'current',
        freebetOfferCategories: { freebetOfferCategory: 'Bet Pack' }
      };
    expect(component.removeFreebetButtonText()).toBe('BET TOKEN ADDED');
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
      component.fanzoneList = [{}] as any[];
      expect(component.freebetButtonText()).toBe('AddTokenAndFreeBet');
    });
    it('should display AddFreeBet and fanzones', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      component.betPackList = [] as any[];
      component.fanzoneList = [{'freeBetId': '122',
      'freeBetName': 'Fazone Football Bundle22','freebetOfferCategories': {
        'freebetOfferCategory':'Fanzone'},}] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });
    it('should display AddFreeBet and without fanzones', () => {
      component.isMobile = false;
      component.freeBets = [{'freeBetId': '122','freeBetName': 'Freebet Football Bundle22'}] as any[];
      component.betPackList = [] as any[];
      component.fanzoneList = [] as any[];
      expect(component.freebetButtonText()).toBe('AddFreeBet');
    });

    it('should display fanzone', () => {
      component.isMobile = false;
      component.freeBets = [] as any[];
      component.fanzoneList = [{'freeBetId': '122',
      'freeBetName': 'Fazone Football Bundle22','freebetOfferCategories': {
        'freebetOfferCategory':'Fanzone'},}] as any[];
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
      component.fanzoneList = [] as any[];
      component.freeBets = [] as any[];
      expect(component.freebetButtonText()).toBe('');
    });
  });

  describe('GA Tracking for Desktop view', () => {
    beforeEach(()=>{
      component.isMobile = false;
      component.showOnDigitKeyborad = false;
    });
    it('should Capture AddTokenAndFreeBet', () => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      component.isBetslip = true;
      component['triggerGtmService']();
      expect(component['getEventdetails']()).toBe('AddTokenAndFreeBet');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'betslip',
        eventAction: 'quick stake',
        eventLabel: 'free bet',
        eventDetails: component.freebetsConfig.addTokenAndFreeBet
      }));
    });

    it('should Capture AddFreeBet', () => {
      component.freeBets = [{}] as any[];
      component['triggerGtmService']();
      expect(component['getEventdetails']()).toBe('AddFreeBet');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'quick stake',
        eventLabel: 'free bet',
        eventDetails: component.freebetsConfig.addFreeBet
      }));
    });

    it('should Capture AddBetToken', () => {
      component.betPackList = [{}] as any[];
      expect(component['getEventdetails']()).toBe('AddBetToken');
    });

    it('should Capture value + BetTokenadded', () => {
      component.betPackList = [{}] as any[];
      component.selected = {value : 1, type: 'current', freeBetOfferCategories: {freebetOfferCategory: 'Bet Pack'}};
      freeBetsFactory.isBetPack.and.returnValue(true);

      expect(component['getEventdetails']()).toEqual('£1 BET TOKEN ADDED');
    });
  });

  describe('GA Tracking for Mobile', () => {
    beforeEach(()=>{
      component.isMobile = true;
      component.showOnDigitKeyborad = true;
    });
    it('should Capture AddTokenAndFreeBet', () => {
      component.freeBets = [{}] as any[];
      component.betPackList = [{}] as any[];
      expect(component['getEventdetails']()).toBe('+TokenAndFreeBet');
    });

    it('should Capture AddFreeBet', () => {
      component.freeBets = [{}] as any[];
      expect(component['getEventdetails']()).toBe('+FreeBet');
    });

    it('should Capture AddBetToken', () => {
      component.betPackList = [{}] as any[];
      component['triggerGtmService']();
      expect(component['getEventdetails']()).toBe('+BetToken');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'quick stake',
        eventLabel: 'free bet',
        eventDetails: component.freebetsConfig.plusToken
      }));
    });

    it('should Capture BetTokenAdded', () => {
      component.selected = {value : 1, type: 'current', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack'}};
      component.betPackList = [{}] as any[];
      freeBetsFactory.isBetPack.and.returnValue(true);
      component['triggerGtmService']();
      expect(component['getEventdetails']()).toBe('BET TOKEN ADDED');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'quick stake',
        eventLabel: 'free bet',
        eventDetails: component.freebetsConfig.betTokenAdded
      }));
    });
  });
});
