import { Bet } from './bet';
import { IBet, IBetPayload, IBetInfo } from '@betslip/services/bet/bet.model';
import { ILeg } from '@betslip/services/models/bet.model';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { IOutcome } from '@core/models/outcome.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import { UserService } from '@core/services/user/user.service';

describe('BetslipBetModel', () => {
  let bet;
  let freeBetService;
  let betStakeService;
  let sportsLegPriceService;
  let overaskService;
  let localeService;
  let fracToDec;
  let filters;
  let betslipFilters;
  let storageService;
  let user;
  let pubSubService;
  let params;

  beforeEach(() => {
    params = {
      isMocked: true,
      uid: '1',
      placed: {
        id: '1'
      },
      docId: '11',
      type: 'single',
      isLotto : true,
      betOffer: {},
      legs: [{ docId: '1' }],
      errs: [],
      freeBets: [],
      allLegs: [{ docId: '1', parts: [{}] }],
      legIds: ['1'],
      freebet: {},
      oddsBoost: { id: 123 },
      payout: [{
        legType: 'Y',
        potential: '1.00'
      }],
      winPlace: '1/4',
      lines: 1,
      stake: {
        doc: 'Y'
      }
    };
    freeBetService = {
      construct: jasmine.createSpy('construct')
    };
    betStakeService = jasmine.createSpyObj('betStakeService', ['construct']);
    sportsLegPriceService = jasmine.createSpyObj('sportsLegPriceService', ['convert']);
    overaskService = {};
    storageService = {
      active: true,
      get: jasmine.createSpy('storage').and.returnValue(true)
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    fracToDec = {
      getDecimal: jasmine.createSpy('getDecimal')
    };
    filters = jasmine.createSpyObj('filters', ['filterAddScore', 'filterPlayerName']);
    betslipFilters = {
      handicapValueFilter: jasmine.createSpy('handicapValueFilter')
    };
    user = { currencySymbol: '$' } as UserService;
    pubSubService = jasmine.createSpyObj('pubSubService', ['publish', 'subscribe', 'unsubscribe']);

    betStakeService.construct.and.callFake(value => value);
    betslipFilters.handicapValueFilter.and.callFake(value => value);
  });

  function createBet(data: Partial<IBet>): Bet {
    return new Bet(data, freeBetService, betStakeService, sportsLegPriceService, overaskService, localeService,
      fracToDec, filters, betslipFilters, storageService, user, pubSubService);
  }

  describe('constructor', () => {
    it('should set initial values', () => {
      bet = createBet(params);

      expect(bet).toEqual(jasmine.objectContaining({
        isMocked: params.isMocked,
        uid: params.uid,
        bsId: 1,
        placed: params.placed,
        docId:  params.docId,
        type: params.type,
        betOffer: params.betOffer,
        errs: params.errs,
        payout: params.payout,
        winPlace: params.winPlace
      }));
    });

    it('should set correct _stake property based on params stake', () => {
      params.stake = { doc: '1' };
      bet = createBet(params);

      expect(bet.stake).toEqual(params.stake);
      expect(betStakeService.construct).not.toHaveBeenCalled();

      params.stake = { value: '1' };
      bet = createBet(params);

      expect(betStakeService.construct).toHaveBeenCalledWith({
        lines: params.lines,
        ...params.stake
      });
    });
  });

  it('should return correct lines', () => {
    params.lines = 1;
    params.winPlace = 'WIN';
    bet = createBet(params);

    expect(bet.lines).toEqual(params.lines);

    params.lines = 1;
    params.winPlace = 'EACH_WAY';
    bet = createBet(params);

    expect(bet.lines).toEqual(params.lines * 2);
  });

  it('should set stake', () => {
    const value = 5;

    bet = createBet(params);
    bet.stake = value;

    expect(bet._stake.perLine).toEqual(value);
  });

  it('should set/get freebet', () => {
    const value = 5;
    const freeBet = { value };

    freeBetService.construct.and.returnValue(freeBet);
    bet = createBet(params);
    bet.freeBet = value;

    expect(freeBetService.construct).toHaveBeenCalledWith(value);
    expect(bet._freeBet).toEqual(freeBet);
    expect(bet.freeBet).toEqual(freeBet);
    expect(bet.freeBets).toEqual(params.freeBets);
  });

  it('should set/get isEachWay', () => {
    params.winPlace = 'EACH_WAY';
    bet = createBet(params);

    expect(bet.isEachWay).toBeTruthy();

    bet.isEachWay = false;
    expect(bet.isEachWay).toBeFalsy();
    expect(bet.winPlace).toEqual('WIN');

    bet.isEachWay = true;
    expect(bet.isEachWay).toBeTruthy();
    expect(bet.winPlace).toEqual('EACH_WAY');
  });

  it('doc oddsBoost active', () => {
    bet = createBet(params);
    bet['getOddsBoostObj'] = jasmine.createSpy('getOddsBoostObj').and.returnValue({});
    bet.stake.doc = jasmine.createSpy().and.returnValue({});
    bet.oddsBoost = { id: 123 };
    const res = bet.doc();
    expect(res).toEqual({
      documentId: '11',
      betTypeRef: { id: 'single' },
      lines: { number: 1 },
      legRef: [{ documentId: '1' }]
    });

    expect(bet['getOddsBoostObj']).toHaveBeenCalled();
    expect(storageService.get).toHaveBeenCalledWith('oddsBoostActive');
  });

  it('doc oddsBoost not active', () => {
    storageService.get = jasmine.createSpy().and.returnValue(false);

    bet = createBet(params);
    bet['getOddsBoostObj'] = jasmine.createSpy('getOddsBoostObj');
    bet.stake.doc = jasmine.createSpy().and.returnValue({});

    bet.doc();

    expect(bet['getOddsBoostObj']).not.toHaveBeenCalled();
    expect(storageService.get).toHaveBeenCalledWith('oddsBoostActive');
  });

  describe('findLegs and findEachWayLegs', () => {
    it('should returned matched legs', () => {
      const legs = [{ docId: '1' }, { docId: 2 }, { }, { docId: '3' }];
      const legIds = ['1', '3'];

      expect(Bet.findLegs(legs as ILeg[], legIds)).toEqual([legs[0] as ILeg, legs[3] as ILeg]);
    });

    it('should return each way legs', () => {
      const legs = [{
        docId: '1',
        winPlace: 'EACH_WAY'
      }, {
        docId: 2,
        firstOutcomeId: '3'
      }, { }, {
        docId: '3',
        winPlace: 'EACH_WAY',
        firstOutcomeId: '3'
      }];
      const legIds = ['1', '2'];

      expect(Bet.findEachWayLegs(legs as ILeg[], legIds)).toEqual([legs[0] as ILeg, legs[3] as ILeg]);
    });
  });

  describe('getPayout', () => {
    it('should return falsy value of not matched legType', () => {
      const payoutData = [{ legType: 'P', potential: 1 }];
      expect(Bet.getPayout()).toBeFalsy();
      expect(Bet.getPayout(payoutData)).toBeFalsy();
    });

    it('should return correct payout value', () => {
      const payoutData = [{ legType: 'P', potential: 1 }, { legType: 'W', potential: 2 }, { legType: 'W', potential: 3 }];
      expect(Bet.getPayout(payoutData)).toEqual(payoutData[1].potential);
    });
  });

  describe('isDisabled', () => {
    it('should return falsy value for non single bet', () => {
      expect(Bet.isDisabled({ type: 'DBL' } as Bet, {})).toBeFalsy();
    });

    it('should check provided params for errors existance', () => {
      expect(Bet.isDisabled({ type: 'SGL', legs: [{
        parts: [{ outcome: {} }]
      }] } as Bet, { errs: [] })).toBeFalsy();
      expect(Bet.isDisabled({ type: 'SGL', legs: [] } as Bet,
        { errs: [ { msg: 'error' } as IBetError] } as Partial<IBet>)).toBeTruthy();
    });

    it('should return true for cases with single bet where there are errors in outcome', () => {
      bet = { type: 'SGL', legs: [{
        parts: [{
          outcome: {
            errorMsg: 'error',
            handicapErrorMsg: 'error',
            priceChange: false,
            handicapChange: false,
            stakeError: false
          }
        }]
      }]};

      expect(Bet.isDisabled(bet as Bet, {})).toBeTruthy();

      bet.legs[0].parts[0].outcome.errorMsg = '';
      expect(Bet.isDisabled(bet as Bet, {})).toBeTruthy();

      bet.legs[0].parts[0].outcome.handicapErrorMsg = '';
      expect(Bet.isDisabled(bet as Bet, {})).toBeTruthy();

      bet.legs[0].parts[0].outcome.priceChange = true;
      expect(Bet.isDisabled(bet as Bet, {})).toBeFalsy();

      bet.legs[0].parts[0].outcome.handicapChange = true;
      expect(Bet.isDisabled(bet as Bet, {})).toBeFalsy();
    });

    it('should return false for cases with single bet where there are no errors in outcome', () => {
      bet = { type: 'SGL', legs: [{
        parts: [{
          outcome: {
            errorMsg: null,
            handicapErrorMsg: null,
            priceChange: false,
            handicapChange: false,
            stakeError: false
          }
        }, {
          outcome: {
            errorMsg: null,
            handicapErrorMsg: null,
            priceChange: false,
            handicapChange: false,
            stakeError: false
          },
          errorMsg: null,
          handicapErrorMsg: null
        }]
      }]};

      expect(Bet.isDisabled(bet as Bet, {})).toBeFalsy();
    });
  });

  describe('getSportType', () => {
    it('should return false for non-racing sport category', () => {
      bet = {
        legs: [{
          parts: [{
            outcome: {
              details: {
                categoryId: '18'
              }
            }
          }]
        }, {
          parts: [{
            outcome: {
              details: {
                categoryId: '20'
              }
            }
          }]
        }]
      };

      expect(Bet.getSportType(bet as Bet)).toBeFalsy();
    });

    it('should return true for racing sport category', () => {
      bet = {
        legs: [{
          parts: [{
            outcome: {
              details: null
            }
          }]
        }, {
          parts: [{
            outcome: {
              details: {
                categoryId: '21'
              }
            }
          }]
        }]
      };

      expect(Bet.getSportType(bet as Bet)).toBeTruthy();
    });
  });

  it('should check outcomes correct score major code', () => {
    expect(Bet.isCS({ outcome: { outcomeMeaningMajorCode: 'MM' }})).toBeFalsy();
    expect(Bet.isCS({ outcome: { outcomeMeaningMajorCode: 'CS' }})).toBeTruthy();
  });

  describe('updateOriginalPrices', () => {
    it('should not add originalPrice property if it not avaialble', () => {
      const outcome = { originalPrice: null };
      const payload = { lp_den: '4', lp_num: '1' };

      Bet.updateOriginalPrices(outcome as IOutcome, payload as IBetPayload);
      expect(outcome.originalPrice).toBeFalsy();
    });

    it('should update originalPrice based on payload', () => {
      const outcome = {
        originalPrice: {
          priceDen: 10,
          priceNum: 11
        } as IOutcomePrice,
        prices: [{
          priceDen: 5,
          priceNum: 6
        }]
      };
      const payload = { lp_den: 4, lp_num: 1 };

      Bet.updateOriginalPrices(outcome as IOutcome, payload as IBetPayload);

      expect(outcome.originalPrice.priceDen).toEqual(payload.lp_den);
      expect(outcome.originalPrice.priceNum).toEqual(payload.lp_num);
    });

    it('should update originalPrice based on outcome prices', () => {
      const outcome = {
        originalPrice: {
          priceDen: 10,
          priceNum: 11
        } as IOutcomePrice,
        prices: [{
          priceDen: 5,
          priceNum: 6
        }]
      };
      const payload = { };

      Bet.updateOriginalPrices(outcome as IOutcome, payload as IBetPayload);

      expect(outcome.originalPrice.priceDen).toEqual(outcome.prices[0].priceDen);
      expect(outcome.originalPrice.priceNum).toEqual(outcome.prices[0].priceNum);
    });
  });

  describe('setPriceData', () => {
    it('should handle case when no price is avaialble', () => {
      bet = {
        price: {
          props: {
            priceNum: null,
            priceDen: null
          }
        }
      };
      const leg = {
        documentId: '1',
        selection: {
          price: {
            props: {
              priceNum: null,
              priceDen: null
            }
          }
        }
      };
      const outcome = { prices: [] };
      const payload = {};

      Bet.setPriceData(bet as Bet, leg as ILeg, outcome as IOutcome, payload as IBetPayload);

      expect(outcome.prices.length).toEqual(0);
    });

    it('should update outcome and bet prices based on payload', () => {
      bet = {
        price: {
          props: {
            priceNum: null,
            priceDen: null
          }
        },
        fracToDec
      };
      const leg = {
        documentId: '1',
        selection: {
          price: {
            props: {
              priceNum: null,
              priceDen: null
            }
          },
          selectionPrice: {},
          params: {
            price: {}
          }
        }
      };
      const outcome = { prices: [{
        priceDen: null,
        priceNum: null
      }] };
      const payload = { lp_den: 4, lp_num: 1 };

      Bet.setPriceData(bet as Bet, leg as ILeg, outcome as IOutcome, payload as IBetPayload);

      expect(outcome.prices[0].priceDen).toEqual(payload.lp_den);
      expect(outcome.prices[0].priceNum).toEqual(payload.lp_num);
      expect(leg.selection.price.props.priceDen).toEqual(payload.lp_den);
      expect(leg.selection.price.props.priceNum).toEqual(payload.lp_num);
      expect(bet.price.props.priceDen).toEqual(payload.lp_den);
      expect(bet.price.props.priceNum).toEqual(payload.lp_num);
    });

    it('should update outcome and bet prices based on original price', () => {
      bet = {
        price: {
          props: null
        },
        fracToDec
      };
      const leg = {
        documentId: '1',
        selection: {
          price: {
            props: null
          },
          selectionPrice: {},
          params: {
            price: {}
          }
        }
      };
      const outcome = {
        prices: [{
          priceDen: null,
          priceNum: null
        }],
        originalPrice: {
          priceDen: 10,
          priceNum: 11
        }
      };
      const payload = { };

      Bet.setPriceData(bet as Bet, leg as ILeg, outcome as IOutcome, payload as IBetPayload);

      expect(leg.selection.price.props.priceDen).toEqual(outcome.originalPrice.priceDen);
      expect(leg.selection.price.props.priceNum).toEqual(outcome.originalPrice.priceNum);
      expect(bet.price.props.priceDen).toEqual(outcome.originalPrice.priceDen);
      expect(bet.price.props.priceNum).toEqual(outcome.originalPrice.priceNum);
    });
  });

  describe('updateOutcomeName', () => {
    it('should parse updated outcome name', () => {
      bet = { betslipFilters };
      const outcome = { name: 'test +5' };

      betslipFilters.handicapValueFilter.and.callFake(value => value);

      expect(Bet.updateOutcomeName('(+5)', outcome as IOutcome, bet as Bet)).toEqual('test +5');
    });

    it('should parse updated outcome name with brackets', () => {
      bet = { betslipFilters };
      const outcome = { name: 'Win (Kids) (+2.0)' };

      betslipFilters.handicapValueFilter.and.callFake(value => value);

      expect(Bet.updateOutcomeName('+2.0', outcome as IOutcome, bet as Bet)).toEqual('Win (Kids) (+2.0)');
    });
  });

  describe('setHandicapData', () => {
    it('should set old value if it was not changed', () => {
      const leg = {
        documentId: '1',
        selection: {
          price: {
            props: null
          },
          legParts: [{}],
          selectionPrice: {},
          params: {
            price: {}
          }
        },
        parts: [{}]
      };
      const outcome = {
        name: 'test +5',
        prices: [{
          handicapValueDec: null,
          rawHandicapValue: null
        }]
      };
      const payload = {
        raw_hcap: '5'
      };
      const handicapValue = '(+5)';
      bet = { betslipFilters };

      Bet.setHandicapData(leg as ILeg, outcome as IOutcome, payload as IBetPayload, handicapValue, bet as Bet);

      expect(outcome.prices[0].handicapValueDec).toEqual(handicapValue);
      expect(outcome.prices[0].rawHandicapValue).toEqual(payload.raw_hcap);
      expect(outcome.name).toEqual('test +5');
    });

    it('should extend first leg part', () => {
      const leg = {
        documentId: '1',
        selection: {
          legParts: [{}]
        },
        parts: [{
          range: { }
        }]
      };
      const outcome = {
        name: 'test',
        prices: [{
          handicapValueDec: 1,
          rawHandicapValue: 5
        }]
      };
      const payload = { };
      const handicapValue = '(+5)';
      bet = { betslipFilters };

      Bet.setHandicapData(leg as ILeg, outcome as IOutcome, payload as IBetPayload, handicapValue, bet as Bet);

      expect(leg.selection.legParts[0]).toEqual(jasmine.objectContaining({
        range: {
          type: 'MATCH_HANDICAP',
          low: handicapValue,
          high: handicapValue
        }
      }));
      expect(leg.parts[0]).toEqual(jasmine.objectContaining({
        range: {
          type: 'MATCH_HANDICAP',
          low: handicapValue,
          high: handicapValue
        }
      }));
    });

    it('should update leg ranges', () => {
      const leg = {
        documentId: '1',
        selection: {
          legParts: [{
            range: {
              high: null,
              low: null
            }
          }]
        },
        parts: [{
          range: {
            high: null,
            low: null
          }
        }]
      };
      const outcome = {
        name: 'test +5',
        prices: [{
          handicapValueDec: 1,
          rawHandicapValue: 5
        }]
      };
      const payload = { };
      const handicapValue = '(+5)';
      bet = { betslipFilters };

      Bet.setHandicapData(leg as ILeg, outcome as IOutcome, payload as IBetPayload, handicapValue, bet as Bet);

      expect(leg.selection.legParts[0].range.high).toEqual(handicapValue);
      expect(leg.selection.legParts[0].range.low).toEqual(handicapValue);
      expect(leg.parts[0].range.low).toEqual(handicapValue);
      expect(leg.parts[0].range.high).toEqual(handicapValue);
    });
  });

  describe('updateSelf', () => {
    it('should not set bet error in case of not single bet', () => {
      const payload = {bet: {}};
      const type = 'notStakeError';
      bet = {
        error: null,
        type: 'DBL',
        params: {
          error: null,
          errorMsg: ''
        }
      };

      Bet.updateSelf(payload as IBetPayload, type, bet as Bet);

      expect(bet.error).toBeNull();
      expect(bet.params.error).toBeNull();
    });

    it('should not set bet error ', () => {
      const payload = {
        type: 'mid',
        bet: {}
      };
      const type = 'stakeError';
      bet = {
        error: null,
        type: 'DBL',
        params: {
          error: null,
          errorMsg: ''
        },
        stake: {
          max: 1,
          min: 2,
          params: { min: '2.00', max: '1.00' }
        },
        user,
        localeService
      };

      Bet.updateSelf(payload as IBetPayload, type, bet);
      expect(bet.error).toBeNull();
      expect(bet.params.error).toBeNull();
    });

    describe('not single bet errors', () => {
      describe('max stakeError', () => {
        it('should set bet error by bet.stake', () => {
          const payload = {
            type: 'max',
            bet: {}
          };
          const type = 'stakeError';
          bet = {
            error: null,
            type: 'DBL',
            params: {
              error: null,
              errorMsg: ''
            },
            stake: {
              max: 10,
              min: 1,
              params: { min: '1.00', max: '10.00' }
            },
            user,
            localeService
          };

          Bet.updateSelf(payload as IBetPayload, type, bet);
          expect(bet.error).toEqual('STAKE_TOO_HIGH');
          expect(localeService.getString).toHaveBeenCalledWith('bs.maxStake', ['10.00', user.currencySymbol]);
        });

        it('should set bet error by payload.bet.stake', () => {
          const payload = {
            type: 'max',
            bet: { stake: { max: 5, min: 1 }}
          };
          const type = 'stakeError';
          bet = {
            error: null,
            type: 'DBL',
            params: {
              error: null,
              errorMsg: ''
            },
            stake: {
              max: 10,
              min: 1,
              params: { min: '1.00', max: '10.00' }
            },
            user,
            localeService
          };

          Bet.updateSelf(payload as IBetPayload, type, bet);
          expect(bet.error).toEqual('STAKE_TOO_HIGH');
          expect(localeService.getString).toHaveBeenCalledWith('bs.maxStake', [5, user.currencySymbol]);
        });
      });

      describe('min stakeError', () => {
        it('should set bet error by bet.stake', () => {
          const payload = {
            type: 'min',
            bet: {}
          };
          const type = 'stakeError';
          bet = {
            error: null,
            type: 'DBL',
            params: {
              error: null,
              errorMsg: ''
            },
            stake: {
              max: 10,
              min: 1,
              params: { min: '1.00', max: '10.00' }
            },
            user,
            localeService
          };

          Bet.updateSelf(payload as IBetPayload, type, bet);
          expect(bet.params.error).toEqual('MINIMUM_STAKE');
          expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', ['1.00', user.currencySymbol]);
        });

        it('should set bet error by payload.bet.stake', () => {
          const payload = {
            type: 'min',
            bet: { stake: { max: 10, min: 3 }}
          };
          const type = 'stakeError';
          bet = {
            error: null,
            type: 'DBL',
            params: {
              error: null,
              errorMsg: ''
            },
            stake: {
              max: 10,
              min: 1,
              params: { min: '1.00', max: '10.00' }
            },
            user,
            localeService
          };

          Bet.updateSelf(payload as IBetPayload, type, bet);
          expect(bet.params.error).toEqual('MINIMUM_STAKE');
          expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', [3, user.currencySymbol]);
        });
      });
    });

    describe('clearError update case', () => {
      it('should clear outcome errors', () => {
        const payload = {bet: {}};
        const type = 'clearError';
        bet = {
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 1,
            min: 2
          } as BetStake,
          legs: [{
            parts: [{
              outcome: {
                error: 'STAKE_TOO_HIGH',
                errorMsg: 'message',
                handicapErrorMsg: 'some message'
              }
            }, {
              outcome: {
                error: 'STAKE_TOO_HIGH',
                errorMsg: 'message',
                handicapErrorMsg: 'some message'
              }
            }]
          }],
          user,
          localeService
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.legs[0].parts[0].outcome).toEqual({
          error: null,
          errorMsg: null,
          handicapErrorMsg: null
        });
        expect(bet.legs[0].parts[1].outcome).toEqual({
          error: null,
          errorMsg: null,
          handicapErrorMsg: null
        });
      });
    });

    describe('outcome update case', () => {
      it('unsuspend', () => {
        bet = createBet(params);
        Bet.updateOriginalPrices = jasmine.createSpy('updateOriginalPrices');
        Bet.setPriceData = jasmine.createSpy('setPriceData');
        const payload = {
          started: 'Y',
          lp_num: '5',
          lp_den: '1',
          status: 'A',
          bet: {}
        };
        const type = 'outcome';
        bet = {
          type: 'SGL',
          params: {},
          legs: [{
            parts: [{
              outcome: {
                errorMsg: 'OUTCOME_SUSPENDED',
                prices: [{
                  priceNum: '3',
                  priceDen: '2'
                }],
                details: {
                  outcomeStatusCode: 'A',
                  marketStatusCode: 'A',
                  eventStatusCode: 'A',
                  info: {
                    isStarted: true
                  }
                }
              }
            }],
          }],
          pubSubService,
          storeOldPrices: () => {},
          overaskService: {},
          localeService: {
            getString: jasmine.createSpy('getString').and.returnValue('OUTCOME_SUSPENDED')
          }
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(Bet.updateOriginalPrices).toHaveBeenCalled();
        expect(Bet.setPriceData).toHaveBeenCalled();

        expect(bet.legs[0].parts[0].outcome.errorMsg).toEqual(null);
      });

      it('unsuspend when previous error message was not about suspend', () => {
        bet = createBet(params);
        Bet.updateOriginalPrices = jasmine.createSpy('updateOriginalPrices');
        Bet.setPriceData = jasmine.createSpy('setPriceData');
        const payload = {
          started: 'Y',
          lp_num: '5',
          lp_den: '1',
          status: 'A',
          bet: {}
        };
        const type = 'outcome';
        bet = {
          type: 'SGL',
          params: {},
          legs: [{
            parts: [{
              outcome: {
                errorMsg: 'STAKE_TOO_HIGH',
                prices: [{
                  priceNum: '3',
                  priceDen: '2'
                }],
                details: {
                  outcomeStatusCode: 'A',
                  marketStatusCode: 'A',
                  eventStatusCode: 'A',
                  info: {
                    isStarted: true
                  }
                }
              }
            }],
          }],
          pubSubService,
          storeOldPrices: () => {},
          overaskService: {},
          localeService: {
            getString: jasmine.createSpy('getString').and.returnValue('OUTCOME_SUSPENDED')
          }
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(Bet.updateOriginalPrices).toHaveBeenCalled();
        expect(Bet.setPriceData).toHaveBeenCalled();

        expect(bet.legs[0].parts[0].outcome.errorMsg).toEqual('STAKE_TOO_HIGH');
      });
    });

    describe('outcome update case', () => {
      it('reboost', () => {
        bet = createBet(params);
        Bet.updateOriginalPrices = jasmine.createSpy('updateOriginalPrices');
        Bet.setPriceData = jasmine.createSpy('setPriceData');
        const payload = {
          started: 'Y',
          lp_num: '5',
          lp_den: '1',
          status: 'A'
        };
        const type = 'outcome';
        bet = {
          type: 'SGL',
          params: {},
          legs: [{
            parts: [{
              outcome: {
                handicapErrorMsg: 'error',
                prices: [{
                  priceNum: '3',
                  priceDen: '2'
                }],
                details: {
                  outcomeStatusCode: 'A',
                  marketStatusCode: 'A',
                  eventStatusCode: 'A',
                  info: {
                    isStarted: true
                  }
                }
              }
            }],
          }],
          pubSubService,
          storeOldPrices: () => {},
          overaskService: {},
          localeService: {
            getString: jasmine.createSpy('getString')
          }
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(Bet.updateOriginalPrices).toHaveBeenCalled();
        expect(Bet.setPriceData).toHaveBeenCalled();

        expect(bet.legs[0].parts[0].outcome.handicapErrorMsg).toEqual(null);
        expect(bet.pubSubService.publish).toHaveBeenCalledWith('ODDS_BOOST_REBOOST');
      });

      it('should update price in case of placeBEtPriceError', () => {
        bet = createBet(params);
        const payload = {
          placeBet: true,
          lp_num: '3',
          lp_den: '2',
        };
        const type = 'outcome';
        bet = {
          type: 'SGL',
          params: {},
          legs: [{
            parts: [{
              outcome: {
                prices: [{
                  priceNum: '3',
                  priceDen: '2'
                }],
                details: {
                  outcomeStatusCode: 'A',
                  marketStatusCode: 'A',
                  eventStatusCode: 'A',
                  info: {
                    isStarted: true
                  }
                }
              }
            }],
          }],
          pubSubService,
          storeOldPrices: jasmine.createSpy('storeOldPrices'),
          overaskService: {}
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.storeOldPrices).not.toHaveBeenCalled();
        expect(Bet.updateOriginalPrices).toHaveBeenCalled();
        expect(Bet.setPriceData).toHaveBeenCalled();
        expect(bet.pubSubService.publish).toHaveBeenCalledWith('ODDS_BOOST_REBOOST');
      });
    });

    describe('stakeError update case', () => {
      it('should set stake error as true for non max and min type', () => {
        const payload = { type: 'mid', bet: {}};
        const type = 'stakeError';
        bet = {
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 10,
            min: 1,
            params: { min: '1.00', max: '10.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: 'STAKE_TOO_HIGH',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.legs[0].parts[0].outcome.stakeError).toBeTruthy();
      });

      it('should set stake error by bet.stake for min payload type', () => {
        const payload = { type: 'min', bet: {}};
        const type = 'stakeError';
        bet = {
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 10,
            min: 1,
            params: { min: '1.00', max: '10.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: '',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.legs[0].parts[0].outcome.error).toEqual('STAKE_TOO_LOW');
        expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', ['1.00', user.currencySymbol]);
      });

      it('should set stake error by payload.bet.stake for min payload type', () => {
        const payload = {
          type: 'min',
          bet: {
          stake: { max: 10, min: 3 },
            combiName: 'SCORECAST'
          }
        };
        const type = 'stakeError';
        bet = {
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 10,
            min: 1,
            params: { min: '1.00', max: '10.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: '',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.params.error).toEqual('STAKE_TOO_LOW');
        expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', [3, user.currencySymbol]);
      });

      it('should set stake error for max payload type with scorecast combi type', () => {
        const payload = { type: 'max', bet: {} };
        const type = 'stakeError';
        bet = {
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 1,
            min: 2,
            params: { min: '2.00', max: '1.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: 'STAKE_TOO_MIN',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        payload.bet['combiName'] = 'SCORECAST';
        Bet.updateSelf(payload as IBetPayload, type, bet);
        expect(bet.params.error).toEqual('STAKE_TOO_HIGH');
        expect(bet.error).toBeNull();
      });

      it('should set stake error by bet.stake for bet with default max type', () => {
        const payload = { type: 'max', bet: {} };
        const type = 'stakeError';
        bet = {
          betComplexName: true,
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 10,
            min: 1,
            params: { min: '1.00', max: '10.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: 'STAKE_TOO_MIN',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        bet['betComplexName'] = false;
        payload.bet['combiName'] = 'NOT_SCORECAST';
        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.error).toBeNull();
        expect(bet.params.error).toBeNull();
        expect(bet.legs[0].parts[0].outcome.error).toEqual('STAKE_TOO_HIGH');
        expect(localeService.getString).toHaveBeenCalledWith('bs.maxStake', ['10.00', user.currencySymbol]);
      });

      it('should set stake error by payload.bet.stake for bet with default max type', () => {
        const payload = { type: 'max', bet: { stake: { min: 1, max: 5 }} };
        const type = 'stakeError';
        bet = {
          betComplexName: true,
          error: null,
          type: 'SGL',
          params: {
            error: null,
            errorMsg: '',
            errs: undefined
          },
          stake: {
            max: 10,
            min: 1,
            params: { min: '1.00', max: '10.00' }
          },
          legs: [{
            parts: [{
              outcome: {
                error: 'STAKE_TOO_MIN',
                errorMsg: 'message',
                handicapErrorMsg: 'some message',
                stakeError: false
              }
            }]
          }],
          user,
          localeService
        };

        bet['betComplexName'] = false;
        payload.bet['combiName'] = 'NOT_SCORECAST';
        Bet.updateSelf(payload as IBetPayload, type, bet);

        expect(bet.error).toBeNull();
        expect(bet.params.error).toBeNull();
        expect(bet.legs[0].parts[0].outcome.error).toEqual('STAKE_TOO_HIGH');
        expect(localeService.getString).toHaveBeenCalledWith('bs.maxStake', [5, user.currencySymbol]);
      });
    });

    it('should update complex bet if outcome changed', () => {
      localeService.getString.and.callFake(n => n === 'bs.forecast' ? 'Forecast' : '');

      bet = createBet(Object.assign({}, params, {
        type: 'SGL',
        lines: 1,
        allLegs: [{
          docId: '1',
          parts: [{
            outcome: { id: '111' }
          }, {
            outcome: { id: '222', prices: [], details: {} }
          }],
          combi: 'FORECAST'
        }],
        docIds: ['1']
      }));

      const payload: any = {
        unique_id: '222_Ad34RFgyhg1',
        status: 'S',
        bet: {}
      };

      bet.update(payload, 'outcome');

      expect(localeService.getString).toHaveBeenCalledWith('bs.OUTCOME_SUSPENDED');
    });

    it('should update complex bet errs when forecast is not available', () => {
      localeService.getString.and.callFake(n => n === 'bs.forecast' ? 'Forecast' : '');

      bet = createBet(Object.assign({}, params, {
        type: 'SGL',
        lines: 1,
        allLegs: [{
          docId: '1',
          parts: [{
            outcome: { id: '111', prices: [], details: {}, tc_avail: 'N' }
          }, {
            outcome: { id: '222', prices: [], details: {}, tc_avail: 'N' }
          }],
          selection: {
            isFCTC: true,
            combi: 'FORECAST'
          }
        }],
        docIds: ['1']
      }));

      const payload: any = {
        unique_id: '222_Ad34RFgyhg1',
        status: 'A',
        bet: {},
        fc_avail: 'N',
        tc_avail: 'N'
      };

      bet.update(payload, 'outcome');
      expect(bet.params.errs).toBeDefined();
    });
    it('should update complex bet errs when tricast is not available', () => {
      localeService.getString.and.callFake(n => n === 'bs.forecast' ? 'Forecast' : '');
      
      bet = createBet(Object.assign({}, params, {
        type: 'SGL',
        lines: 1,
        allLegs: [{
          docId: '1',
          parts: [{
            outcome: { id: '111', prices: [], details: {} }
          }, {
            outcome: { id: '222', prices: [], details: {} }
          }],
          selection: {
            isFCTC: true,
            combi: 'TRICAST'
          }
        }],
        docIds: ['1']
      }));
      bet.params.errs = [{}];
      const payload: any = {
        unique_id: '222_Ad34RFgyhg1',
        status: 'A',
        bet: {},
        fc_avail: 'N',
        tc_avail: 'N'
      };
      bet.updateSelf = jasmine.createSpy('updateSelf').and.returnValue({});
      bet.update(payload, 'outcome');
      expect(bet.params.errs).toBeDefined();
    });
    it('should not remove bet errors if one of the outcomes has error', () => {
      bet = createBet(Object.assign({}, params, {
        type: 'SGL',
        lines: 1,
        allLegs: [{
          docId: '1',
          parts: [{
            outcome: { id: '111', prices: [], details: {} }
          }, {
            outcome: { id: '222', prices: [], details: {}, errorMsg: 'Err' }
          }]
        }],
        docIds: ['1'],
        errs: [{ error: 'Err' }]
      }));

      bet.update({}, 'outcome');

      expect(bet.params.errs).toBeDefined();
    });

    it('should updateSelf (update handicap)', () => {
      const payload = {
        raw_hcap: true,
        hcap_values: {
          H: '+2.0'
        }
      };
      const type = 'outcome';

      bet = {
        makeHandicapChangeMsg: jasmine.createSpy('makeHandicapChangeMsg'),
        type: 'SGL',
        params: {},
        legs: [{
          selection: {
            legParts: [{
              range: {
                high: '10',
                low: '7'
              }
            }]
          },
          parts: [{
            outcome: {
              name: '(name)',
              outcomeMeaningMinorCode: 'L',
              prices: [
                {
                  handicapValueDec: '2'
                }
              ],
              details: {}
            }
          }]
        }],
        overaskService: overaskService,
        localeService: localeService,
        betslipFilters: betslipFilters
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.handicapError).toEqual('HANDICAP_CHANGED');
    });

    it('should updateSelf (update handicap)', () => {
      const payload = {
        raw_hcap: true,
        hcap_values: {
          H: '+2.0'
        }
      };
      const type = 'outcome';

      bet = {
        makeHandicapChangeMsg: jasmine.createSpy('makeHandicapChangeMsg'),
        type: 'SGL',
        params: {},
        legs: [{
          selection: {
            legParts: [{
              range: {
                high: '10',
                low: '7'
              }
            }]
          },
          parts: [{
            outcome: {
              error: 'PRICE_CHANGED',
              name: '(name)',
              outcomeMeaningMinorCode: 'L',
              prices: [
                {
                  handicapValueDec: '2'
                }
              ],
              details: {}
            }
          }]
        }],
        overaskService: overaskService,
        localeService: localeService,
        betslipFilters: betslipFilters
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.error).toEqual(null);
      expect(bet.legs[0].parts[0].outcome.handicapError).toEqual('HANDICAP_CHANGED');
    });

    it('should updateSelf (outcome eventStatusCode S)', () => {
      const payload = {};
      const type = 'outcome';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              prices: [],
              details: {
                eventStatusCode: 'S'
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.error).toEqual('SELECTION_SUSPENDED');
    });

    it('should updateSelf (outcome marketStatusCode S)', () => {
      const payload = {};
      const type = 'outcome';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              prices: [],
              details: {
                marketStatusCode: 'S'
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(localeService.getString).toHaveBeenCalledWith('bs.MARKET_SUSPENDED');
    });

    it('should updateSelf (market, S)', () => {
      const payload = {
        status: 'S'
      };
      const type = 'market';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {}
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome).toEqual(jasmine.objectContaining({
        details: {
          marketStatusCode: 'S'
        },
        error: 'MARKET_SUSPENDED'
      }));
    });

    it('should updateSelf (market, eventStatusCode = S)', () => {
      const payload = {};
      const type = 'market';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                marketStatusCode: 'P',
                eventStatusCode: 'S'
              }
            }
          }]
        }],
        localeService: localeService
      };
      localeService.getString.and.returnValue('testError');

      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome).toEqual(jasmine.objectContaining({
        details: {
          marketStatusCode: 'A',
          eventStatusCode: 'S'
        },
        errorMsg: 'testError'
      }));
      expect(localeService.getString).toHaveBeenCalledWith('bs.SELECTION_SUSPENDED');
    });

    it('should updateSelf (market, market and outcome are unsuspended)', () => {
      const payload = {};
      const type = 'market';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                marketStatusCode: 'P',
                eventStatusCode: 'M',
                outcomeStatusCode: 'S'
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(localeService.getString).toHaveBeenCalledWith('bs.OUTCOME_SUSPENDED');
    });

    it('should updateSelf (market not suspended)', () => {
      const payload = {};
      const type = 'market';

      bet = {
        type: 'SGL',
        params: { errs: [{ live: 'error' }] },
        legs: [{
          parts: [{
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test',
              details: {
                marketStatusCode: 'P',
                eventStatusCode: 'M',
                outcomeStatusCode: 'A'
              }
            }
          }, {
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test'
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome).toEqual(jasmine.objectContaining({
        error: null,
        errorMsg: null,
        handicapErrorMsg: null
      }));
      expect(bet.legs[0].parts[1].outcome).toEqual({
        error: null,
        errorMsg: null,
        handicapErrorMsg: null
      });
      expect(bet.params.err).not.toBeDefined();
    });
    it('should updateSelf (market not suspended) and FC/TC suspended', () => {
      const payload = {};
      const type = 'market';

      bet = {
        type: 'SGL',
        params: { },
        legs: [{
          parts: [{
            outcome: {
              details: {
                marketStatusCode: 'P',
                eventStatusCode: 'M',
                outcomeStatusCode: 'A'
              },
              tc_avail: 'N'
            }
          }, {
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test'
            }
          }],
          selection: {
            isFCTC: true
          }
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
    });

    it('should updateSelf (event payload.started)', () => {
      const payload = {
        started: 'Y'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                info: {}
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.details.info.isStarted).toEqual(true);
      expect(localeService.getString).toHaveBeenCalledWith('bs.EVENT_STARTED');
    });

    it('should updateSelf (event SELECTION_SUSPENDED)', () => {
      const payload = {
        started: 'S',
        status: 'S'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                info: {}
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(localeService.getString).toHaveBeenCalledWith('bs.SELECTION_SUSPENDED');
    });

    it('should updateSelf (event MARKET_SUSPENDED)', () => {
      const payload = {
        started: 'Y',
        status: 'C'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                isMarketBetInRun: true,
                marketStatusCode: 'S',
                info: {}
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.details.eventStatusCode).toEqual('A');
      expect(bet.legs[0].parts[0].outcome.error).toEqual('MARKET_SUSPENDED');
    });

    it('should updateSelf (event OUTCOME_SUSPENDED)', () => {
      const payload = {
        started: 'Y',
        status: 'C'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {
                isMarketBetInRun: true,
                outcomeStatusCode: 'S',
                info: {}
              }
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.error).toEqual('OUTCOME_SUSPENDED');
    });

    it('should updateSelf (event OUTCOME_SUSPENDED)', () => {
      const payload = {
        started: 'Y',
        status: 'C'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: { errs: [{ live: 'error' }] },
        legs: [{
          parts: [{
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test',
              details: {
                isMarketBetInRun: true,
                info: {}
              }
            }
          }, {
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test'
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome).toEqual(jasmine.objectContaining({
        error: null,
        errorMsg: null,
        handicapErrorMsg: null
      }));
      expect(bet.legs[0].parts[1].outcome).toEqual({
        error: null,
        errorMsg: null,
        handicapErrorMsg: null
      });
      expect(bet.params.err).not.toBeDefined();
    });

    it('should updateSelf (event update) when FC/TC is suspended', () => {
      const payload = {
        started: 'Y',
        status: 'C'
      };
      const type = 'event';

      bet = {
        type: 'SGL',
        params: { errs: [{ live: 'error' }] },
        legs: [{
          parts: [{
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test',
              details: {
                isMarketBetInRun: true,
                info: {}
              },
              tc_avail: 'N'
            }
          }, {
            outcome: {
              error: 'error',
              errorMsg: 'errorMsg',
              handicapErrorMsg: 'test'
            }
          }],
          selection: {
            isFCTC: true
          }
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.params.err).not.toBeDefined();
    });

    it('should updateSelf (removed)', () => {
      const payload = {
        name: 'test'
      };
      const type = 'removed';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              details: {}
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(localeService.getString).toHaveBeenCalledWith('bs.SELECTION_REMOVED', ['test']);
    });

    it('should updateSelf (noLiveServ)', () => {
      const payload = {
        name: 'test',
        lp_num: '7'
      };
      const type = 'noLiveServ';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              prices: [{
                priceNum: '12'
              }],
              details: {}
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.error).toEqual('PRICE_CHANGED');
      expect(bet.legs[0].parts[0].outcome.priceChange).toEqual(true);
    });

    it('should updateSelf (noLiveServ)', () => {
      const payload = {
        name: 'test',
        status: 'S'
      };
      const type = 'noLiveServ';

      bet = {
        type: 'SGL',
        params: {},
        legs: [{
          parts: [{
            outcome: {
              prices: [],
              details: {}
            }
          }]
        }],
        localeService: localeService
      };
      Bet.updateSelf(<any>payload, type, <any>bet);
      expect(bet.legs[0].parts[0].outcome.error).toEqual('PRICE_CHANGED');
      expect(bet.legs[0].parts[0].outcome.disabled).toEqual(true);
    });
  });
  it('should updateSelf (noLiveServ)', () => {
    const payload = {
      name: 'test',
      lp_num: '7'
    };
    const type = 'noLiveServ';

    bet = {
      type: 'SGL',
      params: {},
      legs: [{
        parts: [{
          outcome: {
            prices: [{
              priceNum: '12'
            }],
            details: {},
            tc_avail: 'N'
          }
        }],
        selection: {
          isFCTC: true
        }
      }],
      localeService: localeService
    };
    Bet.updateSelf(<any>payload, type, <any>bet);
    expect(bet.legs[0].parts[0].outcome.error).toEqual('PRICE_CHANGED');
    expect(bet.legs[0].parts[0].outcome.priceChange).toEqual(true);
  });
  describe('clone', () => {
    it('should clone', () => {
      bet = createBet(params);
      expect(bet.clone()).toEqual(jasmine.any(Object));
    });

    it('should clone(stake)', () => {
      const clone = {};
      bet.params.stake = {
        clone: jasmine.createSpy('clone').and.returnValue(clone)
      };
      expect(bet.clone() instanceof Bet).toEqual(true);
      expect(bet.params.stake).toEqual(clone);
    });
  });

  it('getOddsBoostObj no enhancedOdds', () => {
    bet = createBet(params);

    bet.oddsBoost = {
      id: '123',
      enhancedOddsPriceDen: '2',
      enhancedOddsPriceNum: '1'
    } as any;

    expect(bet['getOddsBoostObj']()).toEqual({ freebet: { id: '123', enhancedOdds: [{
      priceNum: '1',
      priceDen: '2',
      documentId: '1'
    }] }} as any);
  });

  describe('getInfo', () => {
    const betInfo = {
      params: {
        type: 'TMP'
      },
      price: {
        type: 'LP',
        props: {
          priceNum: '1',
          priceDen: '2'
        }
      },
      legs: [{
        parts: [{
          outcome: {
            details: {
              eachWayPlaces:'2',
              previousOfferedPlaces: '3',
              info: {
                sport: 'sport',
                className: 'className',
                event: '12345',
                time: 123
              },
              typeId: 'id'
            },
            id: '123',
            outcomeMeaningMajorCode: 'FS'
          }
        }, {
          outcome: {
            details: {
              info: {
                sport: 'sport',
                className: 'className',
                event: '12345',
                time: 123
              },
              typeId: 'id'
            },
            id: '123',
            outcomeMeaningMajorCode: 'CS'
          }
        }],
        combi: 'SCORECAST',
        price: {
          props: {
            priceNum: '1',
            priceDen: '1'
          }
        }
      }],
      getEventLiveServChannels: jasmine.createSpy(),
      getSelectionIds: jasmine.createSpy(),
      fracToDec: {
        getDecimal: jasmine.createSpy().and.returnValue(1)
      },
      isCS: true,
      localeService: {
        getString: jasmine.createSpy()
      }
    } as any;
    it('should set priceDec to price obj to scorecast outcome', () => {
      const res = Bet.getInfo(betInfo as Partial<IBetInfo>);
      expect(res.price).toEqual(jasmine.objectContaining({
        priceDec: 1,
        priceNum: '1',
        priceDen: '1'
      } as any));
    });
    it('should set priceDec to price obj to scorecast outcome', () => {
      const res = Bet.getInfo(betInfo as Partial<IBetInfo>);
      expect(res.price).toEqual(jasmine.objectContaining({
        priceDec: 1,
        priceNum: '1',
        priceDen: '1'
      } as any));
    });
  });

  it('betComplexName', () => {
    localeService.getString.and.returnValue('');
    bet = createBet(params);

    Object.defineProperty(bet, 'legs', { value: [{ combi: 'FORECAST' }], configurable: true });
    bet.params.lines = 1;
    expect(bet.betComplexName).toEqual(jasmine.any(String));
    bet.params.lines = 2;
    expect(bet.betComplexName).toEqual(jasmine.any(String));
    bet.params.lines = 3;
    expect(bet.betComplexName).toEqual(jasmine.any(String));

    Object.defineProperty(bet, 'legs', { value: [{ combi: 'TRICAST' }] });
    bet.params.lines = 1;
    expect(bet.betComplexName).toEqual(jasmine.any(String));
    bet.params.lines = 3;
    expect(bet.betComplexName).toEqual(jasmine.any(String));

    expect(localeService.getString).toHaveBeenCalledTimes(6);
  });

  describe('getInfo (forecast/tricast)', () => {
    let betParams;

    beforeEach(() => {
      betParams = Object.assign({}, params, {
        type: 'SGL',
        lines: 1,
        allLegs: [{
          docId: '1',
          selection: { price: { type: 'DIVIDEND' } },
          parts: [{
            outcome: { details: { info: {} } }
          }]
        }],
        docIds: ['1']
      });
    });

    it('shoud return info', () => {
      expect(
        Bet.getInfo( createBet(betParams) )
      ).toEqual(jasmine.any(Object));
    });

    it('shoud return info (lines > 1)', () => {
      betParams.lines = 2;
      expect(
        Bet.getInfo( createBet(betParams) )
      ).toEqual(jasmine.any(Object));
    });

    it('shoud return info with error', () => {
      betParams.allLegs[0].parts[0].outcome.error = 'ERR';
      betParams.allLegs[0].parts[0].outcome.errorMsg = 'Error';
      expect(
        Bet.getInfo( createBet(betParams) )
      ).toEqual(jasmine.any(Object));
    });
  });

  describe('betComplexName', () => {
    beforeEach(() => {
      bet = createBet(params);
      localeService.getString.and.returnValue('test');
    });

    it('should betComplexName (FORECAST 1 line)', () => {
      bet.params.allLegs[0].combi = 'FORECAST';

      expect(bet.betComplexName).toEqual('test');
      expect(localeService.getString).toHaveBeenCalledWith('bs.forecast');
    });

    it('should betComplexName (FORECAST 2 lines)', () => {
      bet.params.allLegs[0].combi = 'FORECAST';
      bet.params.lines = 2;

      expect(bet.betComplexName).toEqual('test 2');
      expect(localeService.getString).toHaveBeenCalledWith('bs.reverseForecast');
    });

    it('should betComplexName (FORECAST 4 lines)', () => {
      bet.params.allLegs[0].combi = 'FORECAST';
      bet.params.lines = 4;

      expect(bet.betComplexName).toEqual('test 4');
      expect(localeService.getString).toHaveBeenCalledWith('bs.combinationForecast');
    });

    it('should betComplexName (TRICAST 1 line)', () => {
      bet.params.allLegs[0].combi = 'TRICAST';

      expect(bet.betComplexName).toEqual('test');
      expect(localeService.getString).toHaveBeenCalledWith('bs.tricast');
    });

    it('should betComplexName (TRICAST 2 lines)', () => {
      bet.params.lines = 2;
      bet.params.allLegs[0].combi = 'TRICAST';

      expect(bet.betComplexName).toEqual('test 2');
      expect(localeService.getString).toHaveBeenCalledWith('bs.combinationTricast');
    });
  });

  describe('clearErr', () => {
    beforeEach(() => {
      bet = createBet(params);
      bet.params.allLegs[0].parts = [{
        outcome: {
          errorMsg: 'string',
          error: 'string',
          handicapErrorMsg: 'string'
        }
      }];
    });

    it('should clearErr', () => {
      bet.type = 'SGL';
      bet.clearErr();
      expect(bet.legs[0].parts[0].outcome).toEqual(jasmine.objectContaining({
        errorMsg: null,
        error: null,
        handicapErrorMsg: null
      }));
    });

    it('should clearErr (!SGL)', () => {
      bet.type = 'DBL';
      bet.clearErr();
      expect(bet.legs[0].parts[0].outcome).not.toEqual(jasmine.objectContaining({
        errorMsg: null,
        error: null,
        handicapErrorMsg: null
      }));
    });
  });

  it('should set/get price', () => {
    bet = createBet(params);
    bet.params.allLegs[0].selection = {
      price: {
        priceDen: '2',
        priceNum: '5'
      }
    };
    expect(bet.price).toEqual(jasmine.objectContaining({
      priceDen: '2',
      priceNum: '5'
    }));

    bet.price = {
      priceDen: '1',
      priceNum: '4'
    };

    expect(bet.price).toEqual(jasmine.objectContaining({
      priceDen: '1',
      priceNum: '4'
    }));
  });

  it('should clearUserData', () => {
    bet.clearUserData();
    expect(bet.isEachWay).toEqual(false);
    expect(bet._stake.perLine).toEqual('');
  });

  describe('getEventLiveServChannels', () => {
    it('should getEventLiveServChannels', () => {
      params.allLegs = [
        {
          docId: '1',
          parts: [
            {
              outcome: {
                details: {
                  marketliveServChannels: '10',
                  eventliveServChannels: '100',
                  outcomeliveServChannels: '200'
                }
              }
            }, {
              outcome: {
                details: {
                  marketliveServChannels: '11',
                  eventliveServChannels: '101',
                  outcomeliveServChannels: '201'
                }
              }
            }
          ]
        },
        {
          docId: '2',
          parts: [
            {
              outcome: {
                details: {
                  marketliveServChannels: '12',
                  eventliveServChannels: '102',
                  outcomeliveServChannels: '202'
                }
              }
            },
            {
              outcome: {
                details: {
                  marketliveServChannels: '13',
                  eventliveServChannels: '103',
                  outcomeliveServChannels: '203'
                }
              }
            }
          ]
        }
      ];
      params.legIds = ['1', '2'];
      bet = createBet(params);

      expect(bet.getEventLiveServChannels()).toEqual(jasmine.objectContaining({
        marketliveServChannels: ['10', '11', '12', '13'],
        eventliveServChannels: ['100', '101', '102', '103'],
        outcomeliveServChannels: ['200', '201', '202', '203']
      }));
    });

    it('should getEventLiveServChannels (no details)', () => {
      params.allLegs = [{
        docId: '1',
        parts: [
          {
            outcome: {
              details: {
                marketliveServChannels: '10',
                eventliveServChannels: '100',
                outcomeliveServChannels: '200'
              }
            }
          },
          { outcome: {} }
        ]
      }];
      params.legIds = ['1'];
      bet = createBet(params);
      expect(bet.getEventLiveServChannels()).toEqual(undefined);
    });
  });

  describe('getSelectionIds', () => {
    it('should getSelectionIds', () => {
      params.allLegs = [
        {
          docId: '1',
          parts: [
            {
              outcome: {
                details: {
                  eventId: '10',
                  marketId: '100',
                  outcomeId: '200',
                  classId: '300',
                  categoryId: '400',
                  typeId: '500'
                }
              }
            }, {
              outcome: {
                details: {
                  eventId: '11',
                  marketId: '12',
                  outcomeId: '13',
                  classId: '14',
                  categoryId: '15',
                  typeId: '16'
                }
              }
            }
          ]
        }
      ];
      params.legIds = ['1'];
      bet = createBet(params);
      expect(bet.getSelectionIds()).toEqual(jasmine.objectContaining({
        eventIds: [ '10', '11' ],
        marketIds: [ '10', '12' ],
        outcomeIds: [ '200', '13' ],
        classIds: [ '300', '14' ],
        categoriesIds: [ '400', '15' ],
        typeIds: [ '500', '16' ]
      }));
    });

    it('should getSelectionIds (no details)', () => {
      params.allLegs = [
        {
          docId: '1',
          parts: [
            {
              outcome: {
                details: {
                  eventId: '10',
                  marketId: '100',
                  outcomeId: '200',
                  classId: '300',
                  categoryId: '400',
                  typeId: '500'
                }
              }
            }, {
              outcome: {}
            }
          ]
        }
      ];
      params.legIds = ['1'];
      bet = createBet(params);
      expect(bet.getSelectionIds()).toEqual(undefined);
    });
  });

  describe('getInfo', () => {
    describe('SGL case', () => {
      beforeEach(() => {
        params.allLegs = [
          {
            selection: {
              price: {
                type: 'test'
              },
            },
            price: {
              type: 'test'
            },
            docId: '1',
            parts: [
              {
                outcome: {
                  id: '5',
                  prices: [],
                  details: {
                    isMarketBetInRun: true,
                    info: {
                      sportId: '10'
                    },
                    markets: [
                      {
                          drilldownTagNames: 'EPR'
                      }
                    ]
                  }
                }
              }
            ]
          }
        ];
        params.lines = 3;
        params.type = 'SGL';
      });

      it('should get info (SGL) with e/w not available if no isEachWayAvailable flag for Bet', () => {
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          Bet: jasmine.any(Object),
          stakeMultiplier: 3,
          isMarketBetInRun: true,
          outcomeIds: ['5'],
          isEachWayAvailable: false
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          isEachWayAvailable: true
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome with eachway and previous offered places with direct supplies', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.details.eachWayPlaces = '2' as any;
        params.allLegs[0].parts[0].outcome.details.previousOfferedPlaces = '3' as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          eachWayPlaces: '2'
        }));
        expect(bet.info()).toEqual(jasmine.objectContaining({
          previousOfferedPlaces: '3'
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome with eachway and previous offered places with direct supplies invalid', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.details.eachWayPlaces = undefined as any;
        params.allLegs[0].parts[0].outcome.details.previousOfferedPlaces = undefined as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          eachWayPlaces: undefined
        }));
        expect(bet.info()).toEqual(jasmine.objectContaining({
          previousOfferedPlaces: undefined
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome with eachway and previous offered places  with direct market supplies', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.details.markets = [{
          eachWayPlaces : '2',
          referenceEachWayTerms : {
            places : '3'
          }
        }]  as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          eachWayPlaces: '2'
        }));
        expect(bet.info()).toEqual(jasmine.objectContaining({
          previousOfferedPlaces: '3'
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome with eachway and previous offered places  with direct market supplies and invalid referenceEachwayterms', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.details.markets = [{
          eachWayPlaces : '2',
          referenceEachWayTerms : undefined
        }]  as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          eachWayPlaces: '2'
        }));
        expect(bet.info()).toEqual(jasmine.objectContaining({
          previousOfferedPlaces: undefined
        }));
      });
      it('should get info (SGL) with e/w available if isEachWayAvailable flag is Y for Bet,' +
        'and Each Way is available for outcome with eachway and previous offered places  with direct market supplies invalid', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.details.markets = undefined  as any;
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          eachWayPlaces: undefined
        }));
        expect(bet.info()).toEqual(jasmine.objectContaining({
          previousOfferedPlaces: undefined
        }));
      });
      it('should get info (SGL) with e/w not available if Each Way is available for Bet and outcome' +
        'but selection is first unnamed favorite', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.outcomeMeaningMinorCode = '1';
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          isEachWayAvailable: false
        }));
      });
      it('should get info (SGL) with e/w not available if Each Way is available for Bet and outcome' +
        'but selection is second unnamed favorite', () => {
        params.eachWayAvailable = 'Y';
        params.allLegs[0].parts[0].outcome.details.eachwayCheckbox = {} as any;
        params.allLegs[0].parts[0].outcome.outcomeMeaningMinorCode = '2';
        bet = createBet(params);
        expect(bet.info()).toEqual(jasmine.objectContaining({
          isEachWayAvailable: false
        }));
      });
    });

    it('should get info (SGL SCORECAST)', () => {
      params.type = 'SGL';
      params.allLegs = [
        {
          price: {
            type: 'SP',
            props: {}
          },
          docId: '1',
          combi: 'SCORECAST',
          selection: {
            price: {
              type: 'SP'
            },
          },
          parts: [
            {
              outcome: {
                outcomeMeaningMajorCode: 'CS',
                details: {
                  info: {
                    className: 'test',
                    sport: 'tennis'
                  }
                }
              }
            },
            {
              outcome: {
                outcomeMeaningMajorCode: 'OS',
                details: {
                  info: {
                    className: 'test'
                  }
                }
              }
            }
          ]
        }
      ];
      bet = createBet(params);
      expect(bet.info()).toEqual(jasmine.objectContaining({
        className: 'test',
        isSP: false,
        combiName: 'SCORECAST',
        sport: 'tennis'
      }));
    });

    it('should get info (SGL DIVIDEND)', () => {
      params.allLegs = [
        {
          combi: 'FORECAST',
          price: {
            type: 'DIVIDEND'
          },
          selection: {
            price: {
              type: 'DIVIDEND'
            },
          },
          docId: '1',
          parts: [
            {
              outcome: {
                details: {
                  info: {
                    time: '2020-10-10 10:10:10'
                  }
                }
              }
            }
          ]
        }
      ];
      params.type = 'SGL';

      bet = createBet(params);
      expect(bet.info()).toEqual(jasmine.objectContaining({
        combiType: 'FORECAST',
        isSP: true
      }));
    });

    it('should get info (DBL)', () => {
      params.type = 'DBL';
      params.allLegs = [
        {
          docId: '1',
          price: {
            type: 'test'
          },
          parts: [
            {
              outcome: {
                prices: [
                  {}
                ],
                details: {
                  eachwayCheckbox: {
                    eachWayFactorDen: '1',
                    eachWayFactorNum: '2'
                  },
                  marketliveServChannels: '10',
                  eventliveServChannels: '100',
                  outcomeliveServChannels: '200'
                }
              }
            },
            { outcome: {} }
          ]
        }
      ];
      bet = createBet(params);
      expect(bet.info()).toEqual(jasmine.objectContaining({
        outcomes: [
          jasmine.objectContaining({
            price: {
              priceType: 'test'
            },
            isEachWayAvailable: true
          })
        ],
        isSP: false
      }));
    });
  });

  describe('storeOldPrices', () => {
    it('should storeOldPrices (isPriceChangeDown)', () => {
      let priceMock = 2;
      const outcome = {
        prices: [
          {
            priceNum: '1',
            priceDen: '2'
          }
        ]
      };
      const payload = {
        lp_num: '10',
        lp_den: '11'
      };
      fracToDec.getDecimal.and.callFake(() => {
        priceMock--;
        return priceMock;
      });

      bet = createBet(params);
      bet.storeOldPrices(outcome, payload);

      expect(outcome['oldModifiedPrice']).toEqual(jasmine.objectContaining({
        priceNum: '1',
        priceDen: '2',
        isPriceChangeUp: false,
        isPriceChangeDown: true
      }));
    });

    it('should storeOldPrices (isPriceChangeUp)', () => {
      let priceMock = 2;
      const outcome = {
        prices: [
          {
            priceNum: '1',
            priceDen: '2'
          }
        ]
      };
      const payload = {
        lp_num: '10',
        lp_den: '11'
      };
      fracToDec.getDecimal.and.callFake(() => {
        priceMock++;
        return priceMock;
      });
      bet = createBet(params);
      bet.storeOldPrices(outcome, payload);

      expect(outcome['oldModifiedPrice']).toEqual(jasmine.objectContaining({
        priceNum: '1',
        priceDen: '2',
        isPriceChangeUp: true,
        isPriceChangeDown: false
      }));
    });
  });

  describe('makeHandicapChangeMsg', () => {
    it('should makeHandicapChangeMsg', () => {
      const payload = {};
      const outcome = {
        prices: [{
          handicapValueDec: '1',
          type: 'SP'
        }]
      };
      const handicapValue = '12';
      bet = createBet(params);
      betslipFilters.handicapValueFilter.and.returnValue('+1');
      localeService.getString.and.returnValue('test');
      expect(bet.makeHandicapChangeMsg(payload, outcome, handicapValue)).toEqual('test');
    });

    it('should makeHandicapChangeMsg (payload.errorMsg)', () => {
      const payload = {
        errorMsg: 'error'
      };
      const outcome = {};
      const handicapValue = '12';
      bet = createBet(params);
      expect(bet.makeHandicapChangeMsg(payload, outcome, handicapValue)).toEqual('error');
    });
  });

  it('should get doc', () => {
    const freeBetDoc = { id: '10' };
    bet = createBet(params);
    bet.stake.doc = jasmine.createSpy('doc');
    freeBetService.construct.and.returnValue({
      doc: jasmine.createSpy('doc').and.returnValue(freeBetDoc),
      id: '10'
    });
    bet.freeBet = {};

    expect(bet.doc()).toEqual(jasmine.objectContaining(freeBetDoc));
  });

  it('should updateHandicap', () => {
    const payload = {};
    const outcome = {
      name: 'test',
      prices: [
        {
          handicapValueDec: '1',
          rawHandicapValue: '3'
        }
      ]
    };
    const leg = {
      parts: [
        {
          range: {
            high: '10',
            low: '5'
          }
        }
      ],
      selection: {
        legParts: [
          {
            range: {
              high: '10',
              low: '5'
            }
          }
        ]
      }
    };
    const handicapValue = null;
    bet = createBet(params);
    bet.updateHandicap(leg, outcome, payload, handicapValue);

    expect(outcome.prices[0]).toEqual(jasmine.objectContaining({
      handicapValueDec: '1',
      rawHandicapValue: '3'
    }));
  });

  describe('setBetTypeInfo', () => {
    beforeEach(() => {
      localeService.getString.and.callFake(v => v);
    });

    it('acca', () => {
      bet = createBet(Object.assign(params, { type: 'ACC4' }));
      expect(bet.typeInfo).toBe('bs.ACC_info');
    });

    it('ss/ds', () => {
      bet = createBet(Object.assign(params, { type: 'SS' }));
      expect(bet.typeInfo).toBe('bs.SSDS_info');
    });

    it('multiple', () => {
      bet = createBet(Object.assign(params, { type: 'YAN' }));
      expect(bet.typeInfo).toBe('bs.YAN_info');
    });

    it('not found', () => {
      localeService.getString.and.callFake(() => 'KEY_NOT_FOUND');
      bet = createBet(Object.assign(params, { type: 'FGL' }));
      expect(bet.typeInfo).toBe('');
    });
  });
  describe('getOddsBoostObj oddsBoost', () => {
    it('getOddsBoostObj', () => {
      bet = createBet(params);

      bet.legs = [{
        docId: '1',
        winPlace: 'WIN'
      }] as any;
      bet.oddsBoost = {
        id: '123',
        enhancedOdds: [{ priceNum: '1', priceDen: '2', documentId: '1' }]
      } as any;

      expect(bet['getOddsBoostObj']()).toEqual({ freebet: { id: '123', enhancedOdds: [{ priceNum: '1', priceDen: '2', documentId: '1' }] } } as any);
    });

    it('getOddsBoostObj winEachway', () => {
      bet = createBet(params);
      bet.legs = [{
        docId: '2',
        winPlace: 'EACH_WAY'
      }] as any;
      bet.oddsBoost = {
        id: '123',
        enhancedOdds: [{ priceNum: '1', priceDen: '2', documentId: '2' }]
      } as any;
      expect(bet['getOddsBoostObj']()).toEqual({ freebet: { id: '123', enhancedOdds: [{ priceNum: '1', priceDen: '2',documentId: '2' }] }} as any);
    });
  })
  describe('getMultipleOddsBoostObj', () => {
    it('when place bet with WinOrEACH_WAY condition', () => {
      bet = createBet(params);
      bet.legs[0].winPlace = 'EACH_WAY';
      bet.oddsBoost = { enhancedOdds: [{ priceNum: '1', priceDen: '2', documentId: '1' }] };
      const result = bet.getMultipleOddsBoostObj();
      expect(result).toBe(bet.oddsBoost.enhancedOdds);
    });

    it('when place bet not with WinOrEACH_WAY condition', () => {
      bet = createBet(params);
      bet.legs[0].winPlace = 'SGL';
      bet.oddsBoost = { enhancedOdds: [{ priceNum: '1', priceDen: '2', documentId: '2' }] };
      const result = bet.getMultipleOddsBoostObj();
      expect(result).toBe(bet.oddsBoost.enhancedOdds);
    })
  })
});
