import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {CompetitionParticipantUpdate} from '../../../../client/private/models';
import {ConfirmDialogComponent} from '../../../../shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'participant-create',
  templateUrl: './participant-create.component.html'
})
export class ParticipantCreateComponent implements OnInit {
  public form: FormGroup;
  public participant: CompetitionParticipantUpdate;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) {}

  ngOnInit() {
    this.participant = {
      id: '',
      obName: '',
      fullName: '',
      abbreviation: ''
    };

    this.form = new FormGroup({
      obName: new FormControl('', [Validators.required]),
      fullName: new FormControl('', []),
      abbreviation: new FormControl('', [])
    });
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }
}
