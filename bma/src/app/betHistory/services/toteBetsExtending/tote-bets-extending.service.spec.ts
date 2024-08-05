import { of as observableOf } from 'rxjs';
import { ToteBetsExtendingService } from '@app/betHistory/services/toteBetsExtending/tote-bets-extending.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('ToteBetsExtendingService', () => {
  let service: ToteBetsExtendingService;
  let siteServerFactory, ukToteEventsLinkingService;
  let totePoolBetBaseArray;
  const totePoolBet = {
    leg: [{
      part: [{
        outcome: {
          event: {
            id: '1'
          }
        }
      }]
    }],
    isScoop6Pool: true
  };

  beforeAll(() => {
    siteServerFactory = {
      getEventsByOutcomeIds: jasmine.createSpy().and.returnValue(Promise.resolve())
    };
    ukToteEventsLinkingService = {
      extendToteEvents: jasmine.createSpy().and.callFake(x => observableOf(x))
    };
    totePoolBetBaseArray = [];

    service = new ToteBetsExtendingService(
      siteServerFactory as any,
      ukToteEventsLinkingService as any
    );
  });

  afterAll(() => {
    service = null;
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#loadEventsForToteBets: should load event for tote events', fakeAsync(() => {
    service.loadEventsForToteBets(null).subscribe(() => {
      expect(siteServerFactory.getEventsByOutcomeIds).not.toHaveBeenCalled();
    });
    tick();

    service.loadEventsForToteBets(totePoolBetBaseArray).subscribe(() => {
      expect(siteServerFactory.getEventsByOutcomeIds).not.toHaveBeenCalled();
    });
    tick();

    totePoolBetBaseArray.push(totePoolBet);
    service.loadEventsForToteBets(totePoolBetBaseArray).subscribe(() => {
      expect(siteServerFactory.getEventsByOutcomeIds).toHaveBeenCalled();
    });
    tick();
  }));

  it('#getScoop6EventIds: should Get Scoop6 event ids', () => {
    const arr = [];
    arr.push(totePoolBet);
    expect(ToteBetsExtendingService.getScoop6EventIds(arr)).toEqual(['1']);
  });

  it('#updateEntityId: should set linkedEntityId property of mainEntity', () => {
    const mainEntityStub = { linkedEntityId: '' } as any,
          extendingEntityStub = { id: 1 } as any;

    ToteBetsExtendingService.updateEntityId(mainEntityStub, extendingEntityStub);
    expect(mainEntityStub.linkedEntityId).toBe(1);
  });

  it('#setLinkedId: should set linkedEntityId property of mainEntity', () => {
    let linkedEntitiesMap = {},
        entityStub = {
          linkedEntityId: 2,
          id: 1
        } as any;

    ToteBetsExtendingService.setLinkedId(linkedEntitiesMap, entityStub);
    expect(linkedEntitiesMap['1']).toBe('2');

    linkedEntitiesMap = {};
    entityStub = {} as any;
    ToteBetsExtendingService.setLinkedId(linkedEntitiesMap, entityStub);
    expect(linkedEntitiesMap).toEqual({});
  });

  it('#extendToteBetsWithEvents: should extend TOTE events with fixed odds events', fakeAsync(() => {
    const betsMap = {
      'x': {
        isToteBet: true,
        fixedEventLinked: false,
        extendWithLinkedEvents: jasmine.createSpy('extendWithLinkedEvents'),
        addLiveUpdatesProperties: jasmine.createSpy('addLiveUpdatesProperties'),
        leg: [
          {
            part: [
              {
                outcome: {
                  event: {
                    id: 'TOTE_event_111'
                  }
                }
              }
            ]
          }
        ]
      },
      'y': {
        isToteBet: true,
        isScoop6Pool: true,
        fixedEventLinked: false,
        extendWithLinkedEvents: jasmine.createSpy('extendWithLinkedEvents'),
        addLiveUpdatesProperties: jasmine.createSpy('addLiveUpdatesProperties'),
        leg: [
          {
            part: [
              {
                outcome: {
                  event: {
                    id: 'TOTE_event_222'
                  }
                }
              }
            ]
          }
        ]
      },
    } as any;

    const toteEvents = [
      {
        id: 'TOTE_event_111',
        linkedEntityId: 'NON_TOTE_event_111',
        markets: [
          {
            id: 'TOTE_mkt_111',
            linkedEntityId: 'NON_TOTE_mkt_111',
            outcomes: [
              {
                id: 'TOTE_out_111',
                linkedEntityId: 'NON_TOTE_out_111',
              }
            ]
          }
        ]
      },
      {
        id: 'TOTE_event_222',
        markets: [
          {
            id: 'TOTE_mkt_222',
            outcomes: [
              {
                id: 'TOTE_out_222',
              }
            ]
          }
        ]
      }];

    const linkedEntitiesMap =  {
      TOTE_event_111: 'NON_TOTE_event_111',
      TOTE_mkt_111: 'NON_TOTE_mkt_111',
      TOTE_out_111: 'NON_TOTE_out_111'
    };

    spyOn(service, 'loadEventsForToteBets').and.returnValue(observableOf(toteEvents as any));
    spyOn<any>(service, 'generateLinkedEntitiesMap').and.callThrough();

    service.extendToteBetsWithEvents(betsMap).subscribe(() => {
      expect(ukToteEventsLinkingService.extendToteEvents).toHaveBeenCalledWith([toteEvents[0]], false, jasmine.anything());
      expect(ukToteEventsLinkingService.extendToteEvents).toHaveBeenCalledWith([toteEvents[1]], true, jasmine.anything());
      Object.values(betsMap).forEach(bet => {
        expect((bet as any).extendWithLinkedEvents).toHaveBeenCalledWith(linkedEntitiesMap);
        expect((bet as any).addLiveUpdatesProperties).toHaveBeenCalled();
      });
    });
    tick();
  }));

  describe('extendToteEvents', () => {
    it('should not fail in case of no events passed', () => {
      service['extendToteEvents']([], []);
      expect(ukToteEventsLinkingService.extendToteEvents).toHaveBeenCalledWith([], true, jasmine.anything());
      expect(ukToteEventsLinkingService.extendToteEvents).toHaveBeenCalledWith([], false, jasmine.anything());
    });
  });

});
