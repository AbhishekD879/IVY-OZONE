import { GamesPointsScoreParser } from '@core/services/scoreParser/parsers/games-points-score-parser';
import { ITeamScoreData } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('GamesPointsScoreParser', () => {
  let parser: GamesPointsScoreParser;
  let eventNamePipe: EventNamePipe;

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new GamesPointsScoreParser(eventNamePipe);
  });

  describe('should match and parse strings:', () => {
    let testString: string,
      expectedHome: ITeamScoreData,
      expectedAway: ITeamScoreData;

    it('as home-team, home-serving, home-score, home-points, away-points, away-score, away-serving, away-team', () => {
      testString = 'TeamA* (3) 1-2 (4) *TeamB';
      expectedHome = { name: 'TeamA', score: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '4', currentPoints: '2', isServing: true };
    });

    it('the trailing (BG) substring is ignored', () => {
      testString = 'TeamA (3) 1-2 (4) *TeamB(BG)';
      expectedHome = { name: 'TeamA', score: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: 'TeamB', score: '4', currentPoints: '2', isServing: true };
    });

    it('the trailing (BG) substring is ignored regardless of spaces', () => {
      testString = 'TeamA* (3) 1-2 (4) TeamB  (BG)  ';
      expectedHome = { name: 'TeamA', score: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '4', currentPoints: '2', isServing: false };
    });

    it('trailing and leading spaces in name and serving marker are trimmed', () => {
      testString = '   Team   A *   (30) 10-20 (40)  *  Team  B  ';
      expectedHome = { name: 'Team   A', score: '30', currentPoints: '10', isServing: true };
      expectedAway = { name: 'Team  B', score: '40', currentPoints: '20', isServing: true };
    });

    it('extra spaces inside (X) U-V (Y) score group are ignored', () => {
      testString = 'TeamA (30)   10-20  (40) TeamB';
      expectedHome = { name: 'TeamA', score: '30', currentPoints: '10', isServing: false };
      expectedAway = { name: 'TeamB', score: '40', currentPoints: '20', isServing: false };
    });

    it('asterisk not directly space-separated from (X) U-V (Y) score group is considered as part of the name', () => {
      testString = 'TeamA*  A (30) 10-20 (40) 1 * TeamB';
      expectedHome = { name: 'TeamA  A', score: '30', currentPoints: '10', isServing: false };
      expectedAway = { name: '1  TeamB', score: '40', currentPoints: '20', isServing: false };
    });

    it('asterisk space-separated from (X) U-V (Y) score group is considered as serving marker', () => {
      testString = 'TeamA* (3) 1-2 (4) *  TeamB';
      expectedHome = { name: 'TeamA', score: '3', currentPoints: '1', isServing: true };
      expectedAway = { name: 'TeamB', score: '4', currentPoints: '2', isServing: true };
    });

    it('any (Z) number space-separated from (U) X-Y (V) score group is treated as part of name', () => {
      testString = 'TeamA (5) (3) 1-2 (4) (6)TeamB';
      expectedHome = { name: 'TeamA (5)', score: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '(6)TeamB', score: '4', currentPoints: '2', isServing: false };
    });

    it('any Z number space-separated from (U) X-Y (V) score group is treated as part of name', () => {
      testString = 'TeamA 5 (3) 1-2 (4) 6TeamB';
      expectedHome = { name: 'TeamA 5', score: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '6TeamB', score: '4', currentPoints: '2', isServing: false };
    });

    it('first (U) X-Y (V) number pair is treated as score', () => {
      testString = 'TeamA (3) 1-2 (4) 5-6 (7) TeamB';
      expectedHome = { name: 'TeamA', score: '3', currentPoints: '1', isServing: false };
      expectedAway = { name: '5-6 (7) TeamB', score: '4', currentPoints: '2', isServing: false };
    });

    it('should define scores if name contain some word in brackets next to scores', () => {
      testString = 'Volero Zurich (Women) (2) 12-5 (0) (predators) CS Volei Alba Blaj';
      expectedHome = { name: 'Volero Zurich (Women)', score: '2', currentPoints: '12', isServing: false };
      expectedAway = { name: '(predators) CS Volei Alba Blaj', score: '0', currentPoints: '5', isServing: false };
    });

    afterEach(() => {
      expect(parser.parse(testString)).toEqual({
        home: expectedHome,
        away: expectedAway,
        type: 'GamesPoints'
      });
    });
  });

  describe('should not match strings and return null', () => {
    it('if general pattern is not matched (no valid (U) X-Y (V) score pair)', () => {
      expect(parser.parse('TeamA vs TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 (4) TeamB')).toEqual(null);
    });

    it('if there is unexpected space in X-Y pair', () => {
      expect(parser.parse('TeamA (3) 1 -2 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 1- 2 (4) TeamB')).toEqual(null);
    });

    it('if there is no mandatory space in (U) X-Y (V) group', () => {
      expect(parser.parse('TeamA (3) 1-2(4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3)1-2 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3)1-2(4) TeamB')).toEqual(null);
    });

    it('if there is no space between (U) X-Y (V) group and team name', () => {
      expect(parser.parse('TeamA(3) 1-2 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 1-2 (4)TeamB')).toEqual(null);
    });

    it('if there is no space between (U) X-Y (V) group and serving mark', () => {
      expect(parser.parse('TeamA *(3) 1-2 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 1-2 (4)* TeamB')).toEqual(null);
    });

    it('if there is unexpected Z number inside (U) X-Y (V) group', () => {
      expect(parser.parse('TeamA (3) 5 1-2 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 1-2 5 (4) TeamB')).toEqual(null);
      expect(parser.parse('TeamA (3) 5 1-2 6 (4) TeamB')).toEqual(null);
    });
  });
});
