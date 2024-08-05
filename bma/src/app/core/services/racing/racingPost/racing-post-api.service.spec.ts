import { fakeAsync, tick } from '@angular/core/testing';
import { Observable, of as observableOf, throwError } from 'rxjs';
import { RacingPostApiService } from '@core/services/racing/racingPost/racing-post-api.service';
import environment from '@environment/oxygenEnvConfig';

describe('RacingPostApiService', () => {
  let service: RacingPostApiService;
  let http;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({ body: 'data' } ))
    };

    service = new RacingPostApiService(http);
  });

  it('should have API params configured', () => {
    expect(service['racingPostApiEndpoint']).toEqual(environment.RACING_POST_API_ENDPOINT);
    expect(service['racingPostOneApiEndpoint']).toEqual(environment.RACING_POST_ONE_API_ENDPOINT);
    expect(service['racingPostApiKey']).toEqual(environment.RACING_POST_API_KEY);
    expect(service['TIMEOUT']).toEqual(10000);
  });

  describe('API calls', () => {
    let response;

    beforeEach(() => {
      response = undefined;
      (service as any).racingPostApiEndpoint = 'api-endpoint';
      (service as any).racingPostOneApiEndpoint = 'api-endpoint';
      (service as any).racingPostApiKey = 'api-key';
    });

    describe('getHorseRaceDetails', () => {
      it('should call Racing Post endpoint with openbet ids provided', () => {
        service.getHorseRaceDetails('1,2,3');
        expect(http.get).toHaveBeenCalledWith('api-endpoint/categories/21/events/1,2,3/content?locale=en-GB&api-key=api-key', {
          observe: 'response',
          params: {},
          headers: {
            accept: 'application/json'
          }
        });
      });
      it('should not call Racing Post when there is no ids', () => {
        service.getHorseRaceDetails('');
        expect(http.get).not.toHaveBeenCalled();
      });
    });

    describe('getHorseRaceOneApiResultDetails', () => {
      it('should call Racing Post endpoint with openbet ids provided', () => {
        service.getHorseRaceOneApiResultDetails('1,2,3');
        expect(http.get).toHaveBeenCalledWith('api-endpoint/categories/21/events/1,2,3/content?locale=en-GB&api-key=api-key', {
          observe: 'response',
          params: {},
          headers: {
            accept: 'application/json'
          }
        });
      });
      it('should not call Racing Post when there is no ids', () => {
        service.getHorseRaceOneApiResultDetails('');
        expect(http.get).not.toHaveBeenCalled();
      });
    });

    describe('getGreyhoundRaceDetails', () => {
      it('should call Racing Post endpoint with openbet ids provided', () => {
        service.getGreyhoundRaceDetails('1,2,3');
        expect(http.get).toHaveBeenCalledWith('api-endpoint/categories/19/events/1,2,3/content?locale=en-GB&api-key=api-key', {
          observe: 'response',
          params: {},
          headers: {
            accept: 'application/json'
          }
        });
      });
      it('should not call Racing Post when there is no ids', () => {
        service.getGreyhoundRaceDetails('');
        expect(http.get).not.toHaveBeenCalled();
      });
    });

    describe('getGreyhoundRaceOneApiResultDetails', () => {
      it('should call Racing Post endpoint with openbet ids provided', () => {
        service.getGreyhoundRaceOneApiResultDetails('1,2,3');
        expect(http.get).toHaveBeenCalledWith('api-endpoint/categories/19/events/1,2,3/content?locale=en-GB&api-key=api-key', {
          observe: 'response',
          params: {},
          headers: {
            accept: 'application/json'
          }
        });
      });

      it('should not call Racing Post when there is no ids', () => {
        service.getGreyhoundRaceOneApiResultDetails('');
        expect(http.get).not.toHaveBeenCalled();
      });
    });

    describe('should normally resolve as data.body', () => {
      let response$;

      it('for getGreyhoundRaceDetails', () => {
        response$ = service.getGreyhoundRaceDetails('1,2,3');
      });
      it('for getHorseRaceDetails', () => {
        response$ = service.getHorseRaceDetails('1,2,3');
      });
      it('for getHorseRaceOneApiResultDetails', () => {
        response$ = service.getHorseRaceOneApiResultDetails('1,2,3');
      });

      afterEach(() => {
        response$.subscribe(data => response = data);
        expect(response).toEqual('data');
      });
    });
    describe('should resolve as empty object by error or timeout', () => {
      let error$, timeout$;

      it('for getGreyhoundRaceDetails', () => {
        http.get.and.returnValue(throwError(null));
        error$ = service.getGreyhoundRaceDetails('1');
        http.get.and.returnValue(new Observable());
        timeout$ = service.getGreyhoundRaceDetails('1');
      });
      it('for getHorseRaceDetails', () => {
        http.get.and.returnValue(throwError(null));
        error$ = service.getHorseRaceDetails('1');
        http.get.and.returnValue(new Observable());
        timeout$ = service.getHorseRaceDetails('1');
      });
      it('for getHorseRaceOneApiResultDetails', () => {
        http.get.and.returnValue(throwError(null));
        error$ = service.getHorseRaceOneApiResultDetails('1');
        http.get.and.returnValue(new Observable());
        timeout$ = service.getHorseRaceOneApiResultDetails('1');
      });

      afterEach(fakeAsync(() => {
        error$.subscribe(data => response = data);
        expect(response).toEqual({});

        response = undefined;
        timeout$.subscribe(data => response = data);
        tick(9999);
        expect(response).toEqual(undefined);
        tick(1);
        expect(response).toEqual({});
      }));
    });
  });
});
