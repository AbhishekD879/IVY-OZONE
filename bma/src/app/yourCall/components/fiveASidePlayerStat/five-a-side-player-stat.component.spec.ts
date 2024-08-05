import { FiveASidePlayerStatComponent } from './five-a-side-player-stat.component';

describe('FiveASidePlayerStatComponent', () => {
  let component: FiveASidePlayerStatComponent;

  beforeEach(() => {
    component = new FiveASidePlayerStatComponent();
  });

  it('should create FiveASidePlayerStatComponent', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnChanges', () => {
    it('should set data (equal stats)', () => {
      component.mainStat = 'Passes';
      component.statLabel = 'passes';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(false);
      expect(component.isMainStat).toEqual(false);
      expect(component.mainLabel).toEqual('yourCall.playerStats.passes');
    });

    it('should set data (not equal stats)', () => {
      component.mainStat = 'Passes';
      component.statLabel = 'goals';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(true);
    });

    it('should set data (statValue = undefined)', () => {
      component.mainStat = 'Passes';
      component.statLabel = 'goals';
      component.statValue = undefined;
      component.ngOnChanges();

      expect(component.statValue).toEqual(0);
      expect(component.isAvailable).toEqual(true);
    });

    it('should set data (statValue = null)', () => {
      component.mainStat = 'Passes';
      component.statLabel = 'goals';
      component.statValue = null;
      component.ngOnChanges();

      expect(component.statValue).toEqual(0);
      expect(component.isAvailable).toEqual(true);
    });

    it('should set data (main stat)', () => {
      component.mainStat = 'Passes';
      component.statLabel = 'main-stat';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(true);
      expect(component.statIcon).toEqual('passes');
      expect(component.label).toEqual('yourCall.playerStats.passes');
    });

   it('should set data (main stat = offsides)', () => {
      component.mainStat = 'Offsides';
      component.statLabel = 'main-stat';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(false);
      expect(component.statIcon).toEqual('offsides');
      expect(component.label).toEqual('yourCall.playerStats.offsides');
    });

    it('should set data (main-stat and "To be carded" market)', () => {
      component.mainStat = 'To Be Carded';
      component.statLabel = 'main-stat';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(true);
      expect(component.isToBeCarded).toEqual(true);
      expect(component.statIcon).toEqual('cards');
      expect(component.label).toEqual('yourCall.playerStats.cards');
    });

    it('should set data (passes and "To be carded market")', () => {
      component.mainStat = 'To Be Carded';
      component.statLabel = 'passes';
      component.statValue = 1;
      component.ngOnChanges();

      expect(component.isAvailable).toEqual(true);
      expect(component.isToBeCarded).toEqual(false);
      expect(component.statIcon).toEqual('passes');
      expect(component.label).toEqual('yourCall.playerStats.passes');
    });
  });
});
