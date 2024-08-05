import { of } from 'rxjs';
import { AutoseoService } from './autoseo.service';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';

describe('AutoseoService', () => {
  let service: AutoseoService;
  let http,domain,brand;
  beforeEach(() => {
    service = new AutoseoService(http, domain, brand);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  describe('getAutoSeoPageList',()=>{
    it('should send request to get autoseopagesList',()=>{
      let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
      service.getAutoSeoPageList();
      expect(sendRequestSpy).toHaveBeenCalled();
    });
  });
  describe('postNewAutoSeoPage',()=>{
    it('should send request to post NewAutoSeoPage',()=>{
      let autoseopage={uri:'/event'} as AutoSeoPage;
      let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
      service.postNewAutoSeoPage(autoseopage);
      expect(sendRequestSpy).toHaveBeenCalled();
    });
  });
  describe('deleteAutoSeoPage',()=>{
    it('should send request to delete AutoSeoPage with id',()=>{
      let autoseopageid = '1';
      let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
      service.deleteAutoSeoPage(autoseopageid);
      expect(sendRequestSpy).toHaveBeenCalled();
    });
  });
  describe('putAutoSeoPageChanges',()=>{
    it('should send request to save autoseopage changes with id',()=>{
      let autoseopageid = '1';
      let autoseopage={uri:'/event'} as AutoSeoPage;
      let sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));
      service.putAutoSeoPageChanges(autoseopageid,autoseopage);
      expect(sendRequestSpy).toHaveBeenCalled();
    });
  });
});
