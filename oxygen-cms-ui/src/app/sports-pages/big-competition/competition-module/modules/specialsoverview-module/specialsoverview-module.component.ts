import {Component, Input, OnInit} from '@angular/core';
import {CompetitionModule, OBEvents, SpecialsOBEvents} from '../../../../../client/private/models';
import {DataSelection} from '../../../../../client/private/models/homemodule.model';
import {AppConstants} from '../../../../../app.constants';
import {GlobalLoaderService} from '../../../../../shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import * as _ from 'lodash';

enum selectIdTypes {
  Type = 'Type',
  Event = 'Event'
}

@Component({
  selector: 'app-specialsoverview-module',
  templateUrl: './specialsoverview-module.component.html',
  styleUrls: ['./specialsoverview-module.component.scss']
})
export class SpecialsoverviewModuleComponent implements OnInit {
  public selectIdTypesEnum: object = selectIdTypes;
  public selectIdTypesOptions: string[] = Object.keys(selectIdTypes);
  // Data loaded from OB
  public eventsSelection: SpecialsOBEvents[] = [];
  // Applied data
  public appliedSelection: SpecialsOBEvents[] = [];
  // Data from selection fields
  public dataSelection: DataSelection = {
    selectionType: this.selectIdTypesOptions[0],
    selectionId: ''
  };
  public loadedTypeIds: number[] = [];
  public loadedEventIds: number[] = [];
  public typeIdAlreadyUsed: number = null;
  public eventIdAlreadyUsed: number = null;
  public invalidEventIds: number[] = [];
  // Duplicate ids between applied and loaded
  public duplicateLoadedIds: SpecialsOBEvents[] = [];
  public invalidEventIdsOnLoad: number[] = [];
  // Used for storing input values in case if it will be changed before applying
  public storedSelectIdValue: string;
  public storedSelectTypeValue: string;
  @Input() module: CompetitionModule;

  constructor(
    private snackBar: MatSnackBar,
    private globalLoaderService: GlobalLoaderService,
    private bigCompetitionAPIService: BigCompetitionAPIService
  ) {}

  ngOnInit() {
    this.initSpecialModule();
  }

  /**
   * Set init data and get saved events
   */
  initSpecialModule(): void {
    this.loadedTypeIds = this.module.specialModuleData.typeIds;
    this.loadedEventIds = this.module.specialModuleData.eventIds;
    // Clear loaded events in "Events in Module" field
    this.appliedSelection = [];
    if (this.module.specialModuleData.typeIds && this.module.specialModuleData.typeIds.length) {
      this.loadOpenBetData(this.module.specialModuleData.typeIds, 'Type', true);
    }
    if (this.module.specialModuleData.eventIds && this.module.specialModuleData.eventIds.length) {
      this.loadOpenBetData(this.module.specialModuleData.eventIds, 'Event', true);
    }
  }

