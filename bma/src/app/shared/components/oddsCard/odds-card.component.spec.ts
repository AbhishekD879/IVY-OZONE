import { OddsCardComponent } from './odds-card.component';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';
describe('OddsCardComponent', () => {
  let component: OddsCardComponent;

  let eventFactory;
  let marketTypeService;
  let timeService;
  let filters;
  let routingHelper;
  let templateService;
  let router;
  let sportsConfigHelperServive, seoDataService,gtmService ;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('routerNavigate')
    };
    eventFactory = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable')
    };
    marketTypeService = {
      getDisplayMarketConfig: jasmine.createSpy('getDisplayMarketConfig').and.returnValue({
        primaryMarket: 'primaryMarket',
        handicapMarket: 'handicapMarket',
        hasPrimaryMarket: true,
        hasHandicapMarket: true,
        displayMarket: {
          id: '1',
          label: 'Market label'
        },
        displayMarketName: 'displayMarketName'
      }),
      extractMarketNameFromEvents: (events: ISportEvent[], isFilterByTemplateMarketName?: boolean): string[] => {
        const marketNames = _.reduce(events, (accumulator, event) => {
          const eventMarketNames = (event.markets || []).map(market => {
            if (isFilterByTemplateMarketName) {
              if (market.templateMarketName === 'Match Betting') {
                market.templateMarketName = 'Match Result';
              }
              return market.templateMarketName;
            }
    
            return market.name;
          });
    
          accumulator.push(...eventMarketNames);
    
          return accumulator;
        }, []);
        return marketNames;
      }
    };
    gtmService={
    push: jasmine.createSpy('push')
    }
    timeService = {
      getLocalHourMin: jasmine.createSpy('getLocalHourMin'),
      getEventTime: jasmine.createSpy('getEventTime')
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    filters = {
        getTeamName: (name, index) => ['Soderberg', 'Gagli', 'Porteous'][index]
    };
    routingHelper = {
      formEdpUrl: jasmine.createSpy().and.returnValue('sport/event/1234567')
    };
    templateService = {
      getTemplate: jasmine.createSpy('getTemplate').and.returnValue({
        name: 'Enhanced Multiples'
      }),
      isMultiplesEvent: jasmine.createSpy('isMultiplesEvent'),
      isListTemplate: (selectedMarket: string)=>{
       return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
      },
      isMultiMarketTemplate: (selectedMarket: string)=>{
       return selectedMarket ? selectedMarket.split(',').length > 0 : false;
      }
    };
    sportsConfigHelperServive = {};

    component = new OddsCardComponent(
      eventFactory,
      marketTypeService,
      timeService,
      filters,
      routingHelper,
      templateService,
      router,
      sportsConfigHelperServive,
      seoDataService,
      gtmService
    );

    component.event = { isFinished: false, markets: [] } as any;
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit with sport config', () => {
      component.sportConfig = {
        config: {
          path: '/football',
          request: {
            categoryId: '16'
          }
        }
      } as any;
      component.event = { isFinished: false, markets: [], name: 'Soderberg/Gagli/Porteous' } as any;
      component.ngOnInit();

      expect(component.sportType).toEqual('/football');
      expect(component.eventFirstName).toEqual('Soderberg');
      expect(component.eventSecondName).toEqual('Gagli');
      expect(component.eventThirdName).toEqual('Porteous');
    });

    it('should call getDisplayMarketConfig', () => {
      const result = {
        primaryMarket: 'primaryMarket',
        handicapMarket: 'handicapMarket',
        hasPrimaryMarket: true,
        hasHandicapMarket: true,
        displayMarket: {
          id: '1',
          label: 'Market label'
        },
        displayMarketName: 'displayMarketName'
      };
      component.sportConfig = {
        config: {
          path: '/football',
          request: {
            categoryId: '21',
            marketTemplateMarketNameIntersects: 'template name'
          }
        }
      } as any;
      component.ngOnInit();

      expect(marketTypeService.getDisplayMarketConfig).toHaveBeenCalledWith('template name', []);
      expect(component.displayMarketConfig).toEqual(result as any);
      expect(component.isOutrightsCard).toEqual(false);
      expect(component.selectedMarket).toEqual('displayMarketName');
      expect(component.selectedMarketObject).toEqual({
        id: '1',
        label: 'Market label'
      });
    });

    it('should call ngOnInit with eventSortCode TNMT', () => {
      component.sportConfig = {
        config: {
          path: '/golf',
          request: {
            categoryId: '16'
          }
        }
      } as any;
      component.event = { isFinished: false, markets: [], name: 'Soderberg/Gagli/Porteous',
      eventSortCode: 'TNMT' } as any;
      component.isMarketSwitcherConfigured = false;
      component.ngOnInit();
      component.sportConfig = {
        config: {
          path: '/golf',
          name: 'golf',
          request: {
            categoryId: '16'
          }
        }
      } as any;
      component.ngOnInit();
      expect(component.sportType).toEqual('/golf');
    });
  });

  it('should call watchHandler', () => {
    component.selectedMarket = 'Round Betting';
    component['watchHandler']();
    expect(component.isListTemplate).toBeFalsy();
  });

  it('should call checkTemplateType', () => {
    component.selectedMarket = 'Round Betting';
    component.event = {
      markets: [{
        dispSortName: 'L2'
      }]
    } as any;
    component.isMarketSwitcherConfigured = true;
    component['checkTemplateType']();
    expect(component.isListTemplate).toBeTruthy();
  });

  describe('goToSeo', () => {
    it('should create seo ', () => {
      component.event = {
        id: '1'
      } as any;
      routingHelper.formEdpUrl.and.returnValue('url');
      component.goToSeo();
      expect(routingHelper.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });

  describe('#goToEvent', () => {
    it('#goToEvent with justReturn - true', () => {
      const callGoToEventCallbackFn = spyOn(component, 'callGoToEventCallback');

      expect(component['goToEvent'](true, 'element $event')).toEqual('sport/event/1234567');
      expect(component['routingHelper'].formEdpUrl).toHaveBeenCalledWith({ isFinished: false, markets: [] } as any);
      expect(callGoToEventCallbackFn).toHaveBeenCalledTimes(0);
      expect(component['router'].navigateByUrl).not.toHaveBeenCalledWith('sport/event/1234567');
    });

    it('#goToEvent with justReturn - false and isEnhancedMultiples - true', () => {
      const callGoToEventCallbackFn = spyOn(component, 'callGoToEventCallback');

      component.isEnhancedMultiples = true;
      expect(component['goToEvent'](false, 'element $event')).toEqual('sport/event/1234567');
      expect(component['routingHelper'].formEdpUrl).toHaveBeenCalledWith({ isFinished: false, markets: [] } as any);
      expect(callGoToEventCallbackFn).toHaveBeenCalledTimes(0);
      expect(component['router'].navigateByUrl).not.toHaveBeenCalledWith('sport/event/1234567');
    });

    it('#goToEvent with justReturn - false and isEnhancedMultiples - false and isFinished true', () => {
      const callGoToEventCallbackFn = spyOn(component, 'callGoToEventCallback');

      component.event.isFinished = true;
      component.isEnhancedMultiples = false;
      expect(component['goToEvent'](false, 'element $event')).toEqual('sport/event/1234567');
      expect(component['routingHelper'].formEdpUrl).toHaveBeenCalledWith({ isFinished: true, markets: [] } as any);
      expect(callGoToEventCallbackFn).toHaveBeenCalledTimes(0);
      expect(component['router'].navigateByUrl).not.toHaveBeenCalledWith('sport/event/1234567');
    });

    it('#goToEvent with justReturn - false and isEnhancedMultiples - false and isFinished false', () => {
      const callGoToEventCallbackFn = spyOn(component, 'callGoToEventCallback');

      component.isEnhancedMultiples = false;
      expect(component['goToEvent'](false, 'element $event')).toEqual('sport/event/1234567');
      expect(component['routingHelper'].formEdpUrl).toHaveBeenCalledWith({ isFinished: false, markets: [] } as any);
      expect(callGoToEventCallbackFn).toHaveBeenCalledTimes(1);
      expect(component['router'].navigateByUrl).toHaveBeenCalledWith('sport/event/1234567');
    });
  });
  describe('#changeCardView', () => {
    it('should isOutrightsCard = false', () => {
      component.sportConfig = {
        config: {
          path: '/football',
          request: {
            categoryId: '21',
            marketTemplateMarketNameIntersects: 'template name'
          }
        }
      } as any;
      component.changeCardView({
        isDisplayed: false
      } as any);

      expect(component.isOutrightsCard).toEqual(false);
    });
    it('should handleOutput', () => {
      component.sportConfig = {
        config: {
          path: '/football',
          request: {
            categoryId: '21',
            marketTemplateMarketNameIntersects: 'template name'
          }
        }
      } as any;
      const output = {
        output: 'marketUndisplayed',
        value: {
          isDisplayed: false
        }
      };
      component.handleOutput(output as any);

      expect(component.isOutrightsCard).toEqual(false);
    });
    it('should handleOutput call goToEventCallback', () => {
      component.sportConfig = {
        config: {
          path: '/football',
          request: {
            categoryId: '21',
            marketTemplateMarketNameIntersects: 'template name'
          }
        }
      } as any;
      const output = {
        output: 'goToEventCallback',
        value: {
          isDisplayed: false
        }
      };
      component.handleOutput(output as any);

      expect(component).toBeTruthy();
    });
  });
  it('should update mmarket display for football', () => {
    component.marketUndisplayed.emit = jasmine.createSpy('component.marketUndisplayed.emit');
    component.sportConfig = {
      config: {
        path: '/football',
        request: {
          categoryId: '16',
          marketTemplateMarketNameIntersects: 'template name'
        }
      }
    } as any;
    component.changeCardView({
      isDisplayed: false
    } as any);

    expect(component.marketUndisplayed.emit).toHaveBeenCalledWith({
      isDisplayed: false
    } as any);
  });
  
  describe('@eventDisplayed',()=>{
    it('get eventDisplayed', () => {
      expect(component.eventDisplayed({ isResulted: true, outcomes: [] } as any)).toBeTruthy();
      expect(component.eventDisplayed({ outcomes: [{}] } as any)).toBeTruthy();
      expect(component.eventDisplayed({ outcomes: [] } as any)).toBeFalsy();
     })
   });

  describe('@onExpand', () => {
    it("#Should call onExpand when isCouponScoreboardOpened is true", () => {
      component.event = {
        id: 1,
        categoryId: 16,
        typeId: 25230
      } as any;
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'click',
        eventCategory: 'coupon stats widget',
        eventLabel: 'hide stats',
        categoryID: 16,
        typeID: 25230,
        eventID: 1
      };
      component.showBoard = true;
      component.onExpand();
      expect(component.showBoard).toBeTruthy()
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);

    })

    it("#Should  call onExpand when isCouponScoreboardOpened is false", () => {
      component.event = {
        id: 1,
        categoryId: 16,
        typeId: 25230
      } as any;
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'click',
        eventCategory: 'coupon stats widget',
        eventLabel: 'show stats',
        categoryID: 16,
        typeID: 25230,
        eventID: 1
      };
      component.showBoard = false;
      component.onExpand();
      expect(component.showBoard).toBeFalsy()
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    })
  }); 
  
  it('should call updateDisplayMarket', () => {
      component.sportConfig = {
        config: {
          oddsCardHeaderType: '',
          isOutrightSport: true,
          path: '/golf',
          request: {
            categoryId: '18'
          }
        }
      } as any;
      component.isMarketSwitcherConfigured = false;
      component.event = { isFinished: false, markets: [{templateMarketName: 'Match Result', name: 'Match Betting'}], name: 'Soderberg/Gagli/Porteous' } as any;
      component['updateDisplayMarket'](component.sportConfig);
      expect(component.event.markets.length).toEqual(1);
      component.sportConfig.config.request.categoryId = '2';
      component['updateDisplayMarket'](component.sportConfig);
      expect(component.event.markets.length).toEqual(1);
  });
  it('should call callGoToEventCallback', () => {
    component.callGoToEventCallback();
    expect(component).toBeTruthy();
  });
  it('should call ngOnChanges', () => {
    const changes = {
      selectedMarket: 'Match Betting',
    } as any;
    component.ngOnChanges(changes);
    expect(component).toBeTruthy();
  });
  it('should call isSportCard', () => {
    component.template = {name: ''};
    expect(component.isSportCard('')).toBeTrue();
  });
  it('should call isSelectedMarket', () => {
    component.selectedMarket = 'Match Result,Total Points';
    expect(component.isSelectedMarket({templateMarketName: 'Match Result1', name: 'Match Result'} as any)).toBeTrue();
    component.selectedMarket = '';
    expect(component.isSelectedMarket({templateMarketName: 'Match Result1', name: 'Match Result'} as any)).toBeTrue();
  });
  it('should call isLive', () => {
    component.isLive = true;
    component.eventStartedOrLive = true;
    expect(component.isLive).toBeTrue();
   });
  it('should call getSelectedMarket', () => {
    component['matchResultMarket'] = {name: 'match'} as any;
    component.selectedMarket = '';
    component['getSelectedMarket']();
    expect(component.selectedMarket).toEqual('Match Result');
   });
  it('should call showStreamIcon', () => {
    component.event = {drilldownTagNames: ''} as any;
    expect(component['showStreamIcon']()).toBeFalse();
    component.event = {drilldownTagNames: 'EVFLAG_AVA,EVFLAG_PVM,EVFLAG_IVM'} as any;
    expect(component['showStreamIcon']()).toBeTrue();
   });

 });
