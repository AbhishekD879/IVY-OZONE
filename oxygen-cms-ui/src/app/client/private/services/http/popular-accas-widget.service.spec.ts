import { of } from 'rxjs/observable/of';
import { HttpClient } from '@angular/common/http';
import { PopularAccasWidgetService } from './popular-accas-widget.service';

describe('PopularAccasWidgetService', () => {
  let service, http: HttpClient, domain, brand;

  beforeEach(() => {
    service = new PopularAccasWidgetService(http, domain, brand);
  });

  it('should getPopularAccasWidgetData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getPopularAccasWidgetData();
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call postPopularAccasWidgetData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.postPopularAccasWidgetData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call putPopularAccasWidgetData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.putPopularAccasWidgetData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call getPopularAccasWidgetCardData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getPopularAccasWidgetCardData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call putPopularAccasWidgetCardData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.putPopularAccasWidgetCardData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call postPopularAccasWidgetCardData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.postPopularAccasWidgetCardData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call reorderPopularAccasWidgetcardData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.reorderPopularAccasWidgetcardData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call getsegmentdata', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getsegmentdata({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call deletePopularAccasWidgetCardData', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.deletePopularAccasWidgetCardData({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call getPopularAccasWidgetCardDataByBrand', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.getPopularAccasWidgetCardDataByBrand({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call uploadSvg', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.uploadSvg({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

  it('should call removeSvg', () => {
    let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
    service.removeSvg({});
    expect(sendRequestSpy).toHaveBeenCalled();
  });

});
