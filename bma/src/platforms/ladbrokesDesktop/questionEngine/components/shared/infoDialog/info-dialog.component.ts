import { Component, ViewChild } from '@angular/core';

import { InfoDialogComponent as AppInfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';

@Component({
  selector: 'info-dialog',
  // templateUrl: '../../../../../../app/questionEngine/components/shared/infoDialog/info-dialog.component.html',
  templateUrl: './info-dialog.component.html',
  styleUrls: ['./info-dialog.component.scss']
})

export class InfoDialogComponent extends AppInfoDialogComponent {
  @ViewChild('infoDialog', { static: true }) dialog;
}
