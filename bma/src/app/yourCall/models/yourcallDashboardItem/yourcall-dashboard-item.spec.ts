import { YourCallDashboardItem } from './yourcall-dashboard-item';

describe('#YourCallDashboardItem', () => {
  let instance;
  let market;
  let selection;

  beforeEach(() => {
    market = {
      title: '',
      getTitle: jasmine.createSpy('getTitle').and.returnValue('MARKET_TITLE'),
      getSelectionTitle: jasmine.createSpy('getSelectionTitle').and.returnValue('SELECTION_TITLE'),
      getBetslipTitle: jasmine.createSpy('getBetslipTitle').and.returnValue('BETSLIP_TITLE')
    } as any;
    selection = {} as any;
    instance = new YourCallDashboardItem({
      market,
      selection
    });
  });

  it('should init component', () => {
    expect(instance).toBeTruthy();
  });

  it('getTitle should return market title with selection title', () => {
    expect(instance.getTitle()).toEqual('MARKET_TITLE SELECTION_TITLE');
  });

  describe('getBetslipFormattedTitle', () => {
    beforeEach(() => {
      selection.title = 'Roberto';
    });

    it('to score N or more goals', () => {
      market.title = 'TO SCORE 3 OR MORE GOALS';
      expect(instance.getBetslipTitle()).toContain('roberto to score 3+ goals');
    });

    it('anytime goalscorer', () => {
      market.title = 'ANYTIME GOALSCORER';
      expect(instance.getBetslipTitle()).toContain('roberto anytime goalscorer');
    });

    it('to be shown a card', () => {
      market.title = 'TO BE SHOWN A CARD';
      expect(instance.getBetslipTitle()).toContain('roberto to be carded');
    });

    it('default title', () => {
      expect(instance.getBetslipTitle()).toBe('BETSLIP_TITLE');
    });

    it('default title', () => {
      instance.getBetslipFormattedTitle = jasmine.createSpy('getBetslipFormattedTitle').and.returnValue(undefined);
      instance.selection = 'DUMMY'
      instance.market = { getBetslipTitle: () => 'dummy' } as any;
      const retVal = instance.getBetslipTitle()
      expect(retVal).toBe('dummy');
    });
  });
});
