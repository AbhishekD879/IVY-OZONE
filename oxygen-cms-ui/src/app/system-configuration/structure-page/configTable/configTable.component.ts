import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {DateRange} from '@app/client/private/models/dateRange.model';
import {ApiClientService} from '@app/client/private/services/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AppConstants} from '@app/app.constants';
import * as _ from 'lodash';
import { TimeRange } from '@app/client/private/models/timeRange.model';

@Component({
  selector: 'config-table',
  templateUrl: './configTable.component.html',
  styleUrls: ['./configTable.component.scss']
})
export class ConfigTableComponent implements OnInit {
  @Input() configItem: any;

  public isDataChanged: boolean = false;

  @Output()
  public clickHandler: EventEmitter<MouseEvent> = new EventEmitter<MouseEvent>();

  constructor(
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar
  ) {}

  handleDateChange(dateValue: DateRange, item) {
    if (!item.realValue) { item.realValue = {}; } // fallback for misconfiguration

    item.realValue.from = dateValue.startDate;
    item.realValue.to = dateValue.endDate;
    this.isDataChanged = true;
  }

  handleTimeChange(dateValue: TimeRange, item) {
    if (!item.realValue) { item.realValue = {}; }

    item.realValue.from = dateValue.startTime;
    item.realValue.to = dateValue.endTime;
    this.isDataChanged = true;
  }

  public saveClick(): void {
    this.dialogService.showConfirmDialog({
      title: 'System Configuration Setup',
      message: 'Are You Sure You Want to Save This Config?',
      yesCallback: () => {
        this.clickHandler.emit();
        this.isDataChanged = false;
      }
    });
  }

  uploadHandler(file: FormData, rowItem: any): void {
    if (rowItem.type === 'svg') {
      this.apiClientService
          .brandConfig()
          .uploadSvg(this.configItem.id, rowItem.name, file)
          .subscribe(() => {
            this.addFileToRowItem(rowItem, (file.get('file') as File).name);
            this.snackBar.open(`Svg Uploaded.`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
    } else if (rowItem.type === 'image') {
      this.apiClientService
          .brandConfig()
          .uploadImage(this.configItem.id, rowItem.name, file)
          .subscribe(() => {
            this.addFileToRowItem(rowItem, (file.get('file') as File).name);
            this.snackBar.open(`Image Uploaded.`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
    }
  }

  removeHandler(rowItem: any): void {
    if (rowItem.type === 'svg' || rowItem.type === 'image') {
      this.apiClientService
        .brandConfig()
        .removeImage(this.configItem.id, rowItem.name)
        .subscribe(() => {
            rowItem.filename = null;
            this.snackBar.open(`Image Deleted.`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
    }
  }

  ngOnInit() {
    /* tslint:disable */
    // Alejandro Del Rio Albrechet
    this.configItem.items.forEach((element) => {
      if (element.type === 'svg' || element.type === 'image') {
        this.addFileToRowItem(element);
      }
    });
    /* tslint:enable */
  }

  /* tslint:disable */
  // Alejandro Del Rio Albrechet
  private addFileToRowItem(element: any, fileName?: string): void {
    element.filename = {
      filename: fileName ? fileName : _.isString(element.realValue) ? element.realValue : element.realValue.value,
      path: '',
      size: 0,
      filetype: element.type
    };
  }
  /* tslint:enable */

  prepareInputMultiselectValue(value: String): Array<String> {
    return !value ? [] : value.split(',');
  }
}
