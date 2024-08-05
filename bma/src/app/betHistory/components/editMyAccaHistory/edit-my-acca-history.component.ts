import { Component, Input, OnInit, ComponentFactoryResolver } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';
import { TimeService } from '@core/services/time/time.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { DeviceService } from '@core/services/device/device.service';
import { IBetHistoryBet, IPageBets } from '../../models/bet-history.model';
import { ICashOutData } from '../../models/cashout-section.model';
import { RegularBet } from '../../betModels/regularBet/regular-bet.class';

import { EditMyAccaHistoryDialogComponent } from '../editMyAccaHistoryDialog/edit-my-acca-history-dialog.component';

@Component({
  selector: 'edit-my-acca-history',
  templateUrl: './edit-my-acca-history.component.html',
  styleUrls: ['./edit-my-acca-history.component.scss']
})
export class EditMyAccaHistoryComponent implements OnInit {
  @Input() bet: { location: string, eventSource: IBetHistoryBet };

  drawerStyles = {
    height: '504px'
  };

  loading: boolean;

  showDrawer: boolean;
  drawerHeader: string;

  bets: ICashOutData[];

  dialog: EditMyAccaHistoryDialogComponent;

  constructor(
    private betHistoryMainService: BetHistoryMainService,
    private cashOutSectionService: CashoutSectionService,
    private timeService: TimeService,
    private localeService: LocaleService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private deviceService: DeviceService
  ) {}

  ngOnInit(): void {
    this.drawerHeader = this.localeService.getString('ema.history.accaHistory');
  }

  onShowHistory(): void {
    if (this.deviceService.isMobile) {
      this.showDrawer = true;
    } else {
      this.showDialog();
    }
  }

  onDrawerShown(): void {
    this.loadHistory();
  }

  showDialog(): void {
    this.loadHistory();

    this.dialogService.openDialog(
      DialogService.API.emaHistoryDialog,
      this.componentFactoryResolver.resolveComponentFactory(EditMyAccaHistoryDialogComponent),
      true, {
        open: (dialog: EditMyAccaHistoryDialogComponent) => {
          dialog.loading = this.loading;
          dialog.bets = this.bets;
          this.dialog = dialog;
        }
      }
    );
  }

  private loadHistory(): void {
    if (this.bets) {
      return;
    }

    this.loading = true;

    this.betHistoryMainService.getHistoryByBetGroupId(this.bet.eventSource.betGroupId).subscribe((res: IPageBets) => {
      const betsMap = this.cashOutSectionService.createDataForRegularBets(res.bets.slice(1));
      const bets: ICashOutData[] = [];

      _.each(betsMap, (bet: RegularBet) => {
        const cashoutUsed = _.isEmpty(bet.winnings) ? '0' : bet.winnings[0].value;
        bet.accaHistory = {
          isOriginal: bet.betGroupOrder === '0',
          isBoosted: !!_.findWhere(bet.betTermsChange, { reasonCode: 'ODDS_BOOST' }),
          partialCashoutHistory: !!_.findWhere(bet.betTermsChange, { reasonCode: 'PARTIAL_CASHOUT' }),
          time: this.timeService.formatByPattern(this.timeService.getLocalDateFromString(bet.date), 'MM/dd/yyyy HH:mm'),
          cashoutUsed,
          cashoutUsedMsg: this.localeService.getString('ema.cashoutHistory.cashoutUsed', [bet.currencySymbol, cashoutUsed])
        };
        bets.push({ eventSource: bet, location: '' });
      });

      if (bets.length === 1) {
        bets[0].eventSource.accaHistory.isExpanded = true;
      }

      this.bets = _.sortBy(bets, (bet: ICashOutData) => +(bet.eventSource as RegularBet).betGroupOrder);
      this.loading = false;

      if (this.dialog) {
        this.dialog.bets = bets;
        this.dialog.loading = false;
      }
    });
  }
}
