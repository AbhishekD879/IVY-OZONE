import { BppCacheService } from '@app/bpp/services/bppProviders/bpp-cache.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync } from '@angular/core/testing';

describe('BppCacheService', () => {
  let service;
  let coreToolsService;
  let pubSubService;

  const responseMock = {
    body: {
      response: {
        model: {
          freebetToken: [
            {
              freebetTokenType: 'SPORTS'
            },
            {
              freebetTokenType: 'BETBOOST'
            },
            {
              freebetTokenType: 'BETBOOST'
            },
            {
              freebetTokenType: 'ACCESS'
            }
          ]
        }
      }
    }
  };

  beforeEach(() => {
    coreToolsService = {
      deepClone: jasmine.createSpy('deepClone').and.callFake((arg) => JSON.parse(JSON.stringify(arg)))
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe')
    };

    service = new BppCacheService(
      coreToolsService,
      pubSubService
    );
  });

  it('should return specified freebets from general response', () => {
    let result = service.processFreebetsResponce(responseMock, 'SPORTS');

    expect(result['SPORTS'].response.model.freebetToken.length).toEqual(1);
    expect(result['SPORTS'].response.model.freebetToken[0].freebetTokenType).toEqual('SPORTS');

    service.cachedFreebetsResponce = {};
    result = service.processFreebetsResponce(responseMock, 'BETBOOST');
    expect(result['BETBOOST'].response.model.freebetToken.length).toEqual(2);
    expect(result['BETBOOST'].response.model.freebetToken[0].freebetTokenType).toEqual('BETBOOST');

    service.cachedFreebetsResponce = {};
    result = service.processFreebetsResponce(responseMock, 'ACCESS');
    expect(result['ACCESS'].response.model.freebetToken[0].freebetTokenType).toEqual('ACCESS');


    expect(service.cachedFreebetsResponce['ACCESS']).toBeDefined();
    expect(service.cachedFreebetsResponce['BETBOOST']).toBeDefined();
    expect(service.cachedFreebetsResponce['SPORTS']).toBeDefined();
  });

  it('should setupCacheRemoveLogic', fakeAsync(() => {
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      if (method === pubSubService.API.SESSION_LOGOUT || method === pubSubService.API.BET_PLACED) {
        cb();

        expect(service.cachedFreebetsResponce).toEqual({});
      }
    });

    service.getFreebetsRequest = {};

    service.processFreebetsResponce(responseMock, 'ACCESS');
  }));

  it('should setup cache event without freebets', () => {
    service.getFreebetsRequest = {};
    delete responseMock.body.response.model.freebetToken;

    service.processFreebetsResponce(responseMock, 'ACCESS');

    expect(service.cachedFreebetsResponce['ACCESS']).toBeDefined();
    expect(service.cachedFreebetsResponce['BETBOOST']).toBeDefined();
    expect(service.cachedFreebetsResponce['SPORTS']).toBeDefined();
  });
});
