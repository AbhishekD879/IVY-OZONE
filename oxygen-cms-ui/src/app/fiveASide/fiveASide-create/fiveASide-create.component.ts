import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import {FiveASideFormation} from '@app/client/private/models/fiveASideFormation.model';
import {MARKETS} from '@app/core/constants/banach-markets.constant';
import {FORMATIONS} from '@app/core/constants/formation.constant';

@Component({
  templateUrl: './fiveASide-create.component.html',
  styleUrls: ['./fiveASide-create.component.scss']
})
export class FiveASideCreateComponent implements OnInit {
  public marketTemplateNames: string[] = MARKETS.map((market) => market.title);  // array of free constant template names for dropdown markets list
  public formations: string[] = FORMATIONS.slice(); // array of free constant names for dropdown formations list
  public form: FormGroup;
  public fiveASideFormation: FiveASideFormation;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.fiveASideFormation = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      title: '',
      actualFormation: '',
      position1: '',
      stat1: null,
      position2: '',
      stat2: null,
      position3: '',
      stat3: null,
      position4: '',
      stat4: null,
      position5: '',
      stat5: null,
      sortOrder: 0
    };

    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      actualFormation: new FormControl('', [Validators.required]),
      position1: new FormControl(''),
      stat1: new FormControl('', [Validators.required]),
      position2: new FormControl(''),
      stat2: new FormControl('', [Validators.required]),
      position3: new FormControl(''),
      stat3: new FormControl('', [Validators.required]),
      position4: new FormControl(''),
      stat4: new FormControl('', [Validators.required]),
      position5: new FormControl(''),
      stat5: new FormControl('', [Validators.required])
    });
  }

  get5ASideFormations(): FiveASideFormation {
    const form = this.form.value;
    this.fiveASideFormation.title = form.title;
    this.fiveASideFormation.actualFormation = form.actualFormation;
    this.fiveASideFormation.position1 = form.position1;
    this.fiveASideFormation.stat1 = this.findStat(form.stat1);
    this.fiveASideFormation.position2 = form.position2;
    this.fiveASideFormation.stat2 = this.findStat(form.stat2);
    this.fiveASideFormation.position3 = form.position3;
    this.fiveASideFormation.stat3 = this.findStat(form.stat3);
    this.fiveASideFormation.position4 = form.position4;
    this.fiveASideFormation.stat4 = this.findStat(form.stat4);
    this.fiveASideFormation.position5 = form.position5;
    this.fiveASideFormation.stat5 = this.findStat(form.stat5);
    return this.fiveASideFormation;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
  findStat(statname) {
    return MARKETS.find((market) => market.title === statname);
  }

  is5ASideFormationsValid(): boolean {
    return this.form.valid;
  }
}
