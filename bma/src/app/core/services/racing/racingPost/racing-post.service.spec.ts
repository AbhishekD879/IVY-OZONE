import { RacingPostService } from '@coreModule/services/racing/racingPost/racing-post.service';
import { of as observableOf } from 'rxjs';
import { ISportEvent } from '@core/models/sport-event.model';

import {
  GREYHOUND_MAPPING_CONFIG,
  HORSERACING_MAPPING_CONFIG
} from '@core/services/racing/racingPost/racing-post-mapping-config.constant';
import {
  STUB_OB_EVENTS, STUB_RP_DATA,
  GREYHOUND_EVENTS, HORSERACING_EVENTS,
  RACINGPOST_GH_RESPONSE, RACINGPOST_HR_RESPONSE, RACE_DATA, RACE_DATA_GH, PREPARE_VERDICT_DATA
} from '@core/services/racing/racingPost/racing-post.service.mock';

describe('RacingPostService', () => {
  let service: RacingPostService;
  let racingPostApiService;
  let cmsService;
  let localeService;
  let timeService;
  let tools;

  beforeEach(() => {
    racingPostApiService = {
      getGreyhoundRaceDetails: jasmine.createSpy().and.returnValue(observableOf([])),
      getHorseRaceDetails: jasmine.createSpy().and.returnValue(observableOf([]))
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        raceInfo: {
          timeFormEnabled: true
        },
        RacingDataHub: {
          isEnabledForGreyhound: true,
          isEnabledForHorseRacing: true,
        }
      }))
    };
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Win or Each Way')
    };
    timeService = {
      getMonthI18nValue: jasmine.createSpy('getMonthI18nValue').and.returnValue('sb.monJanuary')
    };
    tools = {
      getDaySuffix: jasmine.createSpy('getDaySuffix').and.returnValue('th')
    };

    service = new RacingPostService(
      racingPostApiService,
      cmsService,
      timeService,
      tools,
      localeService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#getValuesByKeysMap', () => {
    const values = {
      distance: 1,
      verdict: 'overview text',
      goingCode: 'going status'
    };
    expect(service['getValuesByKeysMap'](values, { distance: 'distance', verdict: 'overview' }))
      .toEqual({ distance: '1', overview: 'overview text' });

    expect(service['getValuesByKeysMap'](values, { distance: 'distance', verdict: 'overview', goingCode: 'going' }))
      .toEqual({ distance: '1', overview: 'overview text', going: 'going status' });

    expect(service['getValuesByKeysMap'](values, { unknownRpApiProperty: 'unknownOBProperty', verdict: 'overview', goingCode: 'going' }))
      .toEqual({ overview: 'overview text', going: 'going status' });

    expect(service['getValuesByKeysMap']({ unknownRpApiProperty: 'unknownOBProperty' }, { verdict: 'overview', goingCode: 'going' }))
      .toEqual({});

    expect(service['getValuesByKeysMap']({}, { verdict: 'overview', goingCode: 'going' }))
      .toEqual({});

    expect(service['getValuesByKeysMap'](values, {}))
      .toEqual({});
  });

  it('#addRacingFormOutcome', () => {
    const outcome_1 = { runnerNumber: 7 },
      outcome_2 = { id: 54321 },
      map = { 7: { raceName: 'ffs text', goingCode: 'going status' } },
      expected = { runnerNumber: 7, racingFormOutcome: { going: 'going status', title: 'ffs text' } };

    service['addRacingFormOutcome'](<any>outcome_1, <any>map, { goingCode: 'going', raceName: 'title' });
    service['addRacingFormOutcome'](<any>outcome_2, <any>map, { goingCode: 'going', raceName: 'title' });

    expect(outcome_1).toEqual(expected);
    expect(outcome_2).toEqual(outcome_2);
  });

  describe('#mergeHorseRaceData, #mergeGreyhoundRaceData', () => {
    let eventsData, racingPostData;
    beforeEach(() => {
      spyOn(service as any, 'prepareVerdictData').and.callThrough();
    });

    describe('#mergeRaceData with proper mapping config', () => {
      beforeEach(() => {
        eventsData = [{ id: 0 }, { id: 1 }];
        racingPostData = { Error: 'false', document: { 0: {}, 1: {} } };
        service['mergeRaceData'] = jasmine.createSpy('mergeRaceData');
      });

      it('should call #mergeRaceData with proper mapping config', () => {
        service.mergeHorseRaceData(eventsData, racingPostData);
        expect(service['mergeRaceData']).toHaveBeenCalledWith(
          [{ id: 0 }, { id: 1 }] as any, { Error: 'false', document: { 0: {}, 1: {} } }, HORSERACING_MAPPING_CONFIG);
      });

      it('should call #mergeRaceData with proper mapping config', () => {
        service.mergeGreyhoundRaceData(eventsData, racingPostData);
        expect(service['mergeRaceData']).toHaveBeenCalledWith(
          [{ id: 0 }, { id: 1 }] as any, { Error: 'false', document: { 0: {}, 1: {} } }, GREYHOUND_MAPPING_CONFIG);
      });
    });

    describe('should properly work with OB events array and single event', () => {
      beforeEach(() => {
        eventsData = JSON.parse(JSON.stringify(STUB_OB_EVENTS));
        racingPostData = JSON.parse(JSON.stringify(STUB_RP_DATA));
      });

      it('should return updated OB events array', () => {
        const result = service.mergeHorseRaceData(eventsData, racingPostData);
        expect(result).toEqual([
          { id: 0, markets: [{ outcomes: [] }], racingFormEvent: { raceType: 'race-0' },
            racingPostVerdict: { starRatings: [], tips: [], verdict: undefined, imgUrl: undefined, isFilled: false, mostTipped: [] }},
          { id: 1, markets: [{ }], racingFormEvent: { raceType: 'race-1' },
            racingPostVerdict: { starRatings: [], tips: [], verdict: undefined, imgUrl: undefined, isFilled: false, mostTipped: [] }},
          { id: 2, markets: [{ outcomes: [] }]},
          { id: 4, markets: [], racingFormEvent: { raceType: 'race-4' },
            racingPostVerdict: { starRatings: [], tips: [], verdict: undefined, imgUrl: undefined, isFilled: false, mostTipped: [] }},
          { id: 5, racingFormEvent: { raceType: 'race-5' },
            racingPostVerdict: { starRatings: [], tips: [], verdict: undefined, imgUrl: undefined, isFilled: false, mostTipped: [] }}
        ] as ISportEvent[]);
      });

      it('should return updated OB events array with single element', () => {
        const result = service.mergeGreyhoundRaceData(eventsData[0], racingPostData);
        expect(result).toEqual([{ id: 0, markets: [{ outcomes: [] }], racingFormEvent: { raceType: 'race-0' } }] as ISportEvent[]);
      });
    });

    describe('should not change anything', () => {
      beforeEach(() => {
        eventsData = JSON.parse(JSON.stringify(STUB_OB_EVENTS));
        racingPostData = JSON.parse(JSON.stringify(STUB_RP_DATA));
      });

      it('if racing post data is unavailable', () => {
        const result = service.mergeHorseRaceData(eventsData, {} as any);
        expect(result).toEqual([
          { id: 0, markets: [{ outcomes: [] }] },
          { id: 1, markets: [{ }] },
          { id: 2, markets: [{ outcomes: [] }] },
          { id: 4, markets: [] },
          { id: 5 }
        ] as ISportEvent[]);
      });
      it('if racing post data does not contain openbet ids', () => {
        const result = service.mergeGreyhoundRaceData(eventsData[2], racingPostData);
        expect(result).toEqual([{ id: 2, markets: [{ outcomes: [] }] }] as ISportEvent[]);
      });

      it('if racing post data under IDs is empty (hello you, coverage)', () => {
        const result = service.mergeGreyhoundRaceData(eventsData.slice(0, 2), { Error: 'false', document: { 0: null, 1: null } } as any);
        expect(result).toEqual([
          { id: 0, markets: [{ outcomes: [] }] },
          { id: 1, markets: [{ }] }
        ] as ISportEvent[]);
      });
    });

    describe('updating HR openbet events', () => {
      let result;
      beforeEach(() => {
        eventsData = JSON.parse(JSON.stringify(HORSERACING_EVENTS));
        result = service.mergeHorseRaceData(eventsData as ISportEvent[], RACINGPOST_HR_RESPONSE as any);
      });

      it('should create/replace racingFormEvent property of each event matched by id', () => {
        expect(result[0].racingFormEvent).toEqual(RACE_DATA[0].racingFormEvent);
        expect(result[1].racingFormEvent).toEqual(RACE_DATA[1].racingFormEvent);
        expect(result[2].racingFormEvent).toEqual(RACE_DATA[2].racingFormEvent);
      });

      it('should create/replace racingFormEvent of each outcome matched by saddle-runnerNumber of openbet events matched by id', () => {
        expect(result[0].markets[0].outcomes[0].racingFormOutcome).toEqual({
          age: '5',
          draw: '3',
          formGuide: 'form-1-1',
          jockey: 'jockey-1-1',
          trainer: 'trianer-1-1',
          officialRating: '3',
          silkName: 'silk-1-1.png',
          weight: '90',
          overview: 'spotlight-1-1',
          courseDistanceWinner: '4',
          formProviderRating: '0',
          starRating: '',
          form: ['form-1-1a', 'form-1-1b']
        });
        expect(result[0].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[0].markets[0].outcomes[2].racingFormOutcome).not.toBeDefined();
        expect(result[0].markets[0].outcomes[3].racingFormOutcome).toEqual({
          jockey: 'jockey-1-4',
          silkName: 'silk-1-4.png',
          starRating: '4'
        });
        expect(result[1].markets[0].outcomes[0].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[1].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[2].markets[0].outcomes[0].racingFormOutcome).not.toBeDefined();
        expect(result[2].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
      });

      it('should add racingPostVerdict to the HR openbet events ', () => {
        expect((service['prepareVerdictData'] as any).calls.allArgs()).toEqual([[eventsData[0]], [eventsData[1]]]);
        expect(result[0].racingPostVerdict).toBeDefined();
        expect(result[1].racingPostVerdict).toBeDefined();
        expect(result[2].racingPostVerdict).not.toBeDefined();
      });
    });

    describe('updating GH openbet events', () => {
      let result;
      beforeEach(() => {
        eventsData = JSON.parse(JSON.stringify(GREYHOUND_EVENTS));
        result = service.mergeGreyhoundRaceData(eventsData as ISportEvent[], RACINGPOST_GH_RESPONSE as any);
      });

      it('should create/replace racingFormEvent property of each event matched by id', () => {
        expect(result[0].racingFormEvent).toEqual(RACE_DATA_GH[0].racingFormEvent);
        expect(result[1].racingFormEvent).toEqual(RACE_DATA_GH[1].racingFormEvent);
        expect(result[2].racingFormEvent).toEqual(RACE_DATA_GH[2].racingFormEvent);
      });

      it('should create/replace racingFormEvent of each outcome matched by saddle-runnerNumber of openbet events matched by id', () => {
        expect(result[0].markets[0].outcomes[0].racingFormOutcome).toEqual({
          overview: 'comment-1-1',
          formGuide: 'last5runs-1-1'
        });
        expect(result[0].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[0].markets[0].outcomes[2].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[1].markets[0].outcomes[0].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[1].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
        expect(result[2].markets[0].outcomes[0].racingFormOutcome).not.toBeDefined();
        expect(result[2].markets[0].outcomes[1].racingFormOutcome).toEqual({ anything: 'not-changed' });
      });

      it('should not add racingPostVerdict to the GH openbet events ', () => {
        expect(service['prepareVerdictData']).not.toHaveBeenCalled();
        expect(result[0].racingPostVerdict).not.toBeDefined();
        expect(result[1].racingPostVerdict).not.toBeDefined();
        expect(result[2].racingPostVerdict).not.toBeDefined();
      });
    });
  });

  describe('Retreiving RacingPost Data', () => {
    let cmsConfig, observable;

    beforeEach(() => {
      cmsConfig = { isEnabledForGreyhound: true, isEnabledForHorseRacing: true };
      spyOn(service, 'getRacingDataHubConfig').and.returnValue(observableOf(cmsConfig));
      racingPostApiService.getHorseRaceDetails.and.returnValue(observableOf({ Error: 'false', document: { 123: { horses: []  } } }));
      racingPostApiService.getGreyhoundRaceDetails.and.returnValue(observableOf({ Error: 'false', document: { 456: { runners: [] } } }));
    });

    describe('#getGreyhoundRacingPostById should call getRacingDataHubConfig for CMS config', () => {
      beforeEach(() => {
        observable = service.getGreyhoundRacingPostById('456');
      });
      describe('and if RacingDataHub has isEnabledForGreyhound: true', () => {
        it('should call racingPostApiService.getGreyhoundRaceDetails and resolve with data returned', () => {
          observable.subscribe(data => expect(data).toEqual({ Error: 'false', document: { 456: { runners: []  } } }));
          expect(racingPostApiService.getGreyhoundRaceDetails).toHaveBeenCalledWith('456');
        });
      });
      describe('and if RacingDataHub has isEnabledForGreyhound: false', () => {
        beforeEach(() => {
          cmsConfig.isEnabledForGreyhound = false;
        });
        it('should not call racingPostApiService.getGreyhoundRaceDetails and resolve with empty object', () => {
          observable.subscribe(data => expect(data).toEqual({}));
          expect(racingPostApiService.getGreyhoundRaceDetails).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(racingPostApiService.getHorseRaceDetails).not.toHaveBeenCalled();
      });
    });

    describe('#getHorseRacingPostById should call getRacingDataHubConfig for CMS config', () => {
      beforeEach(() => {
        observable = service.getHorseRacingPostById('123');
      });
      describe('and if RacingDataHub has isEnabledForHorseRacing: true', () => {
        it('should call racingPostApiService.getGreyhoundRaceDetails and resolve with data returned', () => {
          observable.subscribe(data => expect(data).toEqual({ Error: 'false', document: { 123: { horses: [] } } }));
          expect(racingPostApiService.getHorseRaceDetails).toHaveBeenCalledWith('123');
        });
      });
      describe('and if RacingDataHub has isEnabledForHorseRacing: false', () => {
        it('should not call racingPostApiService.getGreyhoundRaceDetails and resolve with empty object', () => {
          cmsConfig.isEnabledForHorseRacing = false;
          observable.subscribe(data => expect(data).toEqual({}));
          expect(racingPostApiService.getHorseRaceDetails).not.toHaveBeenCalled();
        });
      });

      afterEach(() => {
        expect(racingPostApiService.getGreyhoundRaceDetails).not.toHaveBeenCalled();
      });
    });

    afterEach(() => {
      expect(service.getRacingDataHubConfig).toHaveBeenCalled();
    });
  });

  describe('getRacingDataHubConfig', () => {
    it('should check CMS config and return combined config', (done) => {
      service.getRacingDataHubConfig().subscribe(data => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(data).toEqual({ timeFormEnabled: true, isEnabledForGreyhound: true, isEnabledForHorseRacing: true });
        done();
      });
    });
  });

  describe('updateRacingEventsList', () => {
    let observable;
    const obEventsData = [{ id: 1 }, { id: 2 }];

    beforeEach(() => {
      spyOn(service, 'getHorseRacingPostById').and.returnValue(observableOf({ horses: [] } as any));
      spyOn(service, 'mergeHorseRaceData').and.returnValue([{ id: 1, racingFormEvent: {} }, { id: 2, racingFormEvent: {} }] as any);
      spyOn(service, 'getGreyhoundRacingPostById').and.returnValue(observableOf({ runners: [] } as any));
      spyOn(service, 'mergeGreyhoundRaceData').and.returnValue([{ id: 1, racingFormEvent: {} }, { id: 2, racingFormEvent: {} }] as any);

    });
    describe('should getHorseRacingPostById with eventIds string and merge response with openbet data', () => {
      it('when true isHorseRasing flag provided', () => {
        observable = service.updateRacingEventsList(obEventsData as ISportEvent[], true);
      });
      it('when no isHorseRasing flag provided', () => {
        observable = service.updateRacingEventsList(obEventsData as ISportEvent[]);
      });

      afterEach(() => {
        expect(service.getHorseRacingPostById).toHaveBeenCalledWith('1,2');
        expect(service.mergeHorseRaceData).not.toHaveBeenCalled();
        observable.subscribe(data => { expect(data).toEqual([{ id: 1, racingFormEvent: {} }, { id: 2, racingFormEvent: {} }]); });
        expect(service.mergeHorseRaceData).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }] as any, { horses: [] } as any);
        expect(service.getGreyhoundRacingPostById).not.toHaveBeenCalled();
        expect(service.mergeGreyhoundRaceData).not.toHaveBeenCalled();
      });
    });

    describe('when false isHorseRasing flag provided (greyhound)', () => {
      it('should getGreyhoundRacingPostById with eventIds string and merge response with openbet data', () => {
        observable = service.updateRacingEventsList(obEventsData as ISportEvent[], false);
        expect(service.getGreyhoundRacingPostById).toHaveBeenCalledWith('1,2');
        expect(service.mergeGreyhoundRaceData).not.toHaveBeenCalled();
        observable.subscribe(data => { expect(data).toEqual([{ id: 1, racingFormEvent: {} }, { id: 2, racingFormEvent: {} }]); });
        expect(service.mergeGreyhoundRaceData).toHaveBeenCalledWith([{ id: 1 }, { id: 2 } as any], { runners: [] } as any);
        expect(service.getHorseRacingPostById).not.toHaveBeenCalled();
        expect(service.mergeHorseRaceData).not.toHaveBeenCalled();
      });
    });
    it('case when no events available', () => {
      service.updateRacingEventsList([] as ISportEvent[], false).subscribe((events: ISportEvent[]) => {
        expect(events.length).toBe(0);
      });
    });
  });
  describe('#lastRunText', () => {
    const outcomeData = {
      racingFormOutcome: {
        form: [{
          'rpr': '40',
          'weight': '9-5',
          'raceid': 757677,
          'weightLbs': 131,
          'course': 'Lingfield (AW)',
          'jockey': 'Charles Bishop',
          'date': '2020-06-08T18:20:00',
          'topspeed': '16',
          'outcome': '7/8 8¾L,Breakfast Club[50/1]9-5',
          'condition': 'LIN 5St/Slw Cl5Nv,3K',
          'position': '7',
          'odds': '50/1',
          'comment': 'always towards rear, pushed along early, ridden and outpaced over 2f out, made no impression',
          'noOfRunners': '8',
          'distanceToWinner': '8¾L',
          'courseName': 'Lingfield (AW)',
          'distance': '5f 6y',
          'raceTitle': 'Betway Novice Stakes',
          'isHandicap': false,
          'raceClass': '5',
          'agesAllowed': '3yo+',
          'other': {
            'horseName': 'Breakfast Club',
            'weight': '9-5'
          }
        }]
      }
    } as any;

    it('should set lastRunText if there is form data', () => {
      const lastRunInfo = service['getLastRunText'](outcomeData.racingFormOutcome.form);

      expect(lastRunInfo).not.toBe(null);
    });
    it('should return null if form data is empty', () => {
      const lastRunInfo = service['getLastRunText']([]);

      expect(lastRunInfo).toBe(null);
    });
    it('should return only some fields data', () => {
      const formData = [{
        'rpr': '109',
        'weight': '11-2',
        'raceid': 760147,
        'weightLbs': 156,
        'officialRating': '100',
        'course': 'NEWTON ABBOT',
        'jockey': 'Kielan Woods',
        'date': '2020-07-07T15:45:00',
        'topspeed': '83',
        'outcome': '1/8 1l, Classic Escape[6/1]11-12 t',
        'condition': 'NAB 26Gd  Cl4 HdHc,4K'
      }];
      const lastRunInfo = service['getLastRunText'](formData);

      expect(lastRunInfo).not.toBe(null);
    });
  });
  it('#prepareVerdictData ', () => {
    service['getSaddleNoBySelectionId'] = jasmine.createSpy('getSaddleNoBySelectionId');
    const response = service['prepareVerdictData'](PREPARE_VERDICT_DATA as any);
    expect(response.mostTipped).not.toBeNull();
  });
  it('#prepareVerdictData ', () => {
    service['getSaddleNoBySelectionId'] = jasmine.createSpy('getSaddleNoBySelectionId');
    const request = PREPARE_VERDICT_DATA as any;
    request.racingFormEvent = [];
    const response = service['prepareVerdictData'](request as any);
    expect(response.mostTipped.length).toBe(0);
  });
  it('#prepareVerdictData ', () => {
    service['getSaddleNoBySelectionId'] = jasmine.createSpy('getSaddleNoBySelectionId');
    const request = PREPARE_VERDICT_DATA as any;
    request.racingFormEvent.newspapers = [];
    const response = service['prepareVerdictData'](request as any);
    expect(response.mostTipped.length).toBe(0);
  });
  it('#prepareVerdictData ', () => {
    service['getSaddleNoBySelectionId'] = jasmine.createSpy('getSaddleNoBySelectionId');
    const request = PREPARE_VERDICT_DATA as any;
    request.racingFormEvent.newspapers.length = 0;
    const response = service['prepareVerdictData'](request as any);
    expect(response.mostTipped.length).toBe(0);
  });

  describe('#getSaddleNoBySelectionId', () => {
    it('#should return the saddle no ', () => {
      const racingFormEvent = { horses: [{ rpHorseId: 123, saddle: '1' }] } as any;
      expect(service['getSaddleNoBySelectionId'](racingFormEvent, 123)).toBe('1');
    });
    it('#should return null when horses empty ', () => {
      const racingFormEvent = { horses: [] } as any;
      expect(service['getSaddleNoBySelectionId'](racingFormEvent, 123)).toBe(null);
    });
    it('#should return null when horses are null ', () => {
      const racingFormEvent = { horses: null } as any;
      expect(service['getSaddleNoBySelectionId'](racingFormEvent, 123)).toBe(null);
    });
    it('#should return null when racingFormEvent is null ', () => {
      expect(service['getSaddleNoBySelectionId'](null, 123)).toBe(null);
    });
  });
});
