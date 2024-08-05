import { SBPriceOddsClassDirective } from "./sb-price-odds-class.directive";

describe('SBPriceOddsClassDirective', () => {
  let directive: SBPriceOddsClassDirective, betSlipSelectionsData, elementRef, pubsubService, coreToolsService, rendererService;

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
        REMOVE_FROM_SB_QUICKBET: 'REMOVE_FROM_SB_QUICKBET'
      }
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('uuid_value')
    };
    rendererService = {
      renderer: {
        removeClass: jasmine.createSpy()
      }
    };

    directive = new SBPriceOddsClassDirective(elementRef, pubsubService, coreToolsService, rendererService);
    directive.sbPriceOddsClass = [outcome, 'btn-small', 'bet-up', true];
  });

  describe('@ngOnInit', () => {
    it('should set Price Odds Class on Init', () => {
      expect(directive['activeClass']).toEqual('active');

      directive.ngOnInit();
      expect(coreToolsService.uuid).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledTimes(1);
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('class', 'snb-btn-bet active bet-up btn-small');
    });

    describe('should call subscribe callback function', () => {
      beforeEach(() => {
        pubsubService.subscribe.and.callFake((a, b, fn) => { fn({isAddToBetslip: false}); });
        spyOn<any>(directive, 'setClasses');
        directive.outcome = outcome;
      });

      it('should call setClasses', () => {
        // spyOn<any>(directive, 'checkOutcomeId').and.returnValue(false);
        directive.ngOnInit();

        expect(directive['setClasses']).toHaveBeenCalled();
      });

      it('should change active class', () => {
        directive.ngOnInit();

        expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(elementRef.nativeElement, 'active');
      });
    });
  });

  describe('@ngOnChanges', () => {
    it('should set setClasses on OnChanges', () => {
      const changes = {
        sbPriceOddsClass: {
          currentValue:[{id:'125825053'}],
          firstChange: false
        }
      } as any;
      directive.ngOnChanges(changes);
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('class', 'snb-btn-bet active bet-up btn-small');
    });

    it('should not set classes on OnChanges', () => {
      const changes = {
        sbPriceOddsClass: {
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
      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('sb-bet-432234-uuid_value');
    });
  });

  it('should set getOddsClasses', () => {
    spyOn<any>(directive, 'getOddsClasses').and.callThrough();
    directive['getOddsClasses'] = '';
    expect(directive['getOddsClasses']).toBe('snb-btn-bet active');
  });


});
