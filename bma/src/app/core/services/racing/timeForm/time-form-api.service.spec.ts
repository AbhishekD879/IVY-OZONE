import { fakeAsync, tick } from '@angular/core/testing';
import { Observable, of as observableOf, throwError } from 'rxjs';
import { TimeFormApiService } from '@core/services/racing/timeForm/time-form-api.service';
import environment from '@environment/oxygenEnvConfig';

describe('TimeFormApiService', () => {
  let service: TimeFormApiService;
  let http;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({ body: 'data' } ))
    };

    service = new TimeFormApiService(http);
  });

  it('should have API params configured', () => {
    expect(service['timeFormEndpoint']).toEqual(environment.TIMEFORM_ENDPOINT);
    expect(service['TIMEOUT']).toEqual(10000);
  });

  describe('API calls', () => {
    let response;

    beforeEach(() => {
      response = undefined;
      (service as any).timeFormEndpoint = 'api-endpoint';
    });

    describe('getGreyhoundRaceDetails', () => {
      it('should call Timeform endpoint with openbet ids provided', () => {
        service.getGreyhoundRaceDetails('1,2,3');
        expect(http.get).toHaveBeenCalledWith('api-endpoint/api/v1/greyhoundracing/race/1,2,3/openbet', {
          observe: 'response',
          params: { isArray: true },
          headers: {
            accept: 'application/json'
          }
        });
      });
    });

    it('should normally resolve as data.body', () => {
      service.getGreyhoundRaceDetails('1,2,3').subscribe(data => response = data);
      expect(response).toEqual('data');
    });

    describe('should resolve as null', () => {
      it('on error', () => {
        http.get.and.returnValue(throwError(null));
        service.getGreyhoundRaceDetails('1').subscribe(data => response = data);
        expect(response).toEqual(null);
      });

      it('by timeout', fakeAsync(() => {
        http.get.and.returnValue(new Observable());
        service.getGreyhoundRaceDetails('1').subscribe(data => response = data);
        tick(9999);
        expect(response).toEqual(undefined);
        tick(1);
        expect(response).toEqual(null);
      }));
    });
  });
});
