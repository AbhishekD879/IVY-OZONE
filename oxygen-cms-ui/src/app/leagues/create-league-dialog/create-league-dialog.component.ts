import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { League } from '../../client/private/models/league.model';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../client/private/services/brand.service';

@Component({
  selector: 'app-create-league-dialog',
  templateUrl: './create-league-dialog.component.html',
  styleUrls: ['./create-league-dialog.component.scss']
})
export class CreateLeagueDialogComponent implements OnInit {

  public league: League;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.league = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      sortOrder: -1,
      redirectionUrl: '',
      leagueUrl: '',
      betBuilderUrl: '',
      banner: '',
      name: '',
      lang: '',
      brand: this.brandService.brand,
      categoryId: null,
      typeId: null,
      ssCategoryCode: '',
      tabletBanner: ''
    };
  }

  public getNewLeague(): League {
    return this.league;
  }

  public isValidLeague(): boolean {
    return !!(
      this.league.name && this.league.name.trim().length > 0
    );
  }

  closeDialog() {
    this.dialogRef.close();
  }

}
