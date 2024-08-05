import { PriceOddsClassDirective } from '@shared/components/priceOddsButton/price-odds-class.directive';

describe('PriceOddsClassDirective', () => {
  let directive: PriceOddsClassDirective, betSlipSelectionsData, elementRef, pubsubService, coreToolsService, rendererService;

  const outcome = {
    name: 'Outcome',
    id: '432234',
    prices: [{
      priceType: 'LP'
    }]
  } as any;

  beforeEach(() => {
    betSlipSelectionsData = {
      getSelectionsByOutcomeId: jasmine.createSpy('getSelectionsByOutcomeId').and.returnValue([{}])
    };
    elementRef = {
      nativeElement: {
        setAttribute: jasmine.createSpy('setAttribute')
      }
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        BETSLIP_SELECTIONS_UPDATE: 'BETSLIP_SELECTIONS_UPDATE',
        ADD_TO_QUICKBET: 'ADD_TO_QUICKBET',
        REMOVE_FROM_QUICKBET: 'REMOVE_FROM_QUICKBET'
      }
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('uuid_value')
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy(),
        removeClass: jasmine.createSpy()
      }
    };

    directive = new PriceOddsClassDirective(betSlipSelectionsData, elementRef, pubsubService, coreToolsService, rendererService);
    directive.priceOddsClass = [outcome, 'btn-small', 'bet-up'];
  });

  describe('@ngOnInit', () => {
    it('should set Price Odds Class on Init', () => {
      expect(directive['activeClass']).toEqual('active');

      directive.ngOnInit();
      expect(coreToolsService.uuid).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledTimes(4);
      expect(pubsubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'BETSLIP_SELECTIONS_UPDATE', jasmine.any(Function));
      expect(pubsubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'ADD_TO_QUICKBET', jasmine.any(Function));
      expect(pubsubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'REMOVE_FROM_QUICKBET', jasmine.any(Function));
      expect(betSlipSelectionsData.getSelectionsByOutcomeId).toHaveBeenCalled();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('class', 'btn-bet active bet-up btn-small');
    });

    describe('should call subscribe callback function', () => {
      beforeEach(() => {
        pubsubService.subscribe.and.callFake((a, b, fn) => { fn({isAddToBetslip: false}); });
        spyOn<any>(directive, 'setClasses');
        directive.outcome = outcome;
      });

      it('should call setClasses', () => {
        spyOn<any>(directive, 'checkOutcomeId').and.returnValue(false);
        directive.ngOnInit();

        expect(directive['setClasses']).toHaveBeenCalled();
        expect(directive['checkOutcomeId']).toHaveBeenCalledTimes(2);
      });

      it('should not change active class', () => {
        pubsubService.subscribe.and.callFake((a, b, fn) => { fn({isAddToBetslip: true}); });
        spyOn<any>(directive, 'checkOutcomeId').and.returnValue(false);
        directive.ngOnInit();

        expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
        expect(rendererService.renderer.removeClass).not.toHaveBeenCalled();
      });

      it('should change active class', () => {
        spyOn<any>(directive, 'checkOutcomeId').and.returnValue(true);
        directive.ngOnInit();

        expect(rendererService.renderer.addClass).toHaveBeenCalledWith(elementRef.nativeElement, 'active');
        expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(elementRef.nativeElement, 'active');
      });
    });
  });

  describe('@ngOnChanges', () => {
    it('should set setClasses on OnChanges', () => {
      const changes = {
        priceOddsClass: {
          currentValue:[{id:'125825053'}],
          firstChange: false
        }
      } as any;
      directive.ngOnChanges(changes);
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('class', 'btn-bet active bet-up btn-small');
    });

    it('should not set classes on OnChanges', () => {
      const changes = {
        priceOddsClass: {
          currentValue:[{id:'125825053'}],
          firstChange: false
        },
        priceOddsDisabled: {
          currentValue:[{id:'125825053'}],
          firstChange: true
        }
      } as any;
      directive['setClasses'] = jasmine.createSpy('setClasses');
      directive.ngOnChanges(changes);
    });
  });

  describe('@ngOnDestroy', () => {
    it('should destroy listeners', () => {
      directive.ngOnInit();
      directive.ngOnDestroy();
      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('bet-432234-uuid_value');
    });
  });

  describe('@checkOutcomeId', () => {
    beforeEach(() => {
      directive.outcome = outcome;
    });

    it('should return false if not selection', () => {
      expect(directive['checkOutcomeId'](null)).toEqual(false);
    });

    it('should return false if no outcomes', () => {
      const selection = {
        outcomeId: null,
        outcomes: []
      };
      expect(directive['checkOutcomeId'](selection as any)).toEqual(false);
    });

    it('should return false if outcomeId is different', () => {
      const selection = {
        outcomeId: '1234',
      };

      expect(directive['checkOutcomeId'](selection as any)).toEqual(false);
    });

    it('should return false if selection outcomes empty and no outcomeId', () => {
      const selection = {
        outcomes: []
      };

      expect(directive['checkOutcomeId'](selection as any)).toEqual(false);
    });

    it('should return false if selection outcomes is different', () => {
      const selection = {
        outcomes: [{
          id: '1234'
        }]
      };

      expect(directive['checkOutcomeId'](selection as any)).toEqual(false);
    });

    it('should return true if outcomeId is the same', () => {
      const selection = {
        outcomeId: '432234',
      };

      expect(directive['checkOutcomeId'](selection as any)).toEqual(true);
    });

    it('should return true if selection outcomes is the same', () => {
      const selection = {
        outcomes: [{
          id: '432234'
        }]
      };

      expect(directive['checkOutcomeId'](selection as any)).toEqual(true);
    });
  });
});
