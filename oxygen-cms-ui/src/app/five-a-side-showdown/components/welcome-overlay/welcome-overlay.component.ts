import { Component, OnInit, ViewChild } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IWelcomeOverlay } from '@app/five-a-side-showdown/models/welcome-overlay';
import { lobby_overlay, welcome_overlay, WELCOME_OVERLAY_DEFAULT_VALUS, live_leader_board } from '@app/five-a-side-showdown/constants/welcome-overlay.constants';

@Component({
  selector: 'app-welcome-overlay',
  templateUrl: './welcome-overlay.component.html',
  styleUrls: ['./welcome-overlay.component.scss']
})
export class WelcomeOverlayComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  welcomeOverlay: IWelcomeOverlay;
  readonly WELCOME_OVERLAY: {[key: string]: string} = welcome_overlay;
  readonly LOBBY_OVERLAY: { [key: string]: string } = lobby_overlay;
  readonly LIVE_LEADER_BOARD: { [key: string]: string } = live_leader_board;

  constructor(private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.loadInitialData();
    this.welcomeOverlay = WELCOME_OVERLAY_DEFAULT_VALUS;
  }

  /**
   * To Verify welcome overlay
   * @param {IWelcomeOverlay} termsConditions
   * @returns {boolean}
   */
  verifywelcomeOverlay(termsConditions: IWelcomeOverlay): boolean {
    return !!termsConditions;
  }

  /**
   * To Handle actions
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        break;
    }
  }

  /**
   * To Load initial data
   */
  private loadInitialData(): void {
    this.apiService.welcomeOverlayService()
     .getDetailsByBrand()
     .subscribe((data: {body: IWelcomeOverlay}) => {
        this.welcomeOverlay = data.body;
        this.actionButtons.extendCollection(this.welcomeOverlay);
      }, error => {
        if (error.status === 404) {
          this.welcomeOverlay = this.getDefaultValues();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  /**
   * To assign default values
   * @returns {IWelcomeOverlay}
   */
  private getDefaultValues(): IWelcomeOverlay {
    const popup = {...WELCOME_OVERLAY_DEFAULT_VALUS};
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
   * To handle save and edit scenarios
   */
  private save(): void {
    if (this.welcomeOverlay.createdAt) {
      this.sendRequest('updateWelcomeOverlay');
    } else {
      this.sendRequest('saveWelcomeOverlay');
    }
  }

  /**
   * To revert changes
   */
  private revert(): void {
    this.loadInitialData();
  }

  /**
   * To save and edit
   * @param {string} requestType
   */
  private sendRequest(requestType: string): void {
    this.apiService.welcomeOverlayService()[requestType](this.welcomeOverlay)
      .map((response) => response.body)
      .subscribe((data: IWelcomeOverlay) => {
        this.welcomeOverlay = data;
        this.actionButtons.extendCollection(this.welcomeOverlay);
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

}
