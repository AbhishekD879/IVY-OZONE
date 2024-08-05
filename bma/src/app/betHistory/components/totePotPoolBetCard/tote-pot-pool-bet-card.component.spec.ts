import { TotePotPoolBetCardComponent  } from './tote-pot-pool-bet-card.component';
import TotePotPoolBet from '../../betModels/totePotPoolBetClass/TotePotPoolBetClass';

describe('TotePotPoolBetCardComponent ', () => {
  let component: TotePotPoolBetCardComponent;
  let mockPool;

  beforeEach(() => {
    mockPool = {getRaceTitle: jasmine.createSpy().and.returnValue('21:45 test track')};
    component = new TotePotPoolBetCardComponent();
    component.pool = mockPool as TotePotPoolBet;
  });

  it('should create a comonent', () => {
    expect(component).toBeTruthy();
  });

  it('getLegTitle should return joined string', () => {
    const index: number = 1;
    const result = component.getLegTitle({} as any, index);

    expect(result).toEqual('Leg 2 21:45 test track');
  });

  describe('getOutcomeTitle', () => {
    it('should return only runner name if runner is Unnamed Favourite ', () => {
      expect(component.getOutcomeTitle({
        name: '2nd Unnamed Favourite',
        isFavourite: true
      } as any)).toEqual('2nd Unnamed Favourite');
    });

    it('should return runner number with runner name if runner is not Unnamed Favourite', () => {
      expect(component.getOutcomeTitle({
        name: 'Rockie Balboa',
        isFavourite: false,
        runnerNumber: 8
      } as any)).toEqual('8. Rockie Balboa');
    });
  });

  it('trackByLeg should return joined string', () => {
    const index: number = 11;
    const item: any = {
      eventId: '22',
      marketId: '33'
    };
    const result = component.trackByLeg(index, item);

    expect(result).toEqual('112233');
  });

  it('trackByOutcome should return joined string', () => {
    const index: number = 1;
    const outcome: any = {id : '1'};
    const result = component.trackByOutcome(index, outcome);

    expect(result).toEqual('11');
  });
});
