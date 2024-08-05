import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {CompetitionModule} from '../../../../client/private/models';
import {CompetitionModuleTypes} from '../models/module-types.enum';
import { MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import { BigCompetitionService } from '@app/sports-pages/big-competition/service/big-competition.service';
import * as _ from 'lodash';

@Component({
  selector: 'app-competition-module-add',
  templateUrl: './competition-module-add.component.html',
  styleUrls: ['./competition-module-add.component.scss']
})
export class CompetitionModuleAddComponent implements OnInit {
  public newModule: CompetitionModule;
  public moduleTypes: string[];
  public moduleTypesName: any = CompetitionModuleTypes;
  public form: FormGroup;
  public type: any;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private bigCompetitionService: BigCompetitionService
  ) { }

  ngOnInit() {
    this.type = this.bigCompetitionService.getTabType();
    this.moduleTypes = (this.type === 'subtab' ? Object.keys(_.omit(CompetitionModuleTypes, ['SURFACEBET', 'HIGHLIGHT_CAROUSEL'])) : Object.keys(CompetitionModuleTypes));
    this.newModule = {
      id: '',
      name: '',
      brand: this.brandService.brand,
      createdBy: '',
      createdAt: '',
      updatedAt: '',
      updatedBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      displayOrder: 0,
      maxDisplay: undefined,
      enabled: false,
      type: '',
      promoTag: '',
      status: '',
      markets: [],
      typeId: '',
      viewType: undefined,
      aemPageName: '',
      groupModuleData: {
        sportId: 0,
        areaId: 0,
        competitionId: 0,
        seasonId: 0,
        numberQualifiers: 0,
        details: {}
      },
      specialModuleData: {
        linkUrl: '',
        eventIds: [],
        typeIds: []
      },
      eventIds: [],
      knockoutModuleData: {
        rounds: [],
        events: []
      },
      resultModuleSeasonId: 0,
      surfaceBets: [],
      categoryIDs: [],
      highlightCarousels: []
    };
    this.form = new FormGroup({
      moduleName: new FormControl(this.newModule.name, [Validators.required]),
      moduleType: new FormControl(this.newModule.type, [Validators.required])
    });
  }
  public closeDialog(): void {
    this.dialogRef.close();
  }
}
