import { IScoreParser } from '@core/services/scoreParser/models/score-parser.model';
import { IScoreData, ITypedScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';
import * as _ from 'underscore';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

export abstract class AbstractScoreParser implements IScoreParser {
  protected abstract type: IScoreType;
  protected abstract pattern: RegExp;
  protected scorePattern: RegExp = null;

  constructor(
    public eventNamePipe: EventNamePipe
  ) {}

  /**
   * Matches provided string against pattern chosen by type this instance.
   * If non-string value is passed or pattern does not exist, or match failed - returns null.
   * If succeeded - returns the map with typed score data, assorted by matcher function of this instance.
   * @param {string} name
   * @returns {ITypedScoreData | null}
   */
  parse(name: string): ITypedScoreData | null {
    if (typeof name === 'string') {
      return this.assort(this.eventNamePipe.transform(name).match(this.pattern instanceof RegExp ? this.pattern : null));
    }
    return null;
  }

  /**
   * Returns parser type
   * @returns {IScoreType}
   */
  getType(): IScoreType {
    return this.type;
  }

  /**
   * Returns RegExp for parsing score value(s)
   *
   * @returns {RegExp} scorePattern
   */
  get scoreRegExp(): RegExp {
    return this.scorePattern;
  }
  set scoreRegExp(value:RegExp){}

  /**
   * Check is name proper for current pattern of score parser
   *
   * @returns {boolean}
   */
  test(name: string): boolean {
    if (this.pattern instanceof RegExp) {
      return this.pattern.test(this.eventNamePipe.transform(name));
    }

    return false;
  }

  /**
   * Replaces scores in the name
   *
   * @param {string} event name
   * @param {string} replacer
   * @returns {string} name
   */
  replaceScores(name: string, replacer: string = ''): string {
    if (this.scorePattern instanceof RegExp) {
      name = name.replace(this.scorePattern, replacer);
    }

    return name;
  }

  protected abstract matcher(matchArray: RegExpMatchArray): IScoreData;

  /**
   * Maps the result array of RegExp match to an object, using custom matcher function.
   * If non-array value is passed or mapping failed - returns null.
   * If succeeded - returns the mapped score data, extended with 'type' property of this instance.
   *
   * @param {string[]} matchArray
   * @returns {ITypedScoreData | null}
   */
  private assort(matchArray: string[]): ITypedScoreData | null {
    return _.extend(_.isArray(matchArray) && this.matcher(matchArray as any) || null, { type: this.type });
  }
}
