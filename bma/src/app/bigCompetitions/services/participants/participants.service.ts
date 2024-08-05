import { Injectable } from '@angular/core';
import { FiltersService } from '@core/services/filters/filters.service';
import * as _ from 'underscore';
import { IParticipant, IParticipants, IParticipantFromName } from './participants.model';

@Injectable()
export class ParticipantsService {

  participants: IParticipants[] = [];

  constructor(
    private filtersService: FiltersService
  ) { }
  /**
   * Stores participants details.
   * @param {Object} participants
   */
  store(participants: IParticipants[]): void {
    this.participants = participants;
  }

  /**
   * Parses svg strings from participant details.
   * @return {string}
   */
  getFlagsList(): string {
    return _.reduce(this.participants, (memo, participant) => {
      return participant.svg ? `${memo}${participant.svg}` : memo;
    }, '');
  }

  /**
   * Parses particiapnt from passed name and returns Home and Away details.
   * @param {string} name
   * @return {Object}
   */
  parseParticipantsFromName(name: string): IParticipantFromName {
    const homeName = this.filtersService.getTeamName(name, 0) || name;
    const awayName = this.filtersService.getTeamName(name, 1);

    return {
      HOME: this.getParticipant(homeName.trim()),
      AWAY: this.getParticipant(awayName.trim())
    };
  }

  /**
   * Retrieves participant details from stored map or
   *   returns default values in case if not found stored details.
   * @param {string} name
   * @return {Object}
   * @private
   */
  private getParticipant(name: string = ''): IParticipant {
    if (this.participants[name]) {
      return this.participants[name];
    }

    return {
      name,
      abbreviation: this.createAbbreviation(name)
    };
  }

  /**
   * Creates abbreviation from given name - first 3 characters in upper case.
   * @param {string} name
   * @return {string}
   * @private
   */
  private createAbbreviation(name: string): string {
    return name
      .replace(/\s/g, '')
      .toUpperCase()
      .substr(0, 3);
  }

}
