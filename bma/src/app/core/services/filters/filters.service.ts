import { CurrencyPipe, DatePipe } from '@angular/common';
import { Injectable, Inject } from '@angular/core';
import * as _ from 'underscore';

import { homeAway } from '../../constants/home-away.constant';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { filterStabilize } from './filters.decorators';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IClassModel, IClassResultModel } from '@core/models/class.model';
import { CricketScoreParser } from '@core/services/scoreParser/parsers/cricket-score-parser';
import { GaaScoreParser } from '@core/services/scoreParser/parsers/gaa-score-parser';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { IBetHistoryOutcome } from '@core/models/outcome.model';
import { IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IOutcomeDetailsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import {  IQuickbetOutcomeModel } from '@app/quickbet/models/quickbet-market.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BehaviorSubject } from 'rxjs';
import { Observable } from 'rxjs';
@Injectable()
export class FiltersService {
  private cricketScoreParser: CricketScoreParser;
  private gaaScoreParser: GaaScoreParser;

  constructor(private locale: LocaleService,
              public currencyPipe: CurrencyPipe,
              public datePipe: DatePipe,
              private userService: UserService,
              private coreToolsService: CoreToolsService,
              private eventNamePipe: EventNamePipe,
              private pubsub: PubSubService,
              @Inject('GREYHOUND_CONFIG') private greyhoundConfig: IInitialSportConfig
  ) {
    this.cricketScoreParser = new CricketScoreParser(this.eventNamePipe);
    this.gaaScoreParser = new GaaScoreParser(this.eventNamePipe);
  }

  getComplexTranslation(key: string, replaceKey: string, value: string): string {
    return this.locale.getString(key).replace(replaceKey, value);
  }

  orderBy<T>(list: T[], fields: string[], defaultField: any = ''): T[] {
    return list.slice().sort((a: T, b: T) => fields
      .map((field: string) => {
        let dir: number = 1;
        if (field[0] === '-') {
          dir = -1;
          field = field.substring(1);
        }

        const aField = this.coreToolsService.getOwnDeepProperty(a, field, defaultField);
        const bField = this.coreToolsService.getOwnDeepProperty(b, field, defaultField);

        if (Number(aField) && Number(bField)) {
          const aNumber: number = Number(Number(aField).toFixed(1));
          const bNumber: number = Number(Number(bField).toFixed(1));

          return dir > 0 ? aNumber - bNumber : bNumber - aNumber;
        } else {
          if (bField !== '' && aField > bField) { return dir; } else if (bField === '') { return -dir; }
          if (aField !== '' && aField < bField) { return -(dir); } else if (aField === '') { return dir; }
          return 0;
        }
      })
      .reduce((p: number, n: number) => p ? p : n, 0)
    );
  }

  /**
   * Sorts array of objects sequentially comparing object properties
   * @param items      {array}  array to sort
   * @param properties {array}  properties to compare
   * @return {array}
   */
  chainSort(items: any[], properties: string[]): any[] {
    items.sort((a, b) => {
      for (let i = 0; i < properties.length; ++i) {
        const prop = properties[i];
        const aVal = this.coreToolsService.getOwnDeepProperty(a, prop);
        const bVal = this.coreToolsService.getOwnDeepProperty(b, prop);

        if (aVal > bVal) { return 1; }
        if (aVal < bVal) { return -1; }
      }
      return -1;
    });
    return items;
  }

  sportCatIcon(path: string): string {
    const regExp = /[^A-Z0-9]+/ig;
    return path ? path.replace(regExp, '') : '';
  }

  clearEventName(input: string, categoryCode: string = ''): string {
    let teamName: string = input;
    if (teamName) {
      teamName = teamName.replace(/\s?(\d?\d):(\d{2}):(\d{2})\s?/g, '');
      teamName = teamName.replace(/\s?(\d?\d):(\d{2})\s?/g, '');
      teamName = teamName.replace(/\s?(\d{4})-(\d{2})-(\d{2}):(\d{2})\s?/g, '');
      teamName = teamName.replace(/\s?(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\s?/g, '');
      // TODO: remove this or EventNamePipe (the last ove covers all options)
      teamName = teamName.replace(/\s*\([^)]\BG\)\s*/g, '');
      // Gaelic football
      if (this.gaaScoreParser.test(teamName)) {
        teamName = this.gaaScoreParser.replaceScores(teamName, ' v ');
      }
      // |Player A| (0) 1 2-3 4 (5) |Player B|
      teamName = teamName.replace(/\s?\(?(\d+)?\)\s?(\d+)?\s?(\w+)-(\w+)\s?(\d+)\s?\(?(\d+)?\)\s?/g, ' v ');
      teamName = teamName.replace(/\s?\(?(\d+)?\)\s?(\d+)-(\d+)\s?\(?(\d+)?\)\s?/g, ' v ');
      teamName = teamName.replace(/\s+(\d+-\d+)\s+/g, ' v ');
      // Cricket
      if (this.cricketScoreParser.test(teamName) && categoryCode === 'CRICKET') {
        teamName = this.cricketScoreParser.replaceScores(teamName);
      }
    }
    return teamName;
  }

  currencyPosition(input: string | number, currencySymbol: string): string {
    let result: string = null;

    if (input) {
      result = currencySymbol + input.toString().trim();
    }
    return result;
  }

  setCurrencySymbol(num: number | string, symbol: string): string {
    return (_.isString(num)) ? num : `${symbol} ${num}`;
  }

  filterAddScore(marketName: string, outcomeName: string): string {
    const pattern: RegExp = /\sto (.*) (\d+\+) (.*)/;
    const market: string = marketName.toLowerCase();
    const isHomeAway: boolean = outcomeName && !!(outcomeName.indexOf(homeAway.H) > 0 || outcomeName.indexOf(homeAway.A) > 0); // (H) or (A)
    const isCorrectMarket: boolean = market && !!(market.indexOf('shots') > 0 || market.indexOf('tackles') > 0); // Shots or Tackles Markets
    const scoreMatch: RegExpMatchArray = outcomeName && outcomeName.match(pattern);
    const score: string = scoreMatch && scoreMatch[2];
    return isHomeAway && isCorrectMarket && score ? `${score} ${marketName}` : marketName;
  }

  filterAlphabetsOnly(input: string): string {
    let result = null;
    if (input !== undefined) {
      const myRegexp = /(((\d+)\+)$)|(((\d+)-(\d+))$)|([|])/g;
      result = input.replace(myRegexp, '').replace(/((\s+)$)|(^(\s+))/g, '');
    }
    return result;
  }

  filterAlphabetsOnlyTrimUnderscore(input: string): string {
    let result = null;
    if (input !== undefined) {
      const myRegexp = /(((\d+)\+)$)|(((\d+)-(\d+))$)|([|])/g;
      result = input.replace(myRegexp, '').replace(/((\s+)$)|(^(\s+))/g, '')
        .replace(/\-$/, '');
    }

    return result;
  }

  filterNumbersOnly(input: string): string {
    let result = '';
    if (input !== undefined) {
      const myRegexp = /(((\d+)\+)$)|(((\d+)-(\d+))$)/g,
        value = input.trim();
      if (myRegexp.test(value)) {
        result = value.match(myRegexp)[0];
      }
    }
    return result;
  }

  date(date: string | number | Date, format: string) {
    return this.datePipe.transform(date, format);
  }

  distance(input: string): string {
    const numberFragment: string = input.match(/\d+/)[0],
      inMeters = input.indexOf('Meters') !== -1,
      // 1 meter = 1.09361 yards
      numberInYards = inMeters ? Math.round(Number(numberFragment) * 1.09361) : numberFragment,
      miles = Math.floor(Number(numberInYards) / 1760),  // 1 mile = 1760 yards
      residue = Number(numberInYards) - (miles * 1760),
      furlongs = Math.floor(residue / 220),      // 1 furlong = 220 yards
      yards = Math.round(residue - (furlongs * 220)),
      milesString = miles ? `${miles}m ` : '',
      furlongsString = furlongs ? `${furlongs}f ` : '',
      yardsString = yards ? `${yards}y` : '';
    return ` ${milesString}${furlongsString}${yardsString}`;
  }

  setCurrency(amount: any, symbol?): any {
    const currencySymbol = symbol || this.userService.currencySymbol || '£';

    return this.currencyPipe.transform(amount, currencySymbol, 'code');
  }

  setFreebetCurrency(amount: string|number, symbol?: string): string {
    const currencySymbol = symbol || this.userService.currencySymbol || '£';

    return this.currencyPipe.transform(amount, currencySymbol, 'code', '1.0');
  }

  removeLineSymbol(value: string): string {
    let out;
    if (value !== undefined) {
      out = value.replace(/\|/g, '');
    }
    return out;
  }

  removenNonRunnerFromHorseName(value: string): string {
    return value ? value.replace(/\|/g, '').replace('N/R','') : '';
  }

  orderRightMenuBySection<T>(input: { section: string }[]): T[] {
    let out;
    if (input) {
      const topList = [],
        centerList = [],
        bottomList = [];
      for (let i = 0; i < input.length; i++) {
        if (input[i].section === 'top') {
          topList.push(input[i]);
        }
        if (input[i].section === 'center') {
          centerList.push(input[i]);
        }
        if (input[i].section === 'bottom') {
          bottomList.push(input[i]);
        }
      }
      out = topList.concat(centerList, bottomList);
    }
    return out;
  }

  numberWithCurrency(amount: number, symbolToUse?: string): string {
    const currencySymbol = symbolToUse || this.userService.currencySymbol || '£';
    const currentAmount = isNaN(amount) ? 0 : +amount;
    const currentAmountAbs = `${currencySymbol}${Math.abs(currentAmount).toFixed(2)}`;
    return `${currentAmount >= 0 ? '' : '- '}${currentAmountAbs}`;
  }

  numberSuffix(input: string | number): string {
    const suffixes: string[] = [
      'sb.numSuffixTh',
      'sb.numSuffixSt',
      'sb.numSuffixNd',
      'sb.numSuffixRd'
    ];

    const inputNumber: number = _.isString(input) ? Number(input) : input,
      relevantDigits = inputNumber < 30 ? inputNumber % 20 : inputNumber % 30;

    return relevantDigits <= 3 ? suffixes[relevantDigits] : suffixes[0];
  }

  numberTranslatedSuffix(input: string | number): string {
    return this.locale.getString(this.numberSuffix(input));
  }

  makeHandicapValue(value: string | number, outcome?: (IBetHistoryOutcome | IBetDetailLegPart
    | IOutcomeDetailsResponse | IQuickbetOutcomeModel)): string {
    const result: string = String(value).replace(/[\+,\s\s+]/g, '');
    if (outcome && (outcome['outcomeMeaningMajorCode'] || outcome['eventMarketSort']) === this.locale.getString('app.highLowerVal')) {
      return ` (${result})`;
    } else {
      return result.indexOf('-') === -1 ? ` (+${result})` : ` (${result})`;
    }
  }

  getScoreFromName(input: string): string {
    let result: string = '';
    if (input !== undefined) {
      const myRegexp = /\s?(\d+)\s?-\s?(\d+)\s?/g,
      value = input.trim();
      if (myRegexp.test(value)) {
        result = value.match(myRegexp)[0].trim();
      }
    }
    return result;
  }

  filterPlayerName(name: string): string {
    const pattern: RegExp = /\sto\s(.*)/;
    const isHomeAway: boolean = !!(name.indexOf(homeAway.H) > 0 || name.indexOf(homeAway.A) > 0);
    const filter: string = homeAway.H || homeAway.A;
    return isHomeAway ? name
      .replace(filter, '')
      .replace(pattern, '') : name;
  }

  filterLink(link: string): string {
    /* eslint-disable */
    const regex = new RegExp('^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?');
    /* eslint-enable */
    let clearLink: string;
    if (link) {
      clearLink = link.replace(/ +/g, '');
      // Check if url could decoded correctly, if not - encode percent character
      try {
        decodeURIComponent(clearLink);
      } catch (e) {
        clearLink = clearLink.replace(/%/g, '%25');
      }
      clearLink = regex.test(clearLink) ? clearLink : clearLink.replace('//', '/');
    }
    return clearLink;
  }

  // TODO: create more obvious description/name for this method
  @filterStabilize
  groupBy<T>(input: Array<T>, prop: string): { [id: number]: Array<T> } {
    return !input ? undefined : input.reduce((state, item) => {
      const key: number = item[prop];  // TODO: convert to _.getOwnDeepProperty if necessary
      state[key] && state[key].push(item);
      return state;
    }, { 1: [], 2: [], 3: [] });
  }

  getTeamName(eventName, index): string {
    const scoreRegex = /\s?(\d+)-(\d+)\s?/g;
    if (eventName.indexOf(' vs ') !== -1) {
      return eventName.split(' vs ')[index];
    } else if (eventName.indexOf(' v ') !== -1) {
      return eventName.split(' v ')[index];
    } else if (eventName.indexOf(' @ ') !== -1) {
      return eventName.split(' @ ')[index];
    } else if (eventName.indexOf(' - ') !== -1) {
      return eventName.split(' - ')[index];
    } else if (eventName.indexOf('/') !== -1) {
      return eventName.split('/')[index];
    } else if (this.gaaScoreParser.test(eventName)) {
      return eventName.split(eventName.match(this.gaaScoreParser.scoreRegExp))[index];
    } else if (eventName.match(scoreRegex)) {
      return eventName.split(eventName.match(scoreRegex))[index];
    }

    return '';
  }


  /**
   * getTimeFromName()
   * @param name
   * @returns {string}
   */
  getTimeFromName(name): string {
    const time = name.match(/\d+:\d+/);
    return time ? time[0] : '';
  }

  /**
   * objectPromise()
   * Method allows to use object in "Promise.all()"
   * @param obj
   * @returns {Promise<{}>}
   */
  objectPromise(obj) {
    return Promise.all(Object.keys(obj).map(key => {
      return Promise.resolve(obj[key]).then(val => {
        return { key: key, val: val };
      });
    })).then(items => {
      const result = {};
      items.forEach(item => {
        result[item.key] = item.val;
      });
      return result;
    });
  }

  /**
   * @params input {ClassId}
   * @return {object}
   */
  initialClassIds(allClasses: IClassResultModel, classId: string | number) {
    return !classId ? '' : _.find(allClasses.result, (item: IClassModel) => item.class.id === classId);
  }

  /**
   * @params input {string}
   * @return {string}
   * Filter example: 'Football England' ==> 'England'
   */
  clearSportClassName(className: string, categoryName: string) {
    if (!className) {
      return '';
    }

    if (className === categoryName) {
      return categoryName;
    }

    return className.replace(new RegExp(`${categoryName}\\s?(All\\s)?`), '');
  }

  /**
   * Check if event category is Greyhounds
   * @param {string} eventCategoryId
   * @returns {boolean}
   */
  isGreyhoundsEvent(eventCategoryId: string): boolean {
    return eventCategoryId === this.greyhoundConfig.config.request.categoryId;
  }

   
  filterLinkforRSS(url):Observable<string> {
    const rssUrl = new BehaviorSubject<string>(url);
    this.pubsub.subscribe('userServiceClosureOrPlayBreak', this.pubsub.API.USER_CLOSURE_PLAY_BREAK, val => {
      if (val) {
        rssUrl.next('/promotions/details/exclusion');
      }
    })
    return rssUrl.asObservable();
  }
}
