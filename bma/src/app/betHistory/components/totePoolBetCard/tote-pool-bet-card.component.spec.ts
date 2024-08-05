import { fakeAsync } from '@angular/core/testing';
import { TotePoolBetCardComponent } from './totePoolBetCard.component';
import { of } from 'rxjs';

describe('TotePoolBetCardComponent', () => {
  let component: TotePoolBetCardComponent;
  let router;
  let toteService;

  const fakeEdpUrl = 'event/id';

  beforeEach(() => {
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    toteService = {
      getToteLink: jasmine.createSpy('getToteLink').and.returnValue(of(fakeEdpUrl))
    };

    spyOn(console, 'warn');

    component = new TotePoolBetCardComponent(router, toteService);
  });

  describe('@goToEvent', () => {

    it('should not start redirection if passed pool does not exist', () => {
      component.goToEvent(null);

      expect(toteService.getToteLink).not.toHaveBeenCalled();
    });

    it('should not start redirection if passed pool has neither eventId neither toteEventId', () => {
      component.goToEvent({leg: [{eventId: undefined, toteEventId: undefined}]} as any);

      expect(toteService.getToteLink).not.toHaveBeenCalled();
    });

    it('should start redirection if at least eventId is specified', () => {
      component.goToEvent({leg: [{eventId: '12345'}]} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
    });

    it('should start redirection if at least toteEventId is specified', () => {
      component.goToEvent({leg: [{toteEventId: '12345'}]} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
    });

    it('should redirect if passed pool contains enough data', fakeAsync(() => {
      component.goToEvent({leg: [{toteEventId: '12345'}]} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalled();
    }));

    it('should skip redirect if something went wrong', fakeAsync(() => {
      toteService.getToteLink.and.returnValue(of(''));
      component.goToEvent({leg: [{toteEventId: '12345'}]} as any);

      expect(toteService.getToteLink).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    }));
  });

  it('trackByFn should return unique identifier', () => {
    expect(component.trackByFn(2, { id: 5 } as any)).toEqual('2_5');
  });

  describe('getOutcomeTitle', () => {
    it('should return empty string if pool is not defined', () => {
      component.pool = undefined;
      expect(component.getOutcomeTitle({} as any, 0)).toEqual('');
    });
    it('should return position of runner and his name for the ordered bet', () => {
      component.pool = {
        isOrderedBet: true
      } as any;
      expect(component.getOutcomeTitle({
        name: 'Rockie Balboa'
      } as any, 0)).toEqual('1. Rockie Balboa');
    });

    describe('in not ordered bet case', () => {
      beforeEach(() => {
        component.pool = {
          isOrderedBet: false
        } as any;
      });

      it('should return only runner name if there is only one runner ', () => {
        component.pool.poolOutcomes = new Array(1);
        expect(component.getOutcomeTitle({
          name: 'Rockie Balboa',
          isFavourite: true,
          runnerNumber: 8
        } as any, 0)).toEqual('Rockie Balboa');
      });

      it('should return only runner name if runner is Unnamed Favourite ', () => {
        component.pool.poolOutcomes = new Array(2);
        expect(component.getOutcomeTitle({
          name: '2nd Unnamed Favourite',
          isFavourite: true
        } as any, 0)).toEqual('2nd Unnamed Favourite');
      });

      it('should return runner number with runner name if runner is not Unnamed Favourite', () => {
        component.pool.poolOutcomes = new Array(2);
        expect(component.getOutcomeTitle({
          name: 'Rockie Balboa',
          isFavourite: false,
          runnerNumber: 8
        } as any, 0)).toEqual('8. Rockie Balboa');
      });
    });
  });

  describe('isEventLive', () => {
    it('should return false if there is no leg of eventEntity provided', () => {
      expect(component.isEventLive(undefined)).toBeFalsy();
      expect(component.isEventLive({} as any)).toBeFalsy();
    });
    it('should return true if eventIsLive is true', () => {
      const leg = {
        eventEntity: {
          eventIsLive: true
        }
      };
      expect(component.isEventLive(leg as any)).toBeTruthy();
    });
    it('should return false if event is not started', () => {
      const leg = {
        eventEntity: {
          eventIsLive: false,
          isStarted: false
        }
      };
      expect(component.isEventLive(leg as any)).toBeFalsy();
    });
    it('should return true if event is started started and not finished', () => {
      const leg = {
        eventEntity: {
          eventIsLive: false,
          isStarted: true,
          isFinished: false
        }
      };
      expect(component.isEventLive(leg as any)).toBeTruthy();
    });
    it('should return true if event is started started and not resulted', () => {
      const leg = {
        eventEntity: {
          eventIsLive: false,
          isStarted: true,
          isResulted: false
        }
      };
      expect(component.isEventLive(leg as any)).toBeTruthy();
    });
    it('should return false if event is started started and resulted', () => {
      const leg = {
        eventEntity: {
          eventIsLive: false,
          isStarted: true,
          isResulted: true
        }
      };
      expect(component.isEventLive(leg as any)).toBeFalsy();
    });
    it('should return false if event is started started and finished', () => {
      const leg = {
        eventEntity: {
          eventIsLive: false,
          isStarted: true,
          isFinished: true
        }
      };
      expect(component.isEventLive(leg as any)).toBeFalsy();
    });
  });
});
