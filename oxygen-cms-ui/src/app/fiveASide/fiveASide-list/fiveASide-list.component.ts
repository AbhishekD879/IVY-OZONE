import * as _ from 'lodash';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FiveASideFormation } from '@app/client/private/models/fiveASideFormation.model';
import { FiveASideCreateComponent } from '../fiveASide-create/fiveASide-create.component';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { AppConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import {FiveASideApiService} from '@app/fiveASide/services/fiveASide.api.service';

@Component({
  templateUrl: './fiveASide-list.component.html',
  styleUrls: ['./fiveASide-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class FiveASideListComponent implements OnInit {

  public fiveASideFormations: FiveASideFormation[];
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Title',
      'property': 'title',
      'link': {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      'name': 'Actual Formation',
      'property': 'actualFormation'
    }
  ];
  public searchableProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: FiveASideApiService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .getFormationsList()
      .map(response => {
        return response.body;
      })
      .subscribe((data: FiveASideFormation[]) => {
        this.fiveASideFormations = data;
        this.globalLoaderService.hideLoader();
      }, error => {
         console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createFormation(): void {
    this.dialogService.showCustomDialog(FiveASideCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add Formation Selector',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (formation: FiveASideFormation) => {
        this.apiClientService
          .createFormation(formation)
          .map(response => {
            return response.body;
          })
          .subscribe((data: FiveASideFormation) => {
            this.fiveASideFormations.push(data);
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

  removeHandler(formation: FiveASideFormation): void {
    this.dialogService.showConfirmDialog({
      title: '5 A Side Formation',
      message: 'Are You Sure You Want to Remove Formation?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService
          .deleteFormation(formation.id)
          .subscribe(() => {
            _.remove(this.fiveASideFormations, {id: formation.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .postNewFormationsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Formations order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