  /**
   * Load OB event/'s by Type or Event id
   * @param {array} ids
   * @param {string} idType
   * @param {boolean} initLoad
   */
  loadOpenBetData(ids, idType, initLoad = false): void {
    // Clear events from "Loaded from OpenBat" field
    this.eventsSelection = [];
    if (!initLoad) {
      this.checkId(ids, idType);
    }
    if (ids.length && !this.eventIdAlreadyUsed && !this.typeIdAlreadyUsed) {
      const service = this.bigCompetitionAPIService;
      if (idType === 'Type') {
        // load by Type id
        this.showHideSpinner();
        service
          .getSiteServeEventsByType({ typeIds: ids, onlySpecials: true })
          .map((data: HttpResponse<OBEvents>) => data.body)
          .subscribe((data: OBEvents) => {
            this.handleOBResponse(data, initLoad);
            if (!initLoad && data.valid.length) {
              this.storeInputsValues();
            }
          }, () => {
            this.snackBar.open('OB EVENTS NOT FOUND!!', 'OK!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
      } else {
        // load by Event id
        this.showHideSpinner();
        service
          .getSiteServeEvents({ eventIds: ids, onlySpecials: true })
          .map((data: HttpResponse<OBEvents>) => data.body)
          .subscribe((data: OBEvents) => {
            this.handleOBResponse(data, initLoad);
            if (!initLoad && data.valid.length) {
              this.storeInputsValues();
            }
          }, () => {
            this.snackBar.open('OB EVENTS NOT FOUND!!', 'OK!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
      }
    }
  }

  /**
   * Load Ob data by user action
   */
  public applyDataByUser(ids, idType): void {
    this.loadOpenBetData(ids, idType);
  }

  /**
   * Check if ID already used
   * @param {array} ids
   * @param {string} type
   */
  private checkId(ids, type): void {
    ids = ids.split(',');
    _.map(ids, id => {
      if (this.typeIdAlreadyUsed || this.eventIdAlreadyUsed) {
        return;
      }
      if (type === 'Type') {
        this.typeIdAlreadyUsed = _.find(this.loadedTypeIds, (i) => i.toString() === id);
        return;
      }
      this.eventIdAlreadyUsed = _.find(this.loadedEventIds, (i) => i.toString() === id);
    });
  }

  /**
   * Add new id to module
   * @param {string} ids
   * @param {string} idType
   */
  private addId(ids, idType): void {
    ids = ids.split(',');
    _.each(ids, id => {
      // Do not add invalid ids
      const invalidId = _.find(this.invalidEventIds, i => i === id);
      if ((idType === 'Type') && !invalidId) {
        this.module.specialModuleData.typeIds.push(Number(id));
        this.loadedTypeIds = this.module.specialModuleData.typeIds;
      } else if (!invalidId) {
        this.module.specialModuleData.eventIds.push(Number(id));
        this.loadedEventIds = this.module.specialModuleData.eventIds;
      }
    });
  }

  /**
   * Perform actions on OB response
   * @param {object} data
   * @param {boolean} initLoad
   */
  private handleOBResponse(data, initLoad): void {
    this.showHideSpinner(false);
    if (initLoad) {
      this.appliedSelection = this.appliedSelection.concat(data.valid);
      this.invalidEventIdsOnLoad = this.invalidEventIdsOnLoad.concat(data.invalid);
      this.eventsSelection = [];
    } else {
      this.invalidEventIds = data.invalid;
      this.eventsSelection = this.eventsSelection.concat(data.valid);
    }
    this.checkIdWasApplied();
    this.showMessage(data.valid.length);
  }

  /**
   * Show message banner according to response
   * @param {boolean} dataLength
   */
  private showMessage(dataLength): void {
    if (dataLength) {
      this.snackBar.open('OPENBET EVENTS LOADED!!', 'OK!', {
        duration: AppConstants.HIDE_DURATION
      });
    } else {
      this.snackBar.open('OPENBET EVENTS NOT FOUND!!', 'OK!', {
        duration: AppConstants.HIDE_DURATION
      });
    }
  }

  canReloadEvents(): boolean {
    return !!(this.dataSelection.selectionId && this.dataSelection.selectionType);
  }

  /**
   * Move loaded OB events data to Module data.
   */
  applyOpenBetData(): void {
    this.addId(this.storedSelectIdValue, this.storedSelectTypeValue);
    this.appliedSelection = this.appliedSelection.concat(this.eventsSelection);
    this.eventsSelection = [];
    this.invalidEventIds = [];
  }

  /**
   * Check if duplicate ids present between applied and loaded ids
   */
  checkIdWasApplied(): void {
    const appliedIds = _.map(this.appliedSelection, 'id');
    this.duplicateLoadedIds = _.filter(this.eventsSelection, el => appliedIds.indexOf(el.id) !== -1);
  }

  isIdAlreadyApplied(id): SpecialsOBEvents {
    return _.find(this.duplicateLoadedIds, el => el.id === id);
  }

  removeModuleEvents(): void {
    this.module.specialModuleData.typeIds = [];
    this.module.specialModuleData.eventIds = [];
    this.appliedSelection = [];
    this.loadedTypeIds = [];
    this.loadedEventIds = [];
    this.typeIdAlreadyUsed = null;
    this.eventIdAlreadyUsed = null;
  }

  /**
   * Remove event id from ids list
   * @param {number} id
   */
  public removeEventId(id): void {
    this.module.specialModuleData.eventIds = this.module.specialModuleData.eventIds.filter(item => item !== id);
    this.module.specialModuleData.typeIds = this.module.specialModuleData.typeIds.filter(item => item !== id);
    if (this.module.specialModuleData.eventIds.length || this.module.specialModuleData.typeIds.length) {
      // should perform init on id remove, because event/'s status could change
      this.initSpecialModule();
    } else {
      this.removeModuleEvents();
    }
  }

  /**
   * These values need in case if the user will change input values
   * and after apply changes
   */
  storeInputsValues(): void {
    this.storedSelectTypeValue = this.dataSelection.selectionType;
    this.storedSelectIdValue = this.dataSelection.selectionId;
  }

  clearUsedIdStates(): void {
    this.typeIdAlreadyUsed = null;
    this.eventIdAlreadyUsed = null;
  }

  isIdUsed(): boolean {
    const isUsed = this.dataSelection.selectionType === 'Type' ? this.typeIdAlreadyUsed : this.eventIdAlreadyUsed;
    return !!(isUsed && this.dataSelection.selectionId);
  }

  /**
   * @param {boolean} toShow
   */
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
  }

  /**
   * Remove invalid event ids from module
   */
  public removeInvalidIds(): void {
    _.map(this.invalidEventIdsOnLoad, id => {
      id = Number(id);
      this.loadedTypeIds = this.loadedTypeIds.filter(item => item !== id);
      this.loadedEventIds = this.loadedEventIds.filter(item => item !== id);
      this.module.specialModuleData.eventIds = this.module.specialModuleData.eventIds.filter(item => item !== id);
      this.module.specialModuleData.typeIds = this.module.specialModuleData.typeIds.filter(item => item !== id);
    });
    this.invalidEventIdsOnLoad = [];
  }
}
