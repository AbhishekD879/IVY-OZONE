import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { SportTabLeagueFilterValue } from "@app/client/private/models/sporttabFilters.model";

@Component({
  templateUrl: './league-filter-create.component.html'
})
export class LeagueFilterCreateComponent implements OnInit {
  public form: FormGroup;
  public leagueFilter: SportTabLeagueFilterValue;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
  ) { }

  ngOnInit(): void {
    this.leagueFilter = {
      leagueName: '',
      leagueIds: []
    };

    this.form = new FormGroup({
      leagueName: new FormControl('', [Validators.required]),
      leagueIds: new FormControl('', [
        Validators.required,
        Validators.pattern('^\\s*\\d+\\s*(,\\s*\\d+\\s*)*$')
      ])
    });
  }

  normalizeLeagueFilter(): void {
    const form = this.form.value;
    this.leagueFilter.leagueName = form.leagueName;
    this.leagueFilter.leagueIds = form.leagueIds.replaceAll(' ', '').split(',');
  }

  get leagueIds() {
    return this.form.get('leagueIds')
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isLeagueFilterValid(): boolean {
    return this.form.valid;
  }
}
