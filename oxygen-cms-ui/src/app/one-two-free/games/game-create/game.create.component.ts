import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

import { Game } from '@app/client/private/models/game.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { SeasonsApiService } from '@app/one-two-free/service/seasons.api.service';

@Component({
  selector: 'game-create-dialog',
  templateUrl: './game.create.component.html',
  styleUrls: ['./game.create.component.scss'],
  providers: []
})

export class GameCreateComponent implements OnInit {
  getDataError: string;
  newGame: Game;
  selectedSeason: string;
  seasons = new Array();
  isSeasonSel = false;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private seasonsApiService: SeasonsApiService
  ) { }

  isValidModel() {
    return this.newGame.title.length > 0 && this.isSeasonSel;
  }

  closeDialog() {
    this.dialogRef.close();
  }
  handleVisibilityDateUpdate(data: DateRange): void {
    this.newGame.displayFrom = new Date(data.startDate).toISOString();
    this.newGame.displayTo = new Date(data.endDate).toISOString();
  }

  ngOnInit() {
    this.newGame = {
      status: '',
      displayFrom: '',
      displayTo: '',
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      sortOrder: 0,
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',
      highlighted: false,
      events: [],
      prizes: [],
      title: '',
      enabled: false,
      seasonId: null
    };

    this.loadSeasons();
  }


  /**
   * Method to fetch ALL Seasons for seaosn linking
   * @Param : null
   * @return: list of active and future seasons
  */
  loadSeasons() {
    this.seasonsApiService.getAllSeasons().subscribe(data => {
      this.seasons = data.body.filter(season => {
        return !((new Date(season.displayTo).getTime() < new Date().getTime()))
      })
      this.seasons.push({ id: '', seasonName: 'No PL Teams' });
    });
  }

  /**
   * Action on selecting season
   * 
   * @param value
   * @return void 
   *  Assign selected season as null (n/a) if no season is selected by default
   */
  onSelectSeason(value): void {
    this.selectedSeason = value.value;
    this.selectedSeason == '' ? this.newGame.seasonId = null : this.newGame.seasonId = this.selectedSeason;
    this.isSeasonSel = true;
  }
}
