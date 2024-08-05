import { RaceCardContentComponent } from './race-card-content.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { RacingGaService } from '@app/racing/services/racing-ga.service';

describe('#RaceCardContentComponent', () => {
  let component: RaceCardContentComponent;
  let raceOutcomeData;
  let routingHelperService;
  let localeService;
  let domTools;
  let windowRef;
  let elementRef;
  let renderer;
  let commandService;
  let carouselService;
  let sbFiltersService;
  let filtersService;
  let pubSubService;
  let router;
  let templateService;
  let outcomeUpdateCb;
  let virtualSharedService;
  let datePipe;
  let nextRacesHomeService;
  let eventService;
  let changeDetectorRef;
  let gtmService;

  let sortByOptionsService;
  let racingGaService;
  const mockString = 'More';

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue(mockString)
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, cb) => {
        if (method === 'OUTCOME_UPDATED') {
          outcomeUpdateCb = cb;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        location: {
          pathname: 'pathname'
        }
      }
    };
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    renderer = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => { })
      }
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    racingGaService = new RacingGaService(gtmService, localeService, pubSubService);
    racingGaService.sendGTM = jasmine.createSpy('sendGTM');
    racingGaService.trackNextRacesCollapse = jasmine.createSpy('trackNextRacesCollapse');
    racingGaService.trackNextRace = jasmine.createSpy('trackNextRace');
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(racingGaService)),
      API: {
        RACING_GA_SERVICE: 'test'
      }
    };
    templateService = {
      genTerms: jasmine.createSpy().and.returnValue('test')
    };
    carouselService = {
      get: jasmine.createSpy('get').and.returnValue({
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous')
      })
    };
    domTools = {
      getWidth: jasmine.createSpy('getWidth')
    };
    filtersService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    raceOutcomeData = {
      isGenericSilk: jasmine.createSpy('isGenericSilk'),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
      getSilkStyle: jasmine.createSpy('getSilkStyle'),
      isSilkAvailable: jasmine.createSpy('isSilkAvailable'),
      isValidSilkName: jasmine.createSpy('isValidSilkName')
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue([{
        id: 'outcome1'
      },
      {
        id: 'outcome2'
      }])
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    virtualSharedService = {
      isVirtual: jasmine.createSpy('isVirtual').and.returnValue(true),
      formVirtualEventUrl: jasmine.createSpy('formVirtualEventUrl')
    };

    datePipe = {
      transform: () => '20:15'
    } as any;

    nextRacesHomeService = {
      getGoing: jasmine.createSpy('getGoing'),
      getDistance: jasmine.createSpy('getDistance')
    };
    eventService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue({
        liveStreamAvailable: true
      })
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Price'),
      set: jasmine.createSpy('set'),
    };
    component = new RaceCardContentComponent(elementRef, domTools, raceOutcomeData, routingHelperService, windowRef, commandService,
      localeService, sbFiltersService, filtersService, renderer, carouselService, pubSubService, router, templateService,
      virtualSharedService, datePipe, nextRacesHomeService, eventService, changeDetectorRef,gtmService,sortByOptionsService);

    component['resizeListener'] = () => { };
  });

  describe('#nextSlide, prevSlide', () => {
    it('$nextSlide', () => {
      component.trackGaDesktop = true;
      component.eventCategory = 'Home';
      component.nextSlide();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });

    it('$prevSlide', () => {
      component.trackGaDesktop = true;
      component.eventCategory = 'Home';
      component.prevSlide();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });

    it('#removeLineSymbol', () => {
      const name: string = "hello";
      filtersService.removeLineSymbol.and.returnValue("hello");
      const expectedResult = component.removeLineSymbol(name);
      expect(expectedResult).toBe('hello');
    });
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#isStreamLabelShown', () => {
    const result = component.isStreamLabelShown(({ name: 'event' } as any));

    expect(eventService.isLiveStreamAvailable).toHaveBeenCalledWith({ name: 'event' });
    expect(result).toEqual(true);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      sbFiltersService.orderOutcomeEntities = jasmine.createSpy('sbFiltersService').and.callFake(x => x);
      component.raceMaxSelections = 3;
      component.raceData = [{
        id: 1,
        markets: [
          {
            id: 1,
            outcomes: [
              {
                id: 1
              },
              {
                id: 2
              },
              {
                id: 3
              },
              {
                id: 4
              },
            ]
          }
        ]
      }, { id: 2, markets: [] }] as any;

      windowRef.nativeWindow.setTimeout.and.callFake(cb => cb && cb());
    });

    it('#ngOnInit', () => {
      component.ngOnInit();

      expect(component.raceIndex).toEqual(0);
      expect(component.raceOrigin).toEqual('');
      expect(component.viewFullRaceText).toEqual('More');
      expect(component.eventCategory).toEqual('widget');
      expect(localeService.getString).toHaveBeenCalledWith('sb.viewFullRace');
      expect(pubSubService.subscribe).toHaveBeenCalledWith('RaceCardComponent1', 'OUTCOME_UPDATED', jasmine.any(Function));
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(domTools.getWidth).toHaveBeenCalledTimes(2);
      expect(component.disableScroll).toBeDefined();
      expect(component.isFitSize).toBeDefined();
      expect(component.showCarouselButtons).toBeDefined();
      expect(component.marketOutcomesMap[1]).toEqual([
        {
          id: 1
        },
        {
          id: 2
        },
        {
          id: 3
        }
      ] as any);
      expect(component.raceData[0].markets[0].outcomes.length).toEqual(4);
    });

    it('should check for overlay content with next races', () => {
      component.isEventOverlay = true;
      component.raceOrigin = '';
      component.ngOnInit();
      expect(component.raceOrigin).toEqual('?origin=next-races');
    });

    it('should check for overlay content with overlay false', () => {
      component.isEventOverlay = false;
      component.raceOrigin = '';
      component.ngOnInit();
      expect(component.raceOrigin).toEqual('');
    });

    it('#initShowCarouselButtons', () => {
      component['initShowCarouselButtons'] = jasmine.createSpy('component.initShowCarouselButtons');
      renderer.renderer.listen.and.callFake((a, b, cb) => {
        cb();
      });
      component.raceWidget = 'test';
      component.raceOrigin = 'test';
      component['windowRef'].nativeWindow.location.pathname = '/';
      component.ngOnInit();
      expect(component['initShowCarouselButtons']).toHaveBeenCalled();
    });

    it(`should define channelName without id`, () => {
      delete component.raceData[0].id;

      component.ngOnInit();

      expect(component['channelName']).toEqual('RaceCardComponent');
    });
    it('should set isHR to be true', () => {
      component.raceData = [{ categoryCode: 'HORSE_RACING' }] as any;
      component.ngOnInit();
      expect(component['isHR']).toBeTrue();
    });
    it('should set isHR to be false', () => {
      component.raceData = [{},
       { id: '2', markets: [{ outcomes: [] }]}
      ] as any;
      component.raceData[0] = null;
      component.ngOnInit();
      expect(component['isHR']).toBeFalse();
    });
    it('should set isHR to be false if competitionSection is null', () => {
      component.raceData = [{competitionSection:{}}] as any;
      component.ngOnInit();
      expect(component['isHR']).toBeFalse();
    });
  });

  it('should processOutcomes on OUTCOME_UPDATED', () => {
    const martet = { id: '12' };
    component['processOutcomes'] = jasmine.createSpy();
    component.raceData = [{ id: 1, markets: [{ outcomes: [] }] }, { id: 2, markets: [{ outcomes: [] }] }] as any;

    component.ngOnInit();
    component['raceMarkets'] = ['12', '14'];
    outcomeUpdateCb(martet);

    expect(component['processOutcomes']).toHaveBeenCalledTimes(2);
    expect(component['processOutcomes']).toHaveBeenCalledWith(martet as any);
  });

  it('should processOutcomes on OUTCOME_UPDATED and set new prices', () => {
    const market = { id: '8', outcomes: [{ id: '901', prices: [{ id: '72' }] }] };
    component.raceData = [
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '18' }] }] }]
      },
      {
        id: '2', markets: [{ outcomes: [] }]
      }
    ] as any;
    component.ngOnInit();
    component['raceMarkets'] = ['12', '14', '8'];
    outcomeUpdateCb(market);

    expect(component.raceData).toEqual([
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '72' }] }] }]
      },
      {
        id: '2', markets: [{ outcomes: [] }]
      }
    ] as any);
  });

  it(`should call onchanges with current value false`, () => {
    const changes: any = {
      raceData: {
        currentValue: () => false
        }
    };
    spyOn(component, 'ngOnInit');
    component.ngOnChanges(changes);
    expect(component.ngOnInit).toHaveBeenCalledTimes(1);
});

