import { ToteFreeBetSelectDialogComponent } from './tote-free-bet-select-dialog.component';

    describe('ToteFreeBetSelectDialogComponent', () => {
      let deviceService, windowRef, changeDetectorRef, userService, GtmService, EventVideoStreamProviderService;
      let component: ToteFreeBetSelectDialogComponent;
    
      beforeEach(() => {
        deviceService = {};
        GtmService = { push: jasmine.createSpy('push') };
        EventVideoStreamProviderService = {isStreamAndBet: true};
        windowRef = {
          document: {
            body: {
              classList: {
                add: jasmine.createSpy('add')
              }
            }
          }
        };
        changeDetectorRef = {
          detectChanges: jasmine.createSpy('detectChanges')
        };
        userService = {};
        
        component = new ToteFreeBetSelectDialogComponent(deviceService, windowRef, userService, changeDetectorRef, GtmService, EventVideoStreamProviderService);
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
        it('both tabs available', () => {
          component.open();
      
          expect(component.selected).toBeNull();
          expect(component.freeBets).toBe(component.params.freeBets);
          // @ts-ignore
          expect(component.freeBets[0].id).toBe(2);
          // @ts-ignore
          expect(component.freeBets[1].id).toBe(1);
          expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
      
        it('free bets tab', () => {
          component.params.fanzoneList = [];
          component.open();
          expect(component.selected).toBeNull();
          expect(component.freeBets).toBe(component.params.freeBets);
      
          // @ts-ignore
          expect(component.freeBets[0].id).toBe(2);
          // @ts-ignore
          expect(component.freeBets[1].id).toBe(1);
          expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
    
        it('freebets and fanzone tab ',() => {
          component.params.freeBets =[];
          component.params.fanzoneList = [];
          component.open();
          expect(component.selected).toBeNull();
          expect(component.freeBets).toBe(component.params.freeBets);
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
          component.selected = {} as any;
          component.addFreeBet();
    
          expect(component.params.onSelect).toHaveBeenCalledWith(component.selected);
        });
    
        it('should call onSelect callback- isStreamAndBet true', () => {
          component.isStreamAndBet = true;
          component.selected = {} as any;
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
          component.selected = {} as any;
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
    
      it('removeFreeBet', () => {
        spyOn(component,'trackGADetails').and.callThrough();
        component.removeFreeBet();
        expect(component.trackGADetails).not.toHaveBeenCalled();
      });

      it('tabid', () => {
        component.tabid('activeTab');
        expect(component.activeTab).toBe('activeTab');
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
    