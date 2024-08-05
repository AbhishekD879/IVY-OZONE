import { YOURCALL_EVENTS_STATUS } from '../constants/yourcall-events-status';
import * as _ from 'underscore';
import { IBybEventConfig } from '@yourcall/models/byb-event-config.model';
import { IYourCallGameTeam } from '@yourcall/models/game-data.model';

interface IYourcallEventOptions {
  ds?: any;
  byb?: any;
}

export class YourCallEvent {
  _obEventId: number;

  private readonly _obTypeId: number;
  private readonly _obSportId: number;
  private readonly _title: string;
  private readonly _startDate: string;
  private readonly _isFiveASideNewIconAvailable: boolean;
  private readonly _hasPlayerProps: boolean;
  private readonly _homeTeam: IYourCallGameTeam;
  private readonly _visitingTeam: IYourCallGameTeam;

  private _isEnabledYCTab: boolean;
  private _isFiveASideAvailable: boolean;
  private _byb: IBybEventConfig;

  constructor(obEventId, obTypeId, obSportId, title, homeTeam, visitingTeam, startDate, hasPlayerProps, tabs,
              options: IYourcallEventOptions) {
    this._obEventId = obEventId;
    this._obTypeId = obTypeId;
    this._obSportId = obSportId;
    this._title = title;
    this._startDate = startDate;
    this._homeTeam = _.pick(homeTeam, 'abbreviation', 'title');
    this._visitingTeam = _.pick(visitingTeam, 'abbreviation', 'title');
    this._isEnabledYCTab = tabs.isEnabledYCTab;
    this._isFiveASideAvailable = tabs.isFiveASideAvailable;
    this._isFiveASideNewIconAvailable = tabs.isFiveASideNewIconAvailable;
    this._hasPlayerProps = hasPlayerProps;

    // we should set ds data optionally for DS event because it is required when getting markets/selections
    this.byb = options && options.byb;
  }

  get obEventId(): number {
    return this._obEventId;
  }

  get isFiveASideNewIconAvailable(): boolean {
    return this._isFiveASideNewIconAvailable;
  }

  get isEnabledYCTab(): boolean {
    return this._isEnabledYCTab;
  }

  set isEnabledYCTab(value: boolean) {
    this._isEnabledYCTab = value;
  }

  get isFiveASideAvailable(): boolean {
    return this._isFiveASideAvailable;
  }

  set isFiveASideAvailable(value: boolean) {
    this._isFiveASideAvailable = value;
  }
  
  get hasPlayerProps(): boolean {
    return this._hasPlayerProps;
  }

  get obTypeId(): number {
    return this._obTypeId;
  }

  get obSportId(): number {
    return this._obSportId;
  }

  get title(): string {
    return this._title;
  }

  get homeTeam(): IYourCallGameTeam {
    return this._homeTeam;
  }

  get visitingTeam(): IYourCallGameTeam {
    return this._visitingTeam;
  }

  get startDate(): string {
    return this._startDate;
  }

  get isActive(): boolean {
    return (this._byb && this._byb.status === YOURCALL_EVENTS_STATUS.BYB.ACTIVE);
  }
  set isActive(value:boolean){}

  get byb(): IBybEventConfig {
    return this._byb;
  }

  /**
   * Set BYB (Banach) related event data
   * @param bybData
   */
  set byb(bybData) {
    if (bybData) {
      this._byb = _.pick(bybData, 'status', 'homeTeam', 'visitingTeam');
    }
  }
}
