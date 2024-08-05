import { BetPromotionComponent } from '@app/betHistory/components/betPromotions/bet-promotions.component';
import { BET_PROMO_CONFIG as bet_promos } from '@betHistoryModule/constants/bet-promotions.constant';
import { of } from 'rxjs';

describe('BetPromotionComponent', () => {
  let component: BetPromotionComponent;
  let cmsService, pubSubService, localeService,betInfoDialogService,gtmService;
  let boost, boost2, moneyBack, accaInsurance, twoUpMarket;

  beforeEach(() => {
    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getSystemConfig:  jasmine.createSpy('LuckyBonus').and.returnValue(of(true)),
      systemConfiguration: { LuckyBonus: { SettledBetPopUpHeader: 'betslip header', SettledBetPopUpMessage: 'popup messge'} }
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((...args) => args[2]()),
      unsubscribe: jasmine.createSpy('ununsubscribe'),
      API: {
        BET_EVENTENTITY_UPDATED: 'BET_EVENTENTITY_UPDATED'
      },
      publish: jasmine.createSpy('publish')
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('Match Result')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };
    betInfoDialogService = {
      multiple: jasmine.createSpy()
    };

    component = new BetPromotionComponent(cmsService, pubSubService, localeService,betInfoDialogService,gtmService);
    component.betEventSource = {
      altSettle: {
        rule: [
            {
                "name": "LUCKYX_ALL_CORRECT",
                "num_win": "4",
                "multiplier": "1.10"
            }
        ]
      },
      betTermsChange: [{
        reasonCode: 'ODDS_BOOST'
      }, {
        reasonCode: 'none'
      }],
      betType: 'SGL',
      leg: [{
        eventEntity: {
          drilldownTagNames: 'EVFLAG_MB'
        },
        part: [{eventMarketDesc: 'Match Result'}]
      }],
      claimedOffers: {
        claimedOffer: [{
          offerCategory: 'Acca Insurance',
          status: 'qualified'
        }, {
          offerCategory: 'Acca Insurance',
          status: 'none'
        }, {
          offerCategory: 'none'
        }]
      }
    } as any;
    boost = bet_promos[0];
    boost2 = {
      name: 'boosted',
      label: 'bs.boostedMsg2',
      svgId: 'odds-boost-icon-dark'
    } as any;
    twoUpMarket = bet_promos[1];
    moneyBack = bet_promos[2];
    accaInsurance = bet_promos[3];
  });

  it('should Init component lucky', () => {
    const betEventSource = {
      betTypeRef:{
        id:'L15'
      },
      availableBonuses :{
        availableBonus:{
          multiplier:'2'
        }
      },
      leg:[{
        sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
      }]
    }as any;
    component['checkLuckyBonus'] = jasmine.createSpy('checkLuckyBonus'); 
    component.ngOnInit();
  });

  it('should return true when enable bet pack is false', () => {
    cmsService = { systemConfiguration: { LuckyBonus: { lucky: false } } };
    expect(cmsService.systemConfiguration['LuckyBonus']).toEqual(cmsService.systemConfiguration['LuckyBonus'])
  })
  
  it('should unsync on destroy component', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  describe('#updatePromos should create array of icons', () => {
    it('moneyBack icon', () => {
      component.betEventSource = {
        betType: 'SGL',
        leg: [{
          eventEntity: {
            markets: [{drilldownTagNames: 'MKTFLAG_MB'}]
          }
        }]
      } as any;
    moneyBack = bet_promos[2];
      component['updatePromos']();
      expect(component.promoIcons).toEqual([moneyBack]);
    });

    it('boost icon', () => {
      (cmsService.getToggleStatus as jasmine.Spy).and.returnValue(of(false));
      // (cmsService.getSystemConfig as jasmine.Spy).and.returnValue(of(false));
    
      component.betEventSource = {
        betTermsChange: [{
          reasonCode: 'ODDS_BOOST'
        }, {
          reasonCode: 'none'
        }],
        betType: 'SGL',
        leg: [{
          eventEntity: {
            markets: [{drilldownTagNames: 'MKTFLAG_MB'}]
          },
          part: [{eventMarketDesc: 'Match Result'}]
        }]
      } as any;

      component['updatePromos']();
      expect(component.promoIcons).toEqual([boost]);
    });
 
    describe('#getWinner', () => {
      it('#getWinner L15', () => {
       const lucky = {
        settled: 'Y',
        betType: 'L15',
        altSettle: {
          rule: [{
            num_win: '4'
          }]
        }
       }
        expect(component['getWinner'](lucky)).toBeTrue();
      });
      it('#getWinner L31', () => {
        const lucky = {
        settled: 'Y',
        betType: 'L31',
        altSettle: {
          rule: [{
            num_win: '5'
          }]
        }
       }
        expect(component['getWinner'](lucky)).toBeTrue();
      });
      it('#getWinner L63', () => {
        const lucky = {
        settled: 'Y',
        betType: 'L63',
        altSettle: {
          rule: [{
            num_win: '6'
          }]
        }
       }
        expect(component['getWinner'](lucky)).toBeTrue();
      });
    });

      it('sendGTMData', () => {
        component['sendGtmDataonMoreinFoicon']('lucky15');
        expect(gtmService.push).toHaveBeenCalled();
      }); 
      describe("#betTypeStatus", () => {
        it('should call betTypeStatus with altSettle', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            leg: [{}],
            altSettle: {}
          };
          const res = component.betTypeStatus();
          expect(res).toEqual('AllWinner');
        });
        it('should call betTypeStatus without altSettle', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            betType: 'L15',
            settled: 'N',
            availableBonuses: {
              availableBonus:[{
                multiplier:'1',
                num_win:'4'
              }]
            },
            leg: [
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
          ]
          };
          const res = component.betTypeStatus();
          expect(res).toEqual('AllWinner');
        });
        it('should call betTypeStatus without altSettle and L31', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            betType: 'L31',
            settled: 'N',
            availableBonuses: {
              availableBonus:[{
                multiplier:'1',
                num_win:'5'
              }]
            },
            leg: [
              {eventEntity: {categoryId: '21'},status: 'won' },
              {eventEntity: {categoryId: '21'},status: 'won' },
              {eventEntity: {categoryId: '21'},status: 'won' },
              {eventEntity: {categoryId: '21'},status: 'won' },
              {eventEntity: {categoryId: '21'},status: 'won' },
          ]
          };
          const res = component.betTypeStatus();
          expect(res).toEqual('AllWinner');
        });
        it('should call betTypeStatus without altSettle and L63', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            betType: 'L63',
            settled: 'N',
            availableBonuses: {
              availableBonus:[{
                multiplier:'1',
                num_win:'6'
              }]
            },
            leg: [
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
              {eventEntity: {categoryId: '19'},status: 'won' },
          ]
          };
          const res = component.betTypeStatus();
          expect(res).toEqual('AllWinner');
        });
        it('should call betTypeStatus without altSettle and L63 with loose', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            betType: 'L63',
            settled: 'N',
            availableBonuses: {
              availableBonus:[{
                multiplier:'1',
                num_win:'6'
              }]
            },
            leg: [
              {backupEventEntity: {categoryId: '19'},status: 'lost' },
              {backupEventEntity: {categoryId: '19'},status: 'won' },
              {backupEventEntity: {categoryId: '19'},status: 'won' },
              {backupEventEntity: {categoryId: '19'},status: 'won' },
              {backupEventEntity: {categoryId: '19'},status: 'won' },
              {backupEventEntity: {categoryId: '19'},status: 'won' },
          ]
          };
          const res = component.betTypeStatus();
          expect(res).toEqual('5');
        });
        it('should call betTypeStatus without altSettle and L63 with loose', () => {
          spyOn<any>(component, 'winnerType').and.returnValue('AllWinner');
          component.betEventSource = {
            betType: 'L63',
            receipt: 'O/26382303/0000067',
            settled: 'N',
            availableBonuses: {
              availableBonus:[{
                multiplier:'2',
                num_win:'6'
              }]
            },
            leg: [
              {eventEntity: {categoryId: '19'},status: 'lost' },
              {eventEntity: {categoryId: '19'},status: 'lost' },
              {eventEntity: {categoryId: '19'},status: 'lost' },
              {eventEntity: {categoryId: '19'},status: 'lost' },
              {eventEntity: {categoryId: '19'},status: 'lost' },
              {eventEntity: {categoryId: '19'},status: 'lost' },
          ]
          };
          const res = component.betTypeStatus();
          expect(pubSubService.publish).toHaveBeenCalledWith('LUCKY_BONUS', component.betEventSource.receipt);
          expect(res).toEqual('0');
        });
      });
   

    it('boost 2 icon', () => {
      component.betEventSource = {
        betTermsChange: [{
          reasonCode: 'ODDS_BOOST'
        }, {
          reasonCode: 'none'
        }],
        betType: 'SGL',
        leg: [{
          eventEntity: {
            markets: [{drilldownTagNames: 'MKTFLAG_MB'}]
          },
          part: [{eventMarketDesc: 'Match Result'}]
        }]
      } as any;

      component['updatePromos']();
      expect(component.promoIcons).toEqual([boost2, moneyBack]);
    });

    it('twoUpMarket icon', () => {
      component.betEventSource = {
        betType: 'SGL',
        leg: [{
          eventEntity: {
            categoryId: '16',
            markets: [{drilldownTagNames: 'MKTFLAG_MB'}]
          },
          part: [{eventMarketDesc: 'Match Result'}]
        }]
      } as any;

      component['updatePromos']();
      expect(component.promoIcons).toEqual([twoUpMarket, moneyBack]);
    });

    it('accaInsurance icon', () => {
      (cmsService.getToggleStatus as jasmine.Spy).and.returnValue(of(false));
      // (cmsService.getSystemConfig as jasmine.Spy).and.returnValue(of(false));
      component.betEventSource = {
        betType: 'ACC5',
        claimedOffers: {
          claimedOffer: [{
            offerCategory: 'Acca Insurance',
            status: 'qualified'
          }, {
            offerCategory: 'Acca Insurance',
            status: 'none'
          }, {
            offerCategory: 'none'
          }]
        }
      } as any;

      component['updatePromos']();
      expect(component.promoIcons).toEqual([accaInsurance]);
    });

    it('should have no icons', () => {
      (cmsService.getToggleStatus as jasmine.Spy).and.returnValue(of(false));
      // (cmsService.getSystemConfig as jasmine.Spy).and.returnValue(of(false));
      component.betEventSource = {} as any;
      component['updatePromos']();
      expect(component.promoIcons).toEqual([]);
    });
  });

  it('#isAccaInsurance with defect data', () => {
    component.betEventSource.betType = 'SGL';
    expect(component['isAccaInsurance']()).toBe(false);

    component.betEventSource.betType = 'AC15';
    component.betEventSource.claimedOffers.claimedOffer[0].offerCategory = undefined;
    expect(component['isAccaInsurance']()).toBe(false);

    component.betEventSource.claimedOffers.claimedOffer = undefined;
    expect(component['isAccaInsurance']()).toBe(undefined);
  });

  it('#isMoneyBack with defect data', () => {
    component.betEventSource.leg[0].eventEntity.drilldownTagNames = 'EVFLAG_FI';
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0].eventEntity.drilldownTagNames = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0].eventEntity = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0] = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);
  });

  it('#isMoneyBack on market level', () => {
    component.betEventSource.leg[0].eventEntity.drilldownTagNames = undefined;
    component.betEventSource.leg[0].eventEntity.markets = [{
      drilldownTagNames: 'MKTFLAG_MB'
    }] as any;
    expect(component['isMoneyBack']()).toBe(true);

    component.betEventSource.leg[0].eventEntity.markets[0].drilldownTagNames = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0].eventEntity.markets[0] = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0].eventEntity.markets = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0].eventEntity = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);

    component.betEventSource.leg[0] = undefined;
    expect(component['isMoneyBack']()).toBe(undefined);
  });

  describe('#checkLuckyBonus', () => {
    
    it('should check Lucky Bonus L15',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L15'
        },
        betType: 'L15',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '4'
          }]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyBet).toEqual([{
        "multiplier": "2",
        "num_win": "4",
        "isShown": false
    }]);
    });
    it('should check Lucky Bonus L31',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L31'
        },
        betType: 'L31',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '5'
          }]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyCheck).toEqual(true);
    });
    it('should check Lucky Bonus L63',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L63'
        },
        betType: 'L63',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '6'
          }]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyCheck).toEqual(true);
    });
    it('should check Lucky Bonus L63 with 7',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L63'
        },
        betType: 'L63',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '7'
          }]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyCheck).toEqual(true);
    });
    it('should check Lucky Bonus L15, L63, L31',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L63'
        },
        betType: 'L63',
        availableBonuses :{
          availableBonus:[
            {multiplier:'2', num_win: '7'},
            {multiplier:'2', num_win: '7'},
            {multiplier:'2', num_win: '6'},
          ]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyCheck).toEqual(true);
    });
    it('should check Lucky Bonus L15',()=>{
      spyOn(component, 'isBonusApplicable').and.returnValue(true);
      component.betEventSource={
        betTypeRef:{
          id:'L63'
        },
        betType: 'L63',
        altSettle: {
          rule: [{
            multiplier:'2', num_win: '6'
          }]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyBet.length).toEqual(1);
      component.betEventSource={
        betTypeRef:{
          id:'L63'
        },
        betType: 'L63',
        altSettle: {
          rule: null
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      }as any;
      component['checkLuckyBonus']();
      expect(component.luckyBet.length).toEqual(0);
    });
  })


  it('should called checkLuckyBonus()',()=>{
    const betEventSource = { betTermsChange: [{ stake: { value: 1 }, reasonCode: 'ORIGINAL_VALUES' }] } as any;
    component['getBetType'] = jasmine.createSpy();
    
  });

  it('should call openSelectionMultiplesDialog()', () => {
    component.openSelectionMultiplesDialog(component.betEventSource.betType,'lucky15');
    component.sendGtmDataonMoreinFoicon('lucky15');
});

  it('#isBonusApplicable',()=>{
    expect(component.isBonusApplicable([{multiplier: 2}])).toBeTrue();
  });
  it('#filterOnlyAvailable',()=>{
    expect(component.filterOnlyAvailable([{multiplier: 2}]).length).toEqual(1);
  });
  it('#getBetType',()=>{
    component.betEventSource = {
      bybType: 'Partial'
    } as any;
    expect(component['getBetType']()).toEqual('Partial');
    component.betEventSource = {
      betType: 'Partial'
    } as any;
    expect(component['getBetType']()).toEqual('Match Result');
  });
  it('#winnerType',()=>{
    spyOn<any>(component, 'getWinner').and.returnValue(true);
    expect(component['winnerType']({settled: 'Y'})).toEqual('AllWinner');
    expect(component['winnerType']({settled: 'N',altSettle: {rule: [{num_win: '1'}]}})).toEqual('1');
  });
  describe('#onlyAllWinnerBonusApplicable', () => {
    it('#onlyAllWinnerBonusApplicable L15', () => {
      const luckydata = {
        betTypeRef:{id: 'L15'},
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '4'
          }]
        }
      } as any;
      expect(component.onlyAllWinnerBonusApplicable(luckydata)).toBeTrue();
    });
    it('#onlyAllWinnerBonusApplicable L31', () => {
      const luckydata = {
        betType: 'L31',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '5'
          }]
        }
      } as any;
      expect(component.onlyAllWinnerBonusApplicable(luckydata)).toBeTrue();
    });
    it('#onlyAllWinnerBonusApplicable L63', () => {
      const luckydata = {
        betType: 'L63',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2', num_win: '6'
          }]
        }
      } as any;
      expect(component.onlyAllWinnerBonusApplicable(luckydata)).toBeTrue();
    });
  });
    it("#addWinnerLabel", () => {
      expect(component.addWinnerLabel(1, true)).toEqual('1 WINNER');
      expect(component.addWinnerLabel(2, true)).toEqual('2 WINNERS');
    });
});
