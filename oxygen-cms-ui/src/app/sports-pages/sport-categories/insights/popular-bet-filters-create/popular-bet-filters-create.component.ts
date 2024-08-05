import { Component, Inject, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { ISportTabPopularBetsFilter } from '@app/client/private/models/sporttabFilters.model';
import * as _ from 'lodash';


@Component({
  templateUrl: "./popular-bet-filters-create.component.html",
  providers: [DialogService],
})
export class PopularBetFiltersCreateComponent implements OnInit {
  public sportDataFilter = [];
  popularBetsSportObj: ISportTabPopularBetsFilter;
  public form: FormGroup;
  HourMin: any = [{time:'Hour',short: true},{time: 'Minute',short: false}];
  selectedTime: string;
  btnTitle: string;
  isValueChange: boolean;
  hoursOrMinutes: string;
  defaultCheckBoxHandler:boolean;

  constructor(
    public dialogRef: MatDialogRef<PopularBetFiltersCreateComponent>,
    @Inject(MAT_DIALOG_DATA) public dialog: any
  ) {}

  ngOnInit(): void {
      if (this.dialog.pageType == "create") {
        this.sportDataFilter = this.dialog.sportFilterData;
        this.formpopularBetsSportObjData(false, "", true, 0,false);
        this.btnTitle = "Add Filter";
      };
      if (this.dialog.pageType == "edit") {
      const editData = this.dialog.filter;
      this.formpopularBetsSportObjData(editData.isEnabled, editData.displayName, editData.isTimeInHours, editData.time, editData.isDefault);
      this.defaultCheckBoxHandler = editData.isEnabled,
      this.btnTitle = "Edit Filter";
    };
  }

  /**
   * Filter popup form
   * @param isEnabled 
   * @param displayName 
   * @param isTimeInHours 
   * @param time 
   * @param isDefault 
   */
  private formpopularBetsSportObjData(isEnabled:boolean, displayName: string,isTimeInHours: boolean, time: number, isDefault: boolean): void {
    this.popularBetsSportObj = {
      isEnabled: isEnabled,
      displayName: displayName,
      isTimeInHours: isTimeInHours,
      time: time,
      isDefault: isDefault
    };
    this.selectHoursMinValue(this.popularBetsSportObj);
  }

  /**
   * enable check
   * @param event 
   * @returns 
   */
  public isEnabledSportFilter(event): boolean {
   this.defaultCheckBoxHandler = event.checked;
   if(!event.checked){
    this.popularBetsSportObj.isDefault = false;
  }
   return this.popularBetsSportObj.isEnabled = event.checked;
  }

  public defaultPropertyHandler(event: { checked: boolean }) {
    this.popularBetsSportObj.isDefault = event.checked;
  }

  /**
   * cancel popup
   */
  public cancel(): void {
    this.dialogRef.close();
  }

  /**
   * popup filter values validaiton
   * @returns 
   */
  public popularBetsFilterValid(): boolean {
    this.isValueChange = _.isEqual(this.popularBetsSportObj, this.dialog.filter);
    return !!(this.popularBetsSportObj.displayName && this.popularBetsSportObj.displayName.length > 0 && this.popularBetsSportObj.displayName.length <= 15 && ( this.popularBetsSportObj.time > 0 && this.popularBetsSportObj.time.toString().length <= 4));
  }

  /**
   * setting hours and minutes values
   * @param event 
   */
  selectHoursMinValue(event) {
    const hourMin= event.isTimeInHours ? 'h' : 'm';
    this.hoursOrMinutes = `${event.time}${hourMin}`;
  }

  /**
   * setting hours and minutes values, with time field
   * @param event 
   */
  setHoursMinFormData(event){
    const list = this.hoursOrMinutes.split(/([0-9]+)/);
    this.popularBetsSportObj.isTimeInHours = list[2].includes('h');
    this.popularBetsSportObj.time = Number(list[1]);
  }
}
