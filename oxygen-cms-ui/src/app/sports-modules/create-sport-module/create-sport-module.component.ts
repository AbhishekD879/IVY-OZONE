import { Component, Inject, OnInit } from '@angular/core';
import { ISportModuleType } from '@app/client/private/models/sport-modules/sport-module.model';
import { sportModuleTypes } from '@app/sports-modules/constant/module-types.constant';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { SportsModule } from '@app/client/private/models/homepage.model';
import * as _ from 'lodash';

@Component({
  selector: 'app-create-sport-module',
  templateUrl: './create-sport-module.component.html',
  styleUrls: ['./create-sport-module.component.scss']
})
export class CreateSportModuleComponent implements OnInit {
  sportModuleTypes: ISportModuleType[] = sportModuleTypes;
  moduleName: string;
  moduleType: string;
  createdSportModules: SportsModule[];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) { }

  ngOnInit() {
    this.createdSportModules = this.data.data.sportModules;

    this.sportModuleTypes = _.filter(this.sportModuleTypes, (moduleType) => {
      return _.every(this.createdSportModules, (module: SportsModule) => {
         if (moduleType.type === 'AEM_BANNERS') {
           return module.title !== moduleType.name;
         }
         return module.moduleType !== moduleType.type;
      });
    });

    this.moduleName = this.sportModuleTypes[0] && this.sportModuleTypes[0].name;
    this.moduleType = this.sportModuleTypes[0] && this.sportModuleTypes[0].type;
  }

  onChangeModuleType(moduleName) {
    this.moduleName = moduleName;
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
