import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { MARKET_ORDER, PLAYER_DATA } from './byb-player-stats-constant';
import { BybPlayerstatsComponent } from './byb-player-stats.component';

describe('BybPlayerstatsComponent', () => {
  let component: BybPlayerstatsComponent;
  let deviceService, windowRef;

  beforeEach(() => {
    deviceService = {};
    windowRef = {};
    component = new BybPlayerstatsComponent(deviceService, windowRef);
  });
  it(`should be instance of 'AbstractDialogComponent'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });
  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  describe('open', () => {
    beforeEach(() => {
      spyOn(component as any, 'createPlayerStatMap');
    });
    it('should display stats pop-up', () => {
      const openSpy = spyOn(BybPlayerstatsComponent.prototype['__proto__'], 'open');
      const params = {
        data: {
          player: PLAYER_DATA, market: 'Goals'
        }
      };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component['createPlayerStatMap']).toHaveBeenCalled();
    });

    it('params are not present', () => {
      const openSpy = spyOn(BybPlayerstatsComponent.prototype['__proto__'], 'open');
      const params = undefined;
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component['createPlayerStatMap']).not.toHaveBeenCalled();
    });

    it('params data is not present', () => {
      const openSpy = spyOn(BybPlayerstatsComponent.prototype['__proto__'], 'open');
      const params = { data: undefined };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component['createPlayerStatMap']).not.toHaveBeenCalled();
    });

    it('params data player is not present', () => {
      const openSpy = spyOn(BybPlayerstatsComponent.prototype['__proto__'], 'open');
      const params = { data: { player: undefined, market: 'Goals' } };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component['createPlayerStatMap']).not.toHaveBeenCalled();
    });

    it('params data market is not present', () => {
      const openSpy = spyOn(BybPlayerstatsComponent.prototype['__proto__'], 'open');
      const params = {
        data: {
          player: PLAYER_DATA, market: undefined
        }
      };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component['createPlayerStatMap']).not.toHaveBeenCalled();
    });
  });
  describe('createPlayerStatMap', () => {
    it('creating player stats when player data is undefined', () => {
      component.player = PLAYER_DATA;
      component['createPlayerStatMap'](MARKET_ORDER['goals']);
      expect(component.playerStatMap).toEqual([{ statLabel: 'Goals', statValue: '0' }, { statLabel: 'Appearances', statValue: '0' }, { statLabel: 'Assists', statValue: '0' }, { statLabel: 'Shots per game', statValue: '0' }, { statLabel: 'Passes per game', statValue: '0' }]);
    });
    it('creating player stats when player data is present', () => {
      component.player = {
        id: 1, name: '', teamName: '', teamColors: { primaryColour: '', secondaryColour: '' }, appearances: 3,
        cleanSheets: 3, tackles: 3, passes: 3, crosses: 3, assists: 3,
        shots: 3, shotsOnTarget: 3, shotsOutsideTheBox: 3, goalsInsideTheBox: 3,
        goalsOutsideTheBox: 3, goals: 3, cards: 3, cardsRed: 3, cardsYellow: 3,
        position: { long: '', short: '' }, penaltySaves: 3, conceeded: 3, saves: 3, isGK: false
      };
      component['createPlayerStatMap'](MARKET_ORDER['goals']);
      expect(component.playerStatMap).toEqual([{ statLabel: 'Goals', statValue: 3 }, { statLabel: 'Appearances', statValue: 3 }, { statLabel: 'Assists', statValue: 3 }, { statLabel: 'Shots per game', statValue: 3 }, { statLabel: 'Passes per game', statValue: 3 }]);
    });
  });

});
