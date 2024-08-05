import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {Competition} from '../../../../client/private/models';
import {BrandService} from '../../../../client/private/services/brand.service';
import {ConfirmDialogComponent} from '../../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {SpaceToDashPipe} from '../../../../client/private/pipes/space-to-dash.pipe';
import { SurfaceBetConstants } from '@app/sports-modules/surface-bets/constants/surface-bet.constants';

@Component({
  selector: 'app-competition-add',
  templateUrl: './competition-add.component.html'
})
export class CompetitionAddComponent implements OnInit {
  public form: FormGroup;
  public competition: Competition;
  public surfaceBetConstants: any = SurfaceBetConstants;
  public labelShown: boolean = true;

  constructor(
    private spaceToDashPipe: SpaceToDashPipe,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {}

  ngOnInit() {
    this.competition = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,
      name: '',
      uri: '',
      typeId: undefined,
      enabled: false,
      competitionTabs: [],
      competitionParticipants: [],
      svg: null,
      svgFilename: null,
      svgBgId: null,
      background: null,
      title: ''
    };

    this.form = new FormGroup({
      competitionName: new FormControl('', [Validators.required]),
      competitionUrl: new FormControl({
        value: '',
        disabled: true
      }, [Validators.required]),
      typeId: new FormControl('', [Validators.required, Validators.min(1)]),
      competitionTitle: new FormControl('', [Validators.required])
    });
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public onNameChanged(event: any): void {
    this.competition.uri = `/${this.spaceToDashPipe.transform(event.target.value)}`;
  }
  public get typeId(): AbstractControl {
    return this.form.get('typeId');
  }
}
