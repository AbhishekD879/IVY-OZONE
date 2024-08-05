import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { FiltersService } from '@core/services/filters/filters.service';

import { IGroupedMarket, IMarketsGroup, IMarketPeriod } from '@edp/services/marketsGroup/markets-group.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

// Regexp for clearing team name (https://stackoverflow.com/a/37668315/8368932)
// eslint-disable-next-line
const clearNameRegExp = /[A-Za-z\u00AA\u00B5\u00BA\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0561-\u0587\u05D0-\u05EA\u05F0-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u08A0-\u08B4\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C60\u0C61\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D05-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E87\u0E88\u0E8A\u0E8D\u0E94-\u0E97\u0E99-\u0E9F\u0EA1-\u0EA3\u0EA5\u0EA7\u0EAA\u0EAB\u0EAD-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u170C\u170E-\u1711\u1720-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1877\u1880-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4B\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1CE9-\u1CEC\u1CEE-\u1CF1\u1CF5\u1CF6\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2C2E\u2C30-\u2C5E\u2C60-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312D\u3131-\u318E\u31A0-\u31BA\u31F0-\u31FF\u3400-\u4DB5\u4E00-\u9FD5\uA000-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB65\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]+/g;

@Injectable()
export class MarketsGroupService {
  private marketsNames: any[] = [];
  private outcomesArray: any = [];
  private allGroupedMarkets: any[] = [];
  private groupedMarketToMarketsNamesDictionary;

  constructor(
    private isPropertyAvailableService: IsPropertyAvailableService,
    private cashOutLabelService: CashOutLabelService,
    private filterService: FiltersService,
  ) {}

  /**
   * Returns MarketsGroup Object that going to be added to marketGroup, so this market participates in ordering rules
   *
   * @param {IMarket[]} markets
   * @param {IGroupedMarket} groupedMarket
   * @returns {IMarketsGroup}
   */
  generateMarketsGroup(markets: IMarket[], groupedMarket: IGroupedMarket): IMarketsGroup {
    this.groupMarkets(markets, groupedMarket);
    return {
      id: Math.floor(Math.random() * 1000), // unique identifier to be used in trackBy directive in the list together with single markets
      name: groupedMarket.name,
      localeName: groupedMarket.localeName,
      marketsGroup: true,
      displayOrder: this.getDisplayOrder(markets, this.marketsNames).displayOrder
    };
  }

  /**
   * Group markets in ordering rules
   *
   * @param {IMarket[]} markets
   * @param {IGroupedMarket} groupedMarket
   * @returns {void}
   */
  groupMarkets(markets: IMarket[], groupedMarket: IGroupedMarket): void {
    // Sets Markets as hidden
    const templateMarketNames = this.getMarketNames(groupedMarket, markets);
    _.each(markets, market => {
      if (templateMarketNames.indexOf(market.templateMarketName) !== -1) {
        market.hidden = true;
      }
    });
    this.generateMarkets(markets, groupedMarket);
  }

  /**
   * Update marketConfig item which market belong to.
   * @param {IMarket} market - market object
   * @param {IGroupedMarket[]} groupedMarkets
   */
  updateMarketsGroup(market: IMarket, groupedMarkets: IGroupedMarket[]): void {
    _.each(groupedMarkets, groupedMarket => {
      if (groupedMarket.periods) {
        _.each(groupedMarket.periods, period => this.updateMarketConfig(period, market, groupedMarket));
      } else {
        this.updateMarketConfig(groupedMarket, market, groupedMarket);
      }
    });
  }

  /**
   * Return array that contains grouped markets localeName in which templateMarketName
   *
   * @param {IGroupedMarket[]} groupedMarket
   * @param {string} templateMarketName
   * @returns {IMarketsGroup[]}
   */
  templateMarketInMarketsGroups(groupedMarket: IGroupedMarket[], templateMarketName: string): IMarketsGroup[] {
    const map = this.groupedMarketToMarketsNamesDictionary || this.createGroupedMarketToMarketsNamesDictionary(groupedMarket),
      foundGroups = [];

    for (const marketsGroup in map) {
      if (Object.prototype.hasOwnProperty.call(map, marketsGroup)) {
        if (map[marketsGroup].indexOf(templateMarketName) !== -1) { // handle search in strings and arrays
          foundGroups.push(marketsGroup);
        }
      }
    }

    return foundGroups;
  }

