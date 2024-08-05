import { Component, ViewChild, Input, HostListener, ElementRef } from '@angular/core';
import { Router } from '@angular/router';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { FanzoneSharedService } from '../../services/fanzone-shared.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';


@Component({
  selector: 'fanzone-notification',
  templateUrl: './fanzone-notification.component.html',
  styleUrls: ['./fanzone-notification.component.scss']
})

export class FanzoneNotificationComponent extends AbstractDialogComponent {
  @ViewChild('FanzoneNotification', { static: true }) dialog;
  @Input() initialState: boolean = true;
  public notificationData: IDialogParams;
  public popUp: boolean = true;

  constructor(device: DeviceService, 
    windowRef: WindowRefService, 
    private router: Router, 
    private pubsub: PubSubService,
    private fanzoneSharedService: FanzoneSharedService, 
    private fanzoneStorageService: FanzoneStorageService,
    private elementRef: ElementRef) {
    super(device, windowRef);
  }

  @HostListener('document:click', ['$event'])
  @HostListener('document:touchend', ['$event'])
  clickOutside(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.pubsub.publish(this.pubsub.API.FANZONE_TOGGLE_ON, true);
    }
  }

  /**
   * Method to subscribe/ unsubscribe fanzone
   * @param value - boolean for toggle on/off
   * returns {void}
   */
  onToggleChange(value: boolean): void {
    this.initialState = value;
  }

  /**
   * Method on open of notifications dialog
   * returns {void}
   */
  open(): void {
    this.popUp = true;
    this.initialState = true;
    this.notificationData = this.params;
    this.popUp = false; 
    if(this.notificationData.isPreferenceCentre) {
      this.popUp = this.notificationData.popUp;
      this.initialState = false;
    }
    super.open();
  }

  /**
   * Method on click of confirm user preference
   * returns {void}
   */
  confirm() {
    if (this.popUp === false || this.notificationData.isPreferenceCentre) {
      this.fanzoneSharedService.resignFanzone();
      super.closeDialog();
    }
  }

  /**
   * Method on click of exit notification dialog
   * returns {void}
   */
  close() {
    this.fanzoneSharedService.pushCachedEvents(this.notificationData.exitCTA);
    setTimeout(() => {
      this.popUp = true;
      this.initialState = true;
      this.pubsub.publish(this.pubsub.API.FANZONE_TOGGLE_ON, true);
      if(!this.notificationData.showToggle) {
        const fanzoneTeam = this.fanzoneStorageService.get('fanzone');
        this.router.navigate([`/fanzone/sport-football/${fanzoneTeam.teamName}/now-next`]);
      }
    }, 100);
    super.closeDialog();
  }

  /**
   * Method to return corresponding title and description based on teamId
   * returns {string}
   */
  getTitleAndDescription(type: string) {
    const popupDetails = {title:'', description:''};
    popupDetails.title = this.fanzoneSharedService.isSubscribedToCustomTeam() ? this.notificationData.genericTeamNotificationTitle : this.notificationData.notificationPopupTitle;
    popupDetails.description = this.fanzoneSharedService.isSubscribedToCustomTeam() ? this.notificationData.genericTeamNotificationDescription : this.notificationData.notificationDescriptionDesktop;
    return popupDetails[type];
  }
}