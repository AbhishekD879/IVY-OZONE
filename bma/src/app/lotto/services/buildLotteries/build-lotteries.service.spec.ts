import { BuildLotteriesService } from '@app/lotto/services/buildLotteries/build-lotteries.service';
import environment from '@environment/oxygenEnvConfig';


describe('BuildLotteriesService', () => {
  let buildLotteriesService: BuildLotteriesService;

  const lottoResponse = {
    SSResponse: {
      children: [{
        lottery: {
          description: '49s lotto',
          id: '1',
          name: '49s 6 ball lotto',
          sort: '49S',
          country: 'UK',
          limits:2, 
          lotteryPrice: [
            { numberPicks: '3' },
            { numberPicks: '2' },
            { numberPicks: '1' }
          ],
          draw: [
            { shutAtTime: '2099-01-01' }
          ]
        }
      }, {
        lottery: {
          description: 'Germany lotto',
          id: '2',
          name: 'Germany 6 ball lotto',
          sort: 'GER6',
          country: 'Germany',
          limits: 1, 
          lotteryPrice: [],
          draw: [
            { shutAtTime: '2099-01-01' }
          ]
        }
      }, {
        lottery: {
          description: 'Italy lotto',
          id: '3',
          name: 'Italy 6 ball lotto',
          sort: 'IT6',
          country: 'Italy',
          limits:3,
          lotteryPrice: [],
          draw: [
            { shutAtTime: '2010-01-01' }
          ]
        }
      }]
    }
  };

  const LOTTERIES_CONFIG = environment.LOTTERIES_CONFIG;

  beforeEach(() => {
    buildLotteriesService = new BuildLotteriesService();
  });

  describe('@build', () => {
    it('should create lotto data', () => {
      // buildLotteriesService.LOTTERIES_CONFIG = {
      //   '1': { country: 'UK', excluded: true },
      //   '2': { country: 'Germany'}
      // };
      const result = buildLotteriesService.build(lottoResponse);
      console.log('67::::', result);
      expect([result[1]]).toEqual([{
        description: 'Germany lotto',
        id: '2',
        limits: 1,
        name: 'Germany 6 ball lotto',
        sort: 'GER6',
        country: 'Germany',
        lotteryPrice: [],
        draw: [
          { shutAtTime: '2099-01-01' }
        ]
      }] as any);
    });

    it('should create lotto data with limits property', () => {
      // buildLotteriesService.LOTTERIES_CONFIG = {
      //   '1': { country: 'UK', limits: 2 }
      // };
      const result = buildLotteriesService.build(lottoResponse);
      expect([result[0]]).toEqual([{
        description: '49s lotto',
        id: '1',
        limits: 2,
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
      }] as any);
    });

    it('should create lotto data for properly ids', () => {
      // buildLotteriesService.LOTTERIES_CONFIG = {
      //   '4': { country: 'UK' },
      //   '5': { country: 'Italy'}
      // };
      const result = buildLotteriesService.build(lottoResponse);
      expect(result).toEqual([] as any);
    });

    it('should not set lottery limits',  () => {
      const data = {
        SSResponse: {
          children: [
            // { lottery: {
            //     id: '1',
            //     ballColor: null
            //   }}, { lottery: {
            //     id: '2',
            //     ballColor: null
            //   }}, { lottery: {
            //     id: '3',
            //     ballColor: null
            //   }}
            ]
        }
      };

      buildLotteriesService['arrangeChildren'] = jasmine.createSpy('arrangeChildren');
      buildLotteriesService['getCountry'] = jasmine.createSpy('getCountry');

      // buildLotteriesService.LOTTERIES_CONFIG = {};
      buildLotteriesService.build(data);

      expect(buildLotteriesService['arrangeChildren']).not.toHaveBeenCalled();
      expect(buildLotteriesService['getCountry']).not.toHaveBeenCalled();
    });
  });

  it('Tests if BuildLotteries Service Created', () => {
    expect(buildLotteriesService).toBeTruthy();
    // expect(buildLotteriesService.LOTTERIES_CONFIG).toEqual(LOTTERIES_CONFIG);
  });

  it('#buildLottoResults', () => {
    buildLotteriesService['stripResponceFooter'] = jasmine.createSpy('stripResponceFooter')
      .and.returnValue([]);
    const data = {
      lottery: {
        id: '1'
      }
    };

    buildLotteriesService['buildLottoResults'](data);
    expect(buildLotteriesService['stripResponceFooter']).toHaveBeenCalled();
  });

  it('#stripResponceFooter', () => {
    const data = {
      SSResponse: {
        children: ['ch1', 'ch2', 'ch3']
      }
    };
    const cuttedResponce = buildLotteriesService['stripResponceFooter'](data);

    expect(cuttedResponce).toEqual(['ch1', 'ch2']);
  });

  it('#arrangeChildren', () => {
    const lotteryEntity = {
      children: [
        {
          propKeyCh1: 'propKeyCh1'
        },
        {
          propKeyCh2: 'propKeyCh2'
        },
        {
          propKeyCh3: 'propKeyCh3'
        }
      ],
      propKeyCh1: [],
      propKeyCh2: []
    };
    const expectedResult = {
      propKeyCh1: ['propKeyCh1'],
      propKeyCh2: ['propKeyCh2'],
      propKeyCh3: ['propKeyCh3'],
    };
    const actualResult = buildLotteriesService['arrangeChildren'](lotteryEntity);

    expect(actualResult).toEqual(expectedResult);
  });
});
