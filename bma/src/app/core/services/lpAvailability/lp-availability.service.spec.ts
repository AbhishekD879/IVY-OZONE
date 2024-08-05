import { ISportEvent } from '../../models/sport-event.model';
import { LpAvailabilityService } from './lp-availability.service';
describe('LpAvailabilityService', () => {
  let service: LpAvailabilityService;

  beforeEach(() => {
    service = new LpAvailabilityService();
  });

  it('check, category level', () => {
    expect(service.check(<ISportEvent>{
      categoryId: '161',
      markets: [
        {
          isLpAvailable: true
        }
      ]
    })).toBeTruthy();
    expect(service.check(<ISportEvent>{
      categoryId: '161',
      markets: [
        {
          isLpAvailable: false
        }
      ]
    })).toBeFalsy();
  });

  it('check, Win or Each Way', () => {
    expect(service.check(<ISportEvent>{
      categoryId: '18',
      markets: [
        {
          name: 'Win or Each Way',
          isLpAvailable: true
        }
      ]
    })).toBeTruthy();
    expect(service.check(<ISportEvent>{
      categoryId: '18',
      markets: [
        {
          name: 'Win or Each Way',
          isLpAvailable: false
        }
      ]
    })).toBeFalsy();
  });

});
