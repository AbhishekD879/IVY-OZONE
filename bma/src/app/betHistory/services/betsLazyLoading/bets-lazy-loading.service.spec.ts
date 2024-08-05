import { throwError, of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { BetsLazyLoadingService } from '@app/betHistory/services/betsLazyLoading/bets-lazy-loading.service';

describe('BetsLazyLoadingService', () => {
  let service: BetsLazyLoadingService;
  let betHistoryMainService: any;
  let windowRefService: any;
  let domTools: any;
  let options: any;


  beforeEach(() => {
    options = {
      initialData: 'testData',
      betType: 'testType',
      betfilter: 'testFilter',
      addLazyLoadedBets: 'testBets',
    };

    betHistoryMainService = {
      getHistoryPage: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    windowRefService = {
      nativeWindow: {
        removeEventListener: () => {},
        addEventListener: () => {},
      }
    };

    domTools = {
      getOffset: () => {},
      getHeight: () => {},
      getScrollTop: () => {},
    };

    service = new BetsLazyLoadingService(betHistoryMainService as any, windowRefService as any, domTools as any);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#initialize && #initialize should test laziloading initialization and parameters reset', () => {

    spyOn<any>(service, 'setData').and.callThrough();

    service.initialize(options);

    expect(service.initialData).toEqual('testData');
    expect(service.betType).toEqual('testType');
    expect(service.betfilter).toEqual('testFilter');
    expect(service.addLazyLoadedBets).toEqual('testBets' as any);
    expect(service['setData']).toHaveBeenCalledWith(options.initialData);

    service.reset();

    expect(service.initialData).toEqual(null);
    expect(service.betType).toEqual(null);
    expect(service.betfilter).toEqual(null);
    expect(service.addLazyLoadedBets).toEqual(null);
  });

  it('#scrollHandler should check dome events fire', () => {
    spyOn(domTools, 'getOffset').and.returnValue(10);
    spyOn(document, 'querySelector').and.returnValue('fakeElement' as any);
    spyOn(domTools, 'getHeight').and.returnValue(10);
    spyOn(domTools, 'getScrollTop').and.returnValue(30);
    service['scrollHandler']();
    expect(domTools.getOffset).toHaveBeenCalledWith('fakeElement');
    expect(domTools.getHeight).toHaveBeenCalledWith('fakeElement');
    expect(domTools.getScrollTop).toHaveBeenCalled();
  });
  
  it('#scrollHandler should check dome events fire - lazyload-scroll', () => {
    spyOn(domTools, 'getOffset').and.returnValue(10);
    spyOn(document, 'querySelector').and.returnValue(null);
    spyOn(domTools, 'getHeight').and.returnValue(10);
    spyOn(domTools, 'getScrollTop').and.returnValue(30);
    service['scrollHandler']();
    expect(domTools.getOffset).not.toHaveBeenCalled();
    expect(domTools.getHeight).not.toHaveBeenCalled();
    expect(domTools.getScrollTop).not.toHaveBeenCalled();
  });

  it('#setData should fill component data', () => {
    options.initialData = {
      bets: [],
      // pageToken: 'testPageToken',
      timeStamp: 'testTimeStamp'
    };
    service.addLazyLoadedBets = () => {};
    spyOn(service, 'addLazyLoadedBets');
    spyOn(windowRefService.nativeWindow, 'addEventListener');

    service['setData'](options.initialData, true);
    expect(service.addLazyLoadedBets).toHaveBeenCalled();
    expect(service.timeStamp).toEqual('testTimeStamp');

    options.initialData.pageToken = 'testPageToken';

    service['setData'](options.initialData);
    expect(service.pageToken).toEqual('testPageToken');
    expect(windowRefService.nativeWindow.addEventListener).toHaveBeenCalled();
  });

  it('#loadMore load extra bets - loadMoreCallBack', fakeAsync(() => {
    service.loadMoreCallBack = new Function;
    service.pageToken = 'testPageToken';
    service.betfilter = 'bet';
    spyOn<any>(service, 'loadMoreCallBack');
    spyOn<any>(service, 'reset');

    service['loadMore']();
    tick();
    expect(betHistoryMainService.getHistoryPage).not.toHaveBeenCalled();
    expect(service.reset).not.toHaveBeenCalledWith();
    expect(service.loadMoreCallBack).toHaveBeenCalledWith();
  }));

  it('#loadMore load extra bets', fakeAsync(() => {
    spyOn<any>(service, 'setData');
    spyOn<any>(service, 'reset');

    service['loadMore']();
    tick();
    expect(betHistoryMainService.getHistoryPage).not.toHaveBeenCalled();
    expect(service.reset).toHaveBeenCalledWith();
  }));

  it('#loadMore load extra bets', fakeAsync(() => {
    spyOn<any>(service, 'setData');
    spyOn<any>(service, 'reset');

    service.pageToken = 'testPageToken';
    service['loadMore']();
    tick();
    expect(betHistoryMainService.getHistoryPage).toHaveBeenCalled();
  }));

  it('#loadMore load extra bets error', fakeAsync(() => {
    betHistoryMainService.getHistoryPage = jasmine.createSpy().and.returnValue(throwError({}));
    service = new BetsLazyLoadingService(betHistoryMainService as any, windowRefService as any, domTools as any);

    spyOn<any>(service, 'setData');
    spyOn<any>(service, 'reset');

    service.pageToken = 'testPageToken';
    service['loadMore']();
    tick();
    expect(betHistoryMainService.getHistoryPage).toHaveBeenCalled();
    expect(service.reset).toHaveBeenCalledWith();
  }));
});
