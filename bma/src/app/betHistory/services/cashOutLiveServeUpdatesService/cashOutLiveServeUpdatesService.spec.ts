import {
  CashOutLiveServeUpdatesService
} from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import {
  cashoutBet,
  liveServeUpdate
} from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService.mock';
import { of as observableOf } from 'rxjs';

describe('cashOutLiveServeUpdatesService', () => {
  let service;
  let cashoutErrorMessageService;
  let commentsService;
  let pubsubService;
  let cashOutMapIndexService: any;
  let scoreParser: any;
  let betHistoryMainService;
  let cmsService: any;
  const eventMock = {
    id: 111,
    comments: {},
    categoryCode: 'football',
    clock: {
      refresh: () => {}
    }
  };
  const cashoutUpdateTypeMock = {
    sSELCN: 'outcome',
    sPRICE: 'outcome',
    sEVENT: 'event',
    sEVMKT: 'market'
  };
  const attributesUpdateOnMock = {
    event: {
      propertyName: 'events',
      attributes: ['displayed', 'status']
    },
    market: {
      propertyName: 'markets',
      attributes: ['displayed', 'status']
    },
    outcome: {
      propertyName: 'outcomes',
      attributes: ['displayed', 'status', 'settled', 'lp_num', 'lp_den']
    }
  };

  beforeEach(() => {
    cashOutMapIndexService = {
      outcome: {},
      market: {},
      event: {}
    };
    cashoutErrorMessageService = jasmine.createSpyObj(['getErrorMessage']);
    commentsService = {
      parseScoresFromName: jasmine.createSpy('parseScoresFromName'),
      footballUpdateExtend: jasmine.createSpy('footballUpdateExtend'),
      extendWithScoreType: jasmine.createSpy('extendWithScoreType'),
      sportUpdateExtend: jasmine.createSpy('sportUpdateExtend')
    } as any;
    pubsubService = {
      API: {
        EMA_HANDLE_BET_LIVE_UPDATE: 'EMA_HANDLE_BET_LIVE_UPDATE',
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        CASHOUT_LIVE_SCORE_EVENT_UPDATE: 'CASHOUT_LIVE_SCORE_EVENT_UPDATE',
        CASHOUT_LIVE_SCORE_UPDATE: 'CASHOUT_LIVE_SCORE_UPDATE',
        LIVE_BET_UPDATE: 'LIVE_BET_UPDATE',
        EVENT_STARTED: 'EVENT_STARTED',
        EVENT_FINISHED: 'EVENT_FINISHED'

      },
      publish: jasmine.createSpy('publish')
    };
    scoreParser = {
      parseTypeAndScores: jasmine.createSpy('parseTypeAndScores').and.returnValue({
        score: {
        },
        scoreType: 'Simple'
      })
    } as any;

    betHistoryMainService = {
      getPartsResult: jasmine.createSpy('getPartsResult').and.callFake(r => r[0]),
      setBybLegStatus: jasmine.createSpy('setBybLegStatus')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        HorseRacingBIR: {
          marketsEnabled: ['win or each Way']
        }
      }))
    };

    service = new CashOutLiveServeUpdatesService(
      cashOutMapIndexService,
      cashoutErrorMessageService,
      commentsService,
      pubsubService,
      scoreParser,
      betHistoryMainService,
      cmsService
    );

    service.betsMap = {
      2: {
        event: { id: '11123' },
        market: { id: '123123' },
        outcome: { id: '123123' }
      },
      3: {
        event: { id: '1' },
        market: { id: '111' }
      }
    };
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
    expect(CashOutLiveServeUpdatesService.cashoutUpdateType).toEqual(cashoutUpdateTypeMock);
    expect(CashOutLiveServeUpdatesService.attributesUpdateOn).toEqual(attributesUpdateOnMock);
  });

  it('should call getSystemConfig with config - null', () => {
    cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(null))};
    const service = new CashOutLiveServeUpdatesService(cashOutMapIndexService, cashoutErrorMessageService, commentsService, pubsubService, scoreParser, betHistoryMainService, cmsService );
    expect(service['BIRMarketsEnabled']).toBeFalsy();
  });
  it('should call getSystemConfig with HorseRacingBIR - null', () => {
    cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: null}))};
    const service = new CashOutLiveServeUpdatesService(cashOutMapIndexService, cashoutErrorMessageService, commentsService, pubsubService, scoreParser, betHistoryMainService, cmsService );
    expect(service['BIRMarketsEnabled']).toBeFalsy();
  });
  it('should call getSystemConfig with marketsEnabled - null', () => {
    cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: {marketsEnabled: null}}))};
    const service = new CashOutLiveServeUpdatesService(cashOutMapIndexService, cashoutErrorMessageService, commentsService, pubsubService, scoreParser, betHistoryMainService, cmsService );
    expect(service['BIRMarketsEnabled']).toBeFalsy();
  });

  describe('updateCashOutValue method testing', () => {
    let update: any;
    const cashoutIds = ['127471'];

    beforeEach(() => {
      update = Object.assign({}, liveServeUpdate);
      spyOn(service, 'updateEventEntity');
      spyOn(service, 'updateLegPartResult');
      spyOn(service, 'updatePlacedBetsStatuses');
      spyOn(service, 'getCashOutIdForUpdate').and.returnValue(cashoutIds);
      spyOn(service, 'updateBetAccordingToPush');
    });

    it('should call updateEventEntity', () => {
      spyOn(service, 'eventStartedUpdate');
      update.type = 'sSCBRD';
      service.updateCashOutValue(update);
      expect(service.updateEventEntity).toHaveBeenCalled();
      expect(service.eventStartedUpdate).toHaveBeenCalledWith(update);
    });

    it('should finish function call', () => {
      update.type = null;
      service.updateCashOutValue(update);
      expect(service.updateEventEntity).not.toHaveBeenCalled();
    });

    it('should call _updateLegPartResult', () => {
      update.payload.result = 'W';
      service.updateCashOutValue(update);
      expect(service.updateLegPartResult).toHaveBeenCalled();
    });

    it('should call _updatePlacedBetsStatuses', () => {
      service.updateCashOutValue(update);
      expect(service.updatePlacedBetsStatuses).toHaveBeenCalledWith([ '127471' ], '5447497', 'event', update.payload);
    });

    it('should update placedBets with payload of market', () => {
      const id = '111';
      const betToUpdate = {
        event: { id: '1' },
        market: { id }
      };

      update.type = 'sEVMKT';
      update.id = Number(id);
      service.betsInLiveUpdateProgress = {
        [cashoutIds[0]]: {}
      };

      service.updateCashOutValue(update);
      expect(service.updateBetAccordingToPush).toHaveBeenCalledWith(betToUpdate, id, 'market', update.payload);
    });

    it('should update placedBets with payload of sSELCN', () => {
      const id = '111';
      const betToUpdate = {
        event: { id: '1' },
        market: { id: '111' }
      };

      update.type = 'sSELCN';
      update.id = Number(id);
      service.betsInLiveUpdateProgress = {
        [cashoutIds[0]]: {}
      };

      service.updateCashOutValue(update);
      expect(service.updateBetAccordingToPush).toHaveBeenCalledWith(betToUpdate, id, 'outcome', update.payload);
    });
  });

  it('updateLegPartResult: method testing', () => {
    const betItem = Object.assign({}, cashoutBet);
    const update = Object.assign({}, liveServeUpdate);

    update.id = 132557464;
    service.cashOutMapIndexService.event[update.id] = [{
      id: '127471'
    }];
    service.betsMap = {
      127471: betItem
    };

    service.updateLegPartResult('W', update);

    expect(betItem.leg[0].part[0].result).toBe('W');
  });

  it('should return same value of result if there is no event for update.id', () => {
    const betItem = Object.assign({}, cashoutBet);
    const update = Object.assign({}, liveServeUpdate);

    update.id = 11111;

    service.betsMap = {
      127471: betItem
    };

    betItem.leg[0].part[0].result = 'V';
    service.updateLegPartResult('L', update);
    expect(betItem.leg[0].part[0].result).toBe('V');
  });

  it('updatePlacedBetsStatuses: method testing', () => {
    const outcome = ['1'];
    const market = ['11'];
    const event = ['111'];

    service.betsMap = {
      12747111: {
        outcome,
        market,
        event
      }
    };

    spyOn(service, 'updateBetAccordingToPush');

    service.updatePlacedBetsStatuses(['12747111'], event[0], 'event', {});
    expect(service.updateBetAccordingToPush).toHaveBeenCalledTimes(1);

    delete service.betsMap['12747111'].event;
    service.updatePlacedBetsStatuses(['12747111'], market[0], 'market', {});
    expect(service.updateBetAccordingToPush).toHaveBeenCalledTimes(2);

    delete service.betsMap['12747111'].market;
    service.updatePlacedBetsStatuses(['12747111'], outcome[0], 'outcome', {});
    expect(service.updateBetAccordingToPush).toHaveBeenCalledTimes(3);
  });

  it('updateEventEntity: method testing', () => {
    const betItem: any = Object.assign({}, cashoutBet);
    const update = Object.assign({}, liveServeUpdate);

    let updateType = 'sSCBRD';

    update.id = 5447497;
    spyOn(service, 'eventClockUpdate');
    spyOn(service, 'eventCommentsUpdate');
    service.betsMap = {
      446974: betItem
    };
    service.cashOutMapIndexService.event[update.id] = [{ id: 446974, isSettled: undefined }];
    betItem.leg[0].eventEntity = {
      id: 5447497
    };
    service.updateEventEntity(updateType, update);

    expect(service.eventCommentsUpdate).toHaveBeenCalled();

    updateType = 'sCLOCK';
    service.updateEventEntity(updateType, update);

    expect(service.eventClockUpdate).toHaveBeenCalled();
  });

  it('updates should not be called in case if no cashoutBetsMap field', () => {
    const update = {
      id: 74636478
    };
    const updateType = 'sSCBRD';
    spyOn(service, 'eventClockUpdate');
    spyOn(service, 'eventCommentsUpdate');

    delete service.betsMap;
    service.updateEventEntity(updateType, update);

    expect(service.eventCommentsUpdate).not.toHaveBeenCalled();
    expect(service.eventClockUpdate).not.toHaveBeenCalled();
  });

  it('should update legs', () => {
    const betItem: any = Object.assign({}, cashoutBet);
    const updatedBet: any = Object.assign({}, cashoutBet);

    updatedBet.leg[0].part[0].dispResult = 'W';

    service.updateDispResult(betItem, updatedBet);

    expect(betItem.leg[0].part[0].dispResult).toBe('W');
  });

  describe('bet selection statuses testing', () => {
    let betItem,
      updateId,
      pushType,
      pushPayload;

    beforeEach(() => {
      betItem = JSON.parse(JSON.stringify(cashoutBet));
      updateId = '127471';
      pushType = 'event';
      pushPayload = {
        status: 'S',
        result: 'result'
      };
      betItem.leg[0].part[0].eventId = '2002602';
      betItem.leg[0].part[0].eventId = '2002602';
      betItem.leg[0].part[0].result = 'L';
      betItem.market = [
        '96042516'
      ];
      betItem.outcome = [
        '368091810'
      ];
      betItem.leg[0].eventEntity = {
        id: '2002602',
        markets: [
          {
            id: '96042516',
            outcomes: [
              {
                id: '368091810'
              }
            ]
          }
        ]
      };
    });

    it('updateBetSelectionsStatuses: method testing', () => {
      spyOn(service, 'updateLegStatus');

      service.updateBetSelectionsStatuses(betItem, updateId, pushType, pushPayload);
      expect(service.updateLegStatus).toHaveBeenCalled();
    });

    it('should not update leg status if no market or no outcome or different ids', () => {
      let modifiedBet = Object.assign({}, betItem);
      spyOn(service, 'updateLegStatus');

      modifiedBet.leg[0].eventEntity.id = 'ASDASD';
      service.updateBetSelectionsStatuses(modifiedBet, updateId, pushType, pushPayload);

      expect(service.updateLegStatus).not.toHaveBeenCalled();
      modifiedBet = Object.assign({}, betItem);
      modifiedBet.leg[0].eventEntity.markets[0].id = '12';
      service.updateBetSelectionsStatuses(modifiedBet, updateId, pushType, pushPayload);

      expect(service.updateLegStatus).not.toHaveBeenCalled();

      modifiedBet = Object.assign({}, betItem);
      modifiedBet.leg[0].eventEntity.markets[0].outcomes[0].id = '11';
      service.updateBetSelectionsStatuses(modifiedBet, updateId, pushType, pushPayload);

      expect(service.updateLegStatus).not.toHaveBeenCalled();
    });

    it('should not update leg status if no markets', () => {
      let modifiedBet = JSON.parse(JSON.stringify(betItem));
      spyOn(service, 'updateLegStatus');

      modifiedBet = Object.assign({}, betItem);
      modifiedBet.leg[0].eventEntity.markets = [];
      service.updateBetSelectionsStatuses(modifiedBet, updateId, pushType, pushPayload);

      expect(service.updateLegStatus).not.toHaveBeenCalled();
    });


    it('should not update leg status if no outcomes', () => {
      let modifiedBet = JSON.parse(JSON.stringify(betItem));
      spyOn(service, 'updateLegStatus');

      modifiedBet = Object.assign({}, betItem);
      modifiedBet.leg[0].eventEntity.markets[0].outcomes = [];
      service.updateBetSelectionsStatuses(modifiedBet, updateId, pushType, pushPayload);

      expect(service.updateLegStatus).not.toHaveBeenCalled();

    });

    describe('updateLegStatus', () => {
      let market,
        legItem,
        outcomes,
        ids: any;

      beforeEach(() => {
        spyOn(service, 'getLegStatus').and.returnValue('status');
        spyOn(service as any, 'normalizeUpdatedPartResult').and.callThrough();
        market = betItem.leg[0].eventEntity.markets[0];
        legItem = betItem.leg[0];
        outcomes = market.outcomes;
        ids = {
          event: ['127471'],
          market: ['127471'],
          outcome: ['127471', '490558404']
        };
      });

      describe('should update statuses correctly when changing status on different level', () => {
        describe('for event', () => {
          it('default case', () => {
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect((service as any).normalizeUpdatedPartResult).toHaveBeenCalledWith(legItem.part, null);
            expect(service.getLegStatus).toHaveBeenCalledWith('L', 'S', undefined, [undefined]);
          });
          it('unsuspend result', () => {
            pushPayload.status = 'A';
            market.marketStatusCode = 'A';
            outcomes[0].outcomeStatusCode = 'A';
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', 'A', ['A']);
          });

          describe('when status in payload', () => {
            beforeEach(() => {
              legItem.eventEntity.eventStatusCode = 'A';
              market.marketStatusCode = 'A';
              outcomes[0].outcomeStatusCode = 'A';
            });
            it('not defined - should not update status of market', () => {
              delete pushPayload.status;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', 'A', ['A']);
            });

            it('set to undefined explicitly - should update status of market', () => {
              pushPayload.status = undefined;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', undefined, 'A', ['A']);
            });
          });
        });

        describe('for market', () => {
          beforeEach(() => {
            pushType = 'market';
          });
          it('default case', () => {
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect((service as any).normalizeUpdatedPartResult).toHaveBeenCalledWith(legItem.part, null);
            expect(service.getLegStatus).toHaveBeenCalledWith('L', undefined, 'S', [undefined]);
          });

          it('unsuspend result', () => {
            pushPayload.status = 'A';
            legItem.eventEntity.eventStatusCode = 'A';
            outcomes[0].outcomeStatusCode = 'A';
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', 'A', ['A']);
          });

          describe('when status in payload', () => {
            let newMarket;
            beforeEach(() => {
              legItem.eventEntity.eventStatusCode = 'A';
              outcomes[0].outcomeStatusCode = 'A';
              newMarket = Object.assign({}, market, { name: 'TO BE SHOWN A CARD', marketStatusCode: 'S' });
            });
            it('not defined - should not update status of market', () => {
              delete pushPayload.status;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market: newMarket, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', 'S', ['A']);
            });

            it('set to undefined explicitly - should update status of market', () => {
              pushPayload.status = undefined;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market: newMarket, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', undefined, ['A']);
            });
          });
        });

        describe('for outcome', () => {
          beforeEach(() => {
            pushType = 'outcome';
            outcomes[0].id = '127471';
          });
          it('should not update leg status', () => {
            ids = { outcome: [] };
            legItem.status = null;
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect((service as any).normalizeUpdatedPartResult).not.toHaveBeenCalled();
            expect(legItem.status).toBe(null);
          });

          it('should call getLegStatus', () => {
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect((service as any).normalizeUpdatedPartResult).toHaveBeenCalledWith(legItem.part,
              { outcomeId: '127471', result: 'result' });
            expect(service.getLegStatus).toHaveBeenCalledWith('L', undefined, undefined, ['S']);
          });

          describe('should call getLegStatus (coverage case)', () => {
            beforeEach(() => {
              legItem.status = null;
              (service as any).getLegStatus.and.returnValue('');
            });
            it('status is empty string', () => {
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(legItem.status).toEqual('');
            });
            it('status is null', () => {
              pushPayload.status = '';
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(legItem.status).toEqual(null);
            });
          });

          it('unsuspend result', () => {
            pushPayload.status = 'A';
            market.marketStatusCode = 'A';
            legItem.eventEntity.eventStatusCode = 'A';
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
            expect(service.getLegStatus).toHaveBeenCalledWith('L', 'A', 'A', ['A']);
          });

          describe('when status in payload', () => {
            beforeEach(() => {
              legItem.eventEntity.eventStatusCode = 'S';
              market.marketStatusCode = 'S';
              outcomes[0].outcomeStatusCode = 'S';
            });
            it('is not defined - should not update status of market', () => {
              delete pushPayload.status;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', 'S', 'S', ['S']);
            });

            it('is set to undefined explicitly - should update status of market', () => {
              pushPayload.status = undefined;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('L', 'S', 'S', [undefined]);
            });
          });

          it('shouldn`t update outcome if updated outcome not belong to this bet', () => {
            service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId: '490558404' });
            expect(service.getLegStatus).toHaveBeenCalledWith('L', undefined, undefined, [undefined]);
          });

          describe('should handle handicap result', () => {
            beforeEach(() => {
              pushPayload.result = 'H';
              betItem.leg[0].part[0].result = 'H';
            });

            it('without part[0].dispResult', () => {
              betItem.leg[0].part[0].dispResult = undefined;
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith(undefined, undefined, undefined, ['S']);
            });
            it('with part[0].dispResult', () => {
              betItem.leg[0].part[0].dispResult = 'W';
              service.updateLegStatus({ bet: betItem, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
              expect(service.getLegStatus).toHaveBeenCalledWith('W', undefined, undefined, ['S']);
            });
            afterEach(() => {
              expect((service as any).normalizeUpdatedPartResult).toHaveBeenCalledWith(legItem.part, { outcomeId: '127471', result: 'H' });
            });
          });
        });
      });
    });
  });

  describe('normalizeUpdatedPartResult', () => {
    let parts;
    beforeEach(() => {
      parts = [
        { result: 'W', outcomeId: '101' },
        { result: 'L', outcome: '102' },
        { result: 'H', dispResult: 'V', outcomeId: '103' }
      ];
    });

    it('should return the result of BetHistoryMainService getPartsResult method call', () => {
      expect((service as any).normalizeUpdatedPartResult(parts as any, null)).toEqual('W');
    });

    describe('should call getPartsResult with existing partResults', () => {
      it('when updatedPart is not provided', () => {
        (service as any).normalizeUpdatedPartResult(parts as any, null);
      });
      it('when updatedPart has no "result" property', () => {
        (service as any).normalizeUpdatedPartResult(parts as any, {} as any);
      });
      it('when updatedPart has no "outcomeId" property', () => {
        (service as any).normalizeUpdatedPartResult(parts as any, { result: '-' } as any);
      });
      it('when updatedPart has outcomeId that is does not match any existing part outcomeId property', () => {
        (service as any).normalizeUpdatedPartResult(parts as any, { result: '-', outcomeId: '104' });
      });
      afterEach(() => {
        expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['W', 'L', 'V']);
      });
    });

    it('should call getPartsResult with partResults updated with provided data', () => {
      (service as any).normalizeUpdatedPartResult(parts as any, { result: '-', outcomeId: '103' });
      expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['W', 'L', '-']);
    });

    describe('should replace handicap result code of provided parts to the dispResult property values of existing parts', () => {
      it('(available)', () => {
        parts[0].result = 'H';
        parts[0].dispResult = 'L';
        (service as any).normalizeUpdatedPartResult(parts as any, { result: 'H', outcomeId: '103' });
        expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith(['L', 'L', 'V']);
      });
      it('(undefined if unavailable)', () => {
        parts[0].result = 'H';
        (service as any).normalizeUpdatedPartResult(parts as any, { result: 'H', outcomeId: '102' });
        expect(betHistoryMainService.getPartsResult).toHaveBeenCalledWith([undefined, undefined, 'V']);
      });
    });
  });

  describe('isHRCategory', () => {
    it('leg eventEntity as null', () => {
      const legs: any = [{eventEntity: null}];
      expect(service['isHRCategory'](legs)).toBe(false);
    });
  });
  describe('isEnabledBIRMarket', () => {
    it('BIRMarketsEnabled as null', () => {
      const legs: any = [{eventMarketDesc: 'win or each Way'}];
      service.BIRMarketsEnabled = null;
      expect(service['isEnabledBIRMarket'](legs)).toBe(false);
    });
    it('let part as null', () => {
      const legs: any = [{part: [null]}];
      service.BIRMarketsEnabled = ['win or each Way'];
      expect(service['isEnabledBIRMarket'](legs)).toBe(false);
    });
    it('eventMarketDesc as null', () => {
      const legs: any = [{part: [{eventMarketDesc: null}]}];
      service.BIRMarketsEnabled = ['win or each Way'];
      expect(service['isEnabledBIRMarket'](legs)).toBe(false);
    });
  });
  describe('updateBetFromProxyResponse', () => {
    it('_updateBetFromProxyResponse: method testing', () => {
      const betItem: any = Object.assign({
        resetCashoutSuspendedState: jasmine.createSpy('resetCashoutSuspendedState')
      }, cashoutBet);
      const updatedBetItem: any = Object.assign({}, cashoutBet);

      updatedBetItem.cashoutValue = '2.00';
      betItem.inProgress = false;
      betItem.isPartialInProgress = false;
      betItem.betModelService = {
        getPotentialPayout: jasmine.createSpy('getPotentialPayout')
      };

      service.updateBetFromProxyResponse(betItem, updatedBetItem);
      expect(betItem.cashoutValue).toBe('2.00');
      expect(betItem.resetCashoutSuspendedState).not.toHaveBeenCalled();
    });

    it('_updateBetFromProxyResponse should reset suspended state if shouldActivate is true', () => {
      const betItem: any = Object.assign({
        resetCashoutSuspendedState: jasmine.createSpy('resetCashoutSuspendedState')
      }, cashoutBet);
      const updatedBetItem: any = Object.assign({
        shouldActivate: true
      }, cashoutBet);

      updatedBetItem.cashoutValue = '2.00';
      betItem.inProgress = false;
      betItem.isPartialInProgress = false;
      betItem.betModelService = {
        getPotentialPayout: jasmine.createSpy('getPotentialPayout')
      };

      service.updateBetFromProxyResponse(betItem, updatedBetItem);
      expect(betItem.cashoutValue).toBe('2.00');
      expect(betItem.resetCashoutSuspendedState).toHaveBeenCalled();
    });

    it('should not update bet if update does not have cashout value', () => {
      const bet: any = { isConfirmed: true, inProgress: false, betId: 1 };
      const updatedBet: any = { cashoutStatus: 'Not available', betId: 1 };

      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.isConfirmed).toBeTruthy();
    });

    it('should not update bet if bet is in progress', () => {
      const bet: any = { isConfirmed: true, inProgress: true, betId: 1 };
      const updatedBet: any = { cashoutValue: '5.00', betId: 1 };

      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.isConfirmed).toBeTruthy();
    });

    it('should set cashout message as suspended', () => {
      const bet: any = {
        isConfirmed: true,
        inProgress: false,
        cashoutValue: '1',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        betId: 1,
        legType: 'E',
        leg: [{
          legNo: '1.00',
          legSort: { code: '--', name: '' },
          legType: { code: 'E', name: '' },
          part: [{
            banker: 'N',
            betBirIndex: '',
            betInRunning: 'N',
            eventMarketDesc: 'win or each Way'
          }],
          is_off: true,
          status: 'open',
          eventEntity: {
            categoryId: '21'
          }
        }]
      };
      const updatedBet: any = {
        cashoutValue: '1.00',
        cashoutStatus: '',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.cashoutValue).toBe('CASHOUT_SELN_SUSPENDED');
      bet.leg = null;
      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.cashoutValue).not.toBe('CASHOUT_SELN_SUSPENDED');
    });

    it('should update bet if updated bet has cashout value as not number', () => {
      const bet: any = {
        isConfirmed: true,
        inProgress: false,
        cashoutValue: '1.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        betId: 1
      };
      const updatedBet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: 'Not available',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);

      expect(bet).toEqual(jasmine.objectContaining({
        isConfirmed: false,
        isCashOutUnavailable: true,
        isPartialCashOutAvailable: false,
        cashoutStatus: updatedBet.cashoutStatus
      }));
      expect(cashoutErrorMessageService.getErrorMessage).toHaveBeenCalledWith(updatedBet);
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.UPDATE_CASHOUT_BET, bet);
    });

    it('should convert potentialPayout to N/A if value is numeric zero', () =>{
      const bet: any = {
        isConfirmed: true,
        inProgress: false,
        cashoutValue: '1.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        betId: 1,
        potentialPayout: 0
      };
      const updatedBet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: 'Not available',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);

      expect(bet.potentialPayout).toEqual("N/A");
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.UPDATE_CASHOUT_BET, bet);
    })

    it('should update bet"s stake and potential payout', () => {
      const bet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: 'Not available',
        isCashOutUnavailable: true,
        isPartialCashOutAvailable: false,
        stake: '1.00',
        stakePerLine: '1.00',
        potentialPayout: '3.00',
        betModelService: {
          getPotentialPayout: jasmine.createSpy('getPotentialPayout')
        },
        betId: 1
      };
      const updatedBet: any = {
        cashoutValue: '5.00',
        cashoutStatus: '',
        partialCashoutStatus: '',
        partialCashoutAvailable: 'Y',
        stake: '2.00',
        stakePerLine: '2.00',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);

      expect(bet).toEqual(jasmine.objectContaining({
        cashoutValue: '5.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        stake: '2.00',
        stakePerLine: '2.00'
      }));
      expect(bet.betModelService.getPotentialPayout).toHaveBeenCalledWith(updatedBet);
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.UPDATE_CASHOUT_BET, bet);
    });

    it('bet.isPartialactive should be false', () => {
      const bet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: 'Not available',
        isCashOutUnavailable: true,
        isPartialCashOutAvailable: false,
        isPartialActive: true,
        stake: '1.00',
        stakePerLine: '1.00',
        potentialPayout: '3.00',
        betModelService: {
          getPotentialPayout: jasmine.createSpy('getPotentialPayout')
        },
        betId: 1
      };
      const updatedBet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: '',
        partialCashoutStatus: '',
        partialCashoutAvailable: 'Y',
        stake: '2.00',
        stakePerLine: '2.00',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.isPartialActive).toBeFalsy();
    });

    it('bet.isPartialactive should be true', () => {
      const bet: any = {
        cashoutValue: 'CASHOUT_SELN_SUSPENDED',
        cashoutStatus: 'Not available',
        isCashOutUnavailable: true,
        isPartialCashOutAvailable: false,
        isPartialActive: true,
        stake: '1.00',
        stakePerLine: '1.00',
        potentialPayout: '3.00',
        betModelService: {
          getPotentialPayout: jasmine.createSpy('getPotentialPayout')
        },
        betId: 1
      };
      const updatedBet: any = {
        cashoutValue: '5.00',
        cashoutStatus: '',
        partialCashoutStatus: '',
        partialCashoutAvailable: 'Y',
        stake: '2.00',
        stakePerLine: '2.00',
        betId: 1
      };

      service.updateBetFromProxyResponse(bet, updatedBet);
      expect(bet.isPartialActive).toBeTruthy();
    });
  });

  describe('applyCashoutValueUpdate', () => {
    it('should not execute update process if bet is not found in betsMap', () => {
      const updatePayload: any = { betId: 1 };
      spyOn(service, 'updateBetFromProxyResponse');

      service.applyCashoutValueUpdate(updatePayload);
      expect(service.updateBetFromProxyResponse).not.toHaveBeenCalled();
    });

    it('should not execute update process if bet has some cashout status which means cashout is disabled', () => {
      const updatePayload: any = { betId: 1 };
      const betToUpdate = {
        betId: 1,
        cashoutStatus: 'SELN_SUSP'
      };

      spyOn(service, 'updateBetFromProxyResponse');
      service.betsMap = {
        1: betToUpdate
      };

      service.applyCashoutValueUpdate(updatePayload);
      expect(service.updateBetFromProxyResponse).not.toHaveBeenCalled();
    });

    it('should execute update process if bet has some cashout status but shouldActivate param is true', () => {
      const updatePayload: any = {
        betId: 1,
        cashoutValue: '0.09',
        cashoutStatus: '',
        shouldActivate: true
      };
      const betToUpdate = {
        betId: 1,
        cashoutStatus: 'SELN_SUSP',
        isCashedOut: false
      };

      spyOn(service, 'updateBetFromProxyResponse');
      service.betsMap = {
        1: betToUpdate
      };

      service.applyCashoutValueUpdate(updatePayload);
      expect(service.updateBetFromProxyResponse).toHaveBeenCalled();
    });

    it('should`t execute update process if bet cashoutStatus is not empty but bet is Cached out and shouldActivate param is true', () => {
      const updatePayload: any = {
        betId: 1,
        cashoutValue: '0.09',
        cashoutStatus: '',
        shouldActivate: true
      };
      const betToUpdate = {
        betId: 1,
        isCashedOut: true,
        cashoutStatus: 'BET_SETTLED',
      };

      spyOn(service, 'updateBetFromProxyResponse');
      service.betsMap = {
        1: betToUpdate
      };

      service.applyCashoutValueUpdate(updatePayload);
      expect(service.updateBetFromProxyResponse).not.toHaveBeenCalled();
    });

    it('should apply cashout value update and disable partial cashout', () => {
      const betToUpdate: any = {
        cashoutValue: '3.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        stake: '1.00',
        stakePerLine: '1.00',
        potentialPayout: '3.00',
        betId: 1
      };
      const updatePayload: any = {
        betId: 1,
        cashoutValue: '0.09',
        cashoutStatus: ''
      };

      service.betsMap = {
        1: betToUpdate
      };
      service.applyCashoutValueUpdate(updatePayload);

      expect(betToUpdate).toEqual(jasmine.objectContaining({
        cashoutValue: '0.09',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: false,
        stake: '1.00',
        stakePerLine: '1.00'
      }));
    });

    it('should apply cashout value update if partial cashout is enabled for bet', () => {
      const betToUpdate: any = {
        cashoutValue: '3.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: false,
        stake: '1.00',
        stakePerLine: '1.00',
        potentialPayout: '3.00',
        partialCashoutAvailable: 'Y',
        partialCashoutStatus: 'BET_LOW_CASHOUT',
        betId: 1
      };
      const updatePayload: any = {
        betId: 1,
        cashoutValue: '3.90',
        cashoutStatus: ''
      };

      service.betsMap = {
        1: betToUpdate
      };
      service.applyCashoutValueUpdate(updatePayload);

      expect(betToUpdate).toEqual(jasmine.objectContaining({
        cashoutValue: '3.90',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true
      }));
    });

    it('should apply cashout value update and disable partial', () => {
      const betToUpdate: any = {
        cashoutValue: '0.01',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: false,
        partialCashoutStatus: 'FREEBET_USED',
        betId: 1
      };
      const updatePayload: any = {
        betId: 1,
        cashoutValue: '3.00',
        cashoutStatus: ''
      };

      service.betsMap = {
        1: betToUpdate
      };
      service.applyCashoutValueUpdate(updatePayload);

      expect(betToUpdate).toEqual(jasmine.objectContaining({
        cashoutValue: '3.00',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: false
      }));
    });

    it('should handle only cashoutStatus update', () => {
      const betToUpdate: any = {
        cashoutValue: '1.01',
        cashoutStatus: '',
        isCashOutUnavailable: false,
        isPartialCashOutAvailable: true,
        partialCashoutStatus: '',
        betId: 1
      };
      const updatePayload: any = {
        betId: 1,
        cashoutStatus: 'CASHOUT_BET_NO_CASHOUT'
      };

      service.betsMap = {
        1: betToUpdate
      };
      service.applyCashoutValueUpdate(updatePayload);

      expect(betToUpdate).toEqual(jasmine.objectContaining({
        cashoutValue: '0.00',
        cashoutStatus: 'CASHOUT_BET_NO_CASHOUT',
        isCashOutUnavailable: true,
        isPartialCashOutAvailable: false
      }));
    });
  });

  describe('updateBetDetails', () => {
    beforeEach(() => {
      service['updateBetFromProxyResponse'] = jasmine.createSpy('updateBetFromProxyResponse');
    });

    it('should not call update fn if bet is not found in betsMap', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = { betId: 1 };

      service.updateBetDetails(updatedBet, Date.now(), updatePayloadFn);
      expect(updatePayloadFn).not.toHaveBeenCalled();
    });

    it('should not call update fn if bet lastTimeUpdate is newer then update timestamp', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = { betId: 1 };
      const timestamp = 1000;

      service.betsMap = {
        1: {
          lastTimeUpdate: timestamp + 1
        }
      };

      service.updateBetDetails(updatedBet, timestamp, updatePayloadFn);
      expect(updatePayloadFn).not.toHaveBeenCalled();
    });

    it('should not call update fn if bet lastTimeUpdate is equal with update timestamp', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = { betId: 1 };
      const timestamp = 1000;

      service.betsMap = {
        1: {
          lastTimeUpdate: timestamp
        }
      };

      service.updateBetDetails(updatedBet, timestamp, updatePayloadFn);
      expect(updatePayloadFn).not.toHaveBeenCalled();
    });
    it('should call updateBetFromProxy if bet is Cached out but should be deleted', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = {
        betId: 1,
        cashoutStatus: 'BET_SETTLED'
      };

      service.betsMap = {
        1: {
          lastTimeUpdate: 2,
          isCashedOut: true
        }
      };

      service.updateBetDetails(updatedBet, Date.now(), updatePayloadFn);
      expect(updatePayloadFn).toHaveBeenCalled();
      expect(service.updateBetFromProxyResponse).toHaveBeenCalled();
    });
    it('should`t call updateBetFromProxy if bet is Cached out and should`t be deleted', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = {
        betId: 1,
        cashoutStatus: ''
      };

      service.betsMap = {
        1: {
          lastTimeUpdate: 2,
          isCashedOut: true
        }
      };

      service.updateBetDetails(updatedBet, Date.now(), updatePayloadFn);
      expect(updatePayloadFn).toHaveBeenCalled();
      expect(service.updateBetFromProxyResponse).not.toHaveBeenCalled();
    });

    it('should`t call updateBetFromProxy if not cashoutStatus', () => {
      const updatedBet: any = {
        betId: 1,
      };

      service.betsMap = {
        1: {
          lastTimeUpdate: 2,
          isCashedOut: true
        }
      };

      service.updateBetDetails(updatedBet, 1234);
      expect(service.updateBetFromProxyResponse).not.toHaveBeenCalled();
    });

    it('should call updateBetFromProxy if bet is not Cached out', () => {
      const updatePayloadFn = jasmine.createSpy('updatePayloadFn');
      const updatedBet: any = {
        betId: 1,
        cashoutStatus: 'BET_SETTLED'
      };

      service.betsMap = {
        1: {
          lastTimeUpdate: 2,
          isCashedOut: false
        }
      };

      service.updateBetDetails(updatedBet, Date.now(), updatePayloadFn);
      expect(updatePayloadFn).toHaveBeenCalled();
      expect(service.updateBetFromProxyResponse).toHaveBeenCalled();
    });
  });

  describe('eventCommentsUpdate and eventClockUpdate methods:', () => {
    const payload = {
        ev_id: 111
      };
    let eventDataMock;

    beforeEach(() => {
      eventDataMock = Object.assign({}, eventMock);
    });

    it('eventCommentsUpdate', () => {

      service.eventCommentsUpdate(payload, eventDataMock);
      expect(commentsService.footballUpdateExtend).toHaveBeenCalled();
    });

    it('eventClockUpdate', () => {
      spyOn(eventDataMock.clock, 'refresh');
      service.eventClockUpdate(payload, eventDataMock);

      expect(eventDataMock.clock.refresh).toHaveBeenCalled();
    });

    it('refres should not be called', () => {
      const modifiedObj = Object.assign({}, payload);

      spyOn(eventDataMock.clock, 'refresh');

      modifiedObj.ev_id = 323;

      service.eventClockUpdate(modifiedObj, eventDataMock);

      expect(eventDataMock.clock.refresh).not.toHaveBeenCalled();
    });
  });

  describe('updateBetDetailsInitial', () => {
    let initialData: any;
    const timestamp = 1234;
    const betId = '2147501802';
    const potentialPayout = '0.17';
    const legType = 'W';
    const currency = 'GBP';
    const stakePerLine = '0.11';
    const tokenValue = '0.00';
    const stake = '0.11';
    const betType = 'SGL';

    beforeEach(() => {
      spyOn(service, 'updateBetDetails');

      initialData = {
        asyncDesc: '',
        asyncOriginalStake: '0.11',
        asyncStatus: 'A',
        betType: { code: betType, name: 'Single' },
        bonus: '',
        callId: '',
        cashoutValue: 'CASHOUT_SELN_NO_CASHOUT',
        date: '2020-05-26 08:14:44',
        id: betId,
        leg: [{
          legNo: '1',
          legSort: { code: '--', name: '' },
          legType: { code: legType, name: '' },
          part: [{
            banker: 'N',
            betBirIndex: '',
            betInRunning: 'N'
          }]
        }],
        numLegs: '1',
        numLines: '1',
        numLinesLose: '0',
        numLinesVoid: '0',
        numLinesWin: '0',
        numSelns: '1',
        paid: 'Y',
        partialCashoutAvailable: 'N',
        placedBy: '',
        potentialPayout: [{ value: potentialPayout }],
        receipt: 'O/300053740/0000120',
        settleInfoAttribute: '',
        settled: 'N',
        settledAt: '',
        source: 'M',
        stake: { type: 'current', value: stake, currency, stakePerLine, tokenValue },
        status: 'A',
        tax: '0.00',
        taxRate: '0.00',
        taxType: 'S',
        uniqueId: '017158898927117407076465155273',
        userId: '',
      };
    });

    it(`should define missed properties and updateBetDetails`, () => {
      service.updateBetDetailsInitial(initialData, timestamp);

      expect(initialData).toEqual(jasmine.objectContaining({
        betId, potentialPayout, legType, currency, stakePerLine, tokenValue, stake, betType
      }));
      expect(service.updateBetDetails).toHaveBeenCalledWith(initialData, timestamp);
    });

    it(`should NOT replace betId by id if it exsists`, () => {
      initialData.betId = betId;
      delete initialData.id;
      service.updateBetDetailsInitial(initialData, timestamp);

      expect(initialData.betId).toEqual(betId);
    });

    describe('potentialPayout should be not changed if potentialPayout', () => {
      let potentialPayoutRes;
      it(`is Not array`, () => {
        initialData.potentialPayout = potentialPayoutRes = 'sdfsdf';
      });
      it(`does not have 0 element`, () => {
        initialData.potentialPayout = [];
        potentialPayoutRes = undefined;
      });
      it(`0 element does not have value`, () => {
        delete initialData.potentialPayout[0].value;
        potentialPayoutRes = undefined;
      });
      afterEach(() => {
        service.updateBetDetailsInitial(initialData, timestamp);

        expect(initialData.potentialPayout).toEqual(potentialPayoutRes);
      });
    });

    describe('legType should be not defined if leg', () => {
      it(`is Not array`, () => {
        initialData.leg = 'sdfsdf';
      });
      it(`does not have 0 element`, () => {
        initialData.leg = [];
      });
      it(`0 element does not have legType`, () => {
        delete initialData.leg[0].legType;
      });
      afterEach(() => {
        service.updateBetDetailsInitial(initialData, timestamp);

        expect(initialData.legType).toBeUndefined();
      });
    });

    it(`should Not define properties if it is Not object `, () => {
      initialData.stake = stake;

      service.updateBetDetailsInitial(initialData, timestamp);

      ['currency', 'stakePerLine', 'tokenValue'].forEach((key) => {
        expect(initialData[key]).toBeUndefined();
      });
      expect(initialData.stake).toEqual(stake);
    });

    it(`should not change betType if it not object`, () => {
      initialData.betType = betType;

      service.updateBetDetailsInitial(initialData, timestamp);
      expect(initialData.betType).toEqual(betType);
    });
  });

  describe('updateEventDetail', () =>{

    it('should publish EVENT_FINSHED if the VOD EXITS', () =>{
      service.updateEventDetail( {      
          "eventId": "240801945",
          "vod": true        
      });
      expect(pubsubService.publish).toHaveBeenCalledWith('EVENT_FINSHED',"240801945");
    })
    it('should publish EVENT_FINSHED if the VOD false EXITS', () =>{
      service.updateEventDetail( 
        {
          "eventId": "240801945",
          "vod": false
        
      });
      expect(pubsubService.publish).not.toHaveBeenCalled();
    })

    it('should publish EVENT_FINSHED if the VOD property EXITS', () =>{
      service.updateEventDetail({
          "eventId": "240801945",
        }
      );
      expect(pubsubService.publish).not.toHaveBeenCalled();
    })

  });
  describe('update2UpSelection', () =>{
    it('should publish twoup', () =>{
      service.update2UpSelection({selectionId:555,twoUpSettled:false} as any);
      expect(pubsubService.publish).toHaveBeenCalledWith('TWO_UP_UPDATE',{selectionId:555,twoUpSettled:false} as any);
    });
  })
  describe('updatePayoutDetails', () =>{

    it('should publish the returned value if the returned value is not null', () =>{
      service.betsMap = { "12345" : { potentialPayout: 0.01 }};
      service.updatePayoutDetails([{returns: 0.01, betNo:"12345"}]);
      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.PAYOUT_UPDATE, {updatedReturns: [{returns: 0.01, betNo:"12345"}] });
    })

    it('should not publish the returned value if the returned value is null', () =>{
      service.updatePayoutDetails([]);
      expect(pubsubService.publish).not.toHaveBeenCalled();
    })

  })

  describe('getLegStatus method:', () => {
    let result;
    let eventStatusCode;
    const marketStatusCode = '';
    const selectionStatusCode = '';

    beforeEach(() => {
      result = '';
      eventStatusCode = '';
    });

    it('in case if no result code', () => {
      expect(service.getLegStatus(result, eventStatusCode, marketStatusCode, selectionStatusCode)).toEqual('');
    });

    it('in case if result "won"', () => {
      result = 'W';
      expect(service.getLegStatus(result, eventStatusCode, marketStatusCode, selectionStatusCode)).toEqual('won');
    });

    it('in case if satus open', () => {
      result = '-';
      expect(service.getLegStatus(result, eventStatusCode, marketStatusCode, selectionStatusCode)).toEqual('open');
    });

    it('in case if suspended', () => {
      eventStatusCode = 'S';
      expect(service.getLegStatus(result, eventStatusCode, marketStatusCode, selectionStatusCode)).toEqual('suspended');
    });
  });

  describe('getCashOutIdForUpdate', () => {
    describe('should return cash out bets which have event/market/outcome', () => {
      beforeEach(() => {
        service.cashOutMapIndexService.outcome = { 123: [{ id: 456, isSettled: undefined }] };
        service.betsMap = { 456: { outcomes: { 123: {} }, isDisable: false }, mapState: {} };
      });
      it('when betsMap does not contain mapState property and contains bets', () => {});
      it('when betsMap contains mapState, but isEmpty is falsy', () => {
        service.betsMap.mapState = {};
      });
      afterEach(() => {
        const result = service.getCashOutIdForUpdate('outcome', '123', { status: 'some_status' });
        expect(result).toEqual([456]);
      });
    });

    describe('should return empty array', () => {
      beforeEach(() => {
        service.placedBets = undefined;
      });
      it('when betsMap is not defined', () => {
        service.betsMap = undefined;
      });
      it('when betsMap mapState.isEmpty is true', () => {
        service.betsMap = { mapState: { isEmpty: true } };
      });

      afterEach(() => {
        const result = service.getCashOutIdForUpdate('outcome', '123', { status: 'some_status' });
        expect(result).toEqual([]);
      });
    });
  });

  describe('updateBetAccordingToPush', () => {
    let originalBet, bet, type, id, updatePayload;

    beforeEach(() => {
      originalBet = {
        events: { '123': { displayed: 'N', status: 'S' } },
        markets: { '45': { displayed: 'N', status: 'S' } },
        outcomes: { '76': { displayed: 'N', status: 'S', settled: 'Y' } }
      };
      bet = JSON.parse(JSON.stringify(originalBet));
      updatePayload = { displayed: 'Y', status: 'A', some_other: 'value' };
      spyOn(service as any, 'updateBetSelectionsStatuses').and.callThrough();
    });

    it('should update valid items from push update', () => {
      type = 'event';
      id = '123';
      service.updateBetAccordingToPush(bet, id, type, updatePayload);
      expect(bet.events).toEqual({ 123: { displayed: 'Y', status: 'A' } });
      expect(bet.markets).toEqual(originalBet.markets);
      expect(bet.outcomes).toEqual(originalBet.outcomes);
    });

    it('should create entry with items from push update', () => {
      type = 'market';
      id = '54';
      service.updateBetAccordingToPush(bet, id, type, updatePayload);
      expect(bet.markets).toEqual({
        45: { displayed: 'N', status: 'S' },
        54: { displayed: 'Y', status: 'A' }
      });
      expect(bet.events).toEqual(originalBet.events);
      expect(bet.outcomes).toEqual(originalBet.outcomes);
    });

    it('should not update items if they are not defined in push update', () => {
      type = 'outcome';
      id = '76';
      updatePayload = { lp_den: '10', lp_num: '3' };
      service.updateBetAccordingToPush(bet, id, type, updatePayload);
      expect(bet.outcomes).toEqual({ 76: { displayed: 'N', status: 'S', settled: 'Y', lp_den: '10', lp_num: '3' } });
      expect(bet.events).toEqual(originalBet.events);
      expect(bet.market).toEqual(originalBet.market);
    });

    it('should not create missing fields if they are not defined in push update', () => {
      type = 'market';
      id = '45';
      delete bet.markets[45].status;
      updatePayload = { displayed: 'Y' };
      service.updateBetAccordingToPush(bet, id, type, updatePayload);
      expect(bet.markets).toEqual({ 45: { displayed: 'Y' } });
      expect(bet.outcomes).toEqual(originalBet.outcomes);
      expect(bet.events).toEqual(originalBet.events);
    });


    afterEach(() => {
      expect(service.updateBetSelectionsStatuses).toHaveBeenCalledWith(bet, id, type, updatePayload);
      expect(pubsubService.publish).toHaveBeenCalledWith('EMA_HANDLE_BET_LIVE_UPDATE', { id, type, updatePayload });
    });
  });

  describe('BMA-40873. UpdateEventEntity for live scores updates', () => {
    it('updateEventEntity should publish CASHOUT_LIVE_SCORE_EVENT_UPDATE', () => {
      const betItem: any = Object.assign({}, cashoutBet);
      const update: any = Object.assign({}, liveServeUpdate);

      const updateType = 'sEVENT';

      update.id = 5447497;
      service.betsMap = {
        446974: betItem
      };
      service.cashOutMapIndexService.event[update.id] = [{ id: 446974, isSettled: undefined }];
      betItem.leg[0].eventEntity = {
        id: 5447497
      };
      spyOn<any>(service, 'updateScoresFromNames');
      service['updateEventEntity'](updateType, update);
      update.payload.scores = {};
      update.payload.scoreType = 'Simple';

      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.CASHOUT_LIVE_SCORE_EVENT_UPDATE, update);
    });

    it('updateEventEntity should publish CASHOUT_LIVE_SCORE_EVENT_UPDATE', () => {
      const update = {payload: {}} as any;
      spyOn<any>(service, 'eventCommentsUpdate');
      service['updateEventEntity']('sSCBRD', update);

      expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.CASHOUT_LIVE_SCORE_UPDATE, update);
    });
  });
  describe('updateScoresFromNames', () => {
    it('should set scoreType', () => {
      const event = {} as any;
      service.updateScoresFromNames({
        scoreType: 'Simple'
      } as any, event as any);
      expect(event.scoreType).toEqual('Simple');
    });
    it('should set score in case if comments already exist', () => {
      const event = {
        comments: {
          teams: {
            scores: {
              home: 'oldHome',
              away: 'oldAway'
            }
          }
        }
      } as any;
      const payload = {
        scores: {
          home: 'home',
          away: 'away'
        }
      } as any;
      service.updateScoresFromNames(payload as any, event as any);
      expect(commentsService.sportUpdateExtend).toHaveBeenCalledWith(event.comments, payload.scores);
    });
    it('should set score in case if comments not exists yet', () => {
      const event = {} as any;
      const payload = {
        scores: {
          home: 'home',
          away: 'away'
        }
      } as any;
      service.updateScoresFromNames(payload as any, event as any);
      expect(commentsService.sportUpdateExtend).not.toHaveBeenCalled();
      expect(event.comments.teams).toEqual(payload.scores);
    });
  });

  describe('updatePredicate', () => {
    beforeEach(() => {
      service.placedBets = { '111': {} };
    });

    describe('should return true when there is difference in updated props of non-Tote bet, defined in betsMap', () => {
      it('when bet is isDisable, but is inProgress', () => {
        service.betsMap = { '111': { isDisable: true, inProgress: true } };
      });
      afterEach(() => {
        expect(service['updatePredicate']('111', 'event', { status: 'S'}, {})).toBeTruthy();
      });
    });
    describe('should return false', () => {
      let updateType, updatedElement;

      beforeEach(() => {
        updateType = 'event';
        updatedElement = {};
      });
      it('when betsMap is not defined', () => {
        service.placedBets = undefined;
      });

      it('when betsMap does not contain specified betId', () => {
        service.placedBets = { '222': {} };
      });

      it('when specified bet is a Tote bet', () => {
        service.placedBets = { '111': { isToteBet: true } };
      });

      it('when specified bet is Disabled ans is not in progress', () => {
        service.placedBets = { '111': { isDisable: true, inProgress: false } };
      });

      it('when specified update type is not defined in config', () => {
        updateType = 'not-event';
      });

      it('when there is no difference in significant properties of updated element and push data', () => {
        updatedElement = { status: 'S', prop: 'value' };
      });

      afterEach(() => {
        expect(service['updatePredicate']('111', updateType, { status: 'S' }, updatedElement)).toBeFalsy();
      });
    });
  });

  describe('eventStartedUpdate', () => {
    it('should publish event id if event started and active', () => {
      const update = {
        id: 123456,
        payload: {
          started: 'Y',
          status: 'A',
          is_off: 'Y'
        }
      } as any;

      service['eventStartedUpdate'](update);

      expect(pubsubService.publish).toHaveBeenCalledWith('EVENT_STARTED', '123456');
    });

    it('should not publish event id if event is not started', () => {
      const update = {
        id: 123456,
        payload: {
          started: 'N',
          status: 'A'
        }
      } as any;

      service['eventStartedUpdate'](update);

      expect(pubsubService.publish).not.toHaveBeenCalled();
    });

    it('should not publish event id', () => {
      const update = {
        id: 123456,
        payload: {
          started: 'Y',
          status: 'S'
        }
      } as any;

      service['eventStartedUpdate'](update);

      expect(pubsubService.publish).not.toHaveBeenCalled();
    });
  });
});
