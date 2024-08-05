import { of } from 'rxjs';
import { MyStableService } from './my-stable.service';

describe('MyStableService', () => {
  let service: MyStableService;
  let http;
  let domain;
  let brand;

  beforeEach(() => {

    http = {
      post: jasmine.createSpy('post'),
      get: jasmine.createSpy('get'),
      put: jasmine.createSpy('put'),
      delete: jasmine.createSpy('delete'),
    };

    service = new MyStableService(http, domain, brand)
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should call postMyStableData & send a POST request', () => {
    const testData = {} as any;
    const expectedResponse = { body: {} } as any;
    http.post.and.returnValue(of(expectedResponse));
    service.postMyStableData(testData).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call getMyStableData & send a GET request', () => {
    const expectedResponse = { body: {} } as any;
    http.get.and.returnValue(of(expectedResponse));
    service.getMyStableData().subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call putMyStableData & send a PUT request', () => {
    const id = '123';
    const testData = '' as any;
    const expectedResponse = { body: {} } as any;
    http.put.and.returnValue(of(expectedResponse));
    service.putMyStableData(testData, id).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call getDetailsByBrand & send a GET request', () => {
    const apiUrl = 'https://abc.com';
    const expectedResponse = { body: {} } as any;
    http.get.and.returnValue(of(expectedResponse));
    service.getDetailsByBrand(apiUrl).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call getMyStableById & send a GET request', () => {
    const apiUrl = 'https://abc.com';
    const id = '123';
    const expectedResponse = { body: {} } as any;
    http.get.and.returnValue(of(expectedResponse));
    service.getMyStableById(apiUrl, id).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call postNewMyStableImage & send a POST request', () => {
    const apiUrl = 'https://abc.com';
    const file = new FormData();
    const expectedResponse = { body: {} } as any;
    http.post.and.returnValue(of(expectedResponse));
    service.postNewMyStableImage(file, apiUrl).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call updateNewMyStableImage & send a PUT request', () => {
    const apiUrl = 'https://abc.com';
    const id = '123';
    const file = new FormData();
    const expectedResponse = { body: {} } as any;
    http.put.and.returnValue(of(expectedResponse));
    service.updateNewMyStableImage(file, apiUrl, id).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call removeMyStableUploadedImage & send a DELETE request', () => {
    const apiUrl = 'https://abc.com';
    const id = '123';
    const expectedResponse = { body: {} } as any;
    http.delete.and.returnValue(of(expectedResponse));
    service.removeMyStableUploadedImage(id, apiUrl).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call saveOnBoardingMyStable & send a POST request', () => {
    const apiUrl = 'https://abc.com';
    const request = {} as any;
    const expectedResponse = { body: {} } as any;
    http.post.and.returnValue(of(expectedResponse));
    service.saveOnBoardingMyStable(request, apiUrl).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

  it('should call updateOnBoardingMyStable & send a PUT request', () => {
    const url = 'https://abc.com';
    const request = {} as any;
    const expectedResponse = { body: {} } as any;
    http.put.and.returnValue(of(expectedResponse));
    service.updateOnBoardingMyStable(request, url).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });
  });

});
