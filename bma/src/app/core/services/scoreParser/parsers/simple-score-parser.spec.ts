import { SimpleScoreParser } from '@core/services/scoreParser/parsers/simple-score-parser';
import { ITeamScoreData } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('SimpleScoreParser', () => {
  let parser: SimpleScoreParser;
  let eventNamePipe: EventNamePipe;

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new SimpleScoreParser(eventNamePipe);
  });

  describe('should match and parse strings:', () => {
    let testString: string,
      expectedHome: ITeamScoreData,
      expectedAway: ITeamScoreData;

    it('as home-team, home-score, away-score, away-team', () => {
      testString = 'TeamA 1-2 TeamB';
      expectedHome = { name: 'TeamA', score: '1' };
      expectedAway = { name: 'TeamB', score: '2' };
    });

    it('the trailing (BG) substring is ignored', () => {
      testString = 'TeamA 1-2 TeamB(BG)';
      expectedHome = { name: 'TeamA', score: '1' };
      expectedAway = { name: 'TeamB', score: '2' };
    });

    it('the trailing (BG) substring is ignored regardless of spaces', () => {
      testString = 'TeamA 1-2 TeamB  (BG)  ';
      expectedHome = { name: 'TeamA', score: '1' };
      expectedAway = { name: 'TeamB', score: '2' };
    });

    it('trailing and leading spaces in names are trimmed', () => {
      testString = '   Team A   34-56  Team  B   ';
      expectedHome = { name: 'Team A', score: '34' };
      expectedAway = { name: 'Team  B', score: '56' };
    });

    it('(Z) numbers next to X-Y score pair are treated as part of name if they are not separated by space from it', () => {
      testString = 'TeamA(1) 1-2 (2)TeamB';
      expectedHome = { name: 'TeamA(1)', score: '1' };
      expectedAway = { name: '(2)TeamB', score: '2' };
    });

    it('Z numbers close to X-Y score pair are treated as part of name if they are not separated by space from it', () => {
      testString = 'TeamA1 1-2 2TeamB';
      expectedHome = { name: 'TeamA1', score: '1' };
      expectedAway = { name: '2TeamB', score: '2' };
    });

    it('first X-Y number pair is treated as score', () => {
      testString = 'TeamA 1-2 3-4 TeamB';
      expectedHome = { name: 'TeamA', score: '1' };
      expectedAway = { name: '3-4 TeamB', score: '2' };
    });

    it('numbers that are not part of score should be treated as part of team name', () => {
      testString = '6 TeamA 7 1-2 8 TeamB 9';
      expectedHome = { name: '6 TeamA 7', score: '1' };
      expectedAway = { name: '8 TeamB 9', score: '2' };
    });

    afterEach(() => {
      expect(parser.parse(testString)).toEqual({
        home: expectedHome,
        away: expectedAway,
        type: 'Simple'
      });
    });
  });

  describe('should not match strings and return null', () => {
    it('if general pattern is not matched (no valid X-Y score pair)', () => {
      expect(parser.parse('TeamA vs TeamB')).toEqual(null);
    });

    it('if there is unexpected space in X-Y pair', () => {
      expect(parser.parse('TeamA 1- 2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1 -2 TeamB')).toEqual(null);
    });

    it('if there is no space between X-Y pair and team name', () => {
      expect(parser.parse('TeamA1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2TeamB')).toEqual(null);
    });
  });
});
