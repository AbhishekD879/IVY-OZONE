import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { DialogService } from '@app/core/services/dialogService/dialog.service';

import { IFanzoneData, IFanzonePreferences } from '@app/fanzone/models/fanzone-preferences.model';
import { gtmTackingKeys } from '@app/fanzone/constants/fanzonePreferenceConstants';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneNotificationComponent } from '@app/lazy-modules/fanzone/components/fanzoneNotification/fanzone-notification.component';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-preference-centre',
  templateUrl: './fanzone-preference-centre.component.html',
  styleUrls: ['./fanzone-preference-centre.component.scss']
})
export class FanzonePreferenceCentreAppComponent implements OnInit, OnDestroy {

  preferences: IFanzonePreferences = <IFanzonePreferences>{};
  activatedPreferences: Array<string> = [];
  fanzoneSubscription: boolean = true;
  readonly fanzoneToggleOn: string = 'fanzoneToggleOn';
  readonly noThanks: string = 'noThanks';
  allPreferences: boolean = false;
  constructor(
    public nativeBridge: NativeBridgeService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected dialogService: DialogService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected router: Router,
    protected fanzoneStorageService: FanzoneStorageService,
    protected pubSubService: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected windowRef: WindowRefService,
    protected routingState: RoutingState
  ) { }

  ngOnInit() {
    this.getPreferences();
    this.switchToggleOn();
    this.pubSubService.subscribe(this.noThanks, this.pubSubService.API.FANZONE_NO_THANKS, (data) => {
      this.updatePrefWithSelectTeam();
    })
  }

  /**
   * Method to toggle switch on on exit from preferences dialog 
   * @returns - void
   */
  switchToggleOn(): void {
    this.pubSubService.subscribe(this.fanzoneToggleOn, this.pubSubService.API.FANZONE_TOGGLE_ON, (data) => {
      if (!this.windowRef.document.querySelectorAll('.modal-dialog').length) {
        this.fanzoneSubscription = data;
        this.changeDetectorRef.detectChanges();
      }
    })
  }

  /**
   * Method to get user fanzone preferences
   */
  getPreferences() {
    const route = this.routingState && this.routingState.getPreviousUrl();
    this.preferences = this.router.getCurrentNavigation().extras?.state?.data ?? {};
    if (!Object.keys(this.preferences).length) {
      this.fanzoneSharedService.getFanzonePreferences().subscribe((data: IFanzonePreferences[]) => {
        this.preferences = data[0];
        if (route.includes('now-next')) {
          this.preferences.showToggle = true;
        }
        this.updatePrefWithSelectTeam();
        this.changeDetectorRef.detectChanges();
      });
      this.changeDetectorRef.detectChanges();
    }
    if (Object.keys(this.preferences).length > 0) {
      this.updatePrefWithSelectTeam();
    }
  }

  private updatePrefWithSelectTeam(): void {
    this.fanzoneSubscription = Object.keys(this.fanzoneSharedService.getFanzoneInfo()).length ? true : false;
    const selectedTeam: Array<string> = (this.fanzoneSharedService.getFanzoneInfo()).communication;
    this.preferences.pcKeys.forEach((info) => {
      info.value = false;
      if (selectedTeam && selectedTeam.includes(info.key)) {
        this.activatedPreferences.push(info.key);
        info.value = true;
      }
    })
    this.changeDetectorRef.detectChanges();
    this.allPreferences = this.checkIfAllPreferencesSelected();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * method to check if all preferences are selected
   * @returns - boolean
   */
  checkIfAllPreferencesSelected() {
    return this.preferences.pcKeys.every(v => v.value === true) ? true : false;
  }

  /**
   * on toggle of different preferences
   * @param value - on / off
   * @param key - key of preferences
   */
  preferenceSwitch(event: boolean, key: string, preferenceName: string): void {
    if (this.windowRef.nativeWindow.NativeBridge.pushNotificationsEnabled) {
      const route = this.routingState && this.routingState.getPreviousUrl();
      this.fanzoneSharedService.pushCachedEvents(event ? gtmTackingKeys.toggleOn : gtmTackingKeys.toggleOff, preferenceName, route.includes('now-next') ? 'fanzone' : gtmTackingKeys.show_your_colors);
      this.preferences.pcKeys.forEach((data) => {
        if (data.key === key && event) {
          data.value = true;
          this.activatedPreferences.push(data.key);
        } else if (data.key === key && !event) {
          data.value = false;
          this.activatedPreferences = this.activatedPreferences.filter(e => { return e !== key });
        }
      });
      this.allPreferences = this.checkIfAllPreferencesSelected();
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Method to toggle all preferences on and off
   * @param value - toggle value - on/off
   */
  allPreferencesSwitch(value: boolean) {
    if (this.windowRef.nativeWindow.NativeBridge.pushNotificationsEnabled) {
      const route = this.routingState && this.routingState.getPreviousUrl();
      this.fanzoneSharedService.pushCachedEvents(value ? gtmTackingKeys.toggleOn : gtmTackingKeys.toggleOff, 'All', route.includes('now-next') ? 'fanzone' : gtmTackingKeys.show_your_colors);
      this.preferences.pcKeys.forEach((data) => {
        if (value) {
          this.allPreferences = true;
          data.value = true;
          this.activatedPreferences.push(data.key);
        } else {
          this.allPreferences = false;
          data.value = false;
          this.activatedPreferences = [];
        }
      });
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Method to submit user preferences
   */
  onSubmitPreference() {
    const route = this.routingState && this.routingState.getPreviousUrl();
    this.fanzoneSharedService.pushCachedEvents(gtmTackingKeys.submit, '', route.includes('now-next') ? 'fanzone' : gtmTackingKeys.show_your_colors);
    const fzTeam = this.fanzoneStorageService.get('fanzone');
    const fzPath = `/fanzone/sport-football/${fzTeam.teamName}/now-next`;
    this.fanzoneSharedService.saveTeamOnPlatformOne(<IFanzoneData>{}, this.activatedPreferences, fzPath);
  }

  /**
   * on fanzone unsubscription open dialog
   */
  unsubcribeFanzone() {
    this.fanzoneSubscription = !this.fanzoneSubscription;
    if (!this.fanzoneSubscription) {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(FanzoneNotificationComponent);
      this.dialogService.openDialog('NYT', componentFactory, true, { ...this.preferences, isPreferenceCentre: true });
    }
  }

  /**
   * Method to return corresponding title and description based on teamId
   * returns {string}
   */
  getTitleAndDescription(type: string) {
    const popupDetails = {title:'', description:''};
    popupDetails.title = this.fanzoneSharedService.isSubscribedToCustomTeam() ? this.preferences.genericTeamNotificationTitle : this.preferences.pushPreferenceCentreTitle;
    popupDetails.description = this.fanzoneSharedService.isSubscribedToCustomTeam() ? this.preferences.genericTeamNotificationDescription : this.preferences.pcDescription;
    return popupDetails[type];
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe(this.pubSubService.API.FANZONE_TOGGLE_ON);
  }
}
