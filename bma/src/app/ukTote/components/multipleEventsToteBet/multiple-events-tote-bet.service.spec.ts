import { of } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';

import { MultipleEventsToteBetService } from './multiple-events-tote-bet.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('MultipleEventsToteBetService', () => {
  let ukToteLiveUpdatesService;
  let pubSubService;
  let racingPostService;
  let service: MultipleEventsToteBetService;

  beforeEach(() => {
    ukToteLiveUpdatesService = {
      updateEventStatus: jasmine.createSpy('updateEventStatus'),
      updateMarketStatus: jasmine.createSpy('updateMarketStatus'),
      updateOutcomeStatus: jasmine.createSpy('updateOutcomeStatus')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    racingPostService = {
      getHorseRacingPostById: jasmine.createSpy('getHorseRacingPostById'),
      addRacingFormOutcome: jasmine.createSpy('addRacingFormOutcome')
    };

    service = new MultipleEventsToteBetService(
      ukToteLiveUpdatesService,
      pubSubService,
      racingPostService
    );
  });

  describe('setRacingForm', () => {
    it('add racing form to outcome', fakeAsync(() => {
      racingPostService.getHorseRacingPostById.and.returnValue(of({
        document: {
          '123': { horses: [{ saddle: '1' }] }
        }
      }));

      const events: any = [{
        linkedEventId: 123,
        markets: [{
          outcomes: [{ name: 'Zero' }, { name: 'Unnamed favourite' }]
        }]
      }, {
        linkedEventId: undefined
      }];

      service.setRacingForm(events).subscribe();
      tick();

      expect(racingPostService.getHorseRacingPostById).toHaveBeenCalledWith('123');
      expect(racingPostService.addRacingFormOutcome).toHaveBeenCalledTimes(1);
    }));

    it('no linked events', fakeAsync(() => {
      service.setRacingForm([{}] as any).subscribe();
      tick();
      expect(racingPostService.getHorseRacingPostById).not.toHaveBeenCalled();
    }));

    it('racing post error', fakeAsync(() => {
      racingPostService.getHorseRacingPostById.and.returnValue(of({ Error: 'error' }));

      service.setRacingForm([{ linkedEventId: 1 }] as any).subscribe();
      tick();

      expect(racingPostService.addRacingFormOutcome).not.toHaveBeenCalled();
    }));

    it('no racing post data', fakeAsync(() => {
      racingPostService.getHorseRacingPostById.and.returnValue(of({}));

      service.setRacingForm([{ linkedEventId: 1 }] as any).subscribe();
      tick();

      expect(racingPostService.addRacingFormOutcome).not.toHaveBeenCalled();
    }));
  });

  describe('updateLeg and changeLegs', () => {
    let liveUpdate;
    let legsArray;

    beforeEach(() => {
      liveUpdate = {
        id: 7,
        type: 'sEVENT',
        payload: {
          ev_id: 5,
          ev_mkt_id: 27,
        }
      } as any;

      legsArray = [
        {
          name: 'oneLeg',
          index: 1,
          linkedMarketId: 27,
          event: {
            linkedEventId: 7,
          }
        } as any
      ];

      service['updateSuspendedStatus'] = jasmine.createSpy('updateSuspendedStatus');
    });

    it('updateLegEvent', () => {
      service.updateLegEvent(legsArray, liveUpdate);
      expect(ukToteLiveUpdatesService.updateEventStatus).toHaveBeenCalledWith(legsArray[0].event, liveUpdate);
      expect(service['updateSuspendedStatus']).toHaveBeenCalledWith(legsArray[0]);
    });

    it('updateLegEvent return undefined', () => {
      legsArray[0].event.linkedEventId = 3;

      const result = service.updateLegEvent(legsArray, liveUpdate);
      expect(ukToteLiveUpdatesService.updateEventStatus).not.toHaveBeenCalled();
      expect(service['updateSuspendedStatus']).not.toHaveBeenCalled();
      expect(result).toBeUndefined();
    });

    it('updateLegMarket', () => {
      legsArray[0].event.linkedEventId = 5;

      service.updateLegMarket(legsArray, liveUpdate);
      expect(ukToteLiveUpdatesService.updateMarketStatus).toHaveBeenCalledWith(legsArray[0].event, liveUpdate);
      expect(service['updateSuspendedStatus']).toHaveBeenCalledWith(legsArray[0]);
    });

    it('updateLegOutcome', () => {
      service.updateLegOutcome(legsArray, liveUpdate);
      expect(ukToteLiveUpdatesService.updateOutcomeStatus).toHaveBeenCalledWith(legsArray[0].event, liveUpdate);
      expect(service['updateSuspendedStatus']).toHaveBeenCalledWith(legsArray[0]);
    });

    it('updateLegOutcome return undefined', () => {
      legsArray[0].linkedMarketId = 34;

      const result = service.updateLegOutcome(legsArray, liveUpdate);
      expect(ukToteLiveUpdatesService.updateOutcomeStatus).not.toHaveBeenCalled();
      expect(service['updateSuspendedStatus']).not.toHaveBeenCalled();
      expect(result).toBeUndefined();
    });

    it('changeLegsWithLiveUpdate called updateLegEvent', () => {
      service['updateLegEvent'] = jasmine.createSpy('updateLegEvent');

      service.changeLegsWithLiveUpdate(legsArray, liveUpdate);
      expect(service.updateLegEvent).toHaveBeenCalledWith(legsArray, liveUpdate);
    });

    it('changeLegsWithLiveUpdate called updateLegMarket', () => {
      liveUpdate.type = 'sEVMKT';
      service['updateLegMarket'] = jasmine.createSpy('updateLegMarket');

      service.changeLegsWithLiveUpdate(legsArray, liveUpdate);
      expect(service.updateLegMarket).toHaveBeenCalledWith(legsArray, liveUpdate);
    });

    it('changeLegsWithLiveUpdate called updateLegMarket', () => {
      liveUpdate.type = 'sSELCN';
      service['updateLegOutcome'] = jasmine.createSpy('updateLegOutcome');

      service.changeLegsWithLiveUpdate(legsArray, liveUpdate);
      expect(service.updateLegOutcome).toHaveBeenCalledWith(legsArray, liveUpdate);
    });

    it('changeLegsWithLiveUpdate called default', () => {
      liveUpdate.type = '';
      expect(service.changeLegsWithLiveUpdate(legsArray, liveUpdate)).toBeUndefined();
    });
  });

  it('updateSuspendedStatus', () => {
    const legToUpdate = {
      name: 'legUpdate',
      index: 1,
      updateSuspendedStatus: () => {}
    } as any;

    service['updateSuspendedStatus'](legToUpdate);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.UK_TOTE_LEG_UPDATED, legToUpdate);
  });

});
