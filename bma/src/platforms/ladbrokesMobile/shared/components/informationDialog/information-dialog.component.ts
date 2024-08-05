import { Component } from '@angular/core';
import { InformationDialogComponent as
    OxygenInformationDialogComponent } from '@app/shared/components/informationDialog/information-dialog.component';

@Component({
  selector: 'information-dialog',
  templateUrl: './information-dialog.component.html',
})
export class InformationDialogComponent extends OxygenInformationDialogComponent { }
