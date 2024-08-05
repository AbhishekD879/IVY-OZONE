import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';

import { TimeFormService } from './time-form.service';
import { throwError } from 'rxjs';

describe('TimeFormService', () => {
  let service,
    timeformApiService,
    timeformData;

  beforeEach(() => {

    timeformApiService = {
      getGreyhoundRaceDetails: jasmine.createSpy('getGreyhoundRaceDetails')
    };

    service = new TimeFormService(timeformApiService);
    timeformData = {
      raceDistance: '550',
      raceGradeName: 'A4',
      verdict: 'Scarlet Fiadh is running really well right now and sets a good standard.',
      entries: [{
        openBetIds: [100, 300, 400],
        greyHoundFullName: 'Snoop Dog',
        trainerFullName: 'Dr Dre (Real)',
        oneLineComment: 'Best dog ever',
        positionPrediction: 2,
        starRating: 4,
        statusName: 'Runner'
      }, {
        openBetIds: []
      }, {
        openBetIds: [102, null, 302, 402],
        greyHoundFullName: 'Mo Chuisle',
        trainerFullName: 'A Harrison (Newcastle)',
        oneLineComment: 'Should have a say if getting a clear run. Been handed an easier opening.',
        positionPrediction: 1,
        starRating: 5,
        statusName: 'Runner'
      }, {
        openBetIds: [200],
        greyHoundFullName: 'Jumbos Brother',
        trainerFullName: 'J J Fenwick (Newcastle)',
        oneLineComment: 'Should have a say if getting a clear run.',
        positionPrediction: 1,
        starRating: 5,
        statusName: 'Non-Runner'
      }, {
        openBetIds: [101, 301, 401],
        greyHoundFullName: 'Wath Mercury',
        trainerFullName: 'J J Fenwick (Newcastle)',
        oneLineComment: 'Had been holding form very well prior to taking time off.',
        positionPrediction: 0,
        starRating: 1,
        statusName: 'Runner'
      }, {
        openBetIds: [201],
        greyHoundFullName: 'Saint Reidy',
        trainerFullName: 'H Burton (Newcastle)',
        oneLineComment: 'Unlikely to be too far away at the line. Traps the best of these.',
        positionPrediction: 3,
        starRating: 3,
        statusName: 'Runner'
      }]
    };
  });

  describe('#getGreyhoundRaceById', () => {
    const openbetId = 123;

    it('should call timeformApiService with given id', () => {
      timeformApiService.getGreyhoundRaceDetails.and.returnValue(Promise.resolve({}));

      service.getGreyhoundRaceById(openbetId);
      expect(timeformApiService.getGreyhoundRaceDetails).toHaveBeenCalledWith(openbetId);
    });

    it('should resolve with empty array in case when request to timeformApiService fails', () => {
      timeformApiService.getGreyhoundRaceDetails.and.returnValue(throwError([]));

      service.getGreyhoundRaceById(openbetId)
        .subscribe(() => {}, (result) => {
          expect(result).toEqual([]);
        });
    });

    it('should resolve with timeformApiService response', fakeAsync(() => {
      const timeformResponse = [{ id: 123 }];
      timeformApiService.getGreyhoundRaceDetails.and.returnValue(Promise.resolve(timeformResponse));

      service.getGreyhoundRaceById(openbetId)
        .then(result => {
          expect(result).toEqual(timeformResponse);
        });
      tick();
    }));
  });

  describe('#_getEventSelections', () => {
    it('should return array in case of incorrect passed data', () => {
      expect(service['getEventSelections'](null)).toEqual([]);
    });

    it('should pluck selection names', () => {
      const markets = [{ outcomes: [1, 2] }, { outcomes: [3, 4] }, { outcomes: [5, 6] }];

      expect(service['getEventSelections'](markets)).toEqual([1, 2, 3, 4, 5, 6]);
    });
  });

  describe('#_getTrainerName', () => {
    it('should return empty string in case of incorrect passed data', () => {
      expect(service['getTrainerName']()).toEqual('');
    });

    it('should return trainer name with parsed meeting name', () => {
      expect(service['getTrainerName']('J J Abrams (Hilrow)')).toEqual('J J Abrams');
    });

    it('should return trainer name without meeting name', () => {
      expect(service['getTrainerName']('J J Abrams')).toEqual('J J Abrams');
    });
  });

  describe('#_getTimeformGreyhoundsMap', () => {
    it('should return object in case of incorrect passed data', () => {
      expect(service['getTimeformGreyhoundsMap'](null)).toEqual({});
    });

    it('should pick only data with openbetId', () => {
      expect(service['getTimeformGreyhoundsMap']([{ id: 1 }])).toEqual({});
      expect(service['getTimeformGreyhoundsMap']([{ id: 1, openBetIds: [] }])).toEqual({});
    });

    it('should pick needed keys from passed objects', () => {
      const result = service['getTimeformGreyhoundsMap'](timeformData.entries);

      expect(_.keys(result).length).toEqual(11);
      expect(result[100]).toEqual({
        greyHoundFullName: 'Snoop Dog',
        trainerFullName: 'Dr Dre (Real)',
        trainer: 'Dr Dre',
        oneLineComment: 'Best dog ever',
        positionPrediction: 2,
        statusName: 'Runner',
        starRating: 4,
        stars: [undefined, undefined, undefined, undefined]
      });
    });
  });

  describe('#_getPositionsPrediction', () => {
    it('should return greyhounds with position prediction > 0 and valid status', () => {
      const greyhoundsMap = {
        10: { positionPrediction: 3, statusName: 'Non-Runner' },
        21: { positionPrediction: 1, statusName: 'Runner' },
        31: { positionPrediction: 3, statusName: 'Runner' },
        41: { positionPrediction: 2, statusName: 'Non-Runner' },
        51: { positionPrediction: 2, statusName: 'Runner' }
      };

      expect(service['getPositionsPrediction'](greyhoundsMap)).toEqual([
        { positionPrediction: 1, statusName: 'Runner' },
        { positionPrediction: 2, statusName: 'Runner' },
        { positionPrediction: 3, statusName: 'Runner' }
      ]);
    });
  });

  describe('#mergeGreyhoundRaceData', () => {
    it('should return an empty array if no OB or TF data passed', () => {
      expect(service.mergeGreyhoundRaceData([])).toEqual([]);
    });

    it('should return OB data in array if no TF data passed', () => {
      const openbetEvent = { id: 1 };
      expect(service.mergeGreyhoundRaceData([openbetEvent, null])).toEqual([openbetEvent]);
    });

    it('should merge OB and TF data on event level', () => {
      const openbetEvent = {
        markets: [{
          id: 10,
          outcomes: [{ id: 100 }, { id: 101 }, { id: 102 }]
        }, {
          id: 20,
          outcomes: [{ id: 200 }, { id: 201 }, { id: 202 }]
        }, {
          id: 30,
          outcomes: [{ id: 300 }, { id: 301 }, { id: 302 }]
        }, {
          id: 40,
          outcomes: [{ id: 400 }, { id: 401 }, { id: 402 }]
        }]
      };
      const result = service.mergeGreyhoundRaceData([openbetEvent, timeformData]);

      expect(result[0].timeformData).toEqual(jasmine.objectContaining({
        raceDistance: timeformData.raceDistance,
        raceGradeName: timeformData.raceGradeName,
        verdict: timeformData.verdict
      }));
      expect(result[0].timeformData.winnerPrediction).toEqual({
        greyHoundFullName: 'Mo Chuisle',
        trainerFullName: 'A Harrison (Newcastle)',
        trainer: 'A Harrison',
        oneLineComment: 'Should have a say if getting a clear run. Been handed an easier opening.',
        positionPrediction: 1,
        starRating: 5,
        stars: [undefined, undefined, undefined, undefined, undefined],
        statusName: 'Runner'
      });
    });
  });
});
