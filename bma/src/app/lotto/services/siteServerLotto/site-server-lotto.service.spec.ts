import { of as observableOf,  Observable } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { SiteServerLottoService } from './site-server-lotto.service';
import environment from '@environment/oxygenEnvConfig';

describe('SiteServerLottoService', () => {
  let service: SiteServerLottoService;

  let http;
  let buildLotteriesService;
  // let timeService;
  // let simpleFiltersService;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    buildLotteriesService = {
      build: jasmine.createSpy('build'),
      buildLottoResults: jasmine.createSpy('buildLottoResults')
    };

    // timeService = {
    //   getTimeWithDelta: jasmine.createSpy('getTimeWithDelta'),
    // };

    // simpleFiltersService = {
    //   genFilters: jasmine.createSpy('genFilters')
    // };

    service = new SiteServerLottoService(
      http,
      buildLotteriesService,
      // timeService,
      // simpleFiltersService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('getLotteries', () => {
    service['sendRequest'] = jasmine.createSpy().and.returnValue(observableOf(null));
    expect(service.getLotteries()).toEqual(jasmine.any(Observable));
    expect(service['sendRequest']).toHaveBeenCalledWith(
      `${environment.SITESERVER_LOTTERY_ENDPOINT}/LotteryToDraw?simpleFilter=lottery.hasOpenDraw&translationLang=en&responseFormat=json`
    );
  });

  it('should build lotteries',  fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');

    service['sendRequest'] = jasmine.createSpy().and.returnValue(observableOf({body: {}}));
    service.getLotteries().subscribe(successHandler);
    tick();

    expect(successHandler).toHaveBeenCalled();
    expect(buildLotteriesService.build).toHaveBeenCalledWith({});
  }));

  it('getLottoPreviousResultsFromDate', () => {
    const data = { lottoId: "1", page: 1 ,startDate:"22/2/2222",endDate:"22/2/2222" };
  
    service['sendRequest'] = jasmine.createSpy().and.returnValue(observableOf(null));
    expect(service.getLottoPreviousResultsFromDate(data)).toEqual(jasmine.any(Observable));
    expect(service['sendRequest']).toHaveBeenCalledWith(
      `${environment.SITESERVER_HISTORIC_ENDPOINT}/ResultsForLottery/${data.lottoId}/${data.startDate}/${data.endDate}&translationLang=en&responseFormat=json`
    );
  });

  it('should build lotteries',  fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');
    const data = { lottoId: "1", page: 1 ,startDate:"22/2/2222",endDate:"22/2/2222" };
    service['sendRequest'] = jasmine.createSpy().and.returnValue(observableOf({body: {}}));
    service.getLottoPreviousResultsFromDate(data).subscribe(successHandler);
    tick();
    expect(successHandler).toHaveBeenCalled();
   }));

  it('sendRequest', () => {
    const url = 'http://path/to/api';
    const params = { x: 1, y: 2 };

    const result = service['sendRequest'](url, params);

    expect(http.get).toHaveBeenCalledWith(url, {
      observe: 'response', params
    });
    expect(result).toEqual(jasmine.any(Observable));
  });

  it('sendRequest', () => {
    const url = 'http://path/to/api';

    service['sendRequest'](url);

    expect(http.get).toHaveBeenCalledWith(url, {
      observe: 'response', params: {}
    });
  });
});
