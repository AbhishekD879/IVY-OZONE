import { of as observableOf, Subject } from 'rxjs';
import { CashOutSetDefaultStateService } from '@app/betHistory/services/cashoutSetDefaultStateService/cashout-set-default-state-service';
import { tick, fakeAsync } from '@angular/core/testing';


describe('CashOutSetDefaultStateService', () => {
  let service;
  let raceOutcomeDetailsServiceStub, cashoutMapIndexServiceStub, cashoutDataProviderStub,
    racingPostServiceStub, cmsServiceStub, betHistoryMainService;

  const eventEntity = {
    eventStatusCode: 'A',
    markets: [
      {
        marketStatusCode: 'A',
        id: '27333592'
      },
      {
        marketStatusCode: 'A',
        id: '11111111'
      }
    ]
  };

  beforeEach(() => {
    raceOutcomeDetailsServiceStub = {
      getsilkNamesForEvents: jasmine.createSpy('getsilkNamesForEvents').and.returnValue(['all', 'silknames'])
    };
    cashoutMapIndexServiceStub = {
      getItems: jasmine.createSpy('getItems').and.returnValue(['1', '2'])
    };
    cashoutDataProviderStub = {
      getEventsByOutcomesIds: jasmine.createSpy('getEventsByOutcomesIds').and.returnValue(observableOf([{id: '2'}]))
    };
    racingPostServiceStub = {
      getHorseRacingPostById: jasmine.createSpy('getHorseRacingPostById').and.returnValue(
        observableOf({ Error: false, document: { 2: {} } })),
      mergeHorseRaceData: jasmine.createSpy('mergeHorseRaceData').and.returnValue([{ id: '2', racingFormEvent: {} }])
    };
    cmsServiceStub = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))
    };
    betHistoryMainService = {
      isSingleBet: jasmine.createSpy('isSingleBet').and.returnValue(true),
      getPartsResult: jasmine.createSpy('getPartsResult').and.callFake(r => r[0]),
      setBybLegStatus: jasmine.createSpy('setBybLegStatus')
    };

    service = new CashOutSetDefaultStateService(
      cashoutDataProviderStub as any,
      cashoutMapIndexServiceStub as any,
      raceOutcomeDetailsServiceStub as any,
      racingPostServiceStub as any,
      cmsServiceStub as any,
      betHistoryMainService as any
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#extendMapWithEvents', () => {
    it('should get cashout map index', () => {
      service.extendMapWithEvents(['1'], {});
      expect(cashoutMapIndexServiceStub.getItems).toHaveBeenCalledWith('event');
    });

    it('should check CMS for config', () => {
      service.extendMapWithEvents(['1'], {});
      expect(cmsServiceStub.getSystemConfig).toHaveBeenCalled();
      expect(cashoutDataProviderStub.getEventsByOutcomesIds).not.toHaveBeenCalled();
      expect(racingPostServiceStub.getHorseRacingPostById).not.toHaveBeenCalled();
    });
    describe('when RacingDataHub for HR is enabled in CMS config', () => {
      beforeEach(() => {
        cmsServiceStub.getSystemConfig.and.returnValue(observableOf({ RacingDataHub: { isEnabledForHorseRacing: true } }));
      });

      it('should get data from SiteServer without racingFormOutcome included', () => {
        service.extendMapWithEvents(['1'], {}).subscribe();
        expect(cashoutDataProviderStub.getEventsByOutcomesIds).toHaveBeenCalledWith(['1'], { racingFormOutcome: false });
      });

      describe('should make the Racing Post call with corresponding event IDs', () => {
        let betsMap, cahsoutBets;

        beforeEach(() => {
          betsMap = {
            21: {
              leg: [{
                part: [{
                  outcome: [{ event: { id: '1' }, eventCategory: { id: '19' } }, { event: { id: '2' }, eventCategory: { id: '21' } }]
                }, {
                  outcome: [{ event: { id: '3' }, eventCategory: { id: '21' } }, { event: { id: '3' }, eventCategory: { id: '21' } }]
                }],
                eventEntity: eventEntity
              }, {
                part: [{
                  outcome: [{ event: { id: '4' }, eventCategory: { id: '19' } }, { event: { id: '2' }, eventCategory: { id: '21' } }]
                }, {
                  outcome: [{ event: { id: '7' }, eventCategory: { id: '21' } }, { event: { id: '8' }, eventCategory: { id: '19' } }]
                }],
                eventEntity: eventEntity
              }]
            },
            22: {
              leg: [{
                part: [{
                  outcome: [{ event: { id: '1' }, eventCategory: { id: '19' } }, { event: { id: '9' }, eventCategory: { id: '21' } }]
                }, {
                  outcome: [{ event: { id: '7' }, eventCategory: { id: '21' } }, { event: { id: '9' }, eventCategory: { id: '21' } }]
                }, {
                  outcome: { event: { id: '10' }, eventCategory: { id: '21' } }
                }],
                eventEntity: eventEntity
              }]
            }
          };

          cahsoutBets = {
            31: {
              leg: [{
                part: [{ eventId: '1', outcome: '91' }, { eventId: '2', outcome: '92' }],
                eventEntity: eventEntity
              }, {
                part: [{ eventId: '1', outcome: '91' }, { eventId: '3', outcome: '93' }],
                eventEntity: eventEntity
              }, {
                part: [{ eventId: '4', outcome: '94' }, { eventId: '5', outcome: '95' }],
                eventEntity: eventEntity
              }]
            },
            32: {
              leg: [{
                part: [{ eventId: '6', outcome: '96' }, { eventId: '6', outcome: '96' }],
                eventEntity: eventEntity
              }, {
                part: [{ eventId: '4', outcome: '94' }, { eventId: '7', outcome: '97' }],
                eventEntity: eventEntity
              }]
            },
            33: { leg: [ { part: [{ eventId: '8' }], eventEntity: eventEntity } ] }
          };
          cashoutDataProviderStub.getEventsByOutcomesIds.and.returnValue(observableOf([{ id: '1' }, { id: '2' }]));
          racingPostServiceStub.getHorseRacingPostById.and.returnValue(
            observableOf({ Error: false, document: { 1: {}, 2: {} } }));
          racingPostServiceStub.mergeHorseRaceData.and.returnValue(
            [{ id: '1', racingFormEvent: {} }, { id: '2', racingFormEvent: {} }]);
        });
        it('if HR bets are present in the provided bets map', () => {
          service.extendMapWithEvents(['1'], betsMap as any).subscribe();
          expect(racingPostServiceStub.getHorseRacingPostById).toHaveBeenCalledWith('2,3,7,9,10');
        });

        it('if Cashout bets are present in the provided bets map (no event categoryId data)', () => {
          service.extendMapWithEvents(['1'], cahsoutBets as any).subscribe();
          expect(racingPostServiceStub.getHorseRacingPostById).toHaveBeenCalledWith('1,2,3,4,5,6,7');
        });

        it('should merge racing post data to SS events only after both request are complete', () => {
          const ss$ = new Subject(), rp$ = new Subject();
          cashoutDataProviderStub.getEventsByOutcomesIds.and.returnValue(ss$);
          racingPostServiceStub.getHorseRacingPostById.and.returnValue(rp$);
          const response = service.extendMapWithEvents(['1'], betsMap as any);

          response.subscribe(data => {
            expect(data).toEqual(betsMap);
            expect(data.allSilkNames).toEqual(['all', 'silknames']);
          });

          ss$.next([{ id: 11 }, { id: 22 }]);
          rp$.next({ Error: false, document: { 1: {} } });
          expect(racingPostServiceStub.mergeHorseRaceData).not.toHaveBeenCalled();

          ss$.complete();
          expect(racingPostServiceStub.mergeHorseRaceData).not.toHaveBeenCalled();
          rp$.complete();
          expect(racingPostServiceStub.mergeHorseRaceData).toHaveBeenCalledWith(
            [{ id: 11 }, { id: 22 }], { Error: false, document: { 1: {} } });
        });

        it('covering condition with empty object as legs array item', () => {
          spyOn(service as any, 'updateLegForEvent'); // avoid crash in private method
          service.extendMapWithEvents(['1'], { 0: { leg: [{}] } } as any).subscribe();
          expect(racingPostServiceStub.getHorseRacingPostById).not.toHaveBeenCalled();
        });
      });

      describe('if HR bets are not present in the provided bets map (and neither Cashout bets)', () => {
        let betsMap;

        beforeEach(() => {
          betsMap =  {
            21: {
              leg: [{
                part: [{
                  outcome: [
                    { event: { id: '1' }, eventCategory: { id: '19' } },
                    { event: { id: '2' }, eventCategory: { id: '19' } }
                  ],
                }],
                eventEntity : eventEntity
              }],
            }
          };
          cashoutDataProviderStub.getEventsByOutcomesIds.and.returnValue(observableOf([{ id: '1' }, { id: '2' }]));
          racingPostServiceStub.getHorseRacingPostById.and.returnValue(
            observableOf({ Error: false, document: { 1: {}, 2: {} } }));
          racingPostServiceStub.mergeHorseRaceData.and.callFake((eventsData, raceData) => eventsData);
        });
        it('should not make the Racing Post call', fakeAsync(() => {
          service.extendMapWithEvents(['1'], betsMap as any).subscribe();
          tick();
          expect(racingPostServiceStub.getHorseRacingPostById).not.toHaveBeenCalled();
          expect(racingPostServiceStub.mergeHorseRaceData).toHaveBeenCalledWith([{ id: '1' }, { id: '2' }], undefined);
        }));

        it('should update silks from SS events', fakeAsync(() => {
          service.extendMapWithEvents(['1'], betsMap as any).subscribe();
          tick();
          expect(raceOutcomeDetailsServiceStub.getsilkNamesForEvents.calls.allArgs()).toEqual([ [[{ id: '1' }, { id: '2' }]], [[]] ]);
          expect(betsMap.allSilkNames).toEqual(['all', 'silknames']);
        }));

        it('should merge racing post data to SS events only after the request is complete', () => {
          const ss$ = new Subject(), rp$ = new Subject();
          cashoutDataProviderStub.getEventsByOutcomesIds.and.returnValue(ss$);
          racingPostServiceStub.getHorseRacingPostById.and.returnValue(rp$);
          const response = service.extendMapWithEvents(['1'], betsMap as any);

          response.subscribe(data => {
            expect(data).toEqual(betsMap);
            expect(data.allSilkNames).toEqual(['all', 'silknames']);
          });

          ss$.next([{ id: 11 }, { id: 22 }]);
          expect(racingPostServiceStub.mergeHorseRaceData).not.toHaveBeenCalled();

          ss$.complete();
          expect(racingPostServiceStub.mergeHorseRaceData).toHaveBeenCalledWith(
            [{ id: 11 }, { id: 22 }], undefined);
        });
      });
    });

    describe('should not call Racing Post service and update silks directly from SS events', () => {
      beforeEach(() => {
        racingPostServiceStub.mergeHorseRaceData.and.callFake((eventsData, raceData) => eventsData);
      });
      it('when RacingDataHub for HR is disabled in CMS config', () => {
        cmsServiceStub.getSystemConfig.and.returnValue(observableOf({ RacingDataHub: { isEnabledForHorseRacing: false } }));
      });
      it('when RacingDataHub is not defined in CMS config', () => {
        cmsServiceStub.getSystemConfig.and.returnValue(observableOf({ }));
      });
      it('when CMS config is not available', () => {
        cmsServiceStub.getSystemConfig.and.returnValue(observableOf(null));
      });

      afterEach(() => {
        service.extendMapWithEvents(['1'], { 1: {}, 2: {} } as any)
          .subscribe(data => expect(data).toEqual({ 1: {}, 2: {}, allSilkNames: ['all', 'silknames'] }));
        expect(raceOutcomeDetailsServiceStub.getsilkNamesForEvents.calls.allArgs()).toEqual([ [[{ id: '2' }]], [[]] ]);
        expect(cashoutDataProviderStub.getEventsByOutcomesIds).toHaveBeenCalledWith(['1'], { racingFormOutcome: true });
        expect(racingPostServiceStub.getHorseRacingPostById).not.toHaveBeenCalled();
        expect(racingPostServiceStub.mergeHorseRaceData).toHaveBeenCalledWith([{ id: '2' }], undefined);
      });
    });
  });

  it('#setOutcomeData should set default values', () => {
    // bet will be updated in #setOutcomeData method
    let bet = {
      outcomes: {}
    };
    const outcome = {
      id: '1',
      isDisplayed: true,
      outcomeStatusCode: 'P'
    };
    const price = {
      priceNum: 11,
      priceDen: 22
    };
    const part = {
      outcome: '1'
    };
    const betResultWithPrice = {
      outcomes: {
        '1': {
          displayed: 'Y',
          status: 'P',
          lp_num: 11,
          lp_den: 22,
          settled: 'N'
        }
      }
    };
    service.setOutcomeData(bet, outcome as any, price, '-', part);
    expect(bet).toEqual(betResultWithPrice);

    bet = {
      outcomes: {}
    };

    const betResultWithoutPrice = {
      outcomes: {
        '1': {
          displayed: 'Y',
          status: 'P',
          lp_num: '',
          lp_den: '',
          settled: 'Y'
        }
      }
    };
    service.setOutcomeData(bet, outcome as any, null);
    expect(bet).toEqual(betResultWithoutPrice);
  });

  describe('updateLegForEvent', () => {
    let outcome, betsMap, betsMapResult;

    beforeEach(() => {
      outcome = [
        {
          outcomeStatusCode: 'A',
          result: {
            value: 'P',
            places: 7
          }
        },
        {
          outcomeStatusCode: 'A',
          result: {
            value: 'P',
            places: 7
          }
        },
        {
          outcomeStatusCode: 'A',
          result: {
            value: 'P',
            places: 7
          }
        },
        {
          outcomeStatusCode: 'S',
          result: {
            value: 'P',
            places: 7
          }
        }
      ];

      betsMap = {
        '1': {
          betType: 'SGL',
          leg: {
            '1': {
              eventEntity: {
                eventStatusCode: 'A',
                markets: [
                  {
                    marketStatusCode: 'S',
                    id: '27333592',
                    outcomes: outcome
                  },
                  {
                    marketStatusCode: 'A',
                    id: '11111111',
                    outcomes: outcome
                  }
                ]
              },
              legType: {
                code: 'E'
              },
              part: [{
                result: '-',
                eventId: '5',
                eachWayPlaces: 10,
                outcome,
                marketId: '27333592',
              }]
            }
          },
          outcomes: [
            {
              status: 'A'
            },
            {
              status: 'S'
            }
          ]
        }
      };

      betsMapResult = {
        '1': {
          betType: 'SGL',
          leg: {
            '1': {
              eventEntity: {
                eventStatusCode: 'A',
                markets: [
                  {
                    marketStatusCode: 'S',
                    id: '27333592',
                    outcomes: outcome
                  },
                  {
                    marketStatusCode: 'A',
                    id: '11111111',
                    outcomes: outcome
                  }
                ]
              },
              isBetSettled: false,
              isEventEntity: false,
              legType: {
                code: 'E'
              },
              noEventFromSS: true,
              part: [{
                result: '-',
                eventId: '5',
                eachWayPlaces: 10,
                outcome,
                marketId: '27333592'
              }],
              status: 'suspended'
            }
          },
          outcomes: [
            {
              status: 'A'
            },
            {
              status: 'S'
            }
          ]
        }
      };

      spyOn(service, 'setDefaultValuesToAttributesUpdateOn').and.callThrough();
      spyOn(service, 'getLegStatus').and.callThrough();
    });

    describe('should call setDefaultValuesToAttributesUpdateOn', () => {
      beforeEach(() => {
        const leg = betsMapResult['1'].leg['1'];
        leg.isEventEntity = true;
        leg.noEventFromSS = false;
        leg.eventEntity = {};
        delete leg.status;
      });

      it('and skip direct getLegStatus call ', () => {
        (service as any).setDefaultValuesToAttributesUpdateOn.and.stub();
        service.updateLegForEvent({'5': { id: '123' }} as any, betsMap);
        betsMapResult['1'].leg['1'].eventEntity.id = '123';

        expect(service.setDefaultValuesToAttributesUpdateOn).toHaveBeenCalled();
        expect(service.getLegStatus).not.toHaveBeenCalled();
        expect(betHistoryMainService.isSingleBet).not.toHaveBeenCalled();
        expect(betsMap).toEqual(betsMapResult);
      });

      describe('and sequentially call getLegStatus', () => {
        let eventsFromSS;

        beforeEach(() => {
          betsMap['1'].leg['1'].eventEntity.id = '5';
          betsMap['1'].leg['1'].part[0].id = '5';
          betsMap['1'].leg['1'].part[0].result = 'W';
          betsMap['1'].event = ['5'];
          betsMap['1'].market = ['456'];
          betsMap['1'].outcome = ['789'];
          betsMap['1'].events = {};
          betsMap['1'].markets = {};
          eventsFromSS = { '5': { id: 5, eventStatusCode: 'X', markets: [{
            id: 456, marketStatusCode: 'Y', outcomes: [
              { id: 789, price: [{}], outcomeStatusCode: 'Z' }
            ]
          }] } };
        });

        it('should NOT check statuses if no markets in event', () => {
          betsMap['1'].leg['1'].eventEntity.id = '5';
          betsMap['1'].leg['1'].part[0].id = '5';
          betsMap['1'].leg['1'].part[0].result = 'W';
          betsMap['1'].event = ['5'];
          betsMap['1'].market = [];
          betsMap['1'].outcome = [];
          betsMap['1'].events = {};
          betsMap['1'].markets = {};
          eventsFromSS = { '5': { id: 5, eventStatusCode: 'A', markets: [] } };

          service.updateLegForEvent(eventsFromSS, betsMap);

          expect((service as any).getLegStatus).not.toHaveBeenCalled();
        });

        describe('and use single part for leg status', () => {
          it('for non-handicap result', () => {});
          it('taken from dispResult for handicap result', () => {
            betsMap['1'].leg['1'].part[0].result = 'H';
            betsMap['1'].leg['1'].part[0].dispResult = 'W';
          });
          afterEach(() => {
            service.updateLegForEvent(eventsFromSS, betsMap);
            expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['W']);
            expect((service as any).getLegStatus).toHaveBeenCalledWith('W', true, 'X', 'Y', ['Z']);
          });
        });

        describe('and call getPartsResult for determining multi-part leg status', () => {
          it('for non-handicap result', () => {
            betsMap['1'].leg['1'].part.push({ result: 'L' });
          });
          it('taken from dispResult for handicap result', () => {
            betsMap['1'].leg['1'].part.push({ result: 'H', dispResult: 'L' });
          });
          afterEach(() => {
            betHistoryMainService.getPartsResult.and.returnValue('L');
            service.updateLegForEvent(eventsFromSS, betsMap);
            expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['W', 'L']);
            expect((service as any).getLegStatus).toHaveBeenCalledWith('L', true, 'X', 'Y', ['Z']);
          });
        });
      });
    });

    it('should provide default values', () => {
      betsMapResult['1'].leg['1'].status = 'suspended';
      service.updateLegForEvent({}, betsMap);

      expect(betHistoryMainService.isSingleBet).toHaveBeenCalledWith(betsMap['1']);
      expect(betsMap).toEqual(betsMapResult);
    });

    it('should provide default values (pool)', () => {
      betsMap['1'].outcomes[1].status = 'A';
      betsMap['1'].leg['1'].eventEntity.markets[0].marketStatusCode = 'A';
      betsMapResult['1'].leg['1'].eventEntity.markets[0].marketStatusCode = 'A';
      betsMapResult['1'].outcomes[1].status = 'A';
      betsMapResult['1'].leg['1'].status = 'open';
      service.updateLegForEvent({}, betsMap);

      expect(betHistoryMainService.isSingleBet).toHaveBeenCalledWith(betsMap['1']);
      expect(betsMap).toEqual(betsMapResult);
    });

    it('should provide default values (TRL pool)', () => {
      betsMap['1'].betType = 'TRL';
      betsMapResult['1'].betType = 'TRL';
      betsMapResult['1'].leg['1'].status = 'suspended';
      service.updateLegForEvent({}, betsMap);

      expect(betHistoryMainService.isSingleBet).toHaveBeenCalledWith(betsMap['1']);
      expect(betsMap).toEqual(betsMapResult);
    });

    it('should check outcomes of bet (single)', () => {
      service.updateLegForEvent({}, betsMap);

      expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['-']);
      expect(service.getLegStatus).toHaveBeenCalledWith(
        '-', jasmine.any(Boolean), jasmine.any(String), jasmine.any(String), ['A', 'S']);
    });

    it('should check outcomes of bet market (acca / single-ex-acca)', () => {
      betHistoryMainService.isSingleBet.and.returnValue(false);
      service.updateLegForEvent({}, betsMap);

      expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['-']);
      expect(service.getLegStatus).toHaveBeenCalledWith(
        '-', jasmine.any(Boolean), jasmine.any(String), jasmine.any(String), ['A', 'A', 'A', 'S']);
    });

    it('should determine combined parts result for bet with multi-part leg', () => {
      betsMap['1'].leg['1'].part.push({ result: 'W' }, { result: 'L' });
      betHistoryMainService.getPartsResult.and.returnValue('L');
      service.updateLegForEvent({}, betsMap);
      expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['-', 'W', 'L']);
      expect(service.getLegStatus).toHaveBeenCalledWith(
        'L', jasmine.any(Boolean), jasmine.any(String), jasmine.any(String), ['A', 'S']);
    });
  });

  it('#getLegStatus should calculate status of leg', () => {
    expect(service.getLegStatus('P', true)).toBe('won');
    expect(service.getLegStatus('P', false)).toBe('lost');

    expect(service.getLegStatus('', false, '', '', ['S'])).toBe('suspended');
    expect(service.getLegStatus('', false, '', 'S', [])).toBe('suspended');
    expect(service.getLegStatus('', false, 'S', '', [])).toBe('suspended');

    expect(service.getLegStatus('-', false, '', '', [])).toBe('open');
    expect(service.getLegStatus('P', false, '', '', [])).toBe('lost');
  });
});