  /**
   * Checks is Markets Available
   *
   * @param {IMarket[]} allMarkets
   * @param {IMarket[]} markets
   * @param {IGroupedMarket} groupedMarket
   * @returns {boolean}
   */
  isMarketAvailable(allMarkets: IMarket[], markets: IMarket[], groupedMarket: IGroupedMarket): boolean {
    if (!allMarkets || !markets) { return false; }

    const templateMarketNames = this.getMarketNames(groupedMarket, allMarkets);
    return markets.some(market => _.contains(templateMarketNames, market.templateMarketName));
  }

  /**
   * Remove scores from team name: e.g. Team A 1-3 -> Team A
   *
   * @param {string} team
   * @returns {string}
   */
  removeScores(team: string): string {
    let teamName = team;

    if (team && _.isString(team)) {
      // remove score, pipelines, brackets(e.g. Team A 1-1, |Team A| 1-3, Team A (-1.0), Team A (+2.0) -> Team A)
      teamName = team.replace(/\s?(\d+)\s?-\s?(\d+)\s?/g, ' ')
        .replace(/(\|)/g, '')
        .replace(/\s?\(\+?\-?\d+\.\d+\)\s?/g, ' ')
        .trim();
    }

    return teamName;
  }

  /**
   * Returns array with sorted teams
   *
   * @param {IMarket[]} markets
   * @param {boolean} isDraw
   * @returns {*|Array}
   */
  getTeams(markets: IMarket[], isDraw?: boolean): IOutcome[] {
    const teams = this.findTeams(markets, 'MR') || this.findTeams(markets, 'MH') || this.findTeams(markets, 'CS');
    let outcomes: IOutcome[] = teams && teams.outcomes;
    const teamH = this.getFilteredOutcome(outcomes, teams, 'home'); // Team Home
    const drawT = _.findWhere(outcomes, { outcomeMeaningMinorCode: 2 }); // Draw Teams
    const teamA =  this.getFilteredOutcome(outcomes, teams, 'away'); // Team Away
    outcomes = isDraw ? [teamH, drawT, teamA] : [teamH, teamA];
    return this.filterService.orderBy(outcomes.filter((outcome: IOutcome) => outcome), ['outcomeMeaningMinorCode']);
  }

  /**
   * Create Market Names Array
   *
   * @param {IMarketPeriod | IGroupedMarket} groupedMarket
   * @param {IMarket[]} markets
   */
  private marketNamesArray(groupedMarket: IMarketPeriod | IGroupedMarket, markets: IMarket[]): void {
    groupedMarket.marketsTemplates = _.uniq(_.pluck(_.filter(markets, market => {
      return _.isArray(groupedMarket.marketsNames) ? _.contains(groupedMarket.marketsNames, market.templateMarketName)
        : groupedMarket.marketsNames === market.templateMarketName;
    }), 'templateMarketName'));
    this.marketsNames = this.marketsNames.concat(groupedMarket.marketsNames);
  }

  private getFilteredOutcome(outcomes: IOutcome[], teams: IMarket, pos: string):IOutcome {
    const minorCode = ['H', 'O', 'A', 'D'];
    const marketMeaningMinorCode = 'MR';
    if (pos === 'home') {
      return outcomes.find((outcome: IOutcome) =>
        (teams.dispSortName !== marketMeaningMinorCode) ?
          outcome.outcomeMeaningMinorCode === 1 && !minorCode.includes(outcome.originalOutcomeMeaningMinorCode) :
          outcome.outcomeMeaningMinorCode === 1
      );
    } else {
      return outcomes.find((outcome: IOutcome) =>
        teams.dispSortName !== marketMeaningMinorCode ?
          outcome.outcomeMeaningMinorCode === 3 && !minorCode.includes(outcome.originalOutcomeMeaningMinorCode) :
          outcome.outcomeMeaningMinorCode === 3);
    }
  }

