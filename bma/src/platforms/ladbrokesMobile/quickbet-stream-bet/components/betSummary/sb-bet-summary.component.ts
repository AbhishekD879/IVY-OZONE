import {  Component,
          Input,
          Output,
          EventEmitter, } from '@angular/core';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { IFreebetGroup, IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { LadbrokesBetSummaryComponent } from '@ladbrokesMobile/quickbet/components/betSummary/bet-summary.component';

@Component({
  selector: 'sb-bet-summary',
  templateUrl: '../../../../../app/quickbet-stream-bet/components/betSummary/sb-bet-summary.component.html',
  styleUrls: ['../../../../../app/quickbet-stream-bet/components/betSummary/sb-bet-summary.component.scss']
})
export class SbBetSummaryComponent extends LadbrokesBetSummaryComponent {
  @Input() freebetsList: IFreebetToken[];
  @Input() freebetsGroup: IFreebetGroup;
  @Input() selectedFreeBet: IFreebetToken;
  @Input() freebetsConfig: IFreebetsPopupDetails;
  @Input() isBoostEnabled: boolean;
  @Input() isSelectionBoosted: boolean;
  @Input() canBoostSelection: boolean;
  @Input() showOnDigitKeyborad: boolean;
  @Input() digitKeyboard: boolean;
  @Input() betPackList: IFreebetToken[];
  @Input() betPackGroup: IFreebetGroup;
  @Input() isBetSummaryInReceipt?: boolean;
  @Input() categoryName: string;
  @Input() eventName: string;
  
  @Output() fbChange: EventEmitter<ILazyComponentOutput> = new EventEmitter();
  @Output() stakeClick: EventEmitter<boolean> = new EventEmitter();

  onFreebetChange(event: ILazyComponentOutput): void {
    if(event.output === 'selectedChange') {
      this.fbChange.emit(event);
    }
  }

  showFreeBet(){
    return (this.freebetsList && this.freebetsList.length > 0 || this.betPackList && this.betPackList.length > 0);
  }

  getStakeEntered(){
    return this.currencyPipe.transform(this.selection.stake, this.user.currencySymbol, 'code');
  }

  stakeElemClick(){
    this.stakeClick.emit(true);
  }
}
