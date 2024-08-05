import { Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IDialogParams } from '@app/core/services/dialogService/dialog-params.model';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { FANZONE_GAMES } from '@lazy-modules/fanzone/fanzone.constant';
@Component({
  selector: 'fanzone-game-launch-dialog',
  templateUrl: './fanzone-game-launch-dialog.component.html',
  styleUrls: ['./fanzone-game-launch-dialog.component.scss']
})

export class FanzoneGameLaunchDialogComponent extends AbstractDialogComponent {
  @ViewChild('fanzoneGameLaunchDialog', { static: true }) dialog;
  @ViewChild('iframeGameLaunch', {static: false}) iframe: ElementRef;
  fanzoneGameLaunchData: IDialogParams;
  clearGameLaunchTimeout: number;
  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    private loc: PlatformLocation,
    protected fanzoneGamesService: FanzoneGamesService,
  ) {
    super(device, windowRef);
    loc.onPopState(() => super.closeDialog());
  }

  /**
   * opens Game launch in dialog box
   * @returns void
   */
  open(): void {
    this.fanzoneGameLaunchData = this.params;
    this.dialog.closeOnOutsideClick = false;
    if (this.fanzoneGamesService.isGameClosedForcibly) {
      this.windowRef.nativeWindow.clearTimeout(this.clearGameLaunchTimeout);
    } 
    super.open();
  }

   /**
    * closes the game launch dialog 
    * @returns void
    */
   close(): void {
    this.iframe.nativeElement.contentWindow.postMessage(FANZONE_GAMES.PREVIOUS_CASINO_GAME_CLOSED, '*');
    this.clearGameLaunchTimeout = this.windowRef.nativeWindow.setTimeout(() => {
      if (this.dialog.visible) {
        this.fanzoneGamesService.isGameClosedForcibly = true;
        super.closeDialog();
      }
    }, 2000);
  }

   /**
   * listener for post messages from casino games
   * @param event
   */
   @HostListener('window:message', ['$event'])
   onMessage(event: MessageEvent): void {
     if (event.data === FANZONE_GAMES.PREVIOUS_CASINO_GAME_CLOSED_ACK) {
      this.windowRef.nativeWindow.clearTimeout(this.clearGameLaunchTimeout);
      this.fanzoneGamesService.isGameClosedForcibly = false;
      super.closeDialog();
     }
     if (event.data === FANZONE_GAMES.CASINO_GAME_CLOSED) {
      super.closeDialog();
     }
   }
}
