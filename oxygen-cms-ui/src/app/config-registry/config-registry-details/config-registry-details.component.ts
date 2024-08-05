import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@root/app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-config-registry-details',
  templateUrl: './config-registry-details.component.html'
})
export class ConfigRegistryDetailsComponent implements OnInit {

  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { registryData: any }
  ) { }
  configMap;
  newRegistry: any;
  api:string;
  collections:string;
  patchdata= {};
  btnName = 'Create';

  ngOnInit(): void {
    if (this.data.registryData) {
      this.btnName= 'Update';
      this.patchdata = this.data.registryData;
      this.api=this.data.registryData['key'];
      this.collections=this.data.registryData['values'].join(",");
    } else {
      this.btnName = 'Create';
      this.newRegistry = {}
    }


  }
  closeDialog() {
    this.dialogRef.close();
  }

    /**
   * Base model validation with checking required fields.
   * @return {boolean}
   */

  isValidModel():boolean {
    return this.api && this.api.length > 0  && this.collections && this.collections.length > 0;
  }

   /**
     * Create or Edit single config registry
     * @returns - {void}
     */

  submit(btnName){
    this.newRegistry={};
    this.newRegistry['key'] = this.api;
    this.newRegistry['values'] = this.collections.split(',');
    if(btnName === "Update"){
      this.newRegistry['id'] = this.patchdata['id'];
      this.dialogRef.close({data : this.newRegistry});
    }else{
      this.dialogRef.close({data : this.newRegistry});
    }
  }
}
