import { Injectable } from "@angular/core";

import { CmsService } from '@core/services/cms/cms.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';
import { VanillaApiService } from '@frontend/vanilla/core';

import { FanzoneDetails, IEmailOptin } from "@app/core/services/fanzone/models/fanzone.model";
import { fanzone, FANZONE_CATEGORY_ID, userData, fanzoneEmailKey, UNSUBSCRIBE_CUSTOM_TEAM_ID } from "@app/fanzone/constants/fanzoneconstants";
import {  forkJoin, map, Observable, Subject } from "rxjs";
import environment from '@environment/oxygenEnvConfig';
import { FanzoneStorageService } from "@app/core/services/fanzone/fanzone-storage.service";
import { FZ_GET_MAPPER } from "@app/lazy-modules/fanzone/fanzone.constant";

@Injectable({ providedIn: 'root' })
export class FanzoneHelperService {
  selectedFanzone: FanzoneDetails;
  ctrlName = 'fanzoneCms';
  isEnableFanzone: boolean = false;
  fanzoneTeamUpdate: Subject<FanzoneDetails> = new Subject();
  selectedFanzoneUpdate: Subject<FanzoneDetails> = new Subject();
  fzDataAvailable: boolean = false;
  fanzoneTeams: FanzoneDetails[] = [];
  appBuildVersion: string = '';

  constructor(
    protected user: UserService,
    protected vanillaApiService: VanillaApiService,
    protected pubsub: PubSubService,
    protected cmsService: CmsService,
    protected storageService: StorageService,
    protected fanzoneStorageService: FanzoneStorageService
  ) {
    if (environment.brand === 'ladbrokes') {
      this.fanzoneConfigEnabled();
      this.pubsub.subscribe(this.ctrlName, [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.RELOAD_COMPONENTS], () => {
          this.user.status && this.isEnableFanzone && this.getInitFanzoneData();
          this.user.username && this.getEmailOptinData();
      });
      this.pubsub.subscribe(this.ctrlName, [this.pubsub.API.SESSION_LOGOUT], () => {
        this.storageService.remove(fanzoneEmailKey);
      });
      this.getFzInitialDataFirstTimeUser();
    }
  }

  /**
   * Method to get fz data if user logged in for first time
   * @returns - void
   */
   getFzInitialDataFirstTimeUser(): void {
    if (this.storageService.get(userData) && this.storageService.get(userData).firstLogin && this.isEnableFanzone) {
      this.getInitFanzoneData();
    }
  }

  /**
    * to get user selected fanzone data and publish it if user is logged in and fanzone is enabled
    * @return {void} 
    */
  PublishFanzoneData(): void {
      this.fanzoneConfigEnabled();
        if (this.isEnableFanzone  && !!this.user.username) {
          const fanzoneTeam = this.fanzoneStorageService.get(fanzone);
          fanzoneTeam && fanzoneTeam.teamId && this.getFanzoneTeam(fanzoneTeam);
        }
  }

  /**
   * Method to check if fanzone configuration is enabled or not
   * @returns void
   */
  fanzoneConfigEnabled(): void {
    forkJoin({ menuItems: this.cmsService.getMenuItems(), sysConfig: this.cmsService.getSystemConfig() }).subscribe((data) => {
      const fzMenuIndex = data.menuItems.findIndex(menu => menu.categoryId === FANZONE_CATEGORY_ID);
      this.isEnableFanzone = fzMenuIndex !== -1 && (!data.menuItems[fzMenuIndex].disabled || (data.menuItems[fzMenuIndex].disabled && data.menuItems[fzMenuIndex].fzDisabled));
    });
  }

  /**
   * Method to check if remind me later has been selected in before session
   * @param fzStorage - user selected team
   * @returns boolean - true/false
   */
  relegatedTeamRemindMeLater(fzStorage): boolean {
    return fzStorage && fzStorage.hasOwnProperty('isFanzoneTeamRelegated') && fzStorage.hasOwnProperty('showRelegatedPopupOn');
  }

  /**
   * Method to get fanzone email on subscription
   */
  getEmailOptinData(): void {
    this.getEmailOptin().subscribe((response: IEmailOptin) => {
      this.fanzoneStorageService.set(fanzoneEmailKey, {...FZ_GET_MAPPER, ...response});
    }, (error) => {
      if (error.errorCode === "1") {
        this.fanzoneStorageService.set(fanzoneEmailKey, {...FZ_GET_MAPPER, ...{}});
      }
    });
  }