  /**
   * Returns market names from fakeMarket object
   *
   * @param {IGroupedMarket} groupedMarket
   * @param {IMarket[]} markets
   * @returns {string[] | string}
   */
  private getMarketNames(groupedMarket: IGroupedMarket, markets: IMarket[]): string[] {
    this.marketsNames = [];

    if (groupedMarket.periods) {
      _.each(groupedMarket.periods, marketPeriod => this.marketNamesArray(marketPeriod, markets));
    } else {
      this.marketNamesArray(groupedMarket, markets);
    }

    return this.marketsNames;
  }

  /**
   * Checks is Markets Available
   *
   * @param {IMarket[]} markets
   * @param {IMarket} dispSortName
   * @returns {IOutcome}
   */
  private findTeams(markets: IMarket[], dispSortName: string): IMarket {
    return _.find(_.where(markets, { dispSortName }), market => {
      const outcomes = _.filter(market.outcomes, outcome => !outcome.fakeOutcome && !!outcome.outcomeMeaningMinorCode);
      return outcomes; // [Home, Draw, Away]
    });
  }

  /**
   * Clear Team Name
   *
   * @param {string} team
   * @returns {string}
   */
  private clearTeamName(team: string): string {
    const match = team.match(clearNameRegExp);
    return match ? match.toString().replace(/,/g, ' ') : team;
  }

  /**
   * Find proper Team
   *
   * @param {IMarket[]} markets
   * @param {number} minorCode
   * @returns {string|*}
   */
  private findTeam(markets: IMarket[], minorCode: number): string {
    const team = _.find(this.getTeams(markets, false), { outcomeMeaningMinorCode: minorCode });
    return team ? this.clearTeamName(team.name) : '';
  }

  /**
   * Get Team Name
   *
   * @param {IMarket[]} markets
   * @param {string[]} names
   * @param {boolean} isMarketName
   * @returns {string}
   */
  private getTeamName(markets: IMarket[], names: string[], isMarketName: boolean): string {
    const homeTeam = this.findTeam(markets, 1);
    const awayTeam = this.findTeam(markets, 3);
    const team = isMarketName ? homeTeam : 'Home';
    return [].concat(names).map(n => this.clearTeamName(n)).toString().indexOf(team) !== -1 ? homeTeam : awayTeam;
  }

  /**
   * Get Sorted Outcomes List
   *
   * @param {IOutcome[]} outcomes
   * @param {IGroupedMarket} groupedMarket
   * @param {boolean} isMinorCode
   */
  private getSortedOutcomes(outcomes: IOutcome[], groupedMarket: IGroupedMarket, isMinorCode: boolean) {
    if (outcomes && outcomes.length) {
      let fakeOutcome: any = [];
      const minorCodeArray = groupedMarket.header && groupedMarket.header.length === 2 ? [1, 3] : [1, 2, 3]; // [Home, Draw, Away]
      const propertiesArray = isMinorCode ? minorCodeArray : groupedMarket.marketsNames;
      const getValue = value => isMinorCode ? { outcomeMeaningMinorCode: value } : { marketsNames: value };

      if (_.isArray(propertiesArray) && propertiesArray.length > 1) {
        _.each(propertiesArray, (val, index) => {
          // Push Fake outcome if outcome is empty
          if (!_.findWhere(outcomes, getValue(val)) && outcomes.length < propertiesArray.length) {
            fakeOutcome = {
              fakeOutcome: true,
              name: groupedMarket.header && groupedMarket.header.length === propertiesArray.length ?
                groupedMarket.header[index].name : outcomes[0].name,
              marketsNames: isMinorCode ? outcomes[0].marketsNames : val,
              prices: outcomes[0].prices,
              cashoutAvail: outcomes[0].cashoutAvail,
              outcomeMeaningMinorCode: isMinorCode ? val : outcomes[0].outcomeMeaningMinorCode
            };
            outcomes.push(fakeOutcome);
          }
          // Add property 'sortOrder' to outcome
          if (groupedMarket.headerToMarket) {
            _.each(outcomes, outcome => {
              if (outcome.marketsNames === val.toString() && groupedMarket.headerToMarket[val]) {
                outcome.sortOrder = groupedMarket.headerToMarket[val].sortOrder;
              }
            });
          }
          // Add property 'sortOrder' to outcome
          if (groupedMarket.sortByHeader) {
            _.each(outcomes, outcome => {
              _.each(groupedMarket.header, header => {
                if (outcome.name.toLowerCase().indexOf(header.name) > -1) {
                  outcome.sortOrder = header.sortOrder;
                }
              });
            });
          }
        });
      }
      return this.filterService.orderBy(outcomes, groupedMarket.outcomesSort);
    }
    return outcomes;
  }

