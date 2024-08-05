import { Component, ViewChild, ChangeDetectionStrategy, ChangeDetectorRef, ElementRef } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'free-bet-select-dialog',
  templateUrl: 'free-bet-select-dialog.component.html',
  styleUrls: ['free-bet-select-dialog.component.scss']
})
export class FreeBetSelectDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;

  tab  :string;
  readonly btTab = 'betToken';
  readonly fbTab = 'freeBet';
  readonly both = 'both';
  activeTab : string = this.btTab;
  fanzoneList: IFreeBet[];
  freeBets: IFreeBet[];
  betPackList : IFreeBet[];
  selected: IFreeBet;
  freebetsConfig: IFreebetsPopupDetails;
  validOn: string = this.localeService.getString('bma.validOn');
  isBoostEnabled: boolean;
  isSelectionBoosted: boolean;
  canBoostSelection: boolean;
  isStreamAndBet = false;
  isBrandLadbrokes: boolean;
  categoryName: string;
  eventName: string;
  isBetToken: boolean;

  constructor(device: DeviceService,
    windowRef: WindowRefService,
    protected userService: UserService,
    private localeService: LocaleService,
    public elementRef: ElementRef<HTMLElement>,
    private changeDetectorRef: ChangeDetectorRef,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,
    private gtmService: GtmService,
    private freeBetsService: FreeBetsService) {
    super(device, windowRef);
    this.isBrandLadbrokes = environment.brand === this.localeService.getString(bma.brands.ladbrokes).toLowerCase();
  }

  open(): void {
    this.isStreamAndBet = this.eventVideoStreamProviderService.isStreamAndBet;
    super.open();
    this.selected = null;
    this.isBoostEnabled = this.params.isBoostEnabled;
    this.isSelectionBoosted = this.params.isSelectionBoosted;
    this.canBoostSelection = this.params.canBoostSelection;
    this.betPackList = this.sortByExpiryDate(this.params.betPackList);
    this.freeBets = this.sortByExpiryDate(this.params.freeBets);
    this.fanzoneList = this.sortByExpiryDate(this.params.fanzoneList);
    this.freebetsConfig = this.params.freebetsConfig;
    this.categoryName = this.params.categoryName;
    this.eventName = this.params.eventName;
    const freeBetLength=this.freeBets?.length;
    const fanzoneLength=this.fanzoneList?.length;
    const betPackLength= this.betPackList?.length;
    this.tab = ((freeBetLength || fanzoneLength) && betPackLength) ? this.both :((!freeBetLength && !fanzoneLength) && betPackLength) ? this.btTab : this.fbTab;
    this.changeDetectorRef.detectChanges();
    const isVideoPlayer = this.windowRef.document.querySelector('#rtmpe-hls');
    if(isVideoPlayer?.classList.contains('vjs-fullscreen') || isVideoPlayer?.classList.contains('vjs-fullscreen-control')){
      (isVideoPlayer).appendChild(this.windowRef.document.querySelector('.modals'));
      this.eventVideoStreamProviderService.snbVideoFullScreenExitSubj.subscribe(() => {
        this.closeDialog();
      });
    }
  }

  freeBetClick(freeBet: IFreeBet, betType: string): void {
    this.isBetToken = betType === 'betPack';
    this.selected = freeBet;
  }
  sortByExpiryDate(data){
    return data?.sort((a: IFreeBet, b: IFreeBet) => {
      return Date.parse(a.freebetTokenExpiryDate) - Date.parse(b.freebetTokenExpiryDate);
    });

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
