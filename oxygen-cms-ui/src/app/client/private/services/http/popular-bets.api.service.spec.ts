import { of } from 'rxjs/observable/of';
import { PopularBetsApiService } from './popular-bets.api.service';
import { HttpClient } from '@angular/common/http';

describe('PopularBetsApiService', () => {
  let service, http: HttpClient, domain, brand;
  let router;

  beforeEach(() => {
    
    router = {
      navigate: jasmine.createSpy('most-popular/bet-slip'),
      url: 'most-popular/bet-slip'
  };
  service = new PopularBetsApiService(http, domain, brand, router);
  });

  it('should getDetailsByBrand', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getDetailsByBrand();
    expect(sendRequestSpy).toHaveBeenCalled();
    });

  it('should call saveCMSPopularBetsData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.saveCMSPopularBetsData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call updateCMSPopularBetsData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.updateCMSPopularBetsData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  describe('PopularBetsApiService', () => {
    let service1, http1: HttpClient, domain1, brand1;
  let router1;

  beforeEach(() => {
    
    router1 = {
      navigate: jasmine.createSpy('most-popular/bet-receipt'),
      url: 'most-popular/bet-receipt'
  };
  service1 = new PopularBetsApiService(http1, domain1, brand1, router1);
  }); 

  it('should call updateCMSPopularBetsData', () => {
    let sendRequestSpy = spyOn(service1 as any, 'sendRequest').and.returnValue(of({}));
    service1.updateCMSPopularBetsData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call saveCMSPopularBetsData', () => {
    let sendRequestSpy = spyOn(service1 as any, 'sendRequest').and.returnValue(of({}));
    service1.saveCMSPopularBetsData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  })
});