  /**
   * Is has correct Market Type
   *
   * @param {string[] | string} marketType
   * @param {string} typeName
   * @returns {boolean}
   */
  private isMarketType(marketType: string[] | string, typeName: string): boolean {
    if (marketType) {
      return _.isArray(marketType) ? _.contains(marketType, typeName) : marketType === typeName;
    }
    return false;
  }

  /**
   * Market with template Row
   *
   * @param {IMarket} market
   * @param {IOutcome[]} outcomes
   * @param {IGroupedMarket} groupedMarket
   */
  private createMarketWithTemplateRow(market: IMarket, outcomes: IOutcome[], groupedMarket: IGroupedMarket): void {
    if (groupedMarket.sortOrder) {
      _.each(outcomes, outcome => {
        outcome.sortOrder = groupedMarket.sortOrder[outcome.name] || Number(outcome.outcomeMeaningMinorCode);
      });
      market.outcomes = this.filterService.orderBy(outcomes, groupedMarket.outcomesSort);
    }
  }

  /**
   * Market with type
   *
   * @param {IMarket[]} markets
   * @param {IMarket} market
   * @param {IOutcome[]} outcomes
   * @param {IMarketPeriod} marketPeriod
   * @param {IGroupedMarket} groupedMarket
   */
  private createMarketWithTypeOverUnderMarket(
    markets: IMarket[],
    market: IMarket,
    marketPeriod: IMarketPeriod,
    outcomes: IOutcome[],
    groupedMarket: IGroupedMarket): void {
    const marketsArray: any[] = [];

    _.each(this.getTeams(markets, true), item => {
      const marketName = item.name;
      const filteredOutcomes = _.filter(outcomes, outcome => outcome.name.indexOf(marketName) !== -1);
      const sortedOutcomes = this.getSortedOutcomes(filteredOutcomes, groupedMarket, true);

      if (sortedOutcomes && sortedOutcomes.length) {
        const marketObject = {
          name: marketName,
          priceTypeCodes: market.priceTypeCodes,
          cashoutAvail: market.cashoutAvail,
          outcomes: sortedOutcomes
        };
        marketsArray.push(marketObject);
      }
    });

    groupedMarket.drilldownTagNames = market.drilldownTagNames;

    marketPeriod.markets = marketsArray;
  }

  /**
   * Market with type marketHeader
   *
   * @param {IMarket[]} markets
   * @param {IGroupedMarket} groupedMarket
   */
  private createMarketWithTypeMarketHeader(markets: IMarket[], groupedMarket: IGroupedMarket): void {
    const keyName = groupedMarket.type === 'teams' ? 'outcomeMeaningMinorCode' : 'name';

    if (this.isMarketType(groupedMarket.type, 'noGoalscorer')) {
      this.createMarketWithTypeNoGoalscorer(groupedMarket);
    }

    groupedMarket.markets = _.groupBy(_.flatten(this.outcomesArray), keyName);
    groupedMarket.markets = _.map(groupedMarket.markets, (val, key) => {
      const outcomes = this.getSortedOutcomes(groupedMarket.markets[key], groupedMarket, false);
      return {
        name: key,
        priceTypeCodes: outcomes[0].priceTypeCodes,
        cashoutAvail: _.where(outcomes, { cashoutAvail: 'Y' }).length ? 'Y' : 'N',
        outcomeMeaningMinorCode: _.uniq(_.pluck(outcomes, 'outcomeMeaningMinorCode')),
        outcomePrice: outcomes[0] && outcomes[0].prices[0] && outcomes[0].prices[0].priceDec,
        outcomes
      };
    });

    groupedMarket.periods = _.map(this.getTeams(markets, false), team => {
      return {
        marketsNames: groupedMarket.marketsNames,
        localeName: this.clearTeamName(team.name),
        markets: this.filterService.orderBy(_.filter(groupedMarket.markets, (market: IMarket) => {
          return market.outcomeMeaningMinorCode.indexOf(team.outcomeMeaningMinorCode as string) !== -1;
        }), groupedMarket.marketSort)
      };
    });
  }

