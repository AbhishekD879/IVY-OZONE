import { Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';

import * as fanzoneConst from '@lazy-modules/fanzone/fanzone.constant';

import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { fanzoneUserData } from '@lazy-modules/fanzone/models/fanzone-syc.model';
import { PlatformLocation } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'fanzone-games-dialog',
  templateUrl: './fanzone-games-dialog.component.html',
  styleUrls: ['./fanzone-games-dialog.component.scss']
})

export class FanzoneGamesDialogComponent extends AbstractDialogComponent {
  @ViewChild('fanzoneGamesDialog', { static: true }) dialog;
  fanzonePopupData: IDialogParams;
  fanzoneTeam: fanzoneUserData;
  gtmData = {
    event: fanzoneConst.GTM_DATA.TRACKEVENT,
    eventAction: fanzoneConst.GTM_DATA.EVENTACTION,
    eventCategory: fanzoneConst.GTM_DATA.EVENTCATEGORY,
    eventLabel: fanzoneConst.GTM_DATA.EVENTLABEL
  };

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    private fanzoneStorageService: FanzoneStorageService,
    private gtmService: GtmService,
    protected fanzoneGamesService: FanzoneGamesService,
    protected pubsub: PubSubService,
    private navigationService:NavigationService,
    private loc: PlatformLocation,
    private route: Router,
    private elementRef: ElementRef
  ) {
    super(device, windowRef);
    loc.onPopState(() => super.closeDialog());
  }

  
  @HostListener('document:click', ['$event'])
  @HostListener('document:touchend', ['$event'])
  clickOutside(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target as HTMLElement)) {
      event.stopPropagation();
      this.close();
    }
  }

  /**
   * open Games dialog box
   * @returns void
   */
  open(): void {
    this.fanzonePopupData = this.params;
    this.fanzoneTeam = this.fanzoneStorageService.get('fanzone');
    this.gtmService.push(this.gtmData.event, this.gtmData);
    if (this.route && this.route.url && this.route.url.indexOf(`${fanzoneConst.fanzonePath}`) !== -1) {
      this.fanzoneGamesService.setNewFanzoneGamesPopupSeen();
      super.open();
    }
    this.pubsub.subscribe('gamesPopupSubscription', this.pubsub.API.HIDE_FANZONE_GAMES_TAB, () => {
      super.closeDialog();
    });
  }

  
  /**
    * close the dialog and navigate to games tab
    * @returns void
    */
  play(): void {
    this.navigationService.openUrl(`/fanzone/sport-football/${this.fanzoneTeam.teamName}/games`, true);
    this.pubsub.publish(this.pubsub.API.FANZONE_SHOW_GAMES_TAB);
    this.close();
  }
  
  /**
    * close the dialog and update to storage
    * @returns void
    */
  close(): void {
    this.pubsub.publish(this.pubsub.API.FANZONE_SHOW_GAMES_TOOLTIP);
    super.closeDialog();
    this.pubsub.unsubscribe('gamesPopupSubscription');
  }
}
