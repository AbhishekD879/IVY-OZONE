import { SetsGamesPointsScoreParser } from '@core/services/scoreParser/parsers/sets-games-points-score-parser';
import { ITeamScoreData } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('SetsGamesPointsScoreParser', () => {
  let parser: SetsGamesPointsScoreParser;
  let eventNamePipe: EventNamePipe;

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new SetsGamesPointsScoreParser(eventNamePipe);
  });

  describe('should match and parse strings:', () => {
    let testString: string,
      expectedHome: ITeamScoreData,
      expectedAway: ITeamScoreData;

    it('as home-team, home-serving, home-score, home-points, away-points, away-score, away-serving, away-team', () => {
      testString = 'TeamA* (5) 3 1-2 4 (6) *TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: true };
    });

    it('the trailing (BG) substring is ignored', () => {
      testString = 'TeamA (5) 3 1-2 4 (6) *TeamB(BG)';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: true };
    });

    it('the trailing (BG) substring is ignored regardless of spaces', () => {
      testString = 'TeamA* (5) 3 1-2 4 (6) TeamB   (BG)  ';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('trailing and leading spaces in name and serving marker are trimmed', () => {
      testString = '  Team  A *   (50) 30 10-20 40 (60)  *  Team B  ';
      expectedHome = { name: 'Team  A', score: '50', periodScore: '30', currentPoints: '10', isServing: true };
      expectedAway = { name: 'Team B', score: '60', periodScore: '40', currentPoints: '20', isServing: true };
    });

    it('extra spaces inside (X) N U-V M (Y) score group are ignored', () => {
      testString = 'TeamA (5)  3   1-2   4  (6) TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('asterisk not directly space-separated from (X) N U-V M (Y) score group is considered as part of the name', () => {
      testString = 'TeamA*  A (5) 3 1-2 4 (6) 1 * TeamB';
      expectedHome = { name: 'TeamA  A', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '1  TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('asterisk space-separated from (X) N U-V M (Y) score group is considered as serving marker', () => {
      testString = 'TeamA * (5) 3 1-2 4 (6) *  TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: true };
    });

    it('any (Z) number space-separated from (X) N U-V M (Y) score group is treated as part of name', () => {
      testString = 'TeamA (7) (5) 3 1-2 4 (6) (8)TeamB';
      expectedHome = { name: 'TeamA (7)', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '(8)TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('any Z number space-separated from (X) N U-V M (Y) score group is treated as part of name', () => {
      testString = 'TeamA 7 (5) 3 1-2 4 (6) 8TeamB';
      expectedHome = { name: 'TeamA 7', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '8TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('first (X) N U-V M (Y) number pair is treated as score', () => {
      testString = 'TeamA (5) 3 1-2 4 (6) 8 10-11 9 (7) TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '8 10-11 9 (7) TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: false };
    });

    it('should define scores if scores containe any letter next to dash', () => {
      testString = 'TeamA (5) 3 1-Adv 4 (6) TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: 'Adv', isServing: false };
    });

    it('should define scores if scores containe any letter next to dash', () => {
      testString = 'TeamA (5) 3 Adv-15 4 (6) TeamB';
      expectedHome = { name: 'TeamA', score: '5', periodScore: '3', currentPoints: 'Adv', isServing: false };
      expectedAway = { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '15', isServing: false };
    });

    afterEach(() => {
      expect(parser.parse(testString)).toEqual({
        home: expectedHome,
        away: expectedAway,
        type: 'SetsGamesPoints'
      });
    });
  });

  describe('should not match strings and return null', () => {
    it('if general pattern is not matched (no valid (X) N U-V M (Y) score pair)', () => {
      expect(parser.parse('TeamA vs TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3 1-2 4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 1-2 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 1-2 4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3 1-2 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 (6) TeamB')).toEqual(null);
    });

    it('if there is unexpected space in (X) N U-V M (Y) group', () => {
      expect(parser.parse('TeamA (5) 3 1 -2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1- 2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1 - 2 4 (6) TeamB')).toEqual(null);
    });

    it('if there is no mandatory space in (X) N U-V M (Y) group', () => {
      expect(parser.parse('TeamA (5)3 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 4(6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5)3 1-2 4(6) TeamB')).toEqual(null);
    });

    it('if there is no space between (X) N U-V M (Y) group and team name', () => {
      expect(parser.parse('TeamA (5)3 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 4(6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5)3 1-2 4(6) TeamB')).toEqual(null);
    });

    it('if there is no space between (X) N U-V M (Y) group and serving marker', () => {
      expect(parser.parse('TeamA *(5) 3 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 4 (6)* TeamB')).toEqual(null);
      expect(parser.parse('P. Tester (1) 1 45-30 1 (0) *Pl.T33t').away.isServing).toBeTruthy();
      expect(parser.parse('P. Tester (1) 1 45-30 1 (0) Pl.T33t*').away.isServing).toBeTruthy();
      expect(parser.parse('P. Tester* (1) 1 45-30 1 (0) Pl.T33t').home.isServing).toBeTruthy();
      expect(parser.parse('*P. Tester (1) 1 45-30 1 (0) Pl.T33t').home.isServing).toBeTruthy();
    });

    it('if there is unexpected Z number inside (X) N U-V M (Y) pair', () => {
      expect(parser.parse('TeamA (5) 7 3 1-2 4 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 3 1-2 4 8 (6) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (5) 7 3 1-2 4 8 (6) TeamB')).toEqual(null);
    });
  });
});
