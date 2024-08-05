import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { BybMarket } from '../../../client/private/models';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'byb-markets-create',
  templateUrl: './byb-markets-create.component.html',
  styleUrls: ['./byb-markets-create.component.scss']
})
export class BybMarketsCreateComponent implements OnInit {
  public form: FormGroup;
  market_type: Array<string> = ['N/A', 'Player Bet', 'Team Bet'];
  stat_type: Array<string> = ['Passes', 'Tackles', 'Shots', 'Shots On Target', 'Shots Outside The Box', 'Assists', 'Offsides', 'Goals Inside The Box', 'Goals Outside The Box', 'Shots Against The Woodwork', 'Cards', 'Goals', 'To Be Shown A Card', 'Goalscorer'];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) { }

  ngOnInit() {
    this.form = new FormGroup({
      name: new FormControl('', [
        Validators.required
      ]),
      bybMarket: new FormControl('', [
        Validators.required
      ]),
      incidentGrouping: new FormControl('', [
        Validators.pattern('^\\d+$')
      ]),
      marketGrouping: new FormControl('', [
        Validators.pattern('^\\d+$')
      ]),
      stat: new FormControl('', []),
      marketType: new FormControl('', []),
      popularMarket: new FormControl('', []),
      marketDescription: new FormControl('', [])
    });
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  setStat(event): void {
    if (event !== 'Player Bet') {
      this.form.controls.stat.setValidators([]);
      this.form.controls.stat.setValue('');
    }
  }

  public getBybMarket(): BybMarket {
    return this.form.value;
  }

  public get name(): AbstractControl {
    return this.form.get('name');
  }

  public get marketGroupName(): AbstractControl {
    return this.form.get('bybMarket');
  }

  public get incidentGrouping(): AbstractControl {
    return this.form.get('incidentGrouping');
  }

  public get marketGrouping(): AbstractControl {
    return this.form.get('marketGrouping');
  }
  public get stat(): AbstractControl {
    return this.form.get('stat');
  }

  public get marketType(): AbstractControl {
    return this.form.get('marketType');
  }

  public get popularMarket(): AbstractControl {
    return this.form.get('popularMarket');
  }

  public get marketDescription(): AbstractControl {
    return this.form.get('marketDescription');
  }
}