  /**
   * Method to get get fanzone email subscription info from platform
   * @returns - email optin subscription data
   */
  getEmailOptin(): Observable<IEmailOptin> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get('perferencecenter/emailOptin', '', APIOPTIONS);
  }

  /**
   * Method to check if user has subscribed to a relegated team
   * @returns - Observable<boolean>
   */
  checkIfTeamIsRelegated(teamData?): Observable<boolean> {
    const fanzoneData = teamData && Object.keys(teamData).length ? teamData : this.fanzoneStorageService.get(fanzone);
    return this.cmsService.getFanzone().pipe(map((allTeamsData: FanzoneDetails[]) => {
      if (fanzoneData && fanzoneData.teamId && !this.isCustomTeam(fanzoneData.teamId) && allTeamsData && !(allTeamsData.some((team) => team.teamId === fanzoneData.teamId || team.teamId === fanzoneData.TEAM_ID))) {
        return true;
      }
      return false;
    }));
  }

  /**
   * to fetch fanzone api data ,return user selected filtered fanzone
   * @param {fanzoneTeam: string}
   * @return {Observable} 
   */
  getFanzoneTeam(fanzoneTeam): void {
    this.cmsService.getFanzone().subscribe((teamData) => {
      this.fanzoneTeams = teamData;
      this.checkIfTeamIsRelegated().subscribe((isTeamRelegated) => {
        if (!isTeamRelegated) {
            [this.selectedFanzone] = teamData.filter(selectedFanzone => selectedFanzone.teamId === fanzoneTeam.teamId);
          this.emitSelectedFzUpdate(this.selectedFanzone);
          this.selectedFanzone && this.selectedFanzone.active && this.pubsub.publish(this.pubsub.API.FANZONE_DATA, this.selectedFanzone);
        }
      });
    });
  }

  /**
   * Method to check if team selected is custom team
   * @param teamId - team id
   * @returns - boolean true/false
   */
  isCustomTeam(teamId): boolean {
    return teamId === 'FZ001';
  }

  getInitFanzoneData(): void {
    this.getUserFanzoneTeam().subscribe((response) => {
      if (Object.keys(response).length === 0 || response.errorCode === "NO_RECORD_FOUND") {
        const fzStorage = { isFanzoneExists: false, isResignedUser: false };
        this.isRemindLaterStorageExists(fzStorage, true);
        this.emitTeamUpdate({ isFanzoneExists: false } as any);
      }
      else if (response && response.hasOwnProperty('preferences') && response.preferences.length) {
        const preferenceMap =  response.preferences[0].preferenceMap;
        const preferences = preferenceMap.reduce((obj, { key, value }) => Object.assign(obj, { [key]: value }), {});
        this.fzDataAvailable = true;
        const preference = {
          teamId: preferences.TEAM_ID,
          teamName: preferences.TEAM_NAME
        }
        this.checkIfTeamIsRelegated(preference).subscribe((isRelegated) => {
          const fzStorage = this.fanzoneStorageService.get('fanzone');
          if (this.relegatedTeamRemindMeLater(fzStorage) && !isRelegated) {
            this.fanzoneStorageService.set('fanzone', {});
          } else if(this.relegatedTeamRemindMeLater(fzStorage) && isRelegated) {
            return;
          }
          if ((preference && preference.teamId === UNSUBSCRIBE_CUSTOM_TEAM_ID) || !Object.keys(preferences).length || !preferences.hasOwnProperty('TEAM_ID')) {
            const subscriptionDate = response.preferences[0].subscriptionDate;
            const resignedUser = { isResignedUser: true, subscriptionDate, isFanzoneExists: false };
            if (preference.teamId === UNSUBSCRIBE_CUSTOM_TEAM_ID) {
              resignedUser['isCustomResignedUser'] = true;
            }
            this.isRemindLaterStorageExists(resignedUser);
            this.emitTeamUpdate({ isFanzoneExists: false, isResignedUser: true } as any);
          }
          if (Object.keys(preferences).length && preferences.hasOwnProperty('TEAM_ID') && preferences.TEAM_ID !== UNSUBSCRIBE_CUSTOM_TEAM_ID) {
            const storageData = {
              teamId: preferences.TEAM_ID,
              teamName: preferences.TEAM_NAME,
              communication: preferences.COMM_PREFERENCES,
              subscriptionDate: response.preferences[0].subscriptionDate,
              isFanzoneExists: !this.isCustomTeam(preferences.TEAM_ID),
              isResignedUser: false,
            };
            this.fanzoneStorageService.set('fanzone', storageData);
            this.PublishFanzoneData();
          }
        }, err => {
          console.error(err);
        });
      }
    }, err => {
        console.error(err);
    });
  }

  isRemindLaterStorageExists(fzStorage, tempTeam?: boolean) {
    const team = this.fanzoneStorageService.get('fanzone');
    if(team && team.showSYCPopupOn) {
      fzStorage['showSYCPopupOn'] = team.showSYCPopupOn;
    }
    if(tempTeam && team && team.tempTeam) {
      fzStorage['tempTeam'] = team.tempTeam;
    }
    if(team && team.isCustomResignedUser) {
      fzStorage['isCustomResignedUser'] = team.isCustomResignedUser;
    }
    this.fanzoneStorageService.set('fanzone', fzStorage);
  }

  /**
   * Method to get fanzone user team details
   * @returns Observable
   */
  getUserFanzoneTeam() {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get('perferencecenter/football', '', APIOPTIONS);
  }

  /**
   * Method to add info fanzone info to storage
   * @param object - value to be appended to fanzone storage
   */
  appendToStorage(object) {
    const fanzoneData = this.fanzoneStorageService.get(fanzone)
    const fanzoneInfoData = { ...fanzoneData, ...object };
    this.fanzoneStorageService.set(fanzone, fanzoneInfoData);
    this.emitTeamUpdate(fanzoneInfoData);
  }

  /**
   * returns selected fanzone update subject
   */
  getFanzoneTeamUpdate(): Subject<FanzoneDetails> {
    return this.fanzoneTeamUpdate;
  }

  /**
   * emits value with update if there are some observers
   * @param update
   */
  private emitTeamUpdate(update: FanzoneDetails): void {
    if (this.fanzoneTeamUpdate.observers.length) {
      this.fanzoneTeamUpdate.next(update);
    }
  }

  /**
   * returns selected fanzone update subject
   */
   getSelectedFzUpdate(): Subject<FanzoneDetails> {
    return this.selectedFanzoneUpdate;
  }

  /**
   * emits value with update if there are some observers
   * @param update
   */
   private emitSelectedFzUpdate(update: FanzoneDetails): void {
    if (this.selectedFanzoneUpdate.observers.length) {
      this.selectedFanzoneUpdate.next(update);
    }
  }
}