import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { IScoreParser } from '@core/services/scoreParser/models/score-parser.model';
import { SimpleScoreParser } from '@core/services/scoreParser/parsers/simple-score-parser';
import { GaaScoreParser } from '@core/services/scoreParser/parsers/gaa-score-parser';
import { SetsPointsScoreParser } from '@core/services/scoreParser/parsers/sets-points-score-parser';
import { GamesPointsScoreParser } from '@core/services/scoreParser/parsers/games-points-score-parser';
import { SetsLegsScoreParser } from '@core/services/scoreParser/parsers/sets-legs-score-parser';
import { SetsGamesPointsScoreParser } from '@core/services/scoreParser/parsers/sets-games-points-score-parser';
import { CricketScoreParser } from '@core/services/scoreParser/parsers/cricket-score-parser';
import { ITypedScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

@Injectable({ providedIn: 'root' })
export class ScoreParserService {
  private scoreParsers: IScoreParser[] = [
    new SimpleScoreParser(this.eventNamePipe),            //  TeamA 1-1 TeamB
    new GaaScoreParser(this.eventNamePipe),               //  TeamA 1-2-3-4 TeamB
    new SetsPointsScoreParser(this.eventNamePipe),        //  TeamA (1) 2-3 (4) TeamB -- set/points
    new GamesPointsScoreParser(this.eventNamePipe),       //  TeamA (1) 2-3 (4) TeamB -- game/points
    new SetsGamesPointsScoreParser(this.eventNamePipe),   //  TeamA (1) 2 3-4 5 (6) TeamB
    new CricketScoreParser(this.eventNamePipe),           //  TeamA 10/20 30/40 v TeamB 40/50 60/70
    new SetsLegsScoreParser(this.eventNamePipe)           //  TeamA (1) 2-3 (3) TeamB  -- Sets and Legs
  ];
  private orderedScoreParsers: IScoreParser[] = [
    new GaaScoreParser(this.eventNamePipe),               //  TeamA 1-2-3-4 TeamB
    new SetsGamesPointsScoreParser(this.eventNamePipe),   //  TeamA (1) 2 3-4 5 (6) TeamB
    new SetsPointsScoreParser(this.eventNamePipe),        //  TeamA (1) 2-3 (4) TeamB -- set/points
    new SetsLegsScoreParser(this.eventNamePipe),          //  TeamA (1) 2-3 (3) TeamB  -- Sets and Legs
    new SimpleScoreParser(this.eventNamePipe)             //  TeamA 1-1 TeamB
  ];
  private scoreHeaders: Partial<Record<IScoreType, Array<string>>> = {
    'GamesPoints': ['G', 'P'],
    'SetsPoints': ['S', 'P'],
    'SetsGamesPoints': ['S', 'G', 'P'],
    'SetsLegs': ['S', 'L']
  };
  private fallbackScoreTypes = { };

  constructor(
    private cmsService: CmsService,
    private eventNamePipe: EventNamePipe
  ) {
    this.getFallbackScoreTypes().subscribe( result => {
      this.fallbackScoreTypes = result;
    });
  }

  /**
   * Returns score type for sport, or undefined if no type is assigned in config
   * @param sportId
   * @returns {IScoreType}
   */
  getScoreType(sportId: string): IScoreType {
    return this.fallbackScoreTypes[sportId];
  }

  /**
   * Returns score headers for sport
   * or undefined if no headers are assigned to sport type or fallback scoreboards are disabgled
   * @param sportId
   */
  getScoreHeaders(sportId: string): Array<string> {
    const scoreType = this.getScoreType(sportId);
    return scoreType && this.scoreHeaders[scoreType];
  }

  /**
   * Parse sport score data from event name according to supplied template type
   * @param {string} rawName
   * @param {IScoreType} type
   * @returns {ITypedScoreData}
   */
  parseScores(rawName: string, type: IScoreType): ITypedScoreData | null {
    const parser = this.scoreParsers.find((p: IScoreParser) => p.getType() === type);

    if (parser) {
      return parser.parse(rawName);
    }
    return null;
  }

  /**
   * Define score type by template and return type and parsed scores
   * @param {string} originalEventName - original event name
   * @param {string} categoryCode - event category code
   * @returns {{score: ITypedScoreData; type: IScoreType | null}}
   */
  parseTypeAndScores(originalEventName: string, categoryCode: string = ''): { score: ITypedScoreData | null, scoreType: string} {
    let score;
    if (categoryCode === 'CRICKET') {
      const cricketParseInstance = new CricketScoreParser(this.eventNamePipe);
      score = cricketParseInstance.parse(originalEventName);
    }
    for (let i = 0; !score && i < this.orderedScoreParsers.length; i++) {
      score = this.orderedScoreParsers[i].parse(originalEventName);
      if (score) {
        break;
      }
    }
    if (score) {
      const scoreType = score.type;
      delete score.type;
      return {
        score: score,
        scoreType
      };
    }
    return null;
  }
  /**
   * getFallbackScoreTypes()
   * reads fallback scoreboard config from CMS and stores as categoryId - score type map
   */
  private getFallbackScoreTypes(): Observable<any> {
    return this.cmsService.getSystemConfig()
      .pipe(
        map(
          (config: ISystemConfig) =>
            config.FallbackScoreboard &&
            config.FallbackScoreboard.enabled &&
            Object.keys(config.FallbackScoreboard).reduce(
              (result, scoreType) => {
                if (scoreType !== 'enabled') {
                  const sportIds = (config.FallbackScoreboard[scoreType] as string).split(',');
                  sportIds.forEach(id => {
                    result[id] = scoreType;
                  });
                }
                return result;
              }, {}
            ) || {}
        )
      );
  }
}
