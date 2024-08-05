import { Component, ViewChild, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { ToteFreebet, IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { UserService } from '@core/services/user/user.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'tote-free-bet-select-dialog',
  templateUrl: 'tote-free-bet-select-dialog.component.html',
  styleUrls: ['tote-free-bet-select-dialog.component.scss']
})
export class ToteFreeBetSelectDialogComponent extends AbstractDialogComponent {
  @ViewChild('totefreebetsselect', { static: true }) dialog: any;
  
  tab  :string;
  readonly btTab = 'betToken';
  readonly fbTab = 'freeBet';
  readonly both = 'both';
  freeBets: ToteFreebet[];
  selected: ToteFreebet;
  freebetsConfig: IFreebetsPopupDetails;
  freebetsGroup = [];
  betPackList : IFreeBet[];
  activeTab : string = this.btTab;
  categoryName: string;
  eventName: string;
  isStreamAndBet = false;
  isBetToken: boolean;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    public userService: UserService,
    private changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,  
  ) {
    super(device, windowRef);
  }

  open(): void {
    this.isStreamAndBet = this.eventVideoStreamProviderService.isStreamAndBet;
    super.open();
    this.selected = null;
    this.betPackList = this.sortByExpiryDate(this.params.betPackList);
    this.freeBets = this.sortByExpiryDate(this.params.freeBets);
    this.freebetsConfig = this.params.freebetsConfig;
    const freeBetLength = this.freeBets?.length;
    const betPackLength = this.betPackList?.length;
    this.tab = (freeBetLength && betPackLength) ? this.both :(!freeBetLength && betPackLength) ? this.btTab : this.fbTab;
    this.categoryName = this.params.categoryName;
    this.eventName = this.params.eventName;
    this.changeDetectorRef.detectChanges();
  }

  sortByExpiryDate(data){
    return data?.sort((a: IFreeBet, b: IFreeBet) => {
      return Date.parse(a.freebetTokenExpiryDate) - Date.parse(b.freebetTokenExpiryDate);
    });
  }

  freeBetClick(freeBet: ToteFreebet, betType: string): void {
    this.isBetToken = betType === 'betPack';
    this.selected = freeBet;
  }

  addFreeBet(): void {
    if (this.selected) {
      this.params.onSelect(this.selected);
      if(this.isStreamAndBet) {
        this.trackGADetails(this.isBetToken ? 'bet token - apply' : 'free bet - apply');
      }
     }
  }

  removeFreeBet(): void {
    this.closeDialog(this.isStreamAndBet);
  }

  closeDialog(isClosed:boolean = false) {
    if(this.isStreamAndBet && isClosed) {
      const freebetStatus = this.tab === this.both ? 'bet token and free bet - close' : this.tab === this.btTab ? 'bet token - close' : 'free bet - close'
      this.trackGADetails(freebetStatus,true);
    }
    super.closeDialog();
  }

  trackGADetails(freebetStatus: string,isClosed: boolean = false): void {
    this.gtmService.push('Event.Tracking', {
      'event': 'Event.Tracking',
      'component.CategoryEvent': 'video streaming',
      'component.LabelEvent': 'stream and bet',
      'component.ActionEvent': isClosed ? 'close' : 'click',
      'component.PositionEvent': this.categoryName,
      'component.LocationEvent': this.eventName,
      'component.EventDetails': freebetStatus,
      'component.URLClicked': 'not applicable' ,
      'component.ContentPosition':'not applicable'
    });
  }

  trackByIndex(index: number): number {
    return index;
  }

  /**
   *
   * @param activeTab {string}
   */
  tabid(activeTab: string): void {
    this.activeTab = activeTab;
    this.changeDetectorRef.detectChanges();
  }
  
}