  /**
   * Market with type noGoalscorer
   *
   * @param {IGroupedMarket} groupedMarket
   */
  private createMarketWithTypeNoGoalscorer(groupedMarket: IGroupedMarket): void {
    const noGoalscorerOutcomes = _.where(_.flatten(this.outcomesArray), { outcomeMeaningMinorCode: 2 }); // [Draw]
    if (noGoalscorerOutcomes && noGoalscorerOutcomes.length) {
      const outcomes = this.getSortedOutcomes(noGoalscorerOutcomes, groupedMarket, false);
      groupedMarket.noGoalscorer = {
        name: 'No Goalscorer',
        priceTypeCodes: outcomes[0].priceTypeCodes,
        outcomes
      };
    }
  }

  /**
   * Create Markets Array
   *
   * @param {object} marketPeriod
   * @param {IGroupedMarket} groupedMarket
   * @param {IMarket[]} markets
   */
  private getMarketsObg(markets: IMarket[], groupedMarket: IGroupedMarket, marketPeriod: IMarketPeriod): void {
    const headerArray = [];
    const isTeamsHDA = this.isMarketType(groupedMarket.type, 'marketHeader') || this.isMarketType(groupedMarket.type, 'teams');
    this.outcomesArray = [];

    marketPeriod.markets = _.compact(_.map(markets, marketEntity => {
      return marketPeriod.marketsTemplates.indexOf(marketEntity.templateMarketName) !== -1 ? marketEntity : null;
    }));

    if (marketPeriod.markets.length) {
      _.each(marketPeriod.markets, (market: IMarket) => {
        if(!market.originalMarketName) {
          market.originalMarketName = market.name;
        }
        const outcomes = market.outcomes || [];

        market.outcomeMeaningMinorCode = _.compact(_.uniq(_.pluck(outcomes, 'outcomeMeaningMinorCode')));
        market.outcomes = this.filterService.orderBy(outcomes, groupedMarket.outcomesSort);
        _.each(outcomes, outcome => {
          outcome.cashoutAvail = market.cashoutAvail;
          outcome.marketsNames = market.templateMarketName;
          outcome.priceTypeCodes = market.priceTypeCodes;
          outcome.marketStatusCode = market.marketStatusCode;
          outcome.marketliveServChannels = market.liveServChannels;
          outcome.isMarketBetInRun = market.isMarketBetInRun;
          outcome.alphabetName = this.filterService.filterAlphabetsOnly(outcome.name);
          outcome.numbersName = this.filterService.filterNumbersOnly(outcome.name);
          if (market.rawHandicapValue) {
            outcome.rawHandicapValue = market.rawHandicapValue;
          }
        });

        if (groupedMarket.headerToMarket && groupedMarket.headerToMarket[market.templateMarketName]) {
          headerArray.push(groupedMarket.headerToMarket[market.templateMarketName]);
          groupedMarket.header = this.filterService.orderBy(_.uniq(headerArray), groupedMarket.outcomesSort);
        }

        if (this.isMarketType(groupedMarket.type, 'teamSwitch')) {
          marketPeriod.localeName = this.getTeamName(markets, marketPeriod.marketsNames as string[], false);
        }

        if (this.isMarketType(groupedMarket.type, 'goalName')) {
          const match = market.name.toString().match(/(\d\+\s\w+)|(.\d\.\d\s\w+)/g);
          market.name = match ? match[0] : market.name;
        }

        if (this.isMarketType(groupedMarket.type, 'handicapName')) {
          market.name = market.rawHandicapValue;
        }

        if (this.isMarketType(groupedMarket.type, 'handicapNamePlus')) {
          const handicap = Number(market.rawHandicapValue);
          market.name = (handicap > 0) ? `+${handicap}` : handicap.toString();
        }

        if (this.isMarketType(groupedMarket.type, 'marketName')) {
          market.name = this.getTeamName(markets, [market.name], true);
        }

        if (this.isMarketType(groupedMarket.type, 'minorCode')) {
          market.outcomes = this.getSortedOutcomes(outcomes, groupedMarket, true);
        }

        if (groupedMarket.template === 'row') {
          this.createMarketWithTemplateRow(market, outcomes, groupedMarket);
        }

        if (this.isMarketType(groupedMarket.type, 'overUnderMarket')) {
          this.createMarketWithTypeOverUnderMarket(markets, market, marketPeriod, outcomes, groupedMarket);
        }

        if (isTeamsHDA) {
          this.outcomesArray.push(outcomes);
        }
      });

      if (groupedMarket.marketSort) {
        marketPeriod.markets = this.filterService.orderBy(marketPeriod.markets, groupedMarket.marketSort);
      }

      if (this.isMarketType(groupedMarket.type, 'headerTeamName')) {
        const teamName = this.getTeamName(markets, [marketPeriod.marketsNames as string], false);
        groupedMarket.name = `Over/Under Goals ${teamName}`;
      }

      if (isTeamsHDA) {
        this.createMarketWithTypeMarketHeader(markets, groupedMarket);
      }
    }

    this.allGroupedMarkets = this.allGroupedMarkets.concat(marketPeriod.markets);
  }