it(`should call onchanges with current value true`, () => {
  const changes: any = {
    raceData: {
      currentValue: () => true
      }
  };
  spyOn(component, 'ngOnInit');
  component.ngOnChanges(changes);
  expect(component.ngOnInit).toHaveBeenCalledTimes(1);
});

it(`empty race data`, () => {
  const changes: any = {
    raceData: null
  };
  spyOn(component, 'ngOnInit');
  component.ngOnChanges(changes);
  expect(component.ngOnInit).toHaveBeenCalledTimes(0);
});

it('#isEventVirtual', () => {
  const result = component.isEventVirtual(({
    id: '12345',
    name: 'name',
    categoryId: '39'
  } as any));

  expect(result).toEqual(true);
});

it('#isVirtualSignpost', () => {
  const event ={categoryId : '1'}as any;
  const environment ={CATEGORIES_DATA :{virtuals :[{id:'1'}]}}
  const result = component.isVirtualSignpost(event)
  expect(result).toBe(false)
});

  it('should processOutcomes on OUTCOME_UPDATED and do not update prices if no match', () => {
    const market = { id: '8', outcomes: [{ id: '91', prices: [{ id: '72' }] }] };
    component.raceData = [
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '18' }] }] }]
      }
    ] as any;
    component.ngOnInit();
    component['raceMarkets'] = ['12', '14', '8'];
    outcomeUpdateCb(market);

    expect(component.raceData).toEqual([
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '18' }] }] }]
      }
    ] as any);
  });

  it('should processOutcomes on OUTCOME_UPDATED and do not update prices if no match where selectedOption is Racecard', () => {
    sortByOptionsService = {
      get: jasmine.createSpy('get').and.returnValue('Racecard'),
      set: jasmine.createSpy('set')
    };
    component = new RaceCardContentComponent(elementRef, domTools, raceOutcomeData, routingHelperService, windowRef, commandService,
      localeService, sbFiltersService, filtersService, renderer, carouselService, pubSubService, router, templateService,
      virtualSharedService, datePipe, nextRacesHomeService, eventService, changeDetectorRef, gtmService, sortByOptionsService);

    const market = { id: '8', outcomes: [{ id: '91', prices: [{ id: '72' }] }] };

    component.raceData = [
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '18' }] }] }]
      }
    ] as any;
    component.ngOnInit();
    component['raceMarkets'] = ['12', '14', '8'];
    outcomeUpdateCb(market);

    expect(component.raceData).toEqual([
      {
        id: '8',
        markets: [{ id: '8', outcomes: [{ id: '901', prices: [{ id: '18' }] }] }]
      }
    ] as any);
  });

  describe('trackEvent', () => {
    it('should NOT track Virtual Event', () => {
      virtualSharedService.isVirtual.and.returnValue(false);
      component.trackEvent({} as any, '');

      expect(virtualSharedService.formVirtualEventUrl).not.toHaveBeenCalled();
    });

    it('should track Virtual Event', () => {
      virtualSharedService.isVirtual.and.returnValue(true);
      component.trackEvent({} as any, '');

      expect(virtualSharedService.formVirtualEventUrl).toHaveBeenCalledWith({});
    });

    it('should call seo Event', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.trackEvent({} as any, '');
    });

    it('should call sendGTM trackGaDesktop is true for HR', () => {
      component.trackGaDesktop = true;
      virtualSharedService.isVirtual.and.returnValue(true);
      const entity = {
        categoryId: '21',
        localTime: '22:00',
        originalName: '16:25 Nottingham',
        name: 'Nottingham',
        nameOverride: 'London1',
        typeName: 'Wolverhampton'
      } as any;
      component.eventCategory = 'Home';
      const name = entity.localTime ? `${entity.localTime} ${entity.typeName}` : entity.name;
      const eventName = entity.nameOverride || name;
      component.trackEvent({} as any);
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });

    it('should call sendGTM trackGaDesktop is true for HR', () => {
      component.trackGaDesktop = true;
      virtualSharedService.isVirtual.and.returnValue(true);
      const entity = {
        categoryId: '21',
        localTime: '22:00',
        originalName: '16:25 Nottingham',
        name: 'Nottingham',
        nameOverride: 'London1',
        typeName: 'Wolverhampton'
      } as any;
      component.eventCategory = 'Home';
      component.isEventOverlay = true;
      component.trackEvent(entity as any, 'uk');
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });
    
    it('should call sendGTM trackGaDesktop is true for GH', () => {
      component.trackGaDesktop = true;
      virtualSharedService.isVirtual.and.returnValue(true);
      const entity = {
        categoryId: '16',
        localTime: '22:00',
        originalName: '16:25 Nottingham',
        name: 'Nottingham',
        nameOverride: 'London1',
        typeName: 'Wolverhampton'
      } as any;
      component.trackGaDesktop = false;
      component.trackGa = false;
      component.isEventOverlay = true;
      component.trackEvent(entity as any, 'france');
      expect(commandService.executeAsync).toHaveBeenCalled();
    });

    it('should call sendGTM if trackGa is true', () => {
      component.trackGaDesktop = false;
      component.trackGa = true;
      virtualSharedService.isVirtual.and.returnValue(true);
      component.trackEvent({"name":"test"} as any);
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });

    it('should call when isEventOverlay is true', () => {
      component.isEventOverlay=true;
      component.trackGaDesktop = true;
      component.trackGa = true;
      virtualSharedService.isVirtual.and.returnValue(true);
      component.trackEvent({'localTime':'23',"typeName":"test"} as any,'test');
      expect(commandService.executeAsync).toHaveBeenCalledWith('test');
    });

  });

  it('should generate each way terms', () => {
    const market = {
      eachWayFactorNum: '1',
      eachWayFactorDen: '2',
      eachWayPlaces: '1,2,3',
      outcomes: []
    } as any;
    component.raceData = [
      {
        markets: [market]
      }
    ] as any;

    spyOn(component, 'generateEachWayTerms').and.callThrough();
    component.ngOnInit();
    expect(component.generateEachWayTerms).toHaveBeenCalled();
    expect(component.terms[0]).toEqual('test');
  });

  it('should generate Each Way terms for events(no events)', () => {
    spyOn(component, 'generateTerms');

    component.raceData = <any>[
      {
        categoryCode: 'HORSE_RACING',
        markets: [
          { outcomes: [] }
        ]
      }
    ];
    component.ngOnInit();

    expect(component.generateTerms).not.toHaveBeenCalled();
  });

  it('should generate Each Way terms for events(no markets)', () => {
    spyOn(component, 'generateTerms');

    component.raceData = <any>[
      {
        categoryCode: 'HORSE_RACING',
        markets: [
          { outcomes: [] }
        ]
      }
    ];
    component.ngOnInit();

    expect(component.generateTerms).not.toHaveBeenCalled();
  });

  it('should trackByEvents', () => {
    const event1 = { name: 'test', categoryId: '2', id: 11, markets: [] } as any;
    expect(component.trackByEvents(1, event1)).toBe('11_test_2_01');

    const event2 = { name: 'test', categoryId: '2', id: 11 } as any;
    expect(component.trackByEvents(1, event2)).toBe('11_test_2_undefined1');
  });

  it('should trackByMarkets', () => {
    expect(component.trackByMarkets(1, <any>{ name: 'test', marketStatusCode: '2', id: 11 })).toBe('11_test_2');
  });

  it('should trackByOutcomes', () => {
    expect(component.trackByOutcomes(1, <any>{ name: 'test', runnerNumber: '2', id: 11 })).toBe('11_test_2');
  });


  it('should test generation of template for terms', () => {
    const market = {
      eachWayFactorNum: '1',
      eachWayFactorDen: '2',
      eachWayPlaces: '1,2,3'
    };
    component.generateTerms(<any>market);
    expect(templateService.genTerms).toHaveBeenCalledWith(market, 'sb.newOddsAPlacesExtended');
  });

  describe('#applyFilters', () => {
    it('should filter outcomes of market', () => {
      component.hideNonRunners = false;
      const result = component['applyFilters'](({
        outcomes: [],
        isLpAvailable: 'Yes',
      } as any));
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, false, false, true);
      expect(result).toEqual(([{
        id: 'outcome1'
      },
      {
        id: 'outcome2'
      }] as any));
    });

    it('should filter outcomes of marke and splice for max selections on card', () => {
      component.raceMaxSelections = 1;
      component.hideNonRunners = false;
      const result = component['applyFilters'](({
        outcomes: [],
        isLpAvailable: 'Yes',
      } as any));
      expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith([], 'Yes', true, true, false, false, true);
      expect(result).toEqual(([{
        id: 'outcome1'
      }] as any));
    });
  });

  describe('#showNext', () => {
    it('should get showNext when carousel is defined', () => {
      component['carousel'] = {
        currentSlide: 3,
        slidesCount: 5
      } as any;
      carouselService.get.and.returnValue({
        currentSlide: 3,
        slidesCount: 5
      });

      expect(component.showNext).toEqual(true);
    });

    it('should get showNext when carousel not defined', () => {
      component.showNext = true;
      carouselService.get.and.returnValue(null);

      expect(component.showNext).toEqual(null);
    });
  });

  describe('#showPrev', () => {
    it('should get showPrev when carousel is defined', () => {
      carouselService.get.and.returnValue({
        currentSlide: 3
      });

      expect(component.showPrev).toEqual(true);
    });

    it('should get showPrev when carousel not defined', () => {
      component.showPrev = true;
      carouselService.get.and.returnValue(null);

      expect(component.showPrev).toEqual(null);
    });
  });

  describe('@getEventName', () => {
    it('should return correct virtual name', () => {
      component.isVirtual = true;
      const event = { id: 1, categoryId: 39, name: '18:15 Laddies Leap\'s Lane' } as any;
      expect(component.getEventName(event)).toBe('18:15 Laddies Leap\'s Lane');
    });
    it('should return correct name if NOT Virtual Event', () => {
      component.isVirtual = false;
      const result = component.getEventName(({
        localTime: '2',
        typeName: 'London',
        name: 'London2',
        nameOverride: 'London1'
      }) as any);

      expect(result).toEqual('London1');
    });

    it('should return correct name if NOT Virtual Event and localTime and nameOverride is not there ', () => {
      component.isVirtual = false;
      const result = component.getEventName(({
        typeName: 'London',
        name: 'London2'
      }) as any);

      expect(result).toEqual('London2');
    });

    it('should return correct virtual name for VIRTUAL', () => {
      component.isVirtual = true;
      const event = { id: 1, categoryId: 39, originalName: 'Laddies Leap', categoryCode: 'VIRTUAL' } as any;
      expect(component.getEventName(event)).toBe('Laddies Leap');
    });
  });

  it('#getRunnerNumber return runner number', () => {
    expect(component.getRunnerNumber({} as any)).toBe(undefined);
    expect(component.getRunnerNumber({ runnerNumber: '3' } as any)).toBe('3');
    expect(component.getRunnerNumber({ racingFormOutcome: {} } as any)).toBe(undefined);
    expect(component.getRunnerNumber({ racingFormOutcome: { draw: '6' } } as any)).toBe('6');
  });

  it('#getGoing', () => {
    component.getGoing('G');

    expect(nextRacesHomeService.getGoing).toHaveBeenCalledWith('G');
  });

  it('#getDistance', () => {
    component.getDistance('Distance');

    expect(nextRacesHomeService.getDistance).toHaveBeenCalledWith('Distance');
  });
  it('setTrapNumbers', () => {
    component.raceData = [
      {
        id: 1,
        markets: [
          {
            outcomes: [
              {
                name: 'Test',
                runnerNumber: 2
              }
            ]
          }
        ]
      },
      {
        id: 2,
        markets: [
          {
            outcomes: [
              {
                name: 'Test (RES)',
                runnerNumber: 1,
                displayOrder: 1
              }
            ]
          }
        ]
      }
    ] as any;

    component['setTrapNumbers']();

    expect(component.raceData).toEqual(<any>[
      {
        id: 1,
        markets: [
          {
            outcomes: [
              {
                name: 'Test',
                runnerNumber: 2,
                trapNumber: 2
              }
            ]
          }
        ]
      },
      {
        id: 2,
        markets: [
          {
            outcomes: [
              {
                name: 'Test (RES)',
                displayOrder: 1,
                runnerNumber: 1,
                trapNumber: 1
              }
            ]
          }
        ]
      }
    ]);
  });

  it('setTrapNumbers', () => {
    component.raceData = [
      {
        id: 1,
        markets: [
          {
            outcomes: [
              {
                name: 'Test',
              }
            ]
          }
        ]
      },
      {
        id: 2,
        markets: [
          {
            outcomes: [
              {
                name: 'Test (RES)'
              }
            ]
          }
        ]
      }
    ] as any;

    component['setTrapNumbers']();

    expect(component.raceData).toEqual(<any>[
      {
        id: 1,
        markets: [
          {
            outcomes: [
              {
                name: 'Test',
              }
            ]
          }
        ]
      },
      {
        id: 2,
        markets: [
          {
            outcomes: [
              {
                name: 'Test (RES)'
              }
            ]
          }
        ]
      }
    ]);
  });

  describe('ngOnDestroy', () => {
    it(`should unsubscribe of pubSub`, () => {
      component['channelName'] = 'RaceCardComponent1';
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('RaceCardComponent1');
    });
  });

  describe('isGenericSilk / isGreyhoundSilk / isNumberNeeded', () => {
    const event: any = {};
    it('should return false when generic silk is needed', () => {
      const outcome: any = { racingFormOutcome: {} };
      raceOutcomeData.isGenericSilk.and.returnValue(false);
      const expectedResult = component.isGenericSilk(event, outcome);
      expect(expectedResult).toBe(false);
    });
    it('should return false when isGreyhoundSilk is needed', () => {
      const outcome: any = { racingFormOutcome: {} };
      raceOutcomeData.isGreyhoundSilk.and.returnValue(false);
      const expectedResult = component.isGreyhoundSilk(event, outcome);
      expect(expectedResult).toBe(false);
    });
    it('should return false when isNumberNeeded  is needed', () => {
      const outcome: any = { racingFormOutcome: {} };
      raceOutcomeData.isNumberNeeded.and.returnValue(false);
      const expectedResult = component.isNumberNeeded(event, outcome);
      expect(expectedResult).toBe(false);
    });

    it('should return getSilkStyle', () => {
      const raceData: any = { outcomes: [] };
      const outcomes = [{
        racingFormOutcome: {
          silkName: 'image2.gif'
        }
      }, {
        racingFormOutcome: {
          silkName: 'image1.png'
        }
      }] as any;

      raceOutcomeData.getSilkStyle.and.returnValue(
        {
          'background-image': jasmine.any(String),
          'background-position': jasmine.any(String),
          'background-size': jasmine.any(String)
        });
      const expectedResult = component.getSilkStyle(raceData, outcomes);
      expect(expectedResult).toEqual({
        'background-image': jasmine.any(String),
        'background-position': jasmine.any(String),
        'background-size': jasmine.any(String)
      });

    });
  });
});
