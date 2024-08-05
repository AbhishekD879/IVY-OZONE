import {ApiClientService} from './../../../client/private/services/http/index';
import {GlobalLoaderService} from './../../../shared/globalLoader/loader.service';
import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {AppConstants} from '../../../app.constants';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {StaticTextOtf} from '../../../client/private/models/staticTextOtf.model';
import {StaticTextOtfAPIService} from '../../service/staticTextOtf.api.service';
import {StaticTextOtfCreateComponent} from '../static-text-create/static-text.create.component';

@Component({
  selector: 'static-text-otf-list-page',
  templateUrl: './static-text-list.page.component.html',
  styleUrls: ['./static-text-list.page.component.scss']
})
export class StaticTextOtfListComponent implements OnInit {
  staticTextsData: Array<StaticTextOtf>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Page Name',
      property: 'pageName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Enabled',
      property: 'enabled'
    }
  ];

  filterProperties: Array<string> = [
    'pageName'
  ];
  constructor(
    public snackBar: MatSnackBar,
    private staticTextAPIService: StaticTextOtfAPIService,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {}

  removeStaticText(staticText: StaticTextOtf) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Text',
      message: 'Are You Sure You Want to Remove Static Text?',
      yesCallback: () => {
        this.sendRemoveRequest(staticText);
      }
    });
  }

  removeHandlerMulty(staticTextsIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Static Text (${staticTextsIds.length})`,
      message: 'Are You Sure You Want to Remove Static Texts?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(staticTextsIds.map(id => this.apiClientService.staticTextOtfService().deleteStaticTextOtf(id)))
          .subscribe(() => {
            staticTextsIds.forEach((id) => {
              const index = _.findIndex(this.staticTextsData, { id: id });
              this.staticTextsData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  sendRemoveRequest(staticText: StaticTextOtf) {
    this.staticTextAPIService.deleteStaticTextOtf(staticText.id)
      .subscribe((data: any) => {
        this.staticTextsData.splice(this.staticTextsData.indexOf(staticText), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Static Text is Removed.'
        });
      });
  }

  reloadStaticTexts() {
    this.staticTextAPIService.getStaticTextOtfsData()
      .subscribe((data: any) => {
        this.staticTextsData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  createStaticText() {
    const dialogRef = this.dialog.open(StaticTextOtfCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newStaticText => {
      if (newStaticText) {
        this.staticTextAPIService.postNewStaticTextOtf(newStaticText)
          .subscribe(isOk => {
            if (isOk) {
              this.staticTextsData.push(newStaticText);
              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Static Text is Created and Stored.'
              });
              this.reloadStaticTexts();
            }
          });
      }
    });
  }

  ngOnInit() {
    this.reloadStaticTexts();
  }
}
