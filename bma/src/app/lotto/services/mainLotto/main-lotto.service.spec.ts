import { of as observableOf, Observable, of } from 'rxjs';
import { MainLottoService } from './main-lotto.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { ILottoCms } from '../../models/lotto.model';

describe('MainLottoService', () => {
  let service: MainLottoService;
  let siteServerLottoService;
  let betHistoryMainService;

  const lottoData = [
    {
      description: '49s Lotto',
      name: '49s 6 ball lotto',
      sort: '49S',
      country: 'UK',
      lotteryPrice: [
        { numberPicks: '3' },
        { numberPicks: '2' },
        { numberPicks: '1' }
      ],
      draw: [
        { shutAtTime: '2099-01-01' }
      ]
    },
    {
      description: '49s Lotto',
      name: '49s 7 ball lotto',
      sort: '49BS',
      country: 'UK',
      lotteryPrice: [
        { numberPicks: '2' },
        { numberPicks: '1' }
      ],
      draw: [
        { shutAtTime: '2099-01-01' }
      ]
    },
    {
      description: 'Italy Lotto',
      name: 'Italy 7 ball lotto',
      sort: 'IT7',
      country: 'Italy',
      lotteryPrice: [],
      draw: [
        { shutAtTime: '2010-01-01' }
      ]
    },
    {
      description: 'Italy Lotto',
      name: 'Italy 6 ball lotto',
      sort: 'IT6',
      country: 'Italy',
      lotteryPrice: [],
      draw: [
        { shutAtTime: '2099-01-01' }
      ]
    }
  ];

  const lottoResultData = {
    'lotto-49s': {
      active: true,
      boosterBall: {
        country: 'UK',
        description: '49s Lotto',
        draw: [{
          shutAtTime: '2099-01-01'
        }],
        lotteryPrice: [
          { numberPicks: '1' },
          { numberPicks: '2' }
        ],
        name: '49s 7 ball lotto',
        shutAtTime: '2099-01-01',
        sort: '49BS'
      },
      country: 'UK',
      description: '49s Lotto',
      limits: undefined,
      name: '49s',
      sortCode: '49-lotto',
      normal: {
        country: 'UK',
        description: '49s Lotto',
        draw: [{
          shutAtTime: '2099-01-01'
        }],
        lotteryPrice: [
          { numberPicks: '1' },
          { numberPicks: '2' },
          { numberPicks: '3' }
        ],
        name: '49s 6 ball lotto',
        shutAtTime: '2099-01-01',
        sort: '49S'
      },
      shutAtTime: '2099-01-01',
      uri: 'lotto-49s'
    },
    'italy': {
      active: false,
      country: 'Italy',
      description: 'Italy Lotto',
      sortCode: 'it-lotto',
      limits: undefined,
      name: 'Italy',
      normal: {
        country: 'Italy',
        description: 'Italy Lotto',
        draw: [{
          shutAtTime: '2099-01-01'
        }],
        lotteryPrice: [],
        name: 'Italy 6 ball lotto',
        shutAtTime: '2099-01-01',
        sort: 'IT6'
      },
      shutAtTime: '2099-01-01',
      uri: 'italy'
    }
  };

  beforeEach(() => {
    siteServerLottoService = {
      getLottoPreviousResultsFromDate: jasmine.createSpy('getLottoPreviousResultsFromDate').and.returnValue(of({})),
      getLotteries: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    betHistoryMainService = {
      createRequest: (arg1, arg2) => {
        arg2({})
        return (of(<any>{
          detailLevel: 'DETAILED',
          fromDate: "2/2/2022",
          toDate: "2/2/2022",
          group: 'LOTTERYBET',
          pagingBlockSize: '20'
        })
        )
      },
      normalizeResponse: jasmine.createSpy('normalizeResponse').and.returnValue(of(<any>{
        detailLevel: 'DETAILED',
        fromDate: "2/2/2022",
        toDate: "2/2/2022",
        group: 'LOTTERYBET',
        pagingBlockSize: '20'
      })),
    }

    service = new MainLottoService(
      siteServerLottoService,
      betHistoryMainService
    );

    service.lottoCmsBanner = {
      globalBannerLink: 'string',
      globalBannerText: 'string',
      lottoConfig: [{
        enabled: true,
        bannerLink: 'string',
        bannerText: 'string',
        brand: 'string',
        id: '1',
        infoMessage: 'string',
        label: 'string',
        nextLink: 'string',
        sortOrder: 2,
        ssMappingId: '1,2'
      }]
    } as ILottoCms;

    service.lotteryData = {
      '49s': {
        uri: '49s',
        boosterBall: {
          id: "1"
        },
        normal: {
          id: '1'
        }
      }
    } as any
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getLotteryData', () => {
    it('should return observable', () => {
      service['lotteryData']['a'] = {} as any;
      expect(service.getLotteryData('a')).toEqual(jasmine.any(Observable));

      service['activeLotto'] = 'a';
      expect(service.getLotteryData(null)).toEqual(jasmine.any(Observable));

      service['lotteryData'] = {};
      service['activeLotto'] = null;
      service.getLotteriesByLotto = jasmine.createSpy().and.returnValue(observableOf(null));
      expect(service['getLotteryData'](null)).toEqual(jasmine.any(Observable));
      expect(service.getLotteriesByLotto).toHaveBeenCalled();
    });

    it('should return active lotto from lotto map', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');

      service['lotteryData'] = {};
      service.activeLotto = 'activeLotto';
      service.getLotteriesByLotto = jasmine.createSpy().and.returnValue(observableOf({ activeLotto: {} }));

      service['getLotteryData']('').subscribe(successHandler);
      tick();

      expect(service.getLotteriesByLotto).toHaveBeenCalled();
    }))

    it('should call lotto data cms object', () => {
      service.getLotteryData('');
      expect(service['getLotteryData'](null)).toEqual(jasmine.any(Observable));
    })

    it('should et lotterydata uri false', () => {
      service.lotteryData = {
        '49s': {
          uri: 'irish'
        }
      } as any;
      service.getLotteryData('')
      expect(service['getLotteryData'](null)).toEqual(jasmine.any(Observable));
    })
  });

  it('setLottoCmsBanner', () => {
    const data = {
      globalBannerLink: 'string',
      globalBannerText: 'string',
      lottoConfig: []
    }as ILottoCms;
    service.setLottoCmsBanner(data);
    expect(data).toBeTruthy;
  })

  it('getLottoCmsBanner', () => {
    service.getLottoCmsBanner();
    expect(service['getLottoCmsBanner']).toBeTruthy;
  })

  it('setLottoDialog', () => {
    const data = {
      bannerLink: 'string',
      bannerText: 'string',
      brand: 'string',
      id: 'string',
      infoMessage: 'string',
      label: 'string',
      nextLink: 'string',
      sortOrder: 1,
      ssMappingId: 'string',
      enabled: true
    }
    service.setLottoDialog(data);
    expect(service['setLottoDialog']).toBeTruthy;
    expect(service.lottoInfoDialog).toEqual(data)
  })

  it('getLottoData', () => {
    const value = service.getLottoDialog();
    expect(service['getLottoData']).toBeTruthy;
    expect(value).toEqual(service.lottoInfoDialog)
  })



  describe('getLotteriesByLotto', () => {
    it('should return observable of lotteries', () => {
      expect(service.getLotteriesByLotto()).toEqual(jasmine.any(Observable));
      expect(siteServerLottoService.getLotteries).toHaveBeenCalled();
    });

    it('should ', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');

      service['arrangeByLotto'] = jasmine.createSpy('arrangeByLotto');
      service.getLotteriesByLotto().subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(service['arrangeByLotto']).toHaveBeenCalled();
    }));
  });

  it('getLottoType', () => {
    expect(service.getLottoType({}, true)).toBe('boosterBall');
    expect(service.getLottoType({ id: 1 }, false)).toBe('boosterBall');
    expect(service.getLottoType({ normal: true }, false)).toBe('normal');
  });

  it('getShutAtTime', () => {
    let data = {
      draw: [
        { shutAtTime: '2099-09-30' },
        { shutAtTime: '2099-09-29' }
      ]
    };
    expect(service.getShutAtTime(data as any)).toBe('2099-09-29');

    data = {
      draw: [
        { shutAtTime: '2015-09-30' },
        { shutAtTime: '2016-09-29' }
      ]
    };
    expect(service.getShutAtTime(data as any)).toBeFalsy();
  });

  it('is7BallLottery', () => {
    expect(service['is7BallLottery']('Loto9')).toBeFalsy();
    expect(service['is7BallLottery']('7 BALL')).toBeTruthy();
    expect(service['is7BallLottery']('7 Ball')).toBeTruthy();
  });

  it('sortLotteryPrices', () => {
    const data = [
      { numberPicks: 'z' },
      { numberPicks: 'a' },
      { numberPicks: 'h' },
    ];
    const result = service['sortLotteryPrices'](data as any);
    expect(result).toEqual(jasmine.any(Array));
    expect(result[0].numberPicks).toBe('a');
    expect(result[1].numberPicks).toBe('h');
    expect(result[2].numberPicks).toBe('z');
  });

  describe('@arrangeByLotto', () => {
    it('should create lotto data', () => {
      const result = service['arrangeByLotto'](lottoData as any);
      expect(service.lotteryData).toEqual(lottoResultData as any);
      expect(result).toEqual(lottoResultData as any);
    });

    it('should not set active lotto', () => {
      const data = [
        {
          description: '49s Lotto',
          name: '49s 6 ball lotto',
          sort: '49S',
          country: 'UK',
          lotteryPrice: [
            { numberPicks: '3' },
            { numberPicks: '2' },
            { numberPicks: '1' }
          ],
          draw: [
            { shutAtTime: null }
          ]
        },
        {
          description: '49s Lotto',
          name: '49s 7 ball lotto',
          sort: '49BS',
          country: 'UK',
          lotteryPrice: [
            { numberPicks: '2' },
            { numberPicks: '1' }
          ],
          draw: [
            { shutAtTime: null }
          ]
        },
        {
          description: 'Italy Lotto',
          name: 'Italy 7 ball lotto',
          sort: 'IT7',
          country: 'Italy',
          lotteryPrice: [],
          draw: [
            { shutAtTime: null }
          ]
        },
        {
          description: 'Italy Lotto',
          name: 'Italy 6 ball lotto',
          sort: 'IT6',
          country: 'Italy',
          lotteryPrice: [],
          draw: [
            { shutAtTime: null }
          ]
        }
      ];
      const result = service['arrangeByLotto'](data as any);

      expect(service.lotteryData).toEqual({} as any);
      expect(result).toEqual({} as any);
    });

    it('it should call getHistory()', () => {
      const date = {
        "startDate": "2023-02-27T00:00:00Z",
        "endDate": "2023-03-30T00:00:00Z"
      };
      const value = service['getHistory'](date as any);
      expect(date).toEqual({ "startDate": "2023-02-27T00:00:00Z", "endDate": "2023-03-30T00:00:00Z" })
    });

    it('it should call getHistory() undefined values', () => {
      const date = { startDate: undefined };
      service['getHistory'](date as any);
      expect(date.startDate).toBeUndefined();
    });

    it('it should call getPreviousResultOf() with date', fakeAsync(() => {
      const date = {
        "startDate": "2023-02-27T00:00:00Z",
        "endDate": "2023-03-30T00:00:00Z"
      };
      const res = {};
      service['getPreviousResultOf'](date, "1").subscribe(res);
      tick();
      expect(res).toEqual({});
      expect(date).toEqual({ "startDate": "2023-02-27T00:00:00Z", "endDate": "2023-03-30T00:00:00Z" })
    }));

    it('it should call getPreviousResult() with dateObject', () => {
      const dateObject = {
        startDate: "2023-02-27T00:00:00Z",
        endDate: "2023-03-30T00:00:00Z"
      };
      service['getPreviousResult'](dateObject, '1');
      expect(dateObject.startDate).toEqual("2023-02-27T00:00:00Z");
      expect(dateObject.endDate).toEqual("2023-03-30T00:00:00Z");
    });

    it('it should call getBetHistoryForTimePeriod() with dateObject', () => {
      const dateObject = {
        startDate: "2023-02-27T00:00:00Z",
        endDate: "2023-03-30T00:00:00Z"
      };
      const res = {}
      service['getBetHistoryForTimePeriod'](dateObject).subscribe(res);
      expect(dateObject).toEqual({ "startDate": "2023-02-27T00:00:00Z", "endDate": "2023-03-30T00:00:00Z" })

    });
  });

  describe('@getMenuItems', () => {
    it('should create lotto menu items', () => {
      const result = service.getMenuItems(lottoResultData as any);
      expect(result).toEqual([{
        imageTitle: '49s',
        inApp: true,
        svg: '49s',
        svgId: '49-lotto',
        targetUri: '/lotto/lotto-49s',
        targetUriCopy: 'lotto-49s',
        uri: 'lotto-49s'
      }, {
        imageTitle: 'Italy',
        inApp: true,
        svg: 'Italy',
        svgId: 'it-lotto',
        targetUri: '/lotto/italy',
        targetUriCopy: 'italy',
        uri: 'italy'
      }]);
    });
  });
});
