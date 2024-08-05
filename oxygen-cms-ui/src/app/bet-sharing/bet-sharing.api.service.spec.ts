import { of } from 'rxjs/observable/of';
import { BetSharingAPIService } from './bet-sharing.api.service';
import { HttpClient } from '@angular/common/http';

describe('BetSharingAPIService', () => {
  let service, http: HttpClient, domain, brand;

  beforeEach(() => {
    service = new BetSharingAPIService(http, domain, brand);
  });

  it('should getDetailsByBrand', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getDetailsByBrand();
    expect(sendRequestSpy).toHaveBeenCalled();
    });

  it('should call saveCMSBetShareData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.saveCMSBetShareData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call updateCMSBetShareData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.updateCMSBetShareData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });
});
