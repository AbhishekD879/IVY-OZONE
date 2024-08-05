import { fakeAsync, tick } from '@angular/core/testing';

import { DividendsService } from '@sb/services/dividents/dividends.service';
import { INcastDividendResponse, IRacingResult } from '@sb/models/dividends.model';

describe('DividendsService', () => {
  let service: DividendsService;
  let loadByPortionsServiceStub;
  let filtesrServiceStub;
  let siteServerRequestHelperService;

  const testStr = 'TestString';
  let rawServerResponseStub: any[];
  const dividendsRez = { 123: { FC: testStr, TC: testStr }, 234: { FC: testStr } };

  beforeEach(() => {
    rawServerResponseStub = [{
      racingResult: {
        id: '123',
        children: [
          { ncastDividend: { type: 'FC', dividend: testStr } },
          { ncastDividend: { type: 'TC', dividend: testStr } }
        ]
      }
    }, {
      racingResult: {
        id: '234',
        children: [{ ncastDividend: { type: 'FC', dividend: testStr } }]
      }
    }];
    loadByPortionsServiceStub = {
      get: jasmine.createSpy().and.callFake((cb, reqParams, key: string, eventsIds: number[]) => {
        cb && cb([]);

        return Promise.resolve([]);
      })
    };
    filtesrServiceStub = { setCurrency: jasmine.createSpy().and.returnValue(testStr) };
    siteServerRequestHelperService = {
      getRacingResultsForEvent: jasmine.createSpy().and.returnValue([])
    };

    service = new DividendsService(loadByPortionsServiceStub, filtesrServiceStub, siteServerRequestHelperService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('fetch', () => {
    it(`should call 'callBack'-s`, fakeAsync(() => {
      const testCallBack = jasmine.createSpy();
      service.fetch([1], testCallBack);
      tick();
      expect(testCallBack).toHaveBeenCalledTimes(1);
      expect(loadByPortionsServiceStub.get)
        .toHaveBeenCalledWith(jasmine.any(Function), {} ,'eventsIds', [1]);
      expect(siteServerRequestHelperService.getRacingResultsForEvent)
        .toHaveBeenCalledWith([] ,true);
    }));
  });

  describe('mapEventIdsToDividends', () => {
    it(`should return 'Dividends'`, () => {
      expect(service['mapEventIdsToDividends'](rawServerResponseStub as IRacingResult[]))
        .toEqual(dividendsRez);
    });

    it(`should return 'Dividends' if children has 'ncastDividend'`, () => {
      rawServerResponseStub.push({
        racingResult: {
          id: '234',
          children: [{ finalPosition: { id: '1' } }]
        }
      });

      expect(service['mapEventIdsToDividends'](rawServerResponseStub as IRacingResult[]))
        .toEqual(dividendsRez);
    });
  });

  describe('getDividends', () => {
    it(`should return 'Dividends'`, () => {
      const withDevidents = rawServerResponseStub[0].racingResult.children;
      expect(service['getDividends'](withDevidents as INcastDividendResponse[]))
        .toEqual(dividendsRez['123']);
    });

    it(`should return empty object if No 'Dividends'`, () => {
      rawServerResponseStub.push({
        racingResult: {
          id: '234',
          children: [{ finalPosition: { id: '1' } }]
        }
      });
      const withoutDevidents = rawServerResponseStub[2].racingResult.children;
      expect(service['getDividends'](withoutDevidents as INcastDividendResponse[]))
        .toEqual({});
    });
  });
});
