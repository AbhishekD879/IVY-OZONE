import { EventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('EventMarketsComponent', () => {
  let component: EventMarketsComponent,
    templateService,
    pubSubService,
    routingHelperService,
    seoDataService,
    sportService,
    changeDetectorRef,
    sportService1;

  const eventEntity = {
    id: 1,
    name: 'Event Name',
    eventStatusCode: 'A',
    isActive: true,
    markets: [
      {
        id: '1',
        name: 'Market Name',
        isLpAvailable: true,
        cashoutAvail: 'Y',
        outcomes: [
          {
            id: '1',
            isActive: true,
            isAvailable: true,
            marketId: '1',
            name: 'Outcome Name 1',
            outcomeStatusCode: 'A',
            prices: [
              {
                id: '1',
                displayOrder: '1',
                isActive: true,
                priceDec: 1.4,
                priceDen: 10,
                priceNum: 1,
                priceType: 'LP'
              }
            ]
          },
          {
            id: '2',
            isActive: true,
            isAvailable: true,
            marketId: '1',
            name: 'Outcome Name 2',
            outcomeStatusCode: 'A',
            prices: [
              {
                id: '1',
                displayOrder: '1',
                isActive: true,
                priceDec: 1,
                priceDen: 2,
                priceNum: 1,
                priceType: 'LP'
              }
            ]
          }
        ]
      }
    ]
  };
  
  beforeEach(() => {
    templateService = {
      genTerms: jasmine.createSpy('genTerms')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => { cb(); }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url'),
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    sportService1 = {
      getById: jasmine.createSpy('getById').and.returnValue(observableOf({event: [eventEntity]}))
    };
    sportService = {
      setConfig: jasmine.createSpy('setConfig').and.returnValue(sportService1)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new EventMarketsComponent(
      templateService,
      pubSubService,
      routingHelperService,
      seoDataService,
      sportService,
      changeDetectorRef
    );
    component.eventEntity = eventEntity as any;
    component.panelType = 'outright';
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit methods', () => {
    component.panelType = 'enhancedMultiple';
    const newEntity = {
      id: 1,
      markets: [{
        displayOrder: 3,
        outcomes: [{
          displayOrder: 2,
          prices: [{
            priceDec: 54
          }]
        }, {
          displayOrder: 1,
          prices: [{
            priceDec: 21
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 99
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 23
          }]
        }, {
          displayOrder: 4,
          name: 'b',
          prices: [{
            priceDec: 11
          }]
        }, {
          displayOrder: 4,
          name: 'a',
          prices: [{
            priceDec: 11
          }]
        }]
      }, {
        displayOrder: 2,
        outcomes: [{
          prices: []
        }]
      }, {
        displayOrder: 5,
        outcomes: [{}]
      }]
    } as any;
    component.fetchOutcomes = true;
    component.eventEntity = newEntity;
    sportService1 = {
      getById: jasmine.createSpy('getById').and.returnValue(observableOf({event: [ newEntity ]}))
    };
    component['sportService'] = {
      setConfig: jasmine.createSpy('setConfig').and.returnValue(sportService1)
    } as any;
    const result = {
      id: 1,
      markets: [{
        displayOrder: 2,
        outcomes: [{
          prices: []
        }]
      }, {
        displayOrder: 3,
        outcomes: [{
          displayOrder: 1,
          prices: [{
            priceDec: 21
          }]
        }, {
          displayOrder: 2,
          prices: [{
            priceDec: 54
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 23
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 99
          }]
        }, {
          displayOrder: 4,
          name: 'a',
          prices: [{
            priceDec: 11
          }]
        }, {
          displayOrder: 4,
          name: 'b',
          prices: [{
            priceDec: 11
          }]
        }]
      }, {
        displayOrder: 5,
        outcomes: [{}]
      }]
    } as any;
    spyOn(component, 'goToSeo');
    component.ngOnInit();

    expect(component.showTerms).toEqual(false);
    expect(component.goToSeo).toHaveBeenCalled();
    expect(component.limit).toEqual(undefined);
    expect(component.isShowAllActive).toBeFalsy();
    expect(component.eventEntity).toEqual(result);

  });
  it('should call ngOnInit methods with no event', () => {
    component.panelType = 'enhancedMultiple';
    component.fetchOutcomes = true;
    const newEntity = {
      id: 1,
      markets: [{
        displayOrder: 3,
        outcomes: [{
          displayOrder: 2,
          prices: [{
            priceDec: 54
          }]
        }, {
          displayOrder: 1,
          prices: [{
            priceDec: 21
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 99
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 23
          }]
        }, {
          displayOrder: 4,
          name: 'b',
          prices: [{
            priceDec: 11
          }]
        }, {
          displayOrder: 4,
          name: 'a',
          prices: [{
            priceDec: 11
          }]
        }]
      }, {
        displayOrder: 2,
        outcomes: [{
          prices: []
        }]
      }, {
        displayOrder: 5,
        outcomes: [{}]
      }]
    } as any;

    component.eventEntity = newEntity;
    sportService1 = {
      getById: jasmine.createSpy('getById').and.returnValue(observableOf([ newEntity ]))
    };
    component['sportService'] = {
      setConfig: jasmine.createSpy('setConfig').and.returnValue(sportService1)
    } as any;
    const result = {
      id: 1,
      markets: [{
        displayOrder: 2,
        outcomes: [{
          prices: []
        }]
      }, {
        displayOrder: 3,
        outcomes: [{
          displayOrder: 1,
          prices: [{
            priceDec: 21
          }]
        }, {
          displayOrder: 2,
          prices: [{
            priceDec: 54
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 23
          }]
        }, {
          displayOrder: 3,
          prices: [{
            priceDec: 99
          }]
        }, {
          displayOrder: 4,
          name: 'a',
          prices: [{
            priceDec: 11
          }]
        }, {
          displayOrder: 4,
          name: 'b',
          prices: [{
            priceDec: 11
          }]
        }]
      }, {
        displayOrder: 5,
        outcomes: [{}]
      }]
    } as any;
    spyOn(component, 'goToSeo');
    component.ngOnInit();
    expect(component.isShowAllActive).toBeFalsy();
  });
  it('should call ngOnDestroy methods', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('EventMarketsComponent');
  });

  it('should subscribe to WS_EVENT_UPDATE', () => {
    component.ngOnInit();

    expect(pubSubService.subscribe).toHaveBeenCalledWith('EventMarketsComponent', 'WS_EVENT_UPDATE', jasmine.any(Function));
  });

  it('should call detect changes when pubsub WS_EVENT_UPDATED fired', () => {
    component.ngOnInit();

    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('showAll Button should be visible on featured when more than default amount of markets available', () => {
    component.isFeaturedMarkets = true;
    component.selectionsLimit = 5;
    const newEntity = {
      id: 1,
      markets: [{
        outcomes: [{}, {}, {}, {}, {}, {}, {}]
      }]
    } as any;
    setNewEventEntity(newEntity);
    component.ngOnInit();
    expect(component.limit).toEqual(component.selectionsLimit);
    expect(component.isShowAllActive).toBeTruthy();
  });


  it('should call genTerms for each event market', () => {
    component.ngOnInit();
    expect(templateService.genTerms).toHaveBeenCalledTimes(eventEntity.markets.length);
  });
  
  it('should call ternary operator', () => {
    const newEntity = {id: 1, markets :[]} as any;
    setNewEventEntity(newEntity);
    spyOn(component, 'sortMarkets' as any);
    spyOn(component,'goToSeo');
    component.ngOnInit();
    const newEntity1 = {id: 1, markets :[]} as any;
    setNewEventEntity(newEntity1);
    component.ngOnInit();
    expect(component.goToSeo).toHaveBeenCalled();
  });

  it('should not filter markets if LuckyDip Market is not available', () => {
    environment.brand = 'ladbrokes';
    environment.CURRENT_PLATFORM = 'desktop';

    component['brand'] = 'ladbrokes';
    component['device'] = 'desktop';
    const newEntity =  eventEntity;
    newEntity.markets[0] = {drilldownTagNames : 'MKTFLAG_SP',outcomes : [{id :'123'}]} as any;
    setNewEventEntity(newEntity);
    component.ngOnInit();

    expect(component.eventEntity.markets ).toBeDefined();
  });

  it('should call ternary operator', () => {
    const newEntity =  component['eventEntity'] = {id: 1, markets :[]} as any;
    newEntity.markets[0] = {drilldownTagNames : 'MKTFLAG_SP',outcomes : [{id :'123'}]} as any;
    setNewEventEntity(newEntity);
    spyOn(component, 'sortMarkets' as any);
    spyOn(component,'goToSeo');
    component.ngOnInit();
    const newEntity1 = {id: 1, markets :[]} as any;
    setNewEventEntity(newEntity1);
    component.ngOnInit();
    expect(component.goToSeo).toHaveBeenCalled();
  });

  it('should not call genTerms', () => {
    component.panelType = '';
    component.ngOnInit();
    expect(component.showTerms).toBeFalsy();
  });

  it('trackByIndex', () => {
    const index = 1;
    const result = component.trackByIndex(index);
    expect(result).toBe(index);
  });

  it('getTerms', () => {
    component['getTerms'](eventEntity as any);
    expect(templateService.genTerms).toHaveBeenCalledTimes(eventEntity.markets.length);
  });

  it('test toggleShow function', () => {
    component.allShown = false;

    component.toggleShow();
    expect(component.allShown).toEqual(true);
    expect(component.limit).toEqual(undefined);

    component.toggleShow();
    expect(component.allShown).toEqual(false);
    expect(component.limit).toEqual(component.selectionsLimit);
  });
  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(({id: '1'} as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });

  it('should call getById to fecthOutcomes for MTA sports', ()=>{
    const eventEntity1 = eventEntity;
    eventEntity1.markets = [...eventEntity1.markets, {
      id: '2',
      name: 'LuckyDip',
      isLpAvailable: true,
      cashoutAvail: 'Y',
      drilldownTagNames: 'MKTFLG_LD',
      outcomes: [
        {
          id: '1',
          isActive: true,
          isAvailable: true,
          marketId: '1',
          name: 'Outcome Name 1',
          outcomeStatusCode: 'A',
          prices: [
            {
              id: '1',
              displayOrder: '1',
              isActive: true,
              priceDec: 1.4,
              priceDen: 10,
              priceNum: 1,
              priceType: 'LP'
            }
          ]
        },
        {
          id: '2',
          isActive: true,
          isAvailable: true,
          marketId: '1',
          name: 'Outcome Name 2',
          outcomeStatusCode: 'A',
          prices: [
            {
              id: '1',
              displayOrder: '1',
              isActive: true,
              priceDec: 1,
              priceDen: 2,
              priceNum: 1,
              priceType: 'LP'
            }
          ]
        }
      ]
    } as any];
    setNewEventEntity(eventEntity1);
    component.panelType = 'outright';
    component.eventId = '8867445';
    component.isLuckyDipMarketAvailable = true;
    component.fetchOutcomes = true;
    component.ngOnInit();
    expect(sportService1.getById).toHaveBeenCalled();
  });

  function setNewEventEntity(newEntity){
    component.eventEntity = newEntity;
    sportService1 = {
      getById: jasmine.createSpy('getById').and.returnValue(observableOf({event: [ newEntity ]}))
    };
    component['sportService'] = {
      setConfig: jasmine.createSpy('setConfig').and.returnValue(sportService1)
    } as any;
  }
});
