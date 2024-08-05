import { SeoPage } from '@app/client/private/models/seopage.model';
import { Component, OnInit } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SeoAPIService } from '../../service/seo.api.service';
import { AddSeoPageComponent } from '../add-seo-page-dialog/add-seo-page.component';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';

@Component({
  selector: 'widgets-page',
  templateUrl: './seo.page.component.html',
  styleUrls: ['./seo.page.component.scss']
})
export class SeoPagesListPageComponent implements OnInit {
  seoPagesData: SeoPage[];
  getDataError: string;
  searchField: string = '';

  dataTableColumns: Array<any> = [
    {
      name: 'Page url',
      property: 'url',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Page title',
      property: 'title'
    }
  ];

  filterProperties: Array<string> = [
    'title',
    'url'
  ];

  constructor(
    private dialogService: DialogService,
    private seoAPIService: SeoAPIService,
  ) {}

  get seoPagesAmount(): ActiveInactiveExpired {
    const activePages = this.seoPagesData && this.seoPagesData.filter(seoPage => seoPage.disabled === false);
    const activePagesAmount = activePages && activePages.length;
    const inactivePagesAmount = this.seoPagesData.length - activePagesAmount;

    return {
      active: activePagesAmount,
      inactive: inactivePagesAmount
    };
  }

  handleRemoveSeoPage(page: SeoPage) {
    this.dialogService.showConfirmDialog({
      title: 'Seo Pages List Change',
      message: 'Are You Sure You Want to Remove This Page?',
      yesCallback: () => {
        this.removeSeoPage(page);
      }
    });
  }


  addNewSeoPage(): void {
    this.dialogService.showCustomDialog(AddSeoPageComponent, {
      width: '350px',
      title: 'Add New Seo Page',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (seoPage: SeoPage) => {
        this.seoAPIService.createSeoItem(seoPage)
          .map((data) => data.body)
          .subscribe((data: SeoPage) => {
            this.seoPagesData.push(data);
            this.dialogService.showNotificationDialog({
              title: 'Create Completed',
              message: 'Seo Page is Created.'
            });
          });
      }
    });
  }

 removeSeoPage(page: SeoPage) {
   const index = this.seoPagesData.indexOf(page);

   if (index !== -1 && page.id) {
     // remove page from pages list
     this.seoPagesData.splice(index, 1);

     // make request
     this.seoAPIService.deleteSeoPage(page.id)
       .subscribe(() => {
         this.dialogService.showNotificationDialog({
           title: 'Remove Completed',
           message: 'Seo Page is Removed.'
         });
       });
   }
 }

  ngOnInit() {
    this.seoAPIService.getSeoListData()
      .map((data) => data.body)
      .subscribe((data: SeoPage[]) => {
        this.seoPagesData = data;
      }, error => {
        this.getDataError = error.message;
      });
  }
}
