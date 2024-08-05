import { RacingEventResultedComponent } from './racing-event-resulted.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { oneApi_DATA } from './racing-event-resulted.component.mock';
import { of } from 'rxjs';

describe('RacingEventResultedComponent', () => {
  let component: RacingEventResultedComponent,
      timeService,
      racingResultsService,
      racingPostApiService,
      locale,
      pubsubService,
      gtmService,
      cmsService,
      reloadPage,
      deviceService,
      windowRef,nativeBridgeService
      
  const mockMarket = {
    id: 1,
    categoryId: '21',
    typeId: 1908,
    isEachWayAvailable: true,
    isGpAvailable: true,
    terms: 'Test',
    outcomes : [
      {
        id: 1,
        nonRunner : true,
        name: 'Test N/R',
        runnerNumber: '2',
        racingFormOutcome : { id : 1 }
      },
      {
        id: 2,
        name: 'Lorem',
        runnerNumber: '1',
        racingFormOutcome : { id : 2 }
      }
    ],
    unPlaced : [
      {
        id: 1,
        nonRunner : true,
        name: 'Test N/R',
        runnerNumber: '2',
        racingFormOutcome : { id : 1 }
      },
      {
        id: 2,
        name: 'Lorem',
        runnerNumber: '1',
        racingFormOutcome : { id : 2 }
      }
    ]
  };
  const resultedWEWMarket = {
    id : 1,
    categoryId: 21,
    typeId: 1908,
    cashoutAvail: 'N',
    viewType: 'handicaps',
    isEachWayAvailable: true,
    nonRunners: [{}],
    outcomes : [
      {
        id: 1,
        nonRunner : true,
        name: 'Test N/R',
        runnerNumber: '2',
        racingFormOutcome : { id : 1 }
      },
      {
        id: 2,
        name: 'Lorem',
        runnerNumber: '1',
        racingFormOutcome : { id : 2 }
      }
    ],
    unPlaced : [
      {
        id: 1,
        nonRunner : true,
        name: 'Test N/R',
        runnerNumber: '2',
        racingFormOutcome : { id : 1 }
      },
      {
        id: 2,
        name: 'Lorem',
        runnerNumber: '1',
        racingFormOutcome : { id : 2 }
      }
    ]
  };
  const loseHorses = {
    id: "1",
    name: "|Test N/R|",
    position: "4",
    resultCode: "L",
    runnerNumber: "12",
    siteChannels: "p,P,Q,R,C,I,M,"
  };
  const mockEvent = {
    resultedWEWMarket,
    sortedMarkets : [ mockMarket ],
    startTime : 'Mon Feb 11 2019 12:00:59 GMT+0200 (Eastern European Standard Time)'
  } as any;

  beforeEach(() => {
    timeService = {
      getFullDateFormatSufx: jasmine.createSpy()
    };
    racingResultsService = {
      getRacingResults: jasmine.createSpy().and.returnValue(Promise.resolve({ voidResult: false })),
      isFavourite: jasmine.createSpy().and.returnValue(false),
      mapResultPositionPlaced: jasmine.createSpy('mapResultPositionPlaced'),
      mapResultPositionUnplaced: jasmine.createSpy('mapResultPositionUnplaced')
    };
    locale = {
      getString: jasmine.createSpy().and.returnValue('noRacingResultsFound')
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, listeners, handler) => {
        reloadPage = handler;
        spyOn(component, 'ngOnInit');
        spyOn(component, 'ngOnDestroy');
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_RACING_EVENT_RESULTED: 'RELOAD_RACING_EVENT_RESULTED',
        VIDEO_STREAM_ERROR_DIALOG_CLOSED:'VIDEO_STREAM_ERROR_DIALOG_CLOSED'
      }
    };
    
    racingPostApiService = {
      getHorseRaceOneApiResultDetails: jasmine.createSpy('getHorseRaceOneApiResultDetails').and.returnValue(of(oneApi_DATA)),
    };
    deviceService = {
      isDesktop: true
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        GreyhoundFullResults: {
          enabled: false
        }
      }))
    } as any;
   
    component = new RacingEventResultedComponent(
      timeService,
      racingResultsService,
      racingPostApiService,
      locale,
      pubsubService,
      gtmService,
      cmsService ,
      windowRef,nativeBridgeService, deviceService
    );
    component.eventEntity = mockEvent;
  });

  it('#ngOnInit', fakeAsync(() => {
    component.getEventDate = jasmine.createSpy();
    component.formatAntepostTerms = jasmine.createSpy().and.returnValue('Lorem');
    component.eventEntity.resultedWEWMarket.isEachWayAvailable = true;
    component.eventEntity.resultedWEWMarket.viewType = 'test-no-handicaps';
    component.eventEntity.isUKorIRE = false;
    component['extendOutcome'] = jasmine.createSpy();
    component['setGtmData'] = jasmine.createSpy();

    component.ngOnInit();

    expect(pubsubService.subscribe).toHaveBeenCalledWith('RacingEventResulted', 'RELOAD_RACING_EVENT_RESULTED', jasmine.any(Function));
    reloadPage();
    expect(component.ngOnInit).toHaveBeenCalled();
    expect(component.ngOnDestroy).toHaveBeenCalled();
    expect(racingResultsService.getRacingResults).toHaveBeenCalledWith(mockEvent, false);
    tick();
    expect(component.getEventDate).toHaveBeenCalled();
    expect(component.antepostTerms).toBe('Lorem');
    expect(component.isCashout).toBe(false);
    expect(component.formatAntepostTerms).toHaveBeenCalled();
    expect(component['extendOutcome']).toHaveBeenCalled();
  }));

  it('#ngOnInit cashoutAvail = N', fakeAsync(() => {
    component.getEventDate = jasmine.createSpy();
    component.formatAntepostTerms = jasmine.createSpy();
    component['extendOutcome'] = jasmine.createSpy();
    component.eventEntity.resultedWEWMarket.viewType = 'handicaps';
    component.ngOnInit();

    expect(racingResultsService.getRacingResults).toHaveBeenCalled();
    tick();
    expect(component.getEventDate).toHaveBeenCalled();
    expect(component.isCashout).toBe(true);
    expect(component.formatAntepostTerms).toHaveBeenCalled();
    expect(component['extendOutcome']).toHaveBeenCalledWith(component.eventEntity.resultedWEWMarket.nonRunners);
  }));

  it('#ngOnInit when there are nonRunners', fakeAsync(() => {
    component.getEventDate = jasmine.createSpy();
    component.formatAntepostTerms = jasmine.createSpy();
    component['extendOutcome'] = jasmine.createSpy();

    (racingResultsService.getRacingResults as jasmine.Spy).and.returnValue(Promise.resolve({}));
    component.ngOnInit();

    expect(racingResultsService.getRacingResults).toHaveBeenCalled();
    tick();
    expect(component.isCashout).toBe(true);
    expect(component.getEventDate).toHaveBeenCalled();
    expect(component['extendOutcome']).toHaveBeenCalled();
  }));

  it('#ngOnInit when there are no nonRunners', fakeAsync(() => {
    component['extendOutcome'] = jasmine.createSpy();
    component.eventEntity.resultedWEWMarket.nonRunners = [];
    component.eventEntity.resultedWEWMarket.isEachWayAvailable = false;
    component.ngOnInit();

    expect(component['extendOutcome']).not.toHaveBeenCalled();
  }));

  it('#ngOnInit isEachWayAvailable = false', fakeAsync(() => {
    component.getEventDate = jasmine.createSpy();
    component.formatAntepostTerms = jasmine.createSpy().and.returnValue('Each Way Text');
    component['extendOutcome'] = jasmine.createSpy();
    component.eventEntity.resultedWEWMarket.isEachWayAvailable = false;
    component.eventEntity.resultedWEWMarket.cashoutAvail = 'Y';
    component.eventEntity.resultedWEWMarket.viewType = 'handicaps';
    component.ngOnInit();

    expect(racingResultsService.getRacingResults).toHaveBeenCalled();
    tick();
    expect(component.antepostTerms).toBe('');
    expect(component.isCashout).toBe(true);
    expect(component['getEventDate']).toHaveBeenCalled();
    expect(component['extendOutcome']).toHaveBeenCalledWith(component.eventEntity.resultedWEWMarket.outcomes);
    expect(component['extendOutcome']).toHaveBeenCalledWith(component.eventEntity.resultedWEWMarket.unPlaced);
  }));

  it('#ngOnInit no results', fakeAsync(() => {
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
      GreyhoundFullResults: {
        enabled: true
      }
    }));
    component.eventEntity.resultedWEWMarket.outcomes = [];
    component.ngOnInit();
    tick();
    expect(component.resultsResponseError).toBe('noRacingResultsFound');
  }));

  it('#ngOnInit exception', fakeAsync(() => {
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of(null));
    (racingResultsService.getRacingResults as jasmine.Spy).and.returnValue(Promise.reject('error'));
    component.ngOnInit();
    tick();
    expect(component.resultsResponseError).toBe('noRacingResultsFound');
  }));

  it('#ngOnInit categoryId is equal to racing event category id', fakeAsync(() => {
    component.eventEntity.categoryId = '21';
    component.eventEntity.id = 235806774;
    component.eventEntity.isUKorIRE = true;
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
      GreyhoundFullResults: {}
    }));
    component.ngOnInit();
    tick();
    expect(component.totalResults).toBeFalse();
  }));

  it('#ngOnInit categoryId is equal to racing event category id with non runners', fakeAsync(() => {
    component.eventEntity.categoryId = '21';
    component.eventEntity.id = 235806774;
    component.eventEntity.isUKorIRE = true;
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
      GreyhoundFullResults: {}
    }));
    oneApi_DATA.document['235806774'].results.nonRunners = null;
    oneApi_DATA.document['235806775'].results.nonRunners = null;
    racingPostApiService.getHorseRaceOneApiResultDetails = jasmine.createSpy('getHorseRaceOneApiResultDetails').and.returnValue(of(oneApi_DATA));
    component.ngOnInit();
    tick();
    expect(component.totalResults).toBeTrue();
  }));

  it('#eventEntity is not equal to racing event id', fakeAsync(() => {
    component.eventEntity.categoryId = '21';
    component.eventEntity.id = 235806775;
    component.eventEntity.isUKorIRE = true;
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({}));
    component.ngOnInit();
    tick();
    expect(component.totalResults).toBeFalse();
  }));

  it('#ngOnInit event is greyhound UK Irish event', fakeAsync(() => {
    component.eventEntity.categoryCode = 'GREYHOUNDS';
    component.eventEntity.id = 235806774;
    component.eventEntity.isUKorIRE = true;
    racingPostApiService.getGreyhoundRaceOneApiResultDetails = jasmine.createSpy().and.returnValue(of({"Error":true,"document":{}}));
    cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
      GreyhoundFullResults: {
        enabled: true
      }
    }));
    component.ngOnInit();
    tick();
    expect(component.greyhoundsFullResultsData).toBeDefined();
  }));

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('RacingEventResulted');
  });

  it('#getEventDate', () => {
    component.getEventDate();
    expect(timeService.getFullDateFormatSufx).toHaveBeenCalledWith(new Date(mockEvent.startTime));
  });

  it('#formatAntepostTerms', () => {
    const result = component.formatAntepostTerms('odds places testodds');
    expect(result).toBe('Odds Places testOdds');
  });

  it('#formatAntepostTerms with alphanumeric values', () => {
    const result = component.formatAntepostTerms('123/456 odds');
    expect(result).toBe('123/456 Odds');
  });

  it('#extendOutcome without racingForm', () => {
    component['extendOutcome'](mockMarket.outcomes as any);

    expect(mockMarket.outcomes).toEqual(
      [
        {id: 1, nonRunner: true, name: 'Test N/R', runnerNumber: '2', racingFormOutcome : { id : 1 }},
        {id: 2, name: 'Lorem', runnerNumber: '1', racingFormOutcome : { id : 2 }}
      ] as any
    );
  });

  it('#extendOutcome with racingForm', () => {
    const outcomes = [{ id: 1, runnerNumber: '2', racingFormOutcome: { some: 'lorem' } }] as any;
    component['extendOutcome'](outcomes);

    expect(outcomes).toEqual(
      [
        { id: 1, runnerNumber: '2', racingFormOutcome: { id : 1 } }
      ] as any
    );
  });
  describe('@navigateToUpgrade', () => {
   it("#Should call expandUnplaced when unplaced is false", ()=>{
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: 'horse racing',
      eventLabel:  'Show Full Results',
      categoryID: 21,
      typeID: 1908,
      eventID: 1
    };
     component.unPlaced = false;
     component.eventEntity = mockEvent.resultedWEWMarket;
     component.expandUnplaced();
     expect(component.unPlaced).toBeTruthy()
     expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
   })

  it("#Should call expandUnplaced when unplaced is true", ()=>{
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: 'horse racing',
      eventLabel:  'Show Less Results',
      categoryID: 21,
      typeID: 1908,
      eventID: 1
    };
     component.unPlaced = true;
     component.eventEntity = mockEvent.resultedWEWMarket;
     component.expandUnplaced();
     expect(component.unPlaced).toBeFalsy()
     expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
   });
  });

  describe('isFullResultsRequired',() => {
    it("#should return true if horse racing and is ukorirish", ()=>{
      component.eventEntity.categoryCode = 'HORSE_RACING';
      component.eventEntity.isUKorIRE = true;
      expect(component['isFullResultsRequired']()).toBeTruthy();
    });

    it("#should return true if greyhound racing and is ukorirish and greyhound flag is enabled", ()=>{
      component.eventEntity.categoryCode = 'GREYHOUNDS';
      component.eventEntity.isUKorIRE = true;
      component.isGreyhoundsFullResultsEnabled = true;
      expect(component['isFullResultsRequired']()).toBeTruthy();
    });

    it("#should return false if greyhound racing and is ukorirish and greyhound flag is not enabled", ()=>{
      component.eventEntity.categoryCode = 'GREYHOUNDS';
      component.eventEntity.isUKorIRE = true;
      component.isGreyhoundsFullResultsEnabled = false;
      expect(component['isFullResultsRequired']()).toBeFalsy();
    });

    it("#should return false if greyhound racing and is not ukorirish and greyhound flag is enabled", ()=>{
      component.eventEntity.categoryCode = 'GREYHOUNDS';
      component.eventEntity.isUKorIRE = false;
      component.isGreyhoundsFullResultsEnabled = false;
      expect(component['isFullResultsRequired']()).toBeFalsy();
    });

    it("#should return false if not ukorirish event", ()=>{
      component.eventEntity.categoryCode = 'HORSE_RACING';
      component.eventEntity.isUKorIRE = false;
      expect(component['isFullResultsRequired']()).toBeFalsy();
    });
  })
  describe('playStream',() => {
    it("#calling playstream", ()=>{
      component.preloadStream = true;
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');   
      component.playStream({ preventDefault: () => { } } as any);
      expect(pubsubService.subscribe)
      .toHaveBeenCalledWith('RacingEventComponent', pubsubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED, jasmine.any(Function));
      reloadPage();
       expect(setGtmDataSpy).toHaveBeenCalled();
    });
    it("#hide playstream", ()=>{
      component.preloadStream = true;
      component.filter='showVideoStream';
      const setGtmDataSpy = spyOn(component as any, 'setGtmData');   
      component.playStream({ preventDefault: () => { } } as any);
      expect(setGtmDataSpy).toHaveBeenCalled();
    });
     it('storing GA object', () => {
      component.eventEntity = {
        typeName: 'HORSE RACING'
      } as any;
      component.setGtmData('watchreplay');
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
  })
});
