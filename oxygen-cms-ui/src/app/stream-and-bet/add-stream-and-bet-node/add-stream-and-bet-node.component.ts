import {Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {SABChildElement} from '@app/client/private/models/SABChildElement.model';


@Component({
  selector: 'app-add-stream-and-bet-node',
  templateUrl: './add-stream-and-bet-node.component.html',
  styleUrls: ['./add-stream-and-bet-node.component.scss']
})
export class AddStreamAndBetNodeComponent implements OnInit {
  public node: SABChildElement;
  public nameDropDown: Array<String>;
  public possibleValuesAvailable = false;
  nameToIdMap: Map<string, number>;

  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    this.nameToIdMap = new Map();
    const valuesList = this.data.possibleValues;
    this.nameDropDown = new Array();
    if (valuesList) {
      this.possibleValuesAvailable = true;
      for (let i = 0, len = valuesList.length; i < len; i++) {
        this.nameToIdMap.set(valuesList[i].name, valuesList[i].id);
        this.nameDropDown.push(valuesList[i].name);
      }
    }

    this.node = {
      selection: '',
      name: '',
      siteServeId: 0,
      showItemFor: '',
      children: [],
      parentId: 0
    };
  }

  getId(name: string) {
    this.node.siteServeId = this.nameToIdMap.get(name);
    return this.node.siteServeId;
  }

  getNewCategorySubItem(): SABChildElement {
    return this.node;
  }

  closeDialog() {
    this.dialogRef.close();
  }

}
