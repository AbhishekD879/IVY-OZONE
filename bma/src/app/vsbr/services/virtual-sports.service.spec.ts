import { of as observableOf, throwError, of } from 'rxjs';
import { VirtualSportsService } from './virtual-sports.service';
import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';
import { IVirtualCategoryStructure, IVirtualChildCategory } from '@app/vsbr/models/virtual-sports-structure.model';
import { IVirtualChild } from '@core/services/cms/models/virtual-sports.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('VirtualSportsService', () => {
  let service: VirtualSportsService;
  let vsMapperService;
  let timeService;
  let eventProvider;
  let pubSubService;
  let filterService;
  let localeService;
  let windowRefService;
  let insomniaService;
  let cmsService;
  let eventService;

  const callbacks = {};
  const SSResponseMock = {
    SSResponse: {
      children: [
        {
          event: {
            classId: '287',
            startTime: '2020-01-01',
            name: '20:00 RPR',
            children: [
              { market: {} },
              { market: {} }
            ]
          }
        }
      ]
    }
  };

  const SSResponseMockLegends = {
    SSResponse: {
      children: [
        {
          event: {
            classId: '223',
            startTime: '2020-01-01',
            name: '20:00 Legends',
            children: [
              { market: {} },
              { market: {} }
            ]
          }
        }
      ]
    }
  };

  const classId: string = '287';
  const cmsVirtualSports: any = [{
    id: '5e85df97c9e77c0001d62999',
    title: 'Motorsports',
    tracks: [{
      id: '5e85e070c9e77c0001805f6b',
      title: 'Inspired Cycling',
      classId: classId,
      streamUrl: 'zz',
      numberOfEvents: 4
    }],
    svg: '',
    svgId: '#icon-motor-bikes',
    ctaButtonUrl: 'DO NOT TOUCH',
    ctaButtonText: 'THIS CONFIG!!!!'
  }];

  const event: ISportEvent = {
    id: 230152170,
    name: 'Turin v Maribor Violets',
    eventStatusCode: 'S',
    displayOrder: 1,
    siteChannels: 'P,p,Q,R,C,I,M,',
    eventSortCode: 'MTCH',
    startTime: '2020-04-08T15:42:00Z',
    rawIsOffCode: '-',
    classId: classId,
    typeId: '32614',
    sportId: '39',
    liveServChannels: 'sEVENT0230152170,',
    liveServChildrenChannels: 'SEVENT0230152170,',
    categoryId: '39',
    categoryCode: 'VIRTUAL',
    categoryName: 'Virtual Sports',
    categoryDisplayOrder: '369',
    className: 'Virtual Football',
    classDisplayOrder: '202',
    classSortCode: 'VS',
    typeName: 'Striker Stadium',
    typeDisplayOrder: '0',
    isOpenEvent: 'true',
    isNext24HourEvent: 'true',
    cashoutAvail: 'N',
    startTimeUnix: 1586360520000
  };

  const tracks: IVirtualChild[] = [{
    id: '5e85e070c9e77c0001805f6b',
    title: 'Inspired Cycling',
    classId: classId,
    streamUrl: 'zz',
    numberOfEvents: 4,
    showRunnerNumber: true,
    showRunnerImages: true
  }];

  const child = {
    id: '5e85e070c9e77c0001805f6b',
    showRunnerNumber: true,
    showRunnerImages: true,
    title: 'Inspired Cycling',
    classId: classId,
    typeIds: '1001,1002,1003',
    streamUrl: 'zz',
    numberOfEvents: 4,
    alias: 'inspired-cycling',
    events: [{
      'event': event
    }]
  };

  const childs = new Map<number | string, IVirtualChildCategory>();
  const parentCategory: IVirtualCategoryStructure = {
    id: '5e85df97c9e77c0001d62999',
    title: 'Motorsports',
    tracks: tracks,
    svgId: '#icon-motor-bikes',
    svg: '',
    ctaButtonUrl: 'DO NOT TOUCH',
    ctaButtonText: 'THIS CONFIG!!!!',
    alias: 'motorsports',
    targetUri: '/virtual-sports/motorsports',
    childs: childs
  } as any;
  const legendsParentCategory: IVirtualCategoryStructure = {
    id: '5e85df97c9e77c0001d62999',
    title: 'Legends',
    tracks: tracks,
    svgId: '#icon-motor-bikes',
    svg: '',
    ctaButtonUrl: 'DO NOT TOUCH',
    ctaButtonText: 'THIS CONFIG!!!!',
    alias: 'motorsports',
    targetUri: '/virtual-sports/motorsports',
    childs: childs
  } as any;

  const cloneWithId = (obj, id) => {
    const clone = JSON.parse(JSON.stringify(obj));
    clone.id = id;
    return clone;
  };

  beforeEach(() => {
    timeService = {
      refreshInterval: 1000,
      eventOngoingGuess: 1000,
      selectTimeRangeStart: jasmine.createSpy(),
      selectTimeRangeStartDelta: jasmine.createSpy(),
      selectTimeRangeEnd: jasmine.createSpy(),
      selectTimeRangeEndDelta: jasmine.createSpy(),
      getGmtTime: jasmine.createSpy(),
      formatByPattern: jasmine.createSpy()
    };

    eventProvider = {
      getEvent: jasmine.createSpy().and.returnValue(observableOf(null)),
      getEventsGroup: jasmine.createSpy().and.returnValue(observableOf(null)),
      getEventForClass: jasmine.createSpy().and.returnValue(observableOf(SSResponseMock))
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        VS_EVENT_FINISHED: 'VS_EVENT_FINISHED'
      }
    };

    filterService = {
      removeLineSymbol: (val) => val,
      orderBy: jasmine.createSpy().and.callFake(a => a)
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Each Way: 1/3 odds a places 1,2,3')
    };

    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy(),
        clearInterval: jasmine.createSpy()
      },
      document: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };

    insomniaService = {
      setTimeoutAction: jasmine.createSpy()
    };

    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(observableOf(<any>{
        alias1: true,
        alias2: true
      })),
      getVirtualSports: jasmine.createSpy().and.returnValue(of(cmsVirtualSports))
    };

    eventService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable')
    };

    parentCategory.childs.set(child.classId, child);

    vsMapperService = {
      setParentCategory: jasmine.createSpy('setParentCategory'),
      setChildCategory: jasmine.createSpy('setChildCategory'),
      getChildByAlias: jasmine.createSpy('getChildByAlias').and.returnValue(child),
      getChildByClassId: jasmine.createSpy('getChildByAlias').and.returnValue(child),
      getCategoryByAlias: jasmine.createSpy('getCategoryByAlias').and.returnValue(classId),
      getAliasesByClassId: jasmine.createSpy('getAliasesByClassId').and.returnValue({
        parentAlias: 'motorsports',
        childAlias: 'inspired-cycling'
      }),
      getAllClasses: jasmine.createSpy('getAllClasses').and.returnValue([classId]),
      structure: [parentCategory]
    };

    const setSpy = jasmine.createSpy('setSpy');
    const getSpy = jasmine.createSpy('getSpy').and.returnValue([parentCategory]);

    Object.defineProperty(vsMapperService, 'structure', { get: getSpy });
    Object.defineProperty(vsMapperService, 'structure', { set: setSpy });

    pubSubService.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });

    service = new VirtualSportsService(
      vsMapperService,
      timeService,
      eventProvider,
      pubSubService,
      filterService,
      localeService,
      windowRefService,
      insomniaService,
      cmsService,
      eventService
    );
  });

  describe('addLiveServeUpdateEventListener', () => {
    it('should call addEventListener', () => {
      windowRefService.document.addEventListener.and.callFake((v1, cb) => cb({
        detail: { liveUpdate: null }
      }));

      service.addLiveServeUpdateEventListener();

      expect(windowRefService.document.addEventListener).toHaveBeenCalled();
    });

    it('should define liveServeUpdateEventListenerSubscription', () => {
      service['liveServeUpdateEventListenerSubscription'] = undefined;

      service.addLiveServeUpdateEventListener();
      expect(service['liveServeUpdateEventListenerSubscription']).toBeDefined();


      service['liveServeUpdateEventListenerSubscription']();
      expect(windowRefService.document.removeEventListener).toHaveBeenCalled();
    });
  });

  describe('removeLiveServeUpdateEventListener', () => {
    let removeLiveServeUpdateEventListenerSpy;
    beforeEach(() => {
      removeLiveServeUpdateEventListenerSpy = jasmine.createSpy('removeLiveServeUpdateEventListenerSpy');
    });

    it('should remove event (LIVE_SERVE_UPDATE) listener', () => {
      service['liveServeUpdateEventListenerSubscription'] = () => removeLiveServeUpdateEventListenerSpy();

      service.removeLiveServeUpdateEventListener();

      expect(removeLiveServeUpdateEventListenerSpy).toHaveBeenCalled();
    });

    it('should not remove event (LIVE_SERVE_UPDATE) listener', () => {
      service['liveServeUpdateEventListenerSubscription'] = undefined;

      service.removeLiveServeUpdateEventListener();

      expect(removeLiveServeUpdateEventListenerSpy).not.toHaveBeenCalled();
    });
  });

  it('time', fakeAsync(() => {
    service.time.subscribe(result => expect(result).toBe(Date.now()));
    tick(1000);
    discardPeriodicTasks();
  }));

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('unsubscribeFromUpdates', () => {
    service['updateEventsInterval'] = 1;
    service['currentEventInterval'] = 1;
    service.unsubscribeFromUpdates();
    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalledWith(service['updateEventsInterval']);
  });

  it('unsubscribeFromUpdates', () => {
    service['updateEventsInterval'] = 0;
    service['currentEventInterval'] = 0;
    service.unsubscribeFromUpdates();
    expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
  });

  it('subscribeForUpdates', () => {
    service['updateEventsInterval'] = 1;
    service['currentEventInterval'] = 1;
    service.unsubscribeFromUpdates = jasmine.createSpy();

    service.subscribeForUpdates();
    expect(service.unsubscribeFromUpdates).toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setInterval).toHaveBeenCalledWith(
      jasmine.any(Function), timeService.refreshInterval
    );
  });

  it('subscribeForUpdates, if updateEventsInterval is 0', () => {
    service['updateEventsInterval'] = 0;
    service.unsubscribeFromUpdates = jasmine.createSpy();

    service.subscribeForUpdates();
    expect(service.unsubscribeFromUpdates).not.toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setInterval).toHaveBeenCalledWith(
      jasmine.any(Function), timeService.refreshInterval
    );
  });

  it('subscribeForUpdates, if setInterval is called', () => {
    service['updateEventsInterval'] = 0;
    service.unsubscribeFromUpdates = jasmine.createSpy();
    service['updateEvents'] = jasmine.createSpy();
    windowRefService.nativeWindow.setInterval.and.callFake(cb => cb());

    service.subscribeForUpdates();

    expect(service['updateEvents']).toHaveBeenCalled();
  });

  it('subscribeVSBRForUpdates', () => {
    const events = [{
      event: {
        id: 1,
        liveServChannels: '1,2,3'
      }
    }] as any;

    service.subscribeVSBRForUpdates(events);

    expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
      channel: jasmine.any(Array),
      module: 'vsbr'
    });
  });

  it('unSubscribeVSBRForUpdates', () => {
    service.unSubscribeVSBRForUpdates();

    expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'vsbr');
  });

  describe('finishEvent', () => {
    let liveServeUpdObj;

    beforeEach(() => {
      liveServeUpdObj = {
        subject_number: 1,
        payload: {
          result_conf: 'Y'
        }
      } as any;
      service['subscribedVSBREventsIdList'] = ['1'];
    });

    it('should broadcast VS_EVENT_FINISHED', () => {
      service.finishEvent(liveServeUpdObj);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.VS_EVENT_FINISHED, {
        eventId: liveServeUpdObj.subject_number.toString()
      });
    });

    it('should not broadcast VS_EVENT_FINISHED', () => {
      liveServeUpdObj.payload.result_conf = 'N';

      service.finishEvent(liveServeUpdObj);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not broadcast VS_EVENT_FINISHED if event is not is subscribed list', () => {
      service['subscribedVSBREventsIdList'] = [];

      service.finishEvent(liveServeUpdObj);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('showTerms', () => {
    expect(
      service.showTerms({
        eachWayFactorNum: '', eachWayFactorDen: '', eachWayPlaces: ''
      } as any)
    ).toBeFalsy();

    expect(
      service.showTerms({
        eachWayFactorNum: '2', eachWayFactorDen: '3', eachWayPlaces: '4'
      } as any)
    ).toBeTruthy();

    expect(service.showTerms({} as any)).toBeFalsy();
  });

  it('genTerms', () => {
    const market: any = {
      eachWayFactorNum: '1',
      eachWayFactorDen: '2',
      eachWayPlaces: '3'
    };

    service.genTerms(market);

    expect(localeService.getString).toHaveBeenCalledWith('vsbr.oddsAPlaces', {
      num: market.eachWayFactorNum,
      den: market.eachWayFactorDen,
      arr: '1-2-3'
    });
  });

  it('genTerms if market is invalid', () => {
    const market: any = {};
    const result = service.genTerms(market);

    expect(result).toEqual('');
  });

  it('getActiveClass', () => {
    const childItem = parentCategory.childs.get(classId);
    const childCategory = service.getActiveClass('inspired-cycling');

    expect(childCategory).toEqual(childItem);
  });

  it('filterEvents if there is at least one event ', () => {
    const localEvent = {
      event: {
        isFinished: true,
        isResulted: true
      }
    } as any;
    service['deleteOutDatedEvents'] = jasmine.createSpy();

    service.filterEvents([localEvent]);
    expect(service['deleteOutDatedEvents']).toHaveBeenCalled();
  });

  it('filterEvents if array with events is empty', () => {
    service['deleteOutDatedEvents'] = jasmine.createSpy();
    service.filterEvents([]);
    expect(service['deleteOutDatedEvents']).toHaveBeenCalled();
  });

  describe('@getMarketSectionsArray', () => {
    it('should return empty markets if such were present initially', () => {
      expect(service.getMarketSectionsArray({} as any)).toEqual([]);
    });

    it('it should set correct template to market', () => {
      const localEvent = {
        event: {
          className: 'Virtual Tennis',
          children: [{
            market: {
              templateMarketName: 'Correct score (GAME)',
              name: '|Correct score (GAME)|',
              dispSortName: 'CS',
              displayOrder: '1',
              children: [{
                outcome: {
                  displayOrder: '1'
                }
              }, {
                outcome: {
                  displayOrder: '0'
                }
              }]
            }
          }]
        }
      } as any;
      const market = [{
        displayOrder: 1,
        name: 'Correct score (GAME)',
        sectionTitle: 'Correct score (GAME)',
        templateMarketName: 'Correct score (GAME)',
        template: 'Vertical',
        dispSortName: 'CS',
        children: [{
          outcome: {
            displayOrder: '1'
          }
        }, {
          outcome: {
            displayOrder: '0'
          }
        }]
      }] as any;
      expect(service.getMarketSectionsArray(localEvent)).toEqual(market);
    });

    it('it should set horizontal template for market HH', () => {
      const localEvent = {
        event: {
          className: 'Virtual Football',
          children: [{
            market: {
              name: '|Unknown Market|',
              templateMarketName: 'Head/Head (winner)',
              dispSortName: 'HH',
              displayOrder: '1',
              children: [{
                outcome: {
                  outcomeMeaningMinorCode: 'A',
                  displayOrder: '1'
                }
              }, {
                outcome: {
                  outcomeMeaningMinorCode: 'H',
                  displayOrder: '0'
                }
              }]
            }
          }]
        }
      } as any;
      const market = [{
        displayOrder: 1,
        name: 'Unknown Market',
        sectionTitle: 'Unknown Market',
        templateMarketName: 'Head/Head (winner)',
        template: 'Horizontal',
        dispSortName: 'HH',
        children: [{
          outcome: {
            outcomeMeaningMinorCode: 3,
            displayOrder: '1'
          }
        }, {
          outcome: {
            outcomeMeaningMinorCode: 1,
            displayOrder: '0'
          }
        }]
      }] as any;
      expect(service.getMarketSectionsArray(localEvent)).toEqual(market);
    });

    it('it should set default template if market is unknown', () => {
      const localEvent = {
        event: {
          className: 'Virtual Football',
          children: [{
            market: {
              name: '|Unknown Market|',
              templateMarketName: 'Head/Head (winner)',
              dispSortName: 'HA',
              displayOrder: '1',
              children: [{
                outcome: {
                  outcomeMeaningMinorCode: 'A',
                  displayOrder: '1'
                }
              }, {
                outcome: {
                  outcomeMeaningMinorCode: 'H',
                  displayOrder: '0'
                }
              }]
            }
          }]
        }
      } as any;
      const market = [{
        displayOrder: 1,
        name: 'Unknown Market',
        sectionTitle: 'Unknown Market',
        templateMarketName: 'Head/Head (winner)',
        template: 'Vertical',
        dispSortName: 'HA',
        children: [{
          outcome: {
            outcomeMeaningMinorCode: 3,
            displayOrder: '1'
          }
        }, {
          outcome: {
            outcomeMeaningMinorCode: 1,
            displayOrder: '0'
          }
        }]
      }] as any;
      expect(service.getMarketSectionsArray(localEvent)).toEqual(market);
    });

    it('it should return array of sections objects for CS market', () => {
      const localEvent = {
        event: {
          className: 'Virtual Football',
          children: [{
            market: {
              name: '|Correct score|',
              templateMarketName: 'Correct score',
              dispSortName: 'CS',
              displayOrder: '1',
              children: [{
                outcome: {
                  outcomeMeaningMinorCode: 'S',
                  outcomeMeaningScores: '1,0,',
                  displayOrder: '1'
                }
              }, {
                outcome: {
                  outcomeMeaningMinorCode: 'S',
                  outcomeMeaningScores: '2,0,',
                  displayOrder: '0'
                }
              }]
            }
          }]
        }
      } as any;
      const market = [{
        dispSortName: 'CS',
        displayOrder: 1,
        name: 'Correct score',
        sectionTitle: 'Correct score',
        templateMarketName: 'Correct score',
        template: 'Column',
        children: [{
          outcome: {
            outcomeMeaningMinorCode: 1,
            outcomeMeaningScores: '1,0,',
            displayOrder: '1'
          },
          outcomeMeaningMinorCode: 1
        }, {
          outcome: {
            outcomeMeaningMinorCode: 1,
            outcomeMeaningScores: '2,0,',
            displayOrder: '0'
          },
          outcomeMeaningMinorCode: 1
        }]
      }] as any;
      expect(service.getMarketSectionsArray(localEvent)).toEqual(market);
    });
  });

  it('getMarketSectionsArray', () => {
    service['filterOutcomes'] = jasmine.createSpy().and.returnValue({ name: 'Double Chance' });
    service['groupCorrectScoreOutcomes'] = jasmine.createSpy();
    service['_getMarketSectionTitle'] = jasmine.createSpy();

    const eventItem: any = {
      event: {
        children: [
          { market: {} },
          { market: {} }
        ]
      }
    };

    expect(service.getMarketSectionsArray(eventItem)).toEqual(jasmine.any(Array));
    expect(service['filterOutcomes']).toHaveBeenCalledTimes(2);
    expect(service['_getMarketSectionTitle']).toHaveBeenCalledTimes(2);
  });

  it('getCategoryByAlias', () => {
    expect(service.getCategoryByAlias('inspired-cycling')).toEqual(classId);
  });

  it('getCategoryByAlias', () => {
    vsMapperService.getChildByAlias = jasmine.createSpy('getChildByAlias').and.returnValue(undefined);
    expect(service.getCategoryByAlias('inspired-cycling2')).toBeFalsy();
  });

  it('getAliasesByClassId positive case', () => {
    expect(service.getAliasesByClassId(child.classId)).toEqual({
      parentAlias: parentCategory.alias,
      childAlias: child.alias
    });
  });

  it('getAliasesByClassId if vsMapperService.getAliasesByClassId return undefined', () => {
    vsMapperService.getAliasesByClassId = jasmine.createSpy('getAliasesByClassId').and.returnValue(undefined);

    expect(service.getAliasesByClassId('')).toBeUndefined();
  });

  it('isReloaded', () => {
    service['isReloadedAfterSleep'] = true;
    expect(service.isReloaded()).toEqual(service['isReloadedAfterSleep']);
  });

  it('setIsReloaded', () => {
    service.setIsReloaded(true);
    expect(service['isReloadedAfterSleep']).toEqual(true);
  });

  describe('@eventsData', () => {
    it('should return virtualSports structure', fakeAsync(() => {
      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(result).toEqual([parentCategory]);
          expect(result.length).toEqual(1);
          expect(pubSubService.subscribe).toHaveBeenCalledWith('virtualSport', 'INSOMNIA', jasmine.any(Function));

          expect(eventProvider.getEventForClass).toHaveBeenCalled();
          expect(vsMapperService.setParentCategory).toHaveBeenCalled();
          expect(vsMapperService.setChildCategory).toHaveBeenCalled();
          expect(vsMapperService.getAllClasses).toHaveBeenCalled();
        });

      tick();
    }));

    it('should return virtualSports structure and handle differences between events and classes', fakeAsync(() => {
      const localChild = { ...child };

      localChild.classId = '288';
      parentCategory.childs.set(localChild.classId, localChild);

      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(result).toEqual([parentCategory]);
          expect(result.length).toEqual(1);
          expect(pubSubService.subscribe).toHaveBeenCalledWith('virtualSport', 'INSOMNIA', jasmine.any(Function));

          expect(eventProvider.getEventForClass).toHaveBeenCalled();
          expect(vsMapperService.setParentCategory).toHaveBeenCalled();
          expect(vsMapperService.setChildCategory).toHaveBeenCalled();
          expect(vsMapperService.getAllClasses).toHaveBeenCalled();
        });

      tick();

      // reset to default
      parentCategory.childs.delete(localChild.classId);
    }));

    it('should return virtualSports structure if either getChildByClassId return undefined', fakeAsync(() => {
      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');
      vsMapperService.getChildByClassId = jasmine.createSpy('getChildByClassId').and.returnValue(undefined);
      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(service.updateCategoryClasses).not.toHaveBeenCalled();
        });

      tick();
    }));

    it('should return virtualSports structure and call updateCategoryClasses', fakeAsync(() => {
      SSResponseMock.SSResponse.children[0].event.classId = '288';

      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');

      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(service.updateCategoryClasses).not.toHaveBeenCalled();
          expect(result).toEqual(vsMapperService.structure);
        });

      tick();

      // reset to default
      SSResponseMock.SSResponse.children[0].event.classId = '287';
    }));

    it('should call updateEventsBuffer and return vs structure if lazyload is true', fakeAsync(() => {
      service['eventsBuffer'] = {
        '287': [{ event: { typeId: '5', id: 1 } }]
      } as any;
      service['updateEventsBuffer'] = jasmine.createSpy('updateEventsBuffer');

      service.eventsData(true)
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(result).toEqual([parentCategory]);
          expect(result.length).toEqual(1);

          expect(service['updateEventsBuffer']).toHaveBeenCalled();
          expect(pubSubService.subscribe).toHaveBeenCalledWith('virtualSport', 'INSOMNIA', jasmine.any(Function));
        });

      tick();
    }));

    it('should throw error if there no categories in CMS response', fakeAsync(() => {
      service.vsMapperService.getAllClasses = jasmine.createSpy('getAllClasses').and.returnValue([]);

      service.eventsData()
        .subscribe(() => {
        }, err => {
          expect(err).toEqual('noCategories');
        });

      tick();

      // reset to default
      service.vsMapperService = vsMapperService;
    }));

    it('should throw error if there no categories broken CMS response', fakeAsync(() => {
      service['cmsService'].getVirtualSports = jasmine.createSpy().and.returnValue(of(undefined));

      service.eventsData()
        .subscribe(() => {
        }, err => {
          expect(err).toEqual('noCategories');
        });

      tick();

      // reset to default
      service['cmsService'] = cmsService;
    }));

    it('should throw error if there no child categories in parents', fakeAsync(() => {
      const localVirtualSports = [...cmsVirtualSports];
      localVirtualSports[0].tracks = undefined;

      service['cmsService'].getVirtualSports = jasmine.createSpy().and.returnValue(of(localVirtualSports));
      service.eventsData()
        .subscribe(() => {
        }, err => {
          expect(err).toEqual('noCategories');
        });

      tick();

      // reset to default
      service['cmsService'] = cmsService;
    }));

    it('virtualSport INSOMNIA if  actionType === category-update', fakeAsync(() => {
      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');

      service.eventsData()
        .subscribe(() => {
          const localChild = { ...child };
          const data = { actionType: 'category-update', classId: '287' };
          const response = {
            '287': [{
              'event': {
                classId: '287',
                startTime: '2020-01-01',
                name: 'RPR',
                children: [
                  { market: {} },
                  { market: {} }
                ],
                startTimeUnix: 1577836800000
              }
            }
            ]
          };

          delete localChild.events;
          service.vsMapperService.getChildByClassId = jasmine.createSpy('getChildByClassId').and.returnValue(localChild);

          callbacks['INSOMNIA'](data);

          expect(localChild.events).toBeDefined();
          expect(service.updateCategoryClasses).toHaveBeenCalledWith(response[data.classId], localChild);
          expect(service.updateCategoryClasses).toHaveBeenCalledTimes(2);
        });

      tick();

      // reset changes
      service.vsMapperService = vsMapperService;
    }));

    it('virtualSport INSOMNIA, action category-update, but there no category data for classId', fakeAsync(() => {
      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');

      service.eventsData()
        .subscribe(() => {
          const localChild = { ...child };
          const data = { actionType: 'category-update', classId: '287' };

          delete localChild.events;
          vsMapperService.getChildByClassId = jasmine.createSpy('getChildByClassId').and.returnValue(undefined);

          callbacks['INSOMNIA'](data);

          expect(localChild.events).not.toBeDefined();
          expect(service.updateCategoryClasses).not.toHaveBeenCalledTimes(2);
        });

      tick();
    }));

    it('virtualSport INSOMNIA if  action is category-update and there are no events for category with classId', fakeAsync(() => {
      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');

      service.eventsData()
        .subscribe(() => {
          const localChild = { ...child };
          const data = { actionType: 'category-update', classId: '' };

          delete localChild.events;
          service.vsMapperService.getChildByClassId = jasmine.createSpy('getChildByClassId').and.returnValue(localChild);

          const response = callbacks['INSOMNIA'](data);

          expect(localChild.events).not.toBeDefined();
          expect(service.updateCategoryClasses).toHaveBeenCalledTimes(1);
          expect(response).toEqual(service.vsMapperService.structure);
        });

      tick();

      service.vsMapperService = vsMapperService;
    }));

    it('virtualSport INSOMNIA if  actionType != category-update', fakeAsync(() => {
      service.updateCategoryClasses = jasmine.createSpy('updateCategoryClasses');

      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          const data = { actionType: 'category-update2', classId: '287' };
          const localChild = { ...child };

          delete localChild.events;

          callbacks['INSOMNIA'](data);

          expect(localChild.events).not.toBeDefined();
          expect(service.updateCategoryClasses).not.toHaveBeenCalledTimes(2);
        });

      tick();
    }));

    it('should return virtualSports structure for class Id 223', fakeAsync(() => {
      service.vsMapperService.getAllClasses = jasmine.createSpy('getAllClasses').and.returnValue(['223']);
      eventProvider.getEventForClass = jasmine.createSpy().and.returnValue(observableOf(SSResponseMockLegends));
      const localChild = { ...child };

      localChild.classId = '223';
      legendsParentCategory.childs.set(localChild.classId, localChild);
      service.vsMapperService.structure = [legendsParentCategory];
      service.eventsData()
        .subscribe((result: IVirtualCategoryStructure[]) => {
          expect(result).toEqual([parentCategory]);
          expect(result.length).toEqual(1);
          expect(pubSubService.subscribe).toHaveBeenCalledWith('virtualSport', 'INSOMNIA', jasmine.any(Function));

          expect(eventProvider.getEventForClass).toHaveBeenCalled();
          expect(vsMapperService.setParentCategory).toHaveBeenCalled();
          expect(vsMapperService.setChildCategory).toHaveBeenCalled();
          expect(vsMapperService.getAllClasses).toHaveBeenCalled();
        });

      tick();
    }));
  });

  it('generateClass', () => {
    expect(service.generateClass('He|llo Wor|ld')).toBe('hello-world');
  });

  describe('@updateCategoryClasses', () => {
    let classEvents: any[];
    let childItem;
    let localChild;

    beforeEach(() => {
      localChild = { ...childItem };

      delete localChild.timeLeft;
      delete localChild.startTimeUnix;

      classEvents = [
        {
          event: {
            startTimeUnix: Date.now() * 2
          }
        }
      ];

      service['subscribeForClassUpdates'] = jasmine.createSpy();
      childItem = parentCategory.childs.get(classId);

    });

    it('if startTimeUnix is in the a future', () => {
      service.updateCategoryClasses(classEvents, localChild);

      expect(localChild.startTimeUnix).toEqual(jasmine.any(Number));
      expect(localChild.timeLeft).toEqual(jasmine.any(Number));
      expect(service['subscribeForClassUpdates']).toHaveBeenCalledTimes(1);
    });

    it('if startTimeUnix is in the past', () => {
      const localClassEvents: any[] = [{
        event: {
          startTimeUnix: 1
        }
      }];

      service.updateCategoryClasses(localClassEvents, localChild);

      expect(localChild.timeLeft).toEqual(0);
      expect(windowRefService.nativeWindow.stopEventActual).toBeDefined();
      expect(windowRefService.nativeWindow.useStopEventActual).toBeDefined();
      expect(windowRefService.nativeWindow.stopEventActual).toEqual(jasmine.any(Function));
      expect(windowRefService.nativeWindow.useStopEventActual).toEqual(jasmine.any(Function));
    });

    it('if startTimeUnix for all events is in the past', () => {
      const localClassEvents: any[] = [{
        event: {
          startTimeUnix: 1
        }
      }, {
        event: {
          startTimeUnix: 1
        }
      }, {
        event: {
          startTimeUnix: Date.now() * 2
        }
      }];

      service.updateCategoryClasses(localClassEvents, localChild);

      expect(localChild.timeLeft).not.toEqual(0);
      expect(windowRefService.nativeWindow.stopEventActual).toBeUndefined();
      expect(windowRefService.nativeWindow.useStopEventActual).toBeUndefined();
    });

    it('if events is empty', () => {
      const localClassEvents = [];
      service.updateCategoryClasses(localClassEvents, localChild);

      expect(localChild.startTimeUnix).toBeUndefined();
      expect(localChild.timeLeft).toBeUndefined();
      expect(service['subscribeForClassUpdates']).not.toHaveBeenCalled();
    });
  });

  it('configureOutcomes', () => {
    const markets: any[] = [
      {
        market: {
          children: [
            { outcome: {} },
            { outcome: {} }
          ]
        }
      }
    ];

    expect(service['configureOutcomes'](markets, true)).toBe(markets);
    expect(markets[0].market.children[0].outcome.isUS).toBeTruthy();
    expect(markets[0].market.children[1].outcome.isUS).toBeTruthy();

    expect(service['configureOutcomes'](markets, false)).toBe(markets);
    expect(markets[0].market.children[0].outcome.isUS).toBeFalsy();
    expect(markets[0].market.children[1].outcome.isUS).toBeFalsy();
  });

  it('configureEvents', () => {
    service['configureOutcomes'] = jasmine.createSpy();

    const events: any[] = [
      {
        event: {
          startTime: '2020-01-01',
          name: '20:00 RPR'
        }
      },
      {
        event: null
      }
    ];

    const result = service['configureEvents'](events);

    expect(service['configureOutcomes']).toHaveBeenCalledTimes(1);
    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(1);
    expect(result[0].event.startTimeUnix).toEqual(jasmine.any(Number));
    expect(result[0].event.name).toBe('RPR');
    expect(filterService.orderBy).toHaveBeenCalled();
  });

  it('groupEventsByClass', () => {
    const events: any[] = [
      {
        event: { classId: 'A' }
      },
      {
        event: { classId: 'B' }
      },
      {
        event: { classId: 'A' }
      }
    ];

    const result = service['groupEventsByClass'](events);

    expect(result).toEqual(jasmine.any(Object));
    expect(result['A']).toEqual([events[0], events[2]]);
    expect(result['B']).toEqual([events[1]]);
  });

  it('subscribeForClassUpdates', () => {
    service['subscribeForClassUpdates'](parentCategory.childs.get(classId));

    expect(insomniaService.setTimeoutAction).toHaveBeenCalledWith({
      eventName: `category-update-${classId}`,
      classId: Number(classId),
      actionType: 'category-update'
    }, jasmine.any(Number));
  });

  it('subscribeForClassUpdates if stopEventActual not undefined', () => {
    service['windowRef'].nativeWindow.stopEventActual = 1;

    service['subscribeForClassUpdates'](parentCategory.childs.get(classId));

    expect(insomniaService.setTimeoutAction).not.toHaveBeenCalled();
  });

  it('updateEventsBuffer', () => {
    service['eventsBuffer'] = { A: [], C: [] };

    const events: any = {
      A: [1, 2], B: [3], C: [4]
    };

    service['updateEventsBuffer'](events, ['A', 'C']);

    expect(service['eventsBuffer']['A']).toEqual(events.A);
    expect(service['eventsBuffer']['B']).toBeUndefined();
    expect(service['eventsBuffer']['C']).toEqual(events.C);
  });

  it('getBrTypesString', () => {
    service['BR_TYPE_ID'] = ['A', 'B'];
    expect(service['getBrTypesString']()).toBe(
      'simpleFilter=event.typeId:notEquals:A&simpleFilter=event.typeId:notEquals:B'
    );
  });

  it('updateEvents', () => {
    service.eventsData = jasmine.createSpy().and.returnValue(observableOf(null));
    service['updateEvents']();
    expect(timeService.selectTimeRangeStartDelta).toHaveBeenCalledWith(service['deltaTimeNowUnix']);
    expect(timeService.selectTimeRangeEndDelta).toHaveBeenCalledWith(service['deltaTimeNowUnix']);
    expect(service.eventsData).toHaveBeenCalled();
  });

  it('deleteOutDatedEvents', () => {
    const events: any[] = [
      {
        event: { startTimeUnix: 4070901600000 }
      },
      {
        event: { startTimeUnix: 946677600000 }
      }
    ];

    const result = service['deleteOutDatedEvents'](events);

    expect(result).toBe(events);
    expect(result.length).toBe(1);
  });

  it('_isWinOrEw', () => {
    expect(service['_isWinOrEw']('To Win')).toBeTruthy();
    expect(service['_isWinOrEw']('To Fail')).toBeFalsy();
  });

  it('_isMatchBetting', () => {
    expect(service['_isMatchBetting']('Match Result')).toBeTruthy();
    expect(service['_isMatchBetting']('Match Stats')).toBeFalsy();
  });

  it('_getMarketSectionTitle', () => {
    expect(service['_getMarketSectionTitle']('To Win')).toBeTruthy();
    expect(service['_getMarketSectionTitle']('Match Result')).toBeTruthy();
    expect(service['_getMarketSectionTitle']('HR')).toBe('HR');
  });

  it('reverseMap', () => {
    expect(
      service['reverseMap']({ asd: ['a', 's', 'd'], zxc: ['z', 'x', 'c'] })
    ).toEqual({ a: 'asd', s: 'asd', d: 'asd', z: 'zxc', x: 'zxc', c: 'zxc' });
  });

  it('filterOutcomes', () => {
    const market: any = {
      children: [
        { outcome: { outcomeMeaningMinorCode: 'C' } },
        { outcome: {} }
      ]
    };

    service['sortOutcomes'] = jasmine.createSpy().and.callFake(() => market.children);
    service['getCorrectedOutcomeMeaningMinorCode'] = jasmine.createSpy();

    expect(service['filterOutcomes'](market)).toBe(market);
    expect(service['sortOutcomes']).toHaveBeenCalledWith(market.children);
    expect(service['getCorrectedOutcomeMeaningMinorCode']).toHaveBeenCalledTimes(1);
  });

  it('sortOutcomes', () => {
    let outcomes: any[] = [{}];
    expect(service['sortOutcomes'](outcomes)).toBe(outcomes);

    outcomes = [{
      outcome: { isUS: true }
    }];
    service['sortOutcomes'](outcomes);
    expect(filterService.orderBy).toHaveBeenCalledWith(outcomes, ['outcomeMeaningMinorCode']);
  });

  it('getCorrectedOutcomeMeaningMinorCode', () => {
    [
      {
        outcome: { outcomeMeaningMinorCode: 'H', isUS: true },
        result: 3
      },
      {
        outcome: { outcomeMeaningMinorCode: 'H', isUS: false },
        result: 1
      },
      {
        outcome: { outcomeMeaningMinorCode: 'D' },
        result: 2
      },
      {
        outcome: { outcomeMeaningMinorCode: 'N' },
        result: 2
      },
      {
        outcome: { outcomeMeaningMinorCode: 'L' },
        result: 2
      },
      {
        outcome: { outcomeMeaningMinorCode: 'A', isUS: true },
        result: 1
      },
      {
        outcome: { outcomeMeaningMinorCode: 'A', isUS: false },
        result: 3
      },
      {
        outcome: { outcomeMeaningMinorCode: '9' },
        result: 9
      }
    ].forEach(item => {
      expect(
        service['getCorrectedOutcomeMeaningMinorCode'](item.outcome as any)
      ).toBe(item.result);
    });
  });

  it('groupCorrectScoreOutcomes', () => {
    service['getCode'] = jasmine.createSpy();

    const market: any = {
      children: [
        { outcomeMeaningScores: '1' },
        { outcomeMeaningScores: '1,2' },
        { outcomeMeaningScores: '1,2,3' },
        {}
      ]
    };

    const result = service['groupCorrectScoreOutcomes'](market);

    expect(service['getCode']).toHaveBeenCalledTimes(2);
    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(market.children.length);
  });

  it('getCode', () => {
    expect(service['getCode'](10, 5)).toBe(1);
    expect(service['getCode'](2, 2)).toBe(2);
    expect(service['getCode'](2, 6)).toBe(3);
  });

  describe('@normalizeData', () => {
    it('should not normalize event markets if they are not present', () => {
      const localEvent = {
          event: {
            eventStatusCode: 'A'
          }
        } as any,
        result = {
          eventStatusCode: 'A',
          markets: []
        } as any;

      expect(service.normalizeData(localEvent, false)).toEqual(result);
    });

    it('it should normalize Virtual events Data for WinEw Market', () => {
      const localEvent = {
        event: {
          eventStatusCode: 'A',
          className: 'Virtual Racing',
          children: [{
            market: {
              name: 'Win/Each Way',
              eachWayFactorNum: '1',
              eachWayFactorDen: '3',
              eachWayPlaces: '3',
              children: [{
                outcome: {
                  drawNumber: '1',
                  displayOrder: '1'
                }
              }, {
                outcome: {
                  drawNumber: '2',
                  displayOrder: '0'
                }
              }]
            }
          }]
        }
      } as any;
      const market = {
        eachWayFactorDen: '3',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        isEachWayAvailable: true,
        marketName: 'Win/Each Way',
        name: 'Win/Each Way',
        terms: 'Each Way: 1/3 odds a places 1,2,3',
        outcomes: [{
          drawNumber: '1',
          runnerNumber: '1',
          silkName: '1',
          displayOrder: '1'
        }, {
          drawNumber: '2',
          runnerNumber: '2',
          silkName: '2',
          displayOrder: '0'
        }],
        children: [{
          outcome: {
            drawNumber: '1',
            runnerNumber: '1',
            silkName: '1',
            displayOrder: '1'
          }
        }, {
          outcome: {
            drawNumber: '2',
            silkName: '2',
            runnerNumber: '2',
            displayOrder: '0'
          }
        }]
      };
      const resultEvent = {
        eventStatusCode: 'A',
        className: 'Virtual Racing',
        children: [{
          market: market
        }],
        markets: [market]
      } as any;
      const result = service.normalizeData(localEvent, false);
      expect(result).toEqual(resultEvent);
      expect(localeService.getString).toHaveBeenCalledWith('vsbr.oddsAPlaces', {
        num: '1',
        den: '3',
        arr: '1-2-3'
      });
    });

    it('it should normalize Virtual events Data for different markets', () => {
      const localEvent = {
        event: {
          eventStatusCode: 'A',
          className: 'Virtual Speedway',
          children: [{
            market: {
              name: 'Winning Checkout',
              children: [{
                outcome: {
                  drawNumber: '1',
                  displayOrder: '1'
                }
              }]
            }
          }]
        }
      } as any;
      const market = {
        marketName: 'Winning Checkout',
        name: 'Winning Checkout',
        outcomes: [{
          drawNumber: '1',
          silkName: '1',
          runnerNumber: '1',
          displayOrder: '1'
        }],
        children: [{
          outcome: {
            drawNumber: '1',
            silkName: '1',
            runnerNumber: '1',
            displayOrder: '1'
          }
        }]
      };
      const resultEvent = {
        eventStatusCode: 'S',
        className: 'Virtual Speedway',
        children: [{
          market: market
        }],
        markets: [market]
      } as any;
      const result = service.normalizeData(localEvent, true);
      expect(result).toEqual(resultEvent);
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('it should normalize Virtual events Data if drawNumber is not exist', () => {
      const localEvent = {
        event: {
          eventStatusCode: 'A',
          className: '|Virtual Speedway|',
          children: [{
            market: {
              name: 'Winning Checkout',
              children: [{
                outcome: {
                  silkName: '1',
                  runnerNumber: '1',
                  displayOrder: '1'
                }
              }]
            }
          }]
        }
      } as any;
      const market = {
        marketName: 'Winning Checkout',
        name: 'Winning Checkout',
        outcomes: [{
          silkName: '1',
          runnerNumber: '1',
          displayOrder: '1'
        }],
        children: [{
          outcome: {
            silkName: '1',
            runnerNumber: '1',
            displayOrder: '1'
          }
        }]
      };
      const resultEvent = {
        eventStatusCode: 'S',
        className: '|Virtual Speedway|',
        children: [{
          market: market
        }],
        markets: [market]
      } as any;
      const result = service.normalizeData(localEvent, true);
      expect(result).toEqual(resultEvent);
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('it should normalize Virtual events Data if drawNumber & runnerNumber is not exist', () => {
      const localEvent = {
        event: {
          eventStatusCode: 'A',
          className: '|Virtual Speedway|',
          children: [{
            market: {
              name: 'Winning Checkout',
              children: [{
                outcome: {
                  silkName: '1',
                  displayOrder: '1'
                }
              }]
            }
          }]
        }
      } as any;
      const market = {
        marketName: 'Winning Checkout',
        name: 'Winning Checkout',
        outcomes: [{
          silkName: '1',
          runnerNumber: '1',
          displayOrder: '1'
        }],
        children: [{
          outcome: {
            silkName: '1',
            runnerNumber: '1',
            displayOrder: '1'
          }
        }]
      };
      const resultEvent = {
        eventStatusCode: 'S',
        className: '|Virtual Speedway|',
        children: [{
          market: market
        }],
        markets: [market]
      } as any;
      const result = service.normalizeData(localEvent, true);
      expect(result).toEqual(resultEvent);
      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });

  describe('@getEventsWithRacingForms', () => {
    it('failure due server error', fakeAsync(() => {
      eventProvider.getEventsGroup = jasmine.createSpy().and.returnValue(throwError({}));
      service.getCategoryByAlias = jasmine.createSpy('getCategoryByAlias').and.returnValue(121);
      service['BR_TYPE_ID'] = ['1', '2'];
      let rejected: boolean = false;
      service['eventsBuffer'] = {
        '121': [{ event: { typeId: '5', id: 1 } }]
      } as any;

      service.getEventsWithRacingForms('123').catch(() => {
        rejected = true;
      });
      tick();

      expect(rejected).toBe(true);
    }));

    it('split to chunks and updated event in buffer', fakeAsync(() => {
      const eventFromSiteServe: any = { event: { typeId: '5', id: 1, additionalProperty: 3 } };
      const bufferEvent: any = { event: { typeId: '5', id: 1 } };
      const eventsFromMultipleRequests: any[] =
        [eventFromSiteServe, cloneWithId(eventFromSiteServe, 2), cloneWithId(eventFromSiteServe, 3)];
      service['eventsBuffer'] = {
        '121': [bufferEvent, cloneWithId(bufferEvent, 2), cloneWithId(bufferEvent, 3)]
      } as any;
      service['chunkSize'] = 2;

      eventProvider.getEventsGroup = jasmine.createSpy().and.returnValue(of(<any>eventsFromMultipleRequests));
      service.getCategoryByAlias = jasmine.createSpy('getCategoryByAlias').and.returnValue(121);
      service['BR_TYPE_ID'] = ['1', '2'];

      let bufferEventsUpdated = null;
      service.getEventsWithRacingForms('123').then(result => {
        bufferEventsUpdated = result;
      });
      tick();

      expect(bufferEventsUpdated[0].additionalProperty).toEqual(eventFromSiteServe.additionalProperty);
      expect(eventProvider.getEventsGroup).toHaveBeenCalledTimes(2);
    }));
  });

  describe('@setLegendsTypeIdssport', () => {
    it('set TYPE_IDS_LEGENDS with type ids once all conditions are met', () => {
      const legendsSport = { ...legendsParentCategory };
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).not.toBeUndefined();
    });

    it('set TYPE_IDS_LEGENDS as null when title is Horse Racing', () => {
      const legendsSport = { ...legendsParentCategory };
      legendsSport['title'] = 'Horse Racing';
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).toBeUndefined();
    });

    it('do not set typeIds when type ids are null', () => {
      const legendsSport = { ...legendsParentCategory };
      legendsSport.childs.get('223').typeIds = null;
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).toBeUndefined();
    });

    it('LEGENDS_SPORT_ID is not legends', () => {
      service['LEGENDS_SPORT_ID'] = '225';
      const legendsSport = { ...legendsParentCategory };
      legendsSport.childs.get('223').typeIds = null;
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).toBeUndefined();
    });

    it('set undefined when child map are empty', () => {
      service['LEGENDS_SPORT_ID'] = '225';
      const legendsSport = { ...legendsParentCategory };
      legendsSport.childs.clear();
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).toBeUndefined();
    });

    it('set undefined when childs are null', () => {
      service['LEGENDS_SPORT_ID'] = '223';
      const legendsSport = { ...legendsParentCategory };
      legendsSport.childs = null;
      service['TYPE_IDS_LEGENDS'] = undefined;
      service['setLegendsTypeIds'](legendsSport);
      expect(service['TYPE_IDS_LEGENDS']).toBeUndefined();
    });
  });
});
