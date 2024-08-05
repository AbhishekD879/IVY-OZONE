import { Subject } from 'rxjs';
import { FreeBetSelectDialogComponent } from './free-bet-select-dialog.component';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';

describe('FreeBetSelectDialogComponent', () => {
  let deviceService, windowRef, changeDetectorRef, userService, localeService, elementRef, eventVideoStreamProviderService, elementMock, gtmService;
  let component: FreeBetSelectDialogComponent,
  freeBetsService;

  beforeEach(() => {
    deviceService = {};
    elementMock = {
      elMap: [],
      create: (tagName, attributes = {}) => {
        const el = {
          tagName: tagName,
          _eventListenersMap: {},
          addEventListener: jasmine.createSpy('addEventListener').and.callFake((e, cb) => {
            el._eventListenersMap[e] = cb;
          }),
          attributes: attributes,
          querySelector: jasmine.createSpy(),
          appendChild: jasmine.createSpy('appendChild'),
          classList: {contains: jasmine.createSpy('contains')},
          setAttribute: jasmine.createSpy('setAttribute').and.callFake((attrName, attrValue) => el.attributes[attrName] = attrValue),
          getAttribute: jasmine.createSpy('getAttribute').and.callFake(attrName => el.attributes[attrName]),
          remove: jasmine.createSpy('remove'),
        };
        elementMock.elMap.push(el);
        return el;
      }
    };
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        },
        createElement: jasmine.createSpy().and.callFake(tagName => elementMock.create(tagName)),
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    userService = {};
    elementRef = {};
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Ladbrokes'),
      toLowerCase: jasmine.createSpy()
    };

    eventVideoStreamProviderService = {
      isStreamAndBet: true,
      snbVideoFullScreenExitSubj: new Subject<void>(),
    };
    gtmService = { push: jasmine.createSpy('push') };

    freeBetsService = {
      isBetPack: jasmine.createSpy('isBetPack').and.returnValue(true)
    }


    component = new FreeBetSelectDialogComponent(deviceService, windowRef, userService, localeService, elementRef, changeDetectorRef, eventVideoStreamProviderService, gtmService, freeBetsService);
    component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }, close: jasmine.createSpy('close') };
    component.params = {
      freeBets: [{
        id: 1,
        freebetTokenExpiryDate: 321
      }, {
        id: 2,
        freebetTokenExpiryDate: 123
      }, {
        id: 3,
        freebetTokenExpiryDate: 421
      }],
      fanzoneList: [{
        id: 111,
        freebetTokenExpiryDate: 321,
        freebetOfferCategories: {
          freebetOfferCategory: 'Fanzone'
        }
      }, {
        id: 112,
        freebetTokenExpiryDate: 123,
        freebetOfferCategories: {
          freebetOfferCategory: 'Fanzone'
        }
      }],
      betPackList: [{
        id: 11,
        freebetTokenExpiryDate: 321,
        freebetOfferCategories: {
          freebetOfferCategory: 'Bet Pack'
        }
      }, {
        id: 22,
        freebetTokenExpiryDate: 123,
        freebetOfferCategories: {
          freebetOfferCategory: 'Bet Pack'
        }
      }],
      onSelect: jasmine.createSpy('onSelect')
    };
  });
  describe('open', ()=>{
    it('both tabs available, withArgs(vjs-fullscreen)', () => {
      const element = windowRef.document.createElement('test-element');
      element.classList.contains.and.returnValue(true);
      element.classList.contains.withArgs('vjs-fullscreen').and.returnValue(true);
      windowRef.document.querySelector.and.returnValue(element);
      const closeDialogSpy = spyOn(component,'closeDialog');
      component.open();
      eventVideoStreamProviderService.snbVideoFullScreenExitSubj.next();
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.fanzoneList).toBe(component.params.fanzoneList);
      expect(component.betPackList).toBe(component.params.betPackList);
      // @ts-ignore
      expect(component.freeBets[0].id).toBe(2);
      // @ts-ignore
      expect(component.freeBets[1].id).toBe(1);
       // @ts-ignore
       expect(component.fanzoneList[0].id).toBe(112);
       // @ts-ignore
       expect(component.fanzoneList[1].id).toBe(111);
      // @ts-ignore
      expect(component.betPackList[0].id).toBe(22);
      // @ts-ignore
      expect(component.betPackList[1].id).toBe(11);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('both tabs available, withArgs(vjs-fullscreen-control)', () => {
      const element = windowRef.document.createElement('test-element');
      element.classList.contains.and.returnValue(false);
      element.classList.contains.withArgs('vjs-fullscreen-control').and.returnValue(true);
      windowRef.document.querySelector.and.returnValue(element);
      const closeDialogSpy = spyOn(component,'closeDialog');
      component.open();
      eventVideoStreamProviderService.snbVideoFullScreenExitSubj.next();
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.fanzoneList).toBe(component.params.fanzoneList);
      expect(component.betPackList).toBe(component.params.betPackList);
      // @ts-ignore
      expect(component.freeBets[0].id).toBe(2);
      // @ts-ignore
      expect(component.freeBets[1].id).toBe(1);
       // @ts-ignore
       expect(component.fanzoneList[0].id).toBe(112);
       // @ts-ignore
       expect(component.fanzoneList[1].id).toBe(111);
      // @ts-ignore
      expect(component.betPackList[0].id).toBe(22);
      // @ts-ignore
      expect(component.betPackList[1].id).toBe(11);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  
    it('free bets tab', () => {
      component.params.fanzoneList = [];
      component.open();
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.fanzoneList).toBe(component.params.fanzoneList);
      // @ts-ignore
      expect(component.freeBets[0].id).toBe(2);
      // @ts-ignore
      expect(component.freeBets[1].id).toBe(1);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  
    it('fanzone tab', () => {
      component.params.betPackList = [];
      component.open();
  
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.fanzoneList).toBe(component.params.fanzoneList);
      // @ts-ignore
      expect(component.fanzoneList[0].id).toBe(112);
      // @ts-ignore
      expect(component.fanzoneList[1].id).toBe(111);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('bet tokens tab', () => {
      component.params.freeBets = [];
      component.open();
  
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.betPackList).toBe(component.params.betPackList);
      // @ts-ignore
      expect(component.betPackList[0].id).toBe(22);
      // @ts-ignore
      expect(component.betPackList[1].id).toBe(11);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('freebets and fanzone tab ',() => {
      component.params.freeBets =[];
      component.params.fanzoneList = [];
      component.open();
      expect(component.selected).toBeNull();
      expect(component.freeBets).toBe(component.params.freeBets);
      expect(component.fanzoneList).toBe(component.params.fanzoneList);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    })
    it('free bets undefined', ()=>{
      component.params.freeBets = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });

    it('fanzone undefined', ()=>{
      component.params.fanzoneList = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });
    it('bet tokens undefined', ()=>{
      component.params.betPackList = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });

    it('free bets and  bet tokens undefined', ()=>{
      component.params.freeBets = undefined;
      component.params.betPackList = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });
    it('free bets  and fanzone undefined', ()=>{
      component.params.freeBets = undefined;
      component.params.fanzoneList = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });
    it('free bets  and fanzone and betPack undefined', ()=>{
      component.params.freeBets = undefined;
      component.params.fanzoneList = undefined;
      component.params.betPackList = undefined;
      component.open();
      expect(component.selected).toBe(null);
    });
  })

  it('freeBetClick', () => {
    const freeBet: any = {};
    component.freeBetClick(freeBet, 'betPack');
    expect(component.selected).toBe(freeBet);
  });

  describe('addFreeBet', () => {
    it('should call onSelect callback', () => {
      component.selected = {} as IFreeBet;
      component.addFreeBet();

      expect(component.params.onSelect).toHaveBeenCalledWith(component.selected);
    });

    it('should call onSelect callback- isStreamAndBet true', () => {
      component.isStreamAndBet = true;
      component.selected = {} as IFreeBet;
      component.addFreeBet();

      expect(component.params.onSelect).toHaveBeenCalledWith(component.selected);
    });

    it('should not call onSelect callback', () => {
      component.addFreeBet();

      expect(component.params.onSelect).not.toHaveBeenCalled();
    });

    it('should call onSelect callback with free bet - apply', () => {
      component.isStreamAndBet = true;
      component['freeBetsService'] = {
        isBetPack: jasmine.createSpy('isBetPack').and.returnValue(false)
      }  as any;
      component.isBetToken = true;
      component.selected = {} as IFreeBet;
      spyOn(component,'trackGADetails').and.callThrough();
      component.addFreeBet();
      expect(component.trackGADetails).toHaveBeenCalled();
    });
  });

  it('trackByIndex', () => {
    const index = 5;
    const result = component.trackByIndex(index);
    expect(result).toBe(index);
  });

  it('tabid', () => {
    component.tabid('activeTab');
    expect(component.activeTab).toBe('activeTab');
  });

  it('removeFreeBet', () => {
    spyOn(component,'trackGADetails').and.callThrough();

    component.removeFreeBet();
    
    expect(component.trackGADetails).not.toHaveBeenCalled();
  });

  it('closeDialog', () => {
    component.isStreamAndBet = true;
    component.closeDialog(true);
    
    expect(component.dialog.close).toHaveBeenCalled();
  });

  it('closeDialog with both and tabs are same', () => {
    component.isStreamAndBet = true;
    component.tab = 'both';
    component.closeDialog(true);
    
    expect(component.dialog.close).toHaveBeenCalled();
  });

  it('closeDialog with both and tabs are not same', () => {
    component.isStreamAndBet = true;
    component.tab = 'betToken';
    component.closeDialog(true);
    
    expect(component.dialog.close).toHaveBeenCalled();
  });
  
  it('closeDialog with default parameter', () => {
    component.isStreamAndBet = true;
    component.tab = 'betToken';
    component.closeDialog();
    
    expect(component.dialog.close).toHaveBeenCalled();
  });
});
