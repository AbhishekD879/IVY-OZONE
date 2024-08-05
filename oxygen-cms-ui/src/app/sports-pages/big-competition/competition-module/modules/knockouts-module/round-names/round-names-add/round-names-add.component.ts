import * as _ from 'lodash';

import {Component, Inject, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

import {ConfirmDialogComponent} from '../../../../../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {RoundNameModel} from '../../../../../../../client/private/models/roundName.model';
import {uniqueValidator} from '../../../../../../../shared/validators/unique.validator';

@Component({
  templateUrl: './round-names-add.component.html'
})
export class RoundNamesAddComponent implements OnInit {
  public form: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) private data,
    private dialog: MatDialogRef<ConfirmDialogComponent>,
  ) { }

  ngOnInit() {
    const rounds = this.data && _.isArray(this.data.rounds) ? this.data.rounds : [];

    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      abbreviation: new FormControl('', [
        Validators.required,
        uniqueValidator(rounds, 'abbreviation')
      ]),
      number: new FormControl('', [
        Validators.required,
        Validators.min(1),
        Validators.pattern('^\\d+$')
      ]),
      active: new FormControl('', []),
    });
  }

  public closeDialog(): void {
    this.dialog.close();
  }

  public getRoundName(): RoundNameModel {
    return this.form.value;
  }

  public get name(): AbstractControl {
    return this.form.get('name');
  }

  public get abbreviation(): AbstractControl {
    return this.form.get('abbreviation');
  }

  public get number(): AbstractControl {
    return this.form.get('number');
  }
}