  /**
   * adds proper markets to MarketsGroup Object
   *
   * @param {IMarket[]} markets
   * @param {IGroupedMarket} groupedMarket
   */
  private generateMarkets(markets: IMarket[], groupedMarket: IGroupedMarket): void {
    this.allGroupedMarkets = [];
    const isAnyCashoutAvailable = this.isPropertyAvailableService.isPropertyAvailable(
      this.cashOutLabelService.checkCondition.bind(this.cashOutLabelService)
    );

    if (groupedMarket.periods) {
      _.each(groupedMarket.periods, period => this.getMarketsObg(markets, groupedMarket, period));
    } else {
      this.getMarketsObg(markets, groupedMarket, groupedMarket);
    }
    // adding cashoutAvail property to fakeMarket if there at least one market have: cashoutAvail: 'Y'
    if (this.allGroupedMarkets.length) {
      groupedMarket.cashoutAvail = isAnyCashoutAvailable(this.allGroupedMarkets, [{ cashoutAvail: 'Y' }]);
      groupedMarket.marketsAvailable = true;
    }
  }

  /**
   * Searching for correct DisplayOrder (min value of all Markets in fakeMarket object)
   *
   * @param {IMarket[]} markets
   * @param {string[]} templateMarketNames
   * @returns {IMarket}
   */
  private getDisplayOrder(markets: IMarket[], templateMarketNames: string[]): IMarket {
    return markets.filter(market => {
      return templateMarketNames.indexOf(market.templateMarketName) !== -1;
    }).reduce((min, current) => {
      return min.displayOrder > current.displayOrder ? current : min;
    });
  }

  /**
   * Updates marketConfig item or it's period which market belong to.
   *
   * @param {IMarketPeriod} marketPeriod - marketConfig array item or period if this market type item has periods
   * @param {IMarket} market - market object which was updated
   * @param {IGroupedMarket} groupedMarket - marketConfig array item
   */
  private updateMarketConfig(marketPeriod: IMarketPeriod, market: IMarket, groupedMarket: IGroupedMarket): void {
    _.each(marketPeriod.markets, (groupMarket: IMarket) => {
      if (groupMarket.id === market.id) {
        this.getMarketsObg(marketPeriod.markets, groupedMarket, marketPeriod);
      }
    });
  }

  /**
   * Creates Dictionary that can be used for search or comparison markets templates in grouped markets
   *
   * @param {IGroupedMarket[]} groupedMarket
   * @returns {{}|*}
   */
  private createGroupedMarketToMarketsNamesDictionary(groupedMarket: IGroupedMarket[]): { [key: string]: string[] } {
    this.groupedMarketToMarketsNamesDictionary = {};

    _.each(groupedMarket, (market: IGroupedMarket) => {
      if (market.periods) {
        this.groupedMarketToMarketsNamesDictionary[market.localeName] =
          market.periods.reduce((arr, period) => arr.concat(period.marketsNames), []);
      } else {
        this.groupedMarketToMarketsNamesDictionary[market.localeName] = market.marketsNames;
      }
    });

    return this.groupedMarketToMarketsNamesDictionary;
  }
}
