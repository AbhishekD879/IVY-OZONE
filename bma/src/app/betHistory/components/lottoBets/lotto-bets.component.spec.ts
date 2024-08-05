import { LottoBetsComponent } from './lotto-bets.component';
import { of as observableOf } from 'rxjs';

describe('LottoBetsComponent', () => {
  let component, betHistoryMainService, timeService, userService, filtersService, locale, pubsub, cmsService, currencyPipe, deviceService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test'),
      toLowerCase: jasmine.createSpy('toLowerCase')
    };

    timeService = {
      getLocalDateFromString: jasmine.createSpy().and.returnValue('2019-03-04T16:30:45.000Z'),
      convertDateStr:  jasmine.createSpy().and.returnValue('2019-03-04T16:30:45.000Z')
    };

    filtersService = {
      removeLineSymbol: jasmine.createSpy().and.returnValue('test'),
      date: jasmine.createSpy().and.returnValue(new Date())
    };

    userService = {
      currencySymbol: jasmine.createSpy()
    };

    betHistoryMainService = {
      getLottoBetStatus: jasmine.createSpy().and.returnValue('lost'),
      getCelebrationBanner: jasmine.createSpy('getCelebrationBanner').and.returnValue({})
    };

    pubsub = {      
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(observableOf({
        svg: 'svg',
        svgId: 'svgId'
      }))
    };
    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    component = new LottoBetsComponent(betHistoryMainService, timeService, userService, filtersService, locale, pubsub, cmsService, currencyPipe);
    component.isBetHistoryTab = true;
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    const token = 'bethistory.noLottoBets';
    component.lottoBets = [];
    component.ngOnInit();

    expect(locale.getString).toHaveBeenCalledWith(token);
  });

  describe('#ngOnChanges', () => {
    it('generateLottoHistory should not be called', () => {
      const changes = {
        ngModel: { currentValue: 10}
      } as any;
      component['generateLottoHistory'] = jasmine.createSpy();
      component.ngOnChanges(changes);

      expect(component['generateLottoHistory']).not.toHaveBeenCalled();
    });

    it('generateLottoHistory should be called', () => {
      const changes = {
        lottoBets: { currentValue: 10}
      } as any;
      component['generateLottoHistory'] = jasmine.createSpy();
      component.ngOnChanges(changes);

      expect(component['generateLottoHistory']).toHaveBeenCalled();
    });
  });
  describe('CongratsBanner', () => {
    let bet;
    beforeEach(() => {
      component.celebration = {
        displayCelebrationBanner: true,
        duration: 240000000000,
        winningMessage: 'You have won {amount}!!',
        cashoutMessage: 'You have cashedout {amount}!!'
      };
      bet = {
        totalReturns: '6.00',
        stake: '5.00',
        settledAt: '2019-03-04 11:00:45',
        currency: '$',
        lotteryResults:[{settledAt : "2023-04-11 12:50:00"}]
      };
    });
    it('isCongratsBannerShown with bet', () => {
      expect(component.isCongratsBannerShown(bet)).toBeTrue();
    });
    it('isCongratsBannerShown with celebration as null', () => {
      component.celebration = null;
      expect(component.isCongratsBannerShown(bet)).toBe(undefined);
    });
    it('getReturnValue', () => {
      expect(component.getReturnValue(bet)).toBe('You have won 6.00$!!');
    });
    it('getReturnValue with celebration as null', () => {
      component.celebration = null;
      expect(component.getReturnValue(bet)).toBe(undefined);
    });
    it('getCashoutReturnValue', () => {
      expect(component.getCashoutReturnValue(bet)).toBe('You have cashedout 6.00$!!');
    });
    it('getCashoutReturnValue', () => {
      component.celebration = null;
      expect(component.getCashoutReturnValue(bet)).toBe(undefined);
    });
  });
  it('trackByBall should return joined string', () => {
    const index: number = 11;
    const item: any = {
      ballNo: '22'
    };
    const result = component.trackByBall(index, item);

    expect(result).toEqual('1122');
  });

  it('trackByBet should return joined string', () => {
    const index: number = 11;
    const item: any = {
      id: '22',
      betReceiptId: '33'
    };
    const result = component.trackByBet(index, item);

    expect(result).toEqual('112233');
  });
  describe('#generateLottoHistory', () => {
    let lottoBets;
    beforeEach(() => {
      lottoBets = [{"betType":{"code":"SGL","name":"Single"},"lotteryName":"|49's 6 ball|","drawName":"Lunchtime draw","date":"2023-04-11 10:54:53","lotterySub":{"subId":"6987","numSubs":"1","subReceipt":"L/300537516/0006987","stakePerBet":"1.00","outstandingSubs":"0","date":"2023-04-11 10:54:53"},"pick":[{"ballNo":"32","ballName":""}],"lotteryDraws":[{"winnings":{"value":"0.00"},"refund":{"value":"0.00"},"settled":"N","settledAt":"","lotteryDrawResult":[{pick : [{},{}]}],"xgameId":"64683","drawAt":"2023-04-11 12:50:00"}],"potentialPayout":{"value":null},"stake":{"currency":"GBP","stakePerLine":"1.00","tokenValue":"","value":"1.00"}}];
      component.lottoBets = lottoBets;
     })
    it('generateLottoHistory', () => {
      component['generateLottoHistory']();
      const result = component.lottoHistory;
  
      expect(filtersService.removeLineSymbol).toHaveBeenCalled();
      expect(result[0].balls).toBeDefined();
      expect(result[0].betDate).toBeDefined();
      expect(result[0].betReceiptId).toBeDefined();
      expect(result[0].currency).toBeDefined();
      expect(result[0].drawName).toBeDefined();
      expect(result[0].name).toBeDefined();
      expect(result[0].settled).toBeDefined();
      expect(result[0].stake).toBeDefined();
      expect(result[0].status).toBeDefined();
      expect(result[0].totalReturns).toBeDefined();
    });
    it('generateLottoHistory when bet is not settled', () => {
      component.lottoBets[0].settled = 'N';
      component['generateLottoHistory']();
      const result = component.lottoHistory;
      expect(result[0].totalReturns).toEqual('0.00');
    });
    it('generateLottoHistory when settledAt is not defined', () => {
      component.lottoBets[0].settledAt = undefined;
      component['generateLottoHistory']();
      const result = component.lottoHistory;
      expect(result[0].settledAt).toEqual('');
    });
    it('generateLottoHistory when bet is not settled', () => {
      component.lottoBets[0].settled = 'Y';
      component.settled = 'Y';
      component.lottoBets[0].lotterySub.outstandingSubs=1;
      component['generateLottoHistory']();
      const result = component.lottoHistory;
      expect(result[0].totalReturns).toEqual('0.00');
    });
  });

  it('generateLottoHistory', () => {
    component.lottoBets = [];
    cmsService.getItemSvg.and.returnValue(observableOf({}));
    component['generateLottoHistory']();
    expect(component.sportIconSvgId).toEqual('icon-generic');
  });

  it('generateLottoHistory', () => {
    component.lottoBets  = [{"lotterySub":{"outstandingSubs":"0"},"lotteryDraws":[{"winnings":{"value":"0.00"},"refund":{"value":"0.00"},"settled":"N","lotteryDrawResult":[]}],"potentialPayout":{"value":null},"stake":{"value":"1.00"}}];
    component['generateLottoHistory']();
    expect(component.lottoBets[0].lotteryDraws[0].lotteryDrawResult).toEqual([]);
  });
  
  it('handleToggleMore', () => {
    const bet = {isShowMore: false};
    component.handleToggleMore(bet);
    expect(bet.isShowMore).toBe(true);
  });

});
