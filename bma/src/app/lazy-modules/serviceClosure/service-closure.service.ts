import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { filter, map, mergeMap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { RtmsService, ClaimsService, EventsService } from '@frontend/vanilla/core';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { ApiVanillaService } from '@app/lazy-modules/serviceClosure/api-vanilla.service';
import { ICmsConfigMessages, ICmsSelfExclusionConfig, IEventDetails, IInitDataRespServiceClosure, IPortalWindowObj, IRtmsResponse } from '@app/lazy-modules/serviceClosure/service-closure.model';
import { cmsConfigMessagesDef, IMMEDIATE_BREAK_USER_ACCOUNT } from '@app/lazy-modules/serviceClosure/service-closure.constants';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { TimeService } from '@app/core/services/time/time.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class ServiceClosureService {
  userServiceClosureOrPlayBreakVal: boolean = false;
  userAccountInfo: string = '';
  cmsConfigMessages: ICmsConfigMessages = cmsConfigMessagesDef;
  isGetInitDataCalled = false;

  constructor(
    private userService: UserService,
    private cmsService: CmsService,
    private windowRefService: WindowRefService,
    private rtmsService: RtmsService,
    private claimsService: ClaimsService,
    private eventsService: EventsService,
    private apiVanillaService: ApiVanillaService,
    private pubsub: PubSubService,
    private fanzoneHelperService: FanzoneHelperService,
    private fanzoneStorageService: FanzoneStorageService,
    private timeService: TimeService,
    private router: Router) {
    this.userAccountMessageObs().subscribe((cmsConfigData: ICmsConfigMessages) => {
      this.populateCmsCOnfigs(cmsConfigData);
    });

    this.userServiceClosureOrPlayBreakVal = this.apiVanillaService.persistPlaybreakVal && this.cmsConfigMessages.playBreakEnable;
    this.eventsService.events.subscribe((eventDetails: IEventDetails) => {
      if (eventDetails && eventDetails.eventName === 'PLAY_BREAK' && eventDetails.data && eventDetails.data.playBreak) {
        this.userServiceClosureOrPlayBreakVal = this.cmsConfigMessages.playBreakEnable;
        this.apiVanillaService.persistPlaybreakVal = true;
      }
    });
    this.userService.status && this.pubsub.publish(this.pubsub.API.USER_CLOSURE_PLAY_BREAK, this.userServiceClosureOrPlayBreakVal);
  }

  /**
   * Gets user status and cms message that needs to be displayed
   * @returns {void}
   */
  checkUserServiceClosureStatus(): void {
    if (this.isGetInitDataCalled) {
      return;
    }

    this.rtmsService.messages.subscribe((rtmsWSResp: IRtmsResponse) => {
      this.enablePlaybreak(rtmsWSResp);
    });

    this.playBreakStatusOfUser();
    if (!this.userService.status) {
      return;
    }
    let serviceClosure: boolean;
    const closureDetails = this.getInitValues();
    closureDetails.pipe(
      mergeMap(userStatus => {
        const userClosureDetails = userStatus?.closureDetails?.closureDetails;
        if (userClosureDetails) {
          const userClosureDetailsArr = userClosureDetails.filter(sportsBookuserData => sportsBookuserData?.productId === 'SPORTSBOOK');
          if (userClosureDetailsArr.length) {
            serviceClosure = userClosureDetailsArr[0].isBlocked;
          }
        }
        return this.userAccountMessageObs();
      })
    ).subscribe((data: ICmsConfigMessages) => {
      this.populateCmsCOnfigs(data);
      if (serviceClosure && this.cmsConfigMessages.selfExclusionEnable) {
        this.userServiceClosureOrPlayBreakVal = serviceClosure;
        this.userAccountInfo = this.cmsConfigMessages.selfExclusion;
        this.userService.status && this.pubsub.publish(this.pubsub.API.USER_CLOSURE_PLAY_BREAK, this.userServiceClosureOrPlayBreakVal);
      }
    });
    this.isGetInitDataCalled = true;
  }

  /**
   * populate cms structure
   * @param {ICmsConfigMessages} cmsConfigData
   * @return {void}
   */
  populateCmsCOnfigs(cmsConfigData: ICmsConfigMessages): void {
    if (cmsConfigData) {
      this.cmsConfigMessages.selfExclusion = cmsConfigData.selfExclusion;
      this.cmsConfigMessages.selfExclusionEnable = cmsConfigData.selfExclusionEnable;
      this.cmsConfigMessages.playBreak = cmsConfigData.playBreak;
      this.cmsConfigMessages.playBreakEnable = cmsConfigData.playBreakEnable;
      this.cmsConfigMessages.immediateBreak = cmsConfigData.immediateBreak;
      this.cmsConfigMessages.immediateBreakEnable = cmsConfigData.immediateBreakEnable;
    }
  }

  /**
   * event emitted from vanilla after api call
   * @return {void}
   */
  playBreakStatusOfUser(): void {

    this.userAccountInfo = this.cmsConfigMessages.playBreak;
    this.eventsService.events.pipe(filter(playbreakStatus =>
      playbreakStatus.eventName == 'PLAY_BREAK' && playbreakStatus.data && playbreakStatus.data.playBreak
    )).subscribe((eventDetails: IEventDetails) => {
      this.userServiceClosureOrPlayBreakVal = this.cmsConfigMessages.playBreakEnable;
      this.userAccountInfo = this.cmsConfigMessages.playBreak;
      this.apiVanillaService.persistPlaybreakVal = true;
      this.apiVanillaService.playBreakSubject.next(true);
      this.userService.status && this.pubsub.publish(this.pubsub.API.USER_CLOSURE_PLAY_BREAK, this.userServiceClosureOrPlayBreakVal);
    });
  }

  /**
   * Gets cms configuration
   * @returns Observable<any>
   */
  userAccountMessageObs(): Observable<ICmsConfigMessages> {
    return this.cmsService.getSystemConfig().pipe(
      map((cmsConfigVal: ICmsSelfExclusionConfig) => {
        return cmsConfigVal.SelfExclusion;
      })
    );
  }

  /**
   *updates service fields after api calls
   * @returns void
   */
  updateClosureFlag(): void {
    if (this.windowRefService.nativeWindow.portal && this.windowRefService.nativeWindow.portal.excludedInSameSession && this.cmsConfigMessages && this.cmsConfigMessages.selfExclusionEnable) {
      this.userServiceClosureOrPlayBreakVal = true;
      this.userAccountInfo = this.cmsConfigMessages.selfExclusion;
    }
    if (this.claimsService.get('accountcategoryId') === IMMEDIATE_BREAK_USER_ACCOUNT && this.cmsConfigMessages && this.cmsConfigMessages.immediateBreakEnable) {
      this.userServiceClosureOrPlayBreakVal = true;
      this.userAccountInfo = this.cmsConfigMessages.immediateBreak;
    }
    if (this.windowRefService.nativeWindow.portal && this.windowRefService.nativeWindow.portal.allProductsExcludedInSameSession &&
      this.isOneDayExclusion(this.windowRefService.nativeWindow.portal) && this.cmsConfigMessages.immediateBreakEnable) {
      this.userServiceClosureOrPlayBreakVal = true;
      this.userAccountInfo = this.cmsConfigMessages.immediateBreak;
    }
    this.userService.status && this.pubsub.publish(this.pubsub.API.USER_CLOSURE_PLAY_BREAK, this.userServiceClosureOrPlayBreakVal);
  }

  /**
   *gets window field after user opts for breaks
   * @returns void
   */
  isOneDayExclusion(portalWindowObj: IPortalWindowObj): boolean {
    if (portalWindowObj && portalWindowObj.endDate && portalWindowObj.startDate) {
      const endDate = +new Date(portalWindowObj.endDate);
      const startDate = +new Date(portalWindowObj.startDate);
      const diffTime = Math.abs(endDate - startDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays === 1 ? true : false;
    }
    return false;
  }

  /**
   * checks for rtms ws update
   * @param {IRtmsResponse} message
   * @return {void}
   */
  checkplayBreak(rtmsWSResp: IRtmsResponse): void {
    if (rtmsWSResp.type === 'PLAY_BREAK_START_EVENT') {
      this.userServiceClosureOrPlayBreakVal = this.cmsConfigMessages.playBreakEnable;
      this.userAccountInfo = this.cmsConfigMessages.playBreak;
      this.apiVanillaService.persistPlaybreakVal = true;
    } else if (rtmsWSResp.type === 'PLAY_BREAK_END_EVENT') {
      this.userServiceClosureOrPlayBreakVal = false;
      this.apiVanillaService.persistPlaybreakVal = false;
    }
    this.userService.status && this.pubsub.publish(this.pubsub.API.USER_CLOSURE_PLAY_BREAK, this.userServiceClosureOrPlayBreakVal);
  }

  /**
   * To Change the fanzone team as soon as changed in difference device
   * @param rtmsWSResp RTMS Event Response
   */

  changeFanzoneTeam(rtmsWSResp: IRtmsResponse): void {
    const userData = this.fanzoneStorageService.get('fanzone');
    if (Object.keys(rtmsWSResp.payload.PreferencesObject).length && rtmsWSResp.payload.PreferencesObject.hasOwnProperty('TEAM_ID')) {
      const storageData = {
        teamId: rtmsWSResp.payload.PreferencesObject.TEAM_ID,
        teamName: rtmsWSResp.payload.PreferencesObject.TEAM_NAME,
        subscriptionDate: this.timeService.getSuspendAtTime(),
        isFanzoneExists: rtmsWSResp.payload.PreferencesObject.TEAM_ID !== 'FZ001',
        isResignedUser: false,
      };
      if(userData.teamId !== rtmsWSResp.payload.PreferencesObject.TEAM_ID) {
        this.fanzoneStorageService.set('fanzone', storageData);
        this.fanzoneHelperService.PublishFanzoneData();
      }
    } else {
      if (userData) {
        userData.isResignedUser = true;
        userData.isFanzoneExists = false;
        delete userData.teamId;
        delete userData.teamName;
        delete userData.communication;
      }
      this.fanzoneStorageService.set('fanzone', userData);
      this.pubsub.publish(this.pubsub.API.FANZONE_DATA, {});
      this.router.navigate(['']);
    }
  }

  /**
   * checks for rtms ws update
   * @param {IRtmsResponse} message
   * @return {void}
   */
  enablePlaybreak(rtmsWSResp: IRtmsResponse): void {
    if (rtmsWSResp.type === 'FZ_PLAYER_PREFS') {
      this.changeFanzoneTeam(rtmsWSResp);
    } else if (!this.cmsConfigMessages.playBreak) {
      this.userAccountMessageObs().subscribe((cmsConfigData: ICmsConfigMessages) => {
        this.populateCmsCOnfigs(cmsConfigData);
        this.checkplayBreak(rtmsWSResp);
      });
    } else {
      this.checkplayBreak(rtmsWSResp);
    }
  }

  /**
   *getter to return current user status
   * @return Observable<IInitDataRespServiceClosure>
   */
  get userServiceClosureOrPlayBreak(): boolean {
    return this.userServiceClosureOrPlayBreakVal;
  }

  /**
   * Initial api value for selfexclusion user
   * @return Observable<IInitDataRespServiceClosure>
   */
  getInitValues(): Observable<IInitDataRespServiceClosure> {
    return this.apiVanillaService.get('serviceClosurev2/GetInitData');
  }

  /**
   * checks for playbreak
   * @return {boolean}
   */
  userServiceClosureOrPlayBreakCheck(): boolean {
    if (!this.userServiceClosureOrPlayBreakVal) {
      this.updateClosureFlag();
    }
    return this.userServiceClosureOrPlayBreakVal;
  }
}
