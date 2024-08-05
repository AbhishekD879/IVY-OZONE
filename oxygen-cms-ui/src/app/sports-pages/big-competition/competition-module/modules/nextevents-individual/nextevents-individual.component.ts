import {Component, Input, OnInit} from '@angular/core';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

import {AppConstants} from '@app/app.constants';
import {CompetitionModule} from '../../../../../client/private/models';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import {Event} from '@app/client/private/models/event.model';
import {OBEvents} from '@app/client/private/models/obEvents.model';

@Component({
  selector: 'nextevents-individual',
  templateUrl: './nextevents-individual.component.html',
  styleUrls: ['./nextevents-individual.component.scss']
})
export class NexteventsIndividualComponent implements OnInit {
  @Input() module: CompetitionModule;

  public events: Array<Event> = [];
  public eventId: number;
  public storedEvents: Event[] = [];
  public eventIdIsValid: boolean = true;
  public eventIdExists: boolean = false;
  public appliedSelection: Event[] = [];
  public loadedEventIds: string;
  public invalidEventIds: number[] = [];

  constructor(private bigCompetitionAPIService: BigCompetitionAPIService,
              private snackBar: MatSnackBar) { }

  ngOnInit() {
    this.loadInitData();
  }

  /**
   * Perform call to get events data if module has eventsIds
   */
  private loadInitData(): void {
    if (this.module && this.module.eventIds && this.module.eventIds.length) {
      const options = { eventIds: this.module.eventIds.toString() };

      this.bigCompetitionAPIService.getSiteServeEvents(options)
        .map((events: HttpResponse<OBEvents>) => {
          return events.body;
        })
        .subscribe((events: OBEvents) => {
          this.eventIdIsValid = true;
          this.events = events.valid;
          this.invalidEventIds = events.invalid.map(id => Number(id));
          this.loadedEventIds = this.getValidEventIds();
        });
    }
  }

  /**
   * Concatenate all valid event ids
   * @returns {string}
   */
  private getValidEventIds(): string {
    return _.difference(this.module.eventIds, this.invalidEventIds).join(', ');
  }

  /**
   * Load event data from site serve(id, name)
   */
  public uploadEventData(): void {
    const isEventIdExists = _.find(this.storedEvents, (event: Event) => event.id === this.eventId) ||
      _.find(this.events, (event: Event) => event.id === this.eventId);

    if (!isEventIdExists) {
      this.bigCompetitionAPIService.getSiteServeEvents({ eventIds: this.eventId })
        .map((events: HttpResponse<OBEvents>) => {
          return events.body;
        })
        .subscribe((events: OBEvents) => {
          this.eventIdExists = false;

          if (events.valid.length) {
            _.each(events.valid, event => this.storedEvents.push(event));
            this.eventIdIsValid = true;
            this.showMessage();
            this.eventId = null;
          } else {
            this.eventIdIsValid = this.eventIdExists = false;
          }
        }, () => {
          this.eventIdIsValid = this.eventIdExists = false;
        });
    } else {
      this.eventIdIsValid = this.eventIdExists = true;
    }
  }

  /**
   * Show message banner according to response
   */
  private showMessage(): void {
    this.snackBar.open('OPENBET EVENT LOADED!!', 'OK!', {
      duration: AppConstants.HIDE_DURATION
    });
  }

  /**
   * Move loaded OB events data to Module data.
   */
  public applyOpenBetData(): void {
    this.addId(this.storedEvents);
    this.loadedEventIds = this.getValidEventIds();
    this.storedEvents = [];
  }

  /**
   * Add new event id to module
   * @param {array} events
   */
  private addId(events: Event[]): void {
    _.each(events, event => {
      this.module.eventIds.push(Number(event.id));
      this.events.push(event);
    });
  }

  /**
   * Remove all events from module
   */
  public removeModuleEvents(): void {
    this.module.eventIds = [];
    this.events = [];
    this.loadedEventIds = '';
    this.invalidEventIds = [];
  }

  /**
   * Remove event from events list
   * @param event
   */
  public removeEventId(event: Event): void {
    this.events.splice(this.events.indexOf(event), 1);
    this.module.eventIds.splice(this.module.eventIds.indexOf(Number(event.id)), 1);
    this.loadedEventIds = this.getValidEventIds();

    this.snackBar.open(`EVENT ${event.name} HAS BEEN REMOVED!!!`, 'OK!', {
      duration: AppConstants.HIDE_DURATION
    });
  }

  /**
   * Remove invalid event ids from module
   */
  public removeInvalidIds(): void {
    _.map(this.invalidEventIds, id => {
      this.module.eventIds.splice(this.module.eventIds.indexOf(id), 1);
    });
    this.invalidEventIds = [];
  }

  /**
   * Check if field maxDisplay is valid(not empty)
   * @returns {boolean}
   */
  public isValidForm(): boolean {
    return !!this.module.maxDisplay;
  }

  /**
   * Check if events exists
   * @returns {boolean}
   */
  public isEventsExists(): boolean {
    return !!(this.events.length || this.invalidEventIds.length);
  }
}
