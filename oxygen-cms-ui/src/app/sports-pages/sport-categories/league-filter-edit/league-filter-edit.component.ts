import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { SportTabLeagueFilterValue } from "@app/client/private/models/sporttabFilters.model";


@Component({
  templateUrl: './league-filter-edit.component.html',
  providers: [
    DialogService
  ]
})
export class LeagueFilterEditComponent implements OnInit {
  public leagueFilter: SportTabLeagueFilterValue;
  public form: FormGroup;

  constructor(
    public dialogRef: MatDialogRef<LeagueFilterEditComponent>,
    @Inject(MAT_DIALOG_DATA) public dialog: any
  ) { }

  ngOnInit(): void {
    this.form = new FormGroup({
      leagueName: new FormControl('', [Validators.required]),
      leagueIds: new FormControl('', [
        Validators.required,
        Validators.pattern('^\\s*\\d+\\s*(,\\s*\\d+\\s*)*$')])
    });
    this.leagueFilter = this.dialog.data;
  }

  get leagueIds() {
    return this.form.get('leagueIds')
  }

  normalizeLeagueFilter(): void {
    const form = this.form.value;
    this.leagueFilter.leagueName = form.leagueName;
    this.leagueFilter.leagueIds = typeof form.leagueIds === 'string' ?
      form.leagueIds.replaceAll(' ', '').split(',') : form.leagueIds;
  }

  cancel(): void {
    this.dialogRef.close();
  }
}
