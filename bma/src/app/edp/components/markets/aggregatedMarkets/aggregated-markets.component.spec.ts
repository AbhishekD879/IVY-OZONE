import { ISportEvent } from "@core/models/sport-event.model";
import { IMarket } from "@core/models/market.model";
import { AggregatedMarketsComponent } from "./aggregated-markets.component";

describe('AggregagtedMarketsComponent', ()=>{
    let accordionService,
    gtmService,
    changeDetectorRef,
    pubSubService,
    eventService,
    sportEventPageService,
    templateService,
    cacheEventService,
    filtersService,
    event,
    component: AggregatedMarketsComponent;

    const eventEntity = {
        markets: [
          { 
            id: '1', 
            name: 'Over/Under Goals',
            marketMeaningMinorCode: 'HL',
            outcomes: [{
              name: 'Over', id: 1, outcomeMeaningMinorCode: 1
            }] },
          { id: '2', name: 'Goal Scorer', outcomes: [] },
          { id: '3', name: 'Spread', outcomes: [{id: 1}] },
          { id: '5', name: 'scorer'}
      ]
    } as any;

    beforeEach(()=>{
        accordionService = {
            saveStateDependsOnParams: jasmine.createSpy(),
            getLocationStates: jasmine.createSpy(),
            getState: jasmine.createSpy()
          };
          gtmService = {
            push: jasmine.createSpy()
          };
          pubSubService = {
            subscribe: jasmine.createSpy('subscribe'),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: {
              WS_EVENT_UPDATE: 'WS_EVENT_UPDATE'
            }
          };
      
          changeDetectorRef = {
            markForCheck: jasmine.createSpy('markForCheck'),
            detectChanges: jasmine.createSpy('detectChanges')
          };

          eventService = {
            getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve(eventEntity))
          };

          sportEventPageService = {
            transformMarkets: jasmine.createSpy('transformMarkets')
          };

          templateService = {
            getMarketViewType: jasmine.createSpy('getMarketViewType'),
            getMarketWithSortedOutcomes: jasmine.createSpy('getMarketWithSortedOutcomes'),
            sortOutcomesByPriceAndDisplayOrder: jasmine.createSpy('sortOutcomesByPriceAndDisplayOrder'),
            getCorrectedOutcomeMeaningMinorCode: jasmine.createSpy('getCorrectedOutcomeMeaningMinorCode')
          };

          cacheEventService = {
            storedData: {
                event: {
                    data: [eventEntity]
                }
            }
          };

          filtersService = {
            groupBy: jasmine.createSpy('groupBy')
          };

          event = {
            preventDefault: jasmine.createSpy('preventDefault'),
            stopPropagation: jasmine.createSpy('stopPropagation')
          };

          component = new AggregatedMarketsComponent(
            accordionService,
            gtmService,
            changeDetectorRef,
            pubSubService,
            eventService,
            sportEventPageService,
            templateService,
            cacheEventService,
            filtersService
          );
          component.eventEntity = eventEntity;
          component.isExpanded = true;
    });
    describe('ngOnInit', ()=>{
      it('should detect changes (OUTCOME_UPDATED)', () => {
        component.templateMarketGroup = {
          marketIds: ['1', '2']
        } as any;
        component['init'] = jasmine.createSpy('init');
        pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'UPDATE_OUTCOMES_FOR_MARKET' && cb({id: '7678687'} as IMarket));
        component.ngOnInit();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(pubSubService.subscribe).toHaveBeenCalledWith('accSocketUpdate', 'WS_EVENT_UPDATE', jasmine.any(Function));
        expect(pubSubService.subscribe).toHaveBeenCalledWith('aggregatedMarkets', 'UPDATE_OUTCOMES_FOR_MARKET', jasmine.any(Function));
      
      });
    });

    it('ngOnDestroy', ()=>{
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });
    describe('ngOnChanges', ()=>{
      beforeEach(()=>{
        component['event'] = {id: 1, name: 'Home v Away'} as ISportEvent;
        component.isExpanded = true;
        component['isOnceExpanded'] = true;
      });
      it('ngOnChanges isExpanded', ()=>{
        component.isExpanded = true;
        component['isOnceExpanded'] = false;
        component.templateMarketGroup = {
          marketIds: ['1', '2', '3']
        } as any;
        component.ngOnChanges();
        expect(eventService.getEvent).toHaveBeenCalled();
      });

      it('ngOnChanges accordion expanded once', ()=>{
        
        component.templateMarketGroup = {
          marketIds: ['1', '2', '3', '4', '5']
        } as any;
        component.ngOnChanges();
        expect(eventService.getEvent).toHaveBeenCalled(); 
      });

      it('should add fake outcome for HL markets', ()=>{
        component.templateMarketGroup = {
          marketIds: ['1', '2']
        } as any;
        component['event'] = {id: 1, name: 'Home v Away'} as ISportEvent;

        templateService.getMarketWithSortedOutcomes.and.returnValues([{
          name: 'Over', id: 1, outcomeMeaningMinorCode: 1
        }], [{name: 'Under', id: 2, outcomeMeaningMinorCode: 3}]);
        cacheEventService.storedData.event.data = [{id: '1',
          markets: [
          { 
            id: '1', 
            name: 'Over/Under Goals',
            marketMeaningMinorCode: 'HL',
            outcomes: [{
              name: 'Over', id: 1, outcomeMeaningMinorCode: 1
            }]},
          { 
            id: '2', 
            name: 'Over/Under Goals',
            marketMeaningMinorCode: 'HL',
            outcomes: [{
              name: 'Under', id: 2, outcomeMeaningMinorCode: 3
            }]}
        ]}];
        component.ngOnChanges();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled(); 
      });

      it('should add fake outcome for WH markets', ()=>{
        component.templateMarketGroup = {
          marketIds: ['1', '2']
        } as any;
        component['event'] = {id: 1, name: 'Home vs Away'} as ISportEvent;
        templateService.getMarketWithSortedOutcomes.and.returnValues([{
          name: 'Home', id: 1, outcomeMeaningMinorCode: 1
        }], [{name: 'Away', id: 2, outcomeMeaningMinorCode: 3}]);
        cacheEventService.storedData.event.data = [{
            id: '1',
            name: 'Home v Away',
            markets: [
            { 
              id: '1', 
              name: 'Spread',
              marketMeaningMinorCode: 'WH',
              outcomes: [{
                name: 'Home', id: 1, outcomeMeaningMinorCode: 1
              }]},
            { 
              id: '2', 
              name: 'Spread',
              marketMeaningMinorCode: 'WH',
              outcomes: [{
                name: 'Away', id: 2, outcomeMeaningMinorCode: 3
              }]}
            ]
        }];
        component.ngOnChanges();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled(); 
      });
      it('should add fake outcome for MH markets', ()=>{
        component.templateMarketGroup = {
          marketIds: ['1', '2', '3']
        } as any;
        templateService.getMarketWithSortedOutcomes.and.returnValues([{
          name: 'Home', id: 1, outcomeMeaningMinorCode: 1
        }], [{name: 'Away', id: 2, outcomeMeaningMinorCode: 3}], 
        [{name: 'Tie', id: 2, outcomeMeaningMinorCode: 2}]);
        cacheEventService.storedData.event.data = [{
            id: '1',
            name: 'Home v Away',
            markets: [
            { 
              id: '1', 
              name: 'Handicap 3-way',
              marketMeaningMinorCode: 'MH',
              outcomes: [{
                name: 'Home', id: 1, outcomeMeaningMinorCode: 1
              }]},
            { 
              id: '2', 
              name: 'Handicap 3-way',
              marketMeaningMinorCode: 'MH',
              outcomes: [{
                name: 'Away', id: 2, outcomeMeaningMinorCode: 3
              }]},
            { 
              id: '3', 
              name: 'Handicap 3-way',
              marketMeaningMinorCode: 'MH',
              outcomes: [{
                name: 'Tie', id: 2, outcomeMeaningMinorCode: 2
              }]}
            ]
        }];
        component.ngOnChanges();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled(); 
      });

      it('ngOnChanges accordion expanded once', ()=>{
        component.isExpanded = true;
        component.templateMarketGroup = {
          marketIds: []
        } as any;
        component.ngOnChanges();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled(); 
      });
    });

    describe('toggled', ()=>{
      beforeEach(()=>{
        component.templateMarketGroup = {marketIds: ['1']} as any;
      });
      it('toggled (disabled)', () => {
        component.disabled = true;
        component.setState = jasmine.createSpy();
    
        component.toggled(event);
        expect(component.setState).not.toHaveBeenCalled();
        expect(event.preventDefault).not.toHaveBeenCalled();
        expect(event.stopPropagation).not.toHaveBeenCalled();
      });
    
      it('toggled (enabled)', () => {
        component.disabled = false;
        component.setState = jasmine.createSpy();
        component.trackLabel = 'lbl';
        component.trackCategory = 'cat';
        component.isExpanded = true;
        component.func.emit = jasmine.createSpy();
    
        component.toggled(event);
    
        expect(component.setState).toHaveBeenCalledWith(false);
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          event: 'trackEvent',
          eventCategory: component.trackCategory,
          eventAction: 'show',
          eventLabel: component.trackLabel
        });
        expect(component.func.emit).toHaveBeenCalledWith(true);
        expect(event.preventDefault).toHaveBeenCalled();
        expect(event.stopPropagation).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
    
      it('toggled (enabled) for undefined emit function', () => {
        component.disabled = false;
        component.setState = jasmine.createSpy();
        component.trackLabel = 'lbl';
        component.trackCategory = 'cat';
        component.isExpanded = true;
        component.func = undefined;
    
        component.toggled(event);
        expect(component.func).toBeUndefined();
      });
    });
    
    describe('init', ()=>{
      it('should initialize markets and sort outcomes', ()=>{
        component.eventEntity = {
          id: '10',
          name: 'Test1',
          markets: [{
            id: '20',
            name: 'Total Goals',
            rawHandicapValue: 0.3,
            templateMarketName: 'Total Goals',
            outcomes: [
              {id: '30', name: 'over'},
              {id: '31', name: 'under'}
            ]
          }, {
            id: '30',
            name: 'YourCall Specials',
            templateMarketName: 'YourCall Specials',
            rawHandicapValue: 0.34,
            outcomes: [
              {id: '30', name: 'over'},
              {id: '31', name: 'under'}
            ],
            hidden: true
          }]
        };
        templateService.getMarketWithSortedOutcomes.and.returnValue([
          {id: '30', name: 'over'}, {id: '40', name: 'under'}
        ])
        component.templateMarketGroup = {
          marketIds: ['20', '30']
        } as any;
        cacheEventService.storedData.event.data = [component.eventEntity];
        component['init']();
        expect(sportEventPageService.transformMarkets).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(templateService.getMarketViewType).toHaveBeenCalled();
        expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalled();
        expect(templateService.sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();

        component.eventEntity = {
          id: '10',
          name: 'Test1',
          markets: [{
            id: '20',
            name: 'Total Goals',
            outcomes: [
              {id: '30', name: 'over'},
              {id: '31', name: 'under'}
            ]
          }]
        };
        cacheEventService.storedData.event.data = [component.eventEntity];
        component['init']();
        expect(sportEventPageService.transformMarkets).toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(templateService.getMarketViewType).toHaveBeenCalled();
        expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalled();
      });

      it('should add fake outcome for over/under markets', ()=>{
        component.eventEntity = {
          id: '10',
          name: 'Test1',
          markets: [{
            id: '20',
            name: 'Total Goals',
            marketMeaningMinorCode: 'HL',
            outcomes: [
              {id: '30', name: 'over', outcomeMeaningMinorCode: 1}
            ]
          }, {id: '30',
          name: 'Total Goals',
          marketMeaningMinorCode: 'HL',
          outcomes: [
            {id: '40', name: 'under', outcomeMeaningMinorCode: 3}
          ]}]
        };
        component.templateMarketGroup = {
          marketIds: ['20', '30']
        } as any;
        cacheEventService.storedData.event.data = [component.eventEntity];
        templateService.getMarketWithSortedOutcomes.and.returnValue([
          {id: '30', name: 'over'}, {id: '40', name: 'under'}
        ])
        component['init']();
        expect(component.markets[0].outcomes.length).toEqual(2);
        expect(component.markets[1].outcomes.length).toEqual(2);
      });

      it('should add fake outcome for handicap WW markets', ()=>{
        component.eventEntity = {
          id: '10',
          name: 'home v away',
          markets: [{
            id: '20',
            name: 'Total Goals',
            marketMeaningMinorCode: 'WH',
            outcomes: [
              {id: '30', name: 'home', outcomeMeaningMinorCode: 1}
            ]
          }, {
            id: '30',
            name: 'Total Goals',
            marketMeaningMinorCode: 'WH',
            outcomes: [
              {id: '40', name: 'away', outcomeMeaningMinorCode: 3}
            ]
          }]
        };
        component.templateMarketGroup = {
          marketIds: ['20', '30']
        } as any;
        cacheEventService.storedData.event.data = [component.eventEntity];
        templateService.getMarketWithSortedOutcomes.and.returnValue([
          {id: '30', name: 'home'}, {id: '40', name: 'away'}
        ])
        component['init']();
        expect(component.markets[0].outcomes.length).toEqual(2);
        expect(component.markets[1].outcomes.length).toEqual(2);
      });

      it('should add fake outcome for handicap WDW markets', ()=>{
        component.eventEntity = {
          id: '10',
          name: 'home vs away',
          markets: [{
            id: '20',
            name: 'Total Goals',
            marketMeaningMinorCode: 'MH',
            outcomes: [
              {id: '30', name: 'home', outcomeMeaningMinorCode: 1}
            ]
          }, {
            id: '30',
            name: 'Total Goals',
            marketMeaningMinorCode: 'MH',
            outcomes: [
              {id: '40', name: 'away', outcomeMeaningMinorCode: 3}
            ]
          }]
        };
        component.templateMarketGroup = {
          marketIds: ['20', '30']
        } as any;
        cacheEventService.storedData.event.data = [component.eventEntity];
        templateService.getMarketWithSortedOutcomes.and.returnValue([
          {id: '30', name: 'home'}, {id: '40', name: 'away'}, {id: '50', name: 'tie'}
        ])
        component['init']();
        expect(component.markets[0].outcomes.length).toEqual(3);
        expect(component.markets[1].outcomes.length).toEqual(3);
      });

      it('when the storedData is undefined', ()=>{
        cacheEventService.storedData.event.data = undefined;
        component['init']();
        expect(sportEventPageService.transformMarkets).toHaveBeenCalled();
      })

      it('when the eventEntity is undefined', ()=>{
        cacheEventService.storedData.event.data = [];
        component['init']();
        expect(sportEventPageService.transformMarkets).toHaveBeenCalled();
      })
      
      it('when the markets are undefined', ()=>{
        component.eventEntity = {
          id: '10',
          name: 'Test1'
        };
        component.templateMarketGroup = {
          marketIds: ['20']
        } as any;
        cacheEventService.storedData.event.data = [component.eventEntity];
        component['init']();
        expect(sportEventPageService.transformMarkets).toHaveBeenCalled();
      });
    });
    

    it('toggleShowAll', () => {
      component.showAll = false;
      component.toggleShowAll();
      expect(component.showAll).toEqual(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    describe('selectedMarkets', ()=> {
      it('selectedMarkets should return all markets in array when showAll is true', ()=>{
        component.showAll = true;
        expect(component.selectedMarkets(eventEntity.markets).length).toEqual(component.eventEntity.markets.length);
      });
      it('selectedMarkets should return selectedCount number of markets when showAll is false', ()=>{
        component.eventEntity.markets = [{id:1}, {id:2}, {id:3}, {id:4}, {id:5}, {id:6}, {id:7}, {id:8}, {id:9}, {id:10}];
        component.showAll = false;
        expect(component.selectedMarkets(eventEntity.markets).length).toEqual(8);
      });

      describe('showLessButton', () => {

        it('should be false', () => {
          component.markets = [{id:1}, {id:2}] as any;
          expect(component.showLessButton).toBe(false);
        });

        it('should be true when markets length is greater than selectedCount', () => {
          component.markets = [{id:1}, {id:2}, {id:3}, {id:4}, {id:5}, {id:6}, {id:7}, {id:8}, {id:9}, {id:10}] as any;
          expect(component.showLessButton).toBe(true);
        });
      });
    });

    describe('getOutcomeNames', ()=>{

      it('should return outcomeNames', ()=>{
        component.markets = [{id: 1, outcomes: [{name: 'Celtics'}, {name: 'Mets'}]}] as any;
        const result = ['Celtics', 'Mets'];
        expect(component.getOutcomeNames()).toEqual(result);
      });

      it('should remove handicap value and return outcomeNames', ()=>{
        component.markets = [{id: 1, outcomes: [{name: 'Over (20.5)'}, {name: 'Under (20.5)'}]}] as any;
        const result = ['Over', 'Under'];
        expect(component.getOutcomeNames()).toEqual(result);
      });
    });
    
    it('getTrackById should track by entity.id', () => {
      const entity = {
        id: 111
      };
  
      const result = component.getTrackById(0, entity);
      expect(result).toBe('111_0');
    });

    it('isAccordionExpanded', ()=>{
      component.markets = [{
        viewType: 'Correct Score'
      }] as any;
      component.index = 1;
      expect(component.isAccordionExpanded()).toBeTruthy();

      component.markets = [{
        viewType: 'Scorer'
      }] as any;
      component.index = 2;
      expect(component.isAccordionExpanded()).toBeFalsy();

      component.markets = [{
        viewType: 'WDW'
      }] as any;
      component.index = 0;
      expect(component.isAccordionExpanded()).toBeFalsy();
    });
})