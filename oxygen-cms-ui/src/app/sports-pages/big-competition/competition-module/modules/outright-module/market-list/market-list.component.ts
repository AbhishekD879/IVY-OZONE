import {Component, Input, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import * as _ from 'lodash';

import {DataTableColumn} from '../../../../../../client/private/models/dataTableColumn';
import {DialogService} from '../../../../../../shared/dialog/dialog.service';

import {CompetitionMarket, CompetitionModule} from '../../../../../../client/private/models';
import {MarketDialogComponent} from '../market-dialog/market-dialog.component';
import {BigCompetitionAPIService} from '../../../../service/big-competition.api.service';
import {AppConstants} from '../../../../../../app.constants';

@Component({
  templateUrl: './market-list.component.html'
})
export class OutrightModuleComponent implements OnInit {
  @Input() module: CompetitionModule;

  public competitionMarkets: CompetitionMarket[];

  public searchField: '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Active',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Collapsed',
      property: 'collapsed',
      type: 'boolean'
    },
    {
      name: 'OB Market ID',
      property: 'marketId'
    },
    {
      name: 'Default name',
      property: 'defaultName'
    },
    {
      name: 'Changed name',
      property: 'nameOverride'
    },
    {
      name: 'View Type',
      property: 'viewType',
    },
    {
      name: 'Max Display',
      property: 'maxDisplay'
    }
  ];

  filterProperties: string[] = [
    'nameOverride',
    'defaultName'
  ];

  constructor(private dialog: MatDialog,
              private dialogService: DialogService,
              public snackBar: MatSnackBar,
              private bigCompetitionApiService: BigCompetitionAPIService,
  ) {
  }

  ngOnInit(): void {
    this.competitionMarkets = this.module.markets;
  }

  /**
   * Add Open Bet Market to the markets list
   * @param market
   */
  public addOBMarketId(market: CompetitionMarket): void {
    const dialog = this.dialog.open(MarketDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        market,
        markets: this.competitionMarkets
      }
    });

    dialog.afterClosed()
      .subscribe((newMarket: CompetitionMarket) => {
        if (newMarket) {
          const markets  = _.cloneDeep(this.competitionMarkets);
          markets.push(newMarket);

          this.updateModuleList(this.module, markets, false)
            .subscribe(() => {
              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Market is Created and Stored'
              });
            });
        }
      });
  }

/**
 * Edit Open Bet Market from the markets list
 * @param market
 */
public editMarketId(market: CompetitionMarket) {
  const dialog = this.dialog.open(MarketDialogComponent, {
    width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
    data: {
      market: _.cloneDeep(market)
    }
  });

  dialog.afterClosed()
    .subscribe((newMarket: CompetitionMarket) => {
      if (newMarket) {
        const markets  = _.cloneDeep(this.competitionMarkets);
        _.extend(_.find(markets, m => m.marketId === market.marketId), newMarket);
        this.updateModuleList(this.module, markets, false)
          .subscribe(() => {
            this.dialogService.showNotificationDialog({
              title: 'Save Completed',
              message: 'Market is Saved'
            });
          });
      }
    });
}

  /**
   * Remove Open Bet market from the markets list
   * @param {Object} competitionMarket
   */
  public removeMarketId(competitionMarket: CompetitionMarket): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Market',
      message: `Are You Sure You Want to Remove Market "${competitionMarket.nameOverride}"?`,
      yesCallback: () => {
        const markets  = _.cloneDeep(this.competitionMarkets);
        markets.splice(this.competitionMarkets.indexOf(competitionMarket), 1);

        this.updateModuleList(this.module, markets, competitionMarket)
          .subscribe(() => {
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Market is Removed'
            });
          });
      }
    });
  }

  /**
   * Update module list on adding, editing and removing market
   * @param module
   * @param markets
   * @param removedItem
   * @returns {Observable}
   */
  private updateModuleList(module, markets, removedItem): Observable<void> {
    const updateData = {
      id: module.id,
      name: _.trim(module.name),
      enabled: module.enabled,
      type: module.type,
      markets: markets,
      typeId: module.typeId,
      viewType: undefined,
      maxDisplay: undefined
    };

    return this.bigCompetitionApiService
      .putModuleChanges(updateData)
      .map((response: HttpResponse<CompetitionModule>) => {
        return response.body;
      })

      /* tslint:disable */
      // Olena Haliuk
      .map((module: CompetitionModule) => {
        if (removedItem) {
          this.competitionMarkets.splice(this.competitionMarkets.indexOf(removedItem), 1);
        } else {
          _.extend(this.competitionMarkets, module.markets);
        }
      });
      /* tslint:enable */
  }

  public reorderHandler(): void {
    this.updateModuleList(this.module, this.competitionMarkets, false)
      .subscribe(() => {
        this.snackBar.open('Markets Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }
}
