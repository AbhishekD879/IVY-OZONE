import {Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';

import {CompetitionMarket, CompetitionMarketValid} from '../../../../../../client/private/models';
import {ConfirmDialogComponent} from '../../../../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {BigCompetitionAPIService} from '../../../../service/big-competition.api.service';

@Component({
  templateUrl: './market-dialog.component.html',
  styleUrls: ['./market-dialog.component.scss']
})
export class MarketDialogComponent implements OnInit {
  public marketIsValid: boolean = false;
  public nameIsDisabled: boolean = true;
  public marketEdited: boolean = false;
  public marketExists: boolean = false;
  public action: string = '';
  public competitionMarket: CompetitionMarket;
  public markets;
  public newCompetitionMarket: CompetitionMarket = {
    marketId: '',
    defaultName: 'Default Name',
    nameOverride: '',
    enabled: false,
    viewType: '',
    collapsed: false,
    maxDisplay: 6
  };

  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>,
              private bigCompetitionApiService: BigCompetitionAPIService,
              @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    if (this.data.market) {
      this.competitionMarket = this.data.market;
      this.marketEdited = false;
      this.nameIsDisabled = false;
      this.action = 'Edit';
    } else {
      this.markets = this.data.markets;
      this.marketIsValid = false;
      this.nameIsDisabled = true;
      this.competitionMarket = this.newCompetitionMarket;
      this.action = 'Add';
    }
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public uploadMarketData(): void {
    this.marketExists = !!(_.find(this.markets, m => m.marketId === this.competitionMarket.marketId));
    if (this.marketExists) {
      this.nameIsDisabled = true;
      return;
    }
    this.bigCompetitionApiService.getSiteServeMarket(this.competitionMarket.marketId)
      .map((response: HttpResponse<CompetitionMarketValid>) => {
        return response.body;
      })
      .subscribe((data: CompetitionMarketValid) => {
        this.competitionMarket.nameOverride = this.competitionMarket.defaultName = data.name;
        this.nameIsDisabled = false;
        this.marketIsValid = false;
        this.marketEdited = false;
      }, () => {
        this.marketIsValid = true;
        this.nameIsDisabled = true;
      });
  }

  /**
   * Activate save if all fields in dialog pop-up are valid
   */
  public isValidForSave(): boolean {
    return !!(this.competitionMarket.marketId && this.competitionMarket.maxDisplay
    && this.competitionMarket.viewType && !this.nameIsDisabled && !this.marketEdited && (!this.marketIsValid || !this.marketExists));
  }
}
