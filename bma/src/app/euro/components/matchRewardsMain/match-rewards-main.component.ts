import { Component, OnInit, OnDestroy, ComponentFactoryResolver } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IMatchDayRewardsResponse, IHowItWorks } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { HOW_IT_WORKS, EURO_MESSAGES } from '@app/euro/constants/euro-constants';
import { EuroService } from '@app/euro/services/euro.service';
import { UserService } from '@app/core/services/user/user.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { EuroDialogComponent } from '@app/euro/components/euroDialog/euro-dialog.component';
import { EuroCongratsDialogComponent } from '@app/euro/components/euroCongratsDialog/euro-congrats-dialog.component';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { IEuroMessages } from '@app/euro/models/euro.model';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'match-rewards-main',
  templateUrl: './match-rewards-main.component.html',
  styleUrls: ['./match-rewards-main.component.scss']
})
export class MatchRewardsMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  public euroRespData: IMatchDayRewardsResponse;
  public statusrenderIndex: number;
  public currentBadge: number;
  public totalNoOfBadges: number;
  public freeBetDay: boolean;
  public errorMessage: string;
  public readonly EURO_MESSAGES: IEuroMessages = EURO_MESSAGES;
  private readonly HOW_IT_WORKS_TITLE: string = HOW_IT_WORKS;

  constructor(
    public userService: UserService,
    public pubSubService: PubSubService,
    public deviceService: DeviceService,
    public euroService: EuroService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService
  ) {
    super();
  }

  ngOnInit(): void {
    this.showSpinner();
    this.sessionStatusChange();
    this.pubSubService.subscribe(
      this.HOW_IT_WORKS_TITLE,
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN],
      () => {
        this.showSpinner();
        if (this.userService.bppToken) {
          this.sessionStatusChange();
        }
      });
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe(this.HOW_IT_WORKS_TITLE);
  }

  get dialogComponent() {
    return EuroDialogComponent;
  }

  get congratsDialogComponent() {
    return EuroCongratsDialogComponent;
  }

  /**
   * call to fetch the api data
   * @returns {void}
   */
  public euroResponse(): void {
    this.euroService.getMatchRewardsBadges(this.userService.status).subscribe((euroResponse: IMatchDayRewardsResponse) => {
      this.euroRespData = euroResponse;
      this.euroRespData.currentBadgeLocation = this.euroRespData.placedBetToday ? (this.euroRespData.currentBadgeLocation - 1) :
        this.euroRespData.currentBadgeLocation;
      this.euroApiDataResponse(this.euroRespData);
      this.hideSpinner();
    }, (err: HttpErrorResponse) => {
      this.errorMessage = err?.error?.proxyError?.code === 1500 ? EURO_MESSAGES.ERROR_USER_MESSAGE : EURO_MESSAGES.ERROR_MESSAGE;
      this.showError();
    });
  }

  /**
   * to process euroResponse and call other methods
   * @param {IMatchDayRewardsResponse} euroResponse
   * @returns {void}
   */
  public euroApiDataResponse(euroResponse: IMatchDayRewardsResponse): void {
    if (!euroResponse) {
      return;
    }
    if (euroResponse.currentBadgeLocation !== undefined && euroResponse.freeBetPositionSequence.length) {
      this.totalNoOfBadges = euroResponse.freeBetPositionSequence[euroResponse.freeBetPositionSequence.length - 1];
      this.statusRender(euroResponse.currentBadgeLocation);
      this.currentBadge = euroResponse.currentBadgeLocation;
    }
  }

  /**
   * to calculate the postion of status box
   * @param currentBadge {number}
   * @returns {void}
   */
  public statusRender(currentBadge: number): void {
    const dynamicPosition = this.deviceService.isMobile ?
      EURO_MESSAGES.MOBILE_BADGES_EACH_ROW : EURO_MESSAGES.DESKTOP_BADGES_EACH_ROW;
    let rowCalculator = 1;
    if (currentBadge) {
      rowCalculator = (Math.floor((currentBadge - 1) / dynamicPosition)) + 1;
    }
    this.statusrenderIndex = (dynamicPosition * rowCalculator - 1);
    if (this.totalNoOfBadges <= this.statusrenderIndex) {
      this.statusrenderIndex = this.totalNoOfBadges - 1;
    }
  }

  /**
   * handled logic for howitworks dialog box
   * @returns {void}
   */
  public openPopUp(): void {
    this.euroService.getHowItWorksData().subscribe((howItWorksResponse: IHowItWorks) => {
      this.populateHowItWorks(howItWorksResponse.howItWorks);
    }, () => {
      this.populateHowItWorks(EURO_MESSAGES.ERROR_HOWITWORKS);
    });
  }

  /**
   * handled logic for populating howitworks dialog box
   * @param {howItWorks} string
   * @returns {void}
   */
  populateHowItWorks(howItWorks: string): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.howItWorksDialog, componentFactory, true, {
      dialogClass: EURO_MESSAGES.HOW_IT_WORKS_DIALOG,
      data: {
        howItWorks: howItWorks,
        howItWorksLink: this.euroRespData?.fullTermsURI || '',
      }
    });
  }

  /**
   * Output emits when Freebet is availed
   * @returns {void}
   */
  public showConfetti($event): void {
    this.freeBetDay = true;
    setTimeout(() => { this.freeBetDay = false; }, 2500);
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.congratsDialogComponent);
    this.dialogService.openDialog(DialogService.API.euroCongratsDialog, componentFactory, true, {
      data: {
        freeBetModel: true,
        freeTokenMessage: $event,
      }
    });
  }

  private sessionStatusChange(): void {
    this.euroResponse();
  }
}
