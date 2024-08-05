import { ChangeDetectionStrategy, ChangeDetectorRef, Component, EventEmitter, OnInit, Output } from "@angular/core";
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";
import { SessionStorageService } from "@app/core/services/storage/session-storage.service";
import { IFirstBetDetails } from "@app/lazy-modules/onBoardingTutorial/firstBetPlacement/model/first-bet-placement.model";
import { FirstBetGAService } from "../../services/first-bet-ga.service";
import { UserService } from "@app/core/services/user/user.service";
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from "@app/core/services/windowRef/window-ref.service";
import { SafeResourceUrl } from "@angular/platform-browser";
import { DeviceService } from '@app/core/services/device/device.service';
import { CmsService } from '@core/services/cms/cms.service';
import { map } from "rxjs";
import { HttpResponse } from "@angular/common/http";

@Component({
    selector: 'first-bet-entry-point',
    templateUrl: 'first-bet-entry-point.component.html',
    styleUrls: ['./first-bet-entry-point.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})

export class FirstBetEntryPointComponent implements OnInit {
    firstBetPlacementDetails: IFirstBetDetails;
    isCloseTutorial: boolean = false;
    isFirstBetAvailable: boolean = true;
    iconUrl: SafeResourceUrl | any;
    CMS_ENDPOINT: string;

    @Output() readonly entryClose: EventEmitter<boolean> = new EventEmitter<boolean>();

    private readonly firstBetTitle: string = 'firstBetPlacement';

    constructor(
        private pubSubService: PubSubService,
        private sessionStorageService: SessionStorageService,
        private firstBetGAService: FirstBetGAService,
        private device: DeviceService,
        protected user: UserService,
        protected cdr: ChangeDetectorRef,
        protected cmsService: CmsService,
        public windowRefService: WindowRefService,
    ) {}

    ngOnInit(): void {
        this.CMS_ENDPOINT = environment.CMS_ENDPOINT.split('/api')[0];
        this.isFirstBetAvailable = !this.sessionStorageService.get('firstBetTutorialAvailable');
        this.pubSubService.subscribe('show-tutorial', this.pubSubService.API.FIRST_BET, () => {
            this.isFirstBetAvailable = false;
            this.cdr.detectChanges();
        });
        if (this.device.requestPlatform === 'mobile') {
            this.getFirstBetDetails();
        
            this.pubSubService.subscribe(this.firstBetTitle,[
            this.pubSubService.API.SESSION_LOGOUT,
            this.pubSubService.API.SUCCESSFUL_LOGIN
            ], () => {
            this.getFirstBetDetails();
            if(!this.user.status) {
                this.isFirstBetAvailable = false;
                this.sessionStorageService.remove('firstBetTutorialAvailable');
                this.sessionStorageService.remove('firstBetPlacementDetails');
                this.sessionStorageService.remove('initialTabLoaded');
            }
            });
        }
    }

    openUndo(): void {
        this.isCloseTutorial = true;
        this.windowRefService.document.getElementById("first-bet-id").classList.add('hover');
        this.firstBetGAService.setGtmData('Event.Tracking','close','not applicable','entry level');
    }

    closeUndo(): void {
        this.isCloseTutorial = false;
        this.windowRefService.document.getElementById("first-bet-id").classList.remove('hover');
        this.firstBetGAService.setGtmData('Event.Tracking','click','step 0',`${ this.firstBetPlacementDetails.button.leftButtonDesc } cta`);
    }

    dismiss(flag: boolean = false): void {
        this.isCloseTutorial = false;
        this.isFirstBetAvailable = false;
        this.sessionStorageService.remove('firstBetPlacementDetails');
        this.sessionStorageService.remove('firstBetTutorialAvailable');
        this.sessionStorageService.remove('initialTabLoaded');
        this.sessionStorageService.remove('betPlaced');
        this.sessionStorageService.set('firstBetTutorial', { user: this.user.username, firstBetAvailable: false });
        if (flag) {
          this.firstBetGAService.setGtmData('Event.Tracking','click','step 0',`${ this.firstBetPlacementDetails.button.rightButtonDesc } cta`);
        }
    }

    onStartTutorial(): void {
        this.isFirstBetAvailable = false;
        this.entryClose.emit(false);
        this.sessionStorageService.set('firstBetTutorialAvailable', true);
        this.sessionStorageService.set('firstBetTutorial', { user: this.user.username, firstBetAvailable: true });
        this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL, {step:'pickYourBet', tutorialEnabled: true});
        this.firstBetGAService.setGtmData('Event.Tracking','click','step 0',`${this.firstBetPlacementDetails.homePage.button} cta`);
    }

    private validateUserLastBet(): boolean {
      const validDate = new Date();
      validDate.setMonth(validDate.getMonth() - this.firstBetPlacementDetails.months);
      return (!this.user.lastBet || new Date(this.user.lastBet) < validDate) && 
      ( new Date(this.firstBetPlacementDetails.displayTo) > new Date() || this.firstBetPlacementDetails.expiryDateEnabled ) && 
      new Date() > new Date(this.firstBetPlacementDetails.displayFrom);
    }
  
    private validateUser(): boolean {
      return (this.sessionStorageService.get('firstBetTutorial') === null || this.sessionStorageService.get('firstBetTutorial').firstBetAvailable) || 
      (this.user.username !== this.sessionStorageService.get('firstBetTutorial').user);
    }
  
    private getFirstBetDetails(): void {
      if (this.user.status && +this.user.sportBalance > 0 && this.validateUser()) {
        this.cmsService.getFirstBetDetails().pipe(map((data: HttpResponse<IFirstBetDetails>) => data.body)).subscribe((data) => {
          this.firstBetPlacementDetails = data;
          if (this.validateUserLastBet() && this.firstBetPlacementDetails.isEnable) {
            this.isFirstBetAvailable = true;
            this.iconUrl = `${this.CMS_ENDPOINT}${this.firstBetPlacementDetails.imageUrl}`;
            this.sessionStorageService.set('firstBetPlacementDetails', this.firstBetPlacementDetails);
            this.firstBetGAService.setGtmData('contentView','load','step 0','welcome message');
          } else {
            this.dismiss();
          }
          this.cdr.detectChanges();
        });
      }
    }
}