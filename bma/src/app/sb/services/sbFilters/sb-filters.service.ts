import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IOutcome } from '@core/models/outcome.model';

@Injectable()
export class SbFiltersService {

  constructor() {}

  orderOutcomeEntities(
    input: IOutcome[],
    isLpAvailable: string | boolean,
    sortByNonRunner?: boolean,
    sortByRunnerNumber?: boolean,
    hideNonRunners?: boolean,
    hideFavourite?: boolean,
    sortByTrapNumber?: boolean): IOutcome[] {
    let outcomeEntities = [];
    if (isLpAvailable === 'true' || isLpAvailable === true) {
      outcomeEntities = input;
      outcomeEntities.sort((a: IOutcome, b: IOutcome) => {
        const aPrice = this.outcomePrice(a);
        const bPrice = this.outcomePrice(b);

        if (aPrice !== bPrice) {
          if (aPrice && !bPrice) { return -1; }
          if (!aPrice && bPrice) { return 1; }
          if (aPrice > bPrice) { return 1; }
          if (aPrice < bPrice) { return -1; }
        }

        const aNumber = sortByTrapNumber ? a.trapNumber : a.runnerNumber;
        const bNumber = sortByTrapNumber ? b.trapNumber : b.runnerNumber;
        if (aNumber && bNumber) {
          if (Number(aNumber) > Number(bNumber)) { return 1; }
          if (Number(aNumber) < Number(bNumber)) { return -1; }
        }

        if (a.name > b.name) { return 1; }
        if (a.name < b.name) { return -1; }

        return 1;
      });
    } else {
      outcomeEntities = this.filterSpOutcomes(input, sortByRunnerNumber, sortByTrapNumber);
    }

    if (hideNonRunners) {
      outcomeEntities = _.filter(outcomeEntities, item => item.name.search(/N\/R$/) === -1);
    } else {
      outcomeEntities.forEach((raceOutcome: IOutcome) => {
        raceOutcome.nonRunner = raceOutcome.name.search(/N\/R$/) > -1;
      });

      if (sortByNonRunner) {
        const [runners, nonRunners] = _.partition(outcomeEntities, item => item.name.search(/N\/R$/) === -1),
          orderedNonRunners = _.sortBy(nonRunners, item => Number(item.runnerNumber));
        outcomeEntities = [...runners, ...orderedNonRunners];
      }
    }

    outcomeEntities = this.findFavourite(outcomeEntities, '1', hideFavourite); // '1' - outcomeMeaningMinorCode for UNNAMED FAVOURITE
    outcomeEntities = this.findFavourite(outcomeEntities, '2', hideFavourite); // '2' - outcomeMeaningMinorCode for UNNAMED 2nd FAVOURITE

    const [hasRunnerNumber, withoutRunnerNumber] = _.partition(outcomeEntities, item => item.runnerNumber);

    return [...hasRunnerNumber, ...withoutRunnerNumber];
  }

  orderOutcomesByName(input: IOutcome[]): IOutcome[] {
    const [runners, nonRunners] = _.partition(input, item => item.name.search(/N\/R$/) === -1);
    nonRunners.sort((a: IOutcome, b: IOutcome) => {
      if (a.runnerNumber && b.runnerNumber) {
        if (Number(a.runnerNumber) > Number(b.runnerNumber)) {
          return 1;
        }
        if (Number(a.runnerNumber) < Number(b.runnerNumber)) {
          return -1;
        }
      } else {
        if (a.name > b.name) {
          return 1;
        }
        if (a.name < b.name) {
          return -1;
        }
      }
    });
    const orderedNonRunners = nonRunners.map(nr => {
      nr.nonRunner = true;
      return nr;
    });

    let nammedRunners = runners.filter(r => !r.name.includes('Unnamed'));
    nammedRunners = _.chain(nammedRunners).sortBy((outcome: IOutcome) => outcome.name.toLowerCase()).value();

    let unnammedRunners = runners.filter(r => r.name.includes('Unnamed'));
    unnammedRunners = _.sortBy(unnammedRunners, 'outcomeMeaningMinorCode');

    return [...nammedRunners, ...orderedNonRunners, ...unnammedRunners];
  }

  outcomeMinorCodeName(input: string): string | boolean {
    switch (input) {
      case 'H':
        return 'sb.home';
      case 'A':
        return 'sb.away';
      case 'D':
        return 'sb.draw';
      default:
        return false;
    }
  }

  /*
   * filter SP available outcomes
   * @param {array} outcomes
   * @return {array} sorted outcomes
   */
  private filterSpOutcomes(outcomes: IOutcome[], sortByRunnerNumber: boolean, sortByTrapNumber?: boolean): IOutcome[] {
    const runnerNumbers = this.findRunnerNumbers(outcomes),
      outcomesCountWithoutFav = this.getOutcomesWithoutFav(outcomes);
    let sortedOutcomes;

    if ((runnerNumbers === outcomesCountWithoutFav || runnerNumbers > 0) && sortByRunnerNumber) {
      sortedOutcomes = outcomes;
      sortedOutcomes.sort((a, b) => {
        const aNumber = sortByTrapNumber ? a.trapNumber : a.runnerNumber;
        const bNumber = sortByTrapNumber ? b.trapNumber : b.runnerNumber;
        if (Number(aNumber) < Number(bNumber) || !aNumber) {
          return -1;
        }
        if (Number(aNumber) > Number(bNumber) || !bNumber) {
          return 1;
        }
        return 0;
      });

    } else {
      sortedOutcomes = _.sortBy(outcomes, 'name');
    }
    return sortedOutcomes;
  }

  /**
   * Orders outcomes by price
   * @param outcomeEntity
   */
  private outcomePrice(outcomeEntity: IOutcome): number {
    let price = null;
    if (outcomeEntity.prices[0]) {
      price = (outcomeEntity.prices[0].priceNum / outcomeEntity.prices[0].priceDen) + 1;
    }
    return price;
  }

  /**
   * Finds outcome with according outcomeMeaningMinorCode and moves is to the end of the list
   * @return {*}
   * @param outcomeEntities
   * @param outcomeMeaningMinorCode
   */
  private findFavourite(outcomeEntities: IOutcome[], outcomeMeaningMinorCode: string, hideFavourite?: boolean): IOutcome[] {
    const favourite = _.find(outcomeEntities, (outcome: IOutcome) => {
      return outcome.outcomeMeaningMinorCode === outcomeMeaningMinorCode;
    });
    let filteredOutcomeEntities;
    if (favourite) {
      filteredOutcomeEntities = _.without(outcomeEntities, favourite);
      if (hideFavourite) {
        return filteredOutcomeEntities;
      }
      filteredOutcomeEntities.push(favourite);
    }

    return favourite ? filteredOutcomeEntities : outcomeEntities;
  }

  /*
   * find runner numbers
   * @param {array} outcomes
   * @return {number} number of outcome with runner numbers
   */
  private findRunnerNumbers(outcomes?: IOutcome[]): number {
    return outcomes && outcomes.reduce((sum, curr) => curr.runnerNumber ? sum + 1 : sum, 0);
  }

  /*
   * count outcomes that are not handicaps
   * @param {array} outcomes
   * @return {number} number of non favorite outcomes
   */
  private getOutcomesWithoutFav(outcomes?: IOutcome[]): number {
    return outcomes && outcomes.reduce((sum, curr) => {
      const oMMC = curr.outcomeMeaningMinorCode;
      return oMMC !== '1' && oMMC !== '2' ? sum + 1 : sum;
    }, 0);
  }
}
