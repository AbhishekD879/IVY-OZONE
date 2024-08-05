import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { FilterModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'filter-create',
  templateUrl: './filter-create.component.html',
  styleUrls: ['./filter-create.component.scss']
})
export class FilterCreateComponent implements OnInit {
  getDataError: string;
  newFilter: FilterModel;
  isHaveAll: boolean=false;
  isSpecialCar: boolean=false;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  /**
    * to close the dialog.
    * @returns - {void}
    */
  closeDialog(): void {
    this.dialogRef.close();
  }

  ngOnInit() {
    this.newFilter = {
      filterName: '',
      filterActive: false,
      brand: this.brandService.brand,
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      isLinkedFilter: false,
      linkedFilterWarningText: ''
    };
  }

  /**
* To validate the filter
* @returns - boolean
*/

  public isValid(){
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    this.isHaveAll = (this.newFilter.filterName?.toLowerCase() === 'all') ?  true : false;
    this.isSpecialCar =  (specialChars.test(this.newFilter.filterName)) ? true : false;
    return !(this.newFilter.filterName?.length>0&&(!this.newFilter.isLinkedFilter||this.newFilter.isLinkedFilter&&this.newFilter.linkedFilterWarningText&&this.newFilter.linkedFilterWarningText.length>0)&&!this.isHaveAll&&!this.isSpecialCar)
  }
}
