import { SeoAPIService } from "./seo.api.service";

describe('SeoApiservice', () => {
  let service,
    globalLoaderService,
    apiClientService
  beforeEach(() => {
    globalLoaderService = {
        showLoader: jasmine.createSpy('showLoader'),
        hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
        seoPageService  : jasmine.createSpy('seoPageService').and.returnValue({
            getSingleSeoPage : jasmine.createSpy('getSingleSeoPage').and.returnValue({id:'1',url:'/event'}),
            putSeoPageChanges : jasmine.createSpy('putSeoPageChanges').and.returnValue({id:'2',url:'/inplay'}),
            deleteSeoPage : jasmine.createSpy('deleteSeoPage').and.returnValue({id:'3',url:'/inplay'}),
            getSeoPageList : jasmine.createSpy('getSeoPageList').and.returnValue({url:'/event'}),
            postNewSeoPage : jasmine.createSpy('postNewSeoPage').and.returnValue({id:'4',url:'/sport'}),
      }),
      autoseoPageService: jasmine.createSpy('autoseoPageService').and.returnValue({
        getAutoSeoPageList : jasmine.createSpy('getAutoSeoPageList').and.returnValue({id:'1',url:'/event'}),
        putAutoSeoPageChanges : jasmine.createSpy('putAutoSeoPageChanges').and.returnValue({id:'2',url:'/sport'}),
        deleteAutoSeoPage : jasmine.createSpy('deleteAutoSeoPage').and.returnValue({id:'3',url:'/inplay'}),
        postNewAutoSeoPage : jasmine.createSpy('postNewAutoSeoPage').and.returnValue({id:'4',url:'/event'}),
    })
    };
    service = new SeoAPIService(
      globalLoaderService,
      apiClientService
    );
  });

  it('should be created', () => {
    expect(service).toBeDefined();
  });
  it('should call wrappedObservable and call getseopageslist', () => {
     spyOn(service, 'wrappedObservable');
     service.getSeoListData();
     service.getData = {url:'/event'};
   expect(globalLoaderService.showLoader).toHaveBeenCalled();  
   expect(apiClientService.seoPageService().getSeoPageList).toHaveBeenCalled();
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call wrappedObservable and call getsingleseopage', () => {
     spyOn(service, 'wrappedObservable');
     service.getSingSeoItemData('1');
     service.getData = {id:'1',url:'/event'};
   expect(apiClientService.seoPageService().getSingleSeoPage).toHaveBeenCalledWith('1');
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call wrappedObservable and call putseopagechanges', () => {
     spyOn(service, 'wrappedObservable');
     service.putSeoItemChanges({id:'2',url:'/inplay'});
     service.getData = {id:'2',url:'/inplay'};
   expect(globalLoaderService.showLoader).toHaveBeenCalled();  
   expect(apiClientService.seoPageService().putSeoPageChanges).toHaveBeenCalledWith('2',{id:'2',url:'/inplay'});
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call wrappedObservable and call deleteSeopage', () => {
     spyOn(service, 'wrappedObservable');
     service.deleteSeoPage('2');
     service.getData = {id:'3',url:'/inplay'};
   expect(globalLoaderService.showLoader).toHaveBeenCalled();  
   expect(apiClientService.seoPageService().deleteSeoPage).toHaveBeenCalledWith('2');
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call wrappedObservable and call postnewseopage', () => {
    spyOn(service, 'wrappedObservable');
     service.createSeoItem({id:'4',url:'/sport'});
     service.getData = {id:'4',url:'/sport'};
   expect(globalLoaderService.showLoader).toHaveBeenCalled();  
   expect(apiClientService.seoPageService().postNewSeoPage).toHaveBeenCalledWith({id:'4',url:'/sport'});
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getData);    
  });
  it('should call wrappedObservable and call postnewautoseopage', () => {
     spyOn(service, 'wrappedObservable');
     service.createAutoSeoItem({id:'4',url:'/event'});
     service.getautoseoData= {id:'4',url:'/event'};
   expect(globalLoaderService.showLoader).toHaveBeenCalled();  
   expect(apiClientService.autoseoPageService().postNewAutoSeoPage).toHaveBeenCalledWith({id:'4',url:'/event'});
   expect(service.wrappedObservable).toHaveBeenCalledWith(service.getautoseoData);    
  });
  it('should call wrappedObservable and call deletenewautoseopage', () => {
    spyOn(service, 'wrappedObservable');
    service.deleteAutoSeoPage('3');
    service.getautoseoData= {id:'3',url:'/inplay'};
  expect(globalLoaderService.showLoader).toHaveBeenCalled();  
  expect(apiClientService.autoseoPageService().deleteAutoSeoPage).toHaveBeenCalledWith('3');
  expect(service.wrappedObservable).toHaveBeenCalledWith(service.getautoseoData);    
 });
  it('should call wrappedObservable and call putautoseopagechanges', () => {
    spyOn(service, 'wrappedObservable');
    service.putAutoSeoItemChanges({ id: '2', url: '/sport' });
    service.getautoseoData = { id: '2', url: '/sport' }
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.autoseoPageService().putAutoSeoPageChanges).toHaveBeenCalledWith('2', { id: '2', url: '/sport' });
    expect(service.wrappedObservable).toHaveBeenCalledWith(service.getautoseoData);
  });
  it('should call wrappedObservable and call getautoseopagesData', () => {
    spyOn(service, 'wrappedObservable');
    service.getAutoSeoListData();
    service.getautoseoData = { id: '1', url: '/event' };
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.autoseoPageService().getAutoSeoPageList).toHaveBeenCalled();
    expect(service.wrappedObservable).toHaveBeenCalledWith(service.getautoseoData);
  });
  it('should call hideloader', () => {
    service.handleRequestError('error');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
