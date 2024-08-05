import { IBetHistoryBet, IBetHistoryLeg } from '../../models/bet-history.model';
import { BetLegListComponent  } from './bet-leg-list.component';

describe('BetLegListComponent', () => {
  let component: BetLegListComponent;

  beforeEach(() => {
    component = new BetLegListComponent();
    component.bet = {
      eventSource: {
        leg: []
      },
      location: ''
    } as any;

    component.bet = {
      eventSource: {
        id: 1, betType: '', stake: '',
        leg: [{
          part:
            [{ price: [{ priceType: { code: '' } }] }] 
        }] as IBetHistoryLeg[]
      } as IBetHistoryBet
      , location: 'Test'
    };
  });

  it('should create a comonent', () => {
    expect(component).toBeTruthy();
  });

  it('trackByLeg should return joined string', () => {
    const index: number = 1;
    const leg: any = {
      id: '22',
      status: 'test'
    };
    const result: string = component.trackByLeg(index, leg);

    expect(result).toEqual('1test');
  });
  describe('Test updateLeg', () => {
    let leg: IBetHistoryLeg;
    beforeEach(() => {
      leg = component.bet.eventSource.leg[0];
    });

    it('should call updateLeg() and return isBog=false if priceType.codes is "" ', () => {
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(false);
    });

    it('should call updateLeg() and return isBog=false if priceType is "null" ', () => {
      leg.part[0].price[0].priceType = null;
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(false);
    });

    it('should call updateLeg() and return isBog=false if priceType.codes is "null" ', () => {
      leg.part[0].price[0].priceType.code = null;
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(false);
    });

    it('should call updateLeg() and return isBog=true if priceType.codes is "GP" ', () => {
      leg.part[0].price[0].priceType.code = 'GP';
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(true);
    });

    it('should call updateLeg() and return isBog=false if priceType.codes is "S" ', () => {
      leg.part[0].price[0].priceType.code = 'S';
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(false);
    });

    it('should call updateLeg() and return isBog=false if price is null ', () => {
      leg.part[0].price = null;
      const updatedLeg = component.updateLeg(leg);

      expect(updatedLeg.part[0].isBog).toBe(false);
    });

  });
});
