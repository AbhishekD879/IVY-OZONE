import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../../../shared/dialog/dialog.service';
import {OlympicsAPIService} from '../../service/olympics.api.service';
import {Sport} from '../../../../client/private/models/sport.model';
import {AddOlympicsPageComponent} from '../add-olympics-page-dialog/add-olympics-page.component';
import {HttpResponse} from '@angular/common/http';
import {DataTableColumn} from '../../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../../client/private/models/activeInactiveExpired.model';
import {AppConstants} from '../../../../app.constants';
import {Order} from '../../../../client/private/models/order.model';

@Component({
  selector: 'olympics-page',
  templateUrl: './olympics.page.component.html',
  styleUrls: ['./olympics.page.component.scss']
})
export class OlympicsPagesListPageComponent implements OnInit {
  olympicsPagesData: Sport[];
  getDataError: string;
  searchField: string = '';
  public isLoading: boolean = false;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'imageTitle',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    }, {
      name: 'Category ID',
      property: 'categoryId'
    }, {
      name: 'Alt',
      property: 'alt'
    }, {
      name: 'Filename',
      property: 'fileNameString'
    }, {
      name: 'Target URI',
      property: 'targetUri'
    }, {
      name: 'In App',
      property: 'inApp',
      type: 'boolean'
    }, {
      name: 'Show In Inplay',
      property: 'showInPlay',
      type: 'boolean'
    }, {
      name: 'Is Outright Sport',
      property: 'isOutrightSport',
      type: 'boolean'
    }
  ];


  filterProperties: Array<string> = [
    'imageTitle'
  ];

  constructor(
    private dialogService: DialogService,
    private olympicsAPIService: OlympicsAPIService,
    private snackBar: MatSnackBar
  ) {
  }

  get olympicsPagesAmount(): ActiveInactiveExpired {
    const activePages = this.olympicsPagesData && this.olympicsPagesData.filter(olympicsPage => olympicsPage.disabled === false);
    const activePagesAmount = activePages && activePages.length;
    const inactivePagesAmount = this.olympicsPagesData.length - activePagesAmount;

    return {
      active: activePagesAmount,
      inactive: inactivePagesAmount
    };
  }

  public handleRemoveOlympicsPage(page: Sport): void {
    this.dialogService.showConfirmDialog({
      title: 'Olympics Pages List Change',
      message: 'Are You Sure You Want to Remove This Page?',
      yesCallback: () => {
        this.removeOlympicsPage(page);
      }
    });
  }


  public addNewOlympicsPage(): void {
    this.dialogService.showCustomDialog(AddOlympicsPageComponent, {
      width: '350px',
      title: 'Add New Olympics Page',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (olympicsPage: Sport) => {
        this.olympicsAPIService
            .createOlympicsItem(olympicsPage)
            .map((data: HttpResponse<Sport>) => {
              return data.body;
            })
            .subscribe((data: Sport) => {
              this.olympicsPagesData.push(data);
              this.dialogService.showNotificationDialog({
                title: 'Create Completed',
                message: 'Olympics Page is Created.'
              });
            });
      }
    });
  }

 public removeOlympicsPage(page: Sport): void {
   const index = this.olympicsPagesData.indexOf(page);

   if (index !== -1 && page.id) {
     // remove page from pages list
     this.olympicsPagesData.splice(index, 1);

     // make request
     this.olympicsAPIService.deleteOlympicsPage(page.id)
       .subscribe(() => {
         this.dialogService.showNotificationDialog({
           title: 'Remove Completed',
           message: 'Olympics Page is Removed.'
         });
       });
   }
 }

 public get sports(): { inApp: number; inPlay: number; outright: number } {
   return {
    inApp: this.olympicsPagesData.filter(sport => sport.inApp).length,
    inPlay: this.olympicsPagesData.filter(sport => sport.showInPlay).length,
    outright: this.olympicsPagesData.filter(sport => sport.isOutrightSport).length
   };
 }

 reorderHandler(newOrder: Order): void {
  this.olympicsAPIService
    .postNewOlympicsOrder(newOrder)
    .subscribe(() => {
      this.snackBar.open(`Header menu order saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
}

  ngOnInit(): void {
    this.isLoading = true;
    this.olympicsAPIService.getOlympicsListData()
      .map((data: HttpResponse<Sport>) => {
        return data.body;
      })
      .subscribe((data: Sport[]) => {
        this.olympicsPagesData = data.map((sport: Sport) => {
          const file = sport.filename;
          sport.fileNameString = file && file.filename ? `${file.filename}/${file.path}` : '';
          return sport;
        });
        this.isLoading = false;
      }, error => {
        this.getDataError = error.message;
        this.isLoading = false;
      });
  }
}
