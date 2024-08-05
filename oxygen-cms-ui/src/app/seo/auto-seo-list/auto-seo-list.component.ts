import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { AppConstants } from '@app/app.constants';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { AutoseoPageDialogComponent } from './auto-seo-dialog/auto-seo-dialog.component';
import { SeoAPIService } from '@app/seo/service/seo.api.service';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';

@Component({
  selector: 'app-auto-seo-list',
  templateUrl: './auto-seo-list.component.html'
})
export class AutoSeolistComponent implements OnInit {
  autoseoPagesData: AutoSeoPage[];
  getDataError: string;
  searchField: string = '';
  styleduri: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Page url',
      property: 'uri',
      type : 'autoseo',
      customOnClickHandler: (autoseopage: AutoSeoPage) =>  this.editAutoSeoPage(autoseopage)
    },
    {
      name: 'Page title',
      property: 'metaTitle'
    },
    {
      name: 'Page Descripion',
      property: 'metaDescription'
    }
  ];

  filterProperties: Array<string> = [
    'uri',
    'metaTitle'
  ];

  constructor(
    private dialogService: DialogService,
    private seoAPIService: SeoAPIService
  ) {}
  /**
   * loads autoseoPagesData
   */
  ngOnInit() {
    this.loadIntialData();
   }
  /**
   * handles autoseopage deletion
   * @param autoseopage 
   */
  handleRemoveAutoSeoPage(autoseopage: AutoSeoPage): void {
    this.dialogService.showConfirmDialog({
      title: 'Auto Seo Pages List Change',
      message: 'Are You Sure You Want to Remove This Page?',
      yesCallback: () => {
        this.removeAutoSeoPage(autoseopage);
      }
    });
  }
  /**
   * adds new autoseopage
   */
  addNewAutoSeoPage(): void {
    this.dialogService.showCustomDialog(AutoseoPageDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Auto Seo Page',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (autoseoPage: AutoSeoPage) => {
        this.seoAPIService.createAutoSeoItem(autoseoPage)
          .map((autoseopagedata: HttpResponse<AutoSeoPage>) => autoseopagedata.body)
          .subscribe((autoseopagedata: AutoSeoPage) : void => {
            this.autoseoPagesData.push(autoseopagedata);
            this.dialogService.showNotificationDialog({
              title: 'Create Completed',
              message: 'AutoSeo Page is Created.'
            });
          },
          error => {
            this.getDataError = error.message; });
      }
    });
  }
  /**
   * removes autoseopage
   * @param autoseopage 
   */
  removeAutoSeoPage(autoseopage: AutoSeoPage): void {
    const autoseopageindex = this.autoseoPagesData.findIndex((autoseopagedata:AutoSeoPage)=>autoseopagedata.id===autoseopage.id);
    if (autoseopageindex !== -1 && autoseopage.id) {
      // remove page from pages list
      this.autoseoPagesData.splice(autoseopageindex, 1);
      // make request
      this.seoAPIService.deleteAutoSeoPage(autoseopage.id)
        .subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'AutoSeo Page is Removed.'
          });
        },
        error => {
          this.getDataError = error.message;});
    }
  }
  /**
   * loads intial autoseoPagesData
   */
  loadIntialData():void{
    this.seoAPIService.getAutoSeoListData()
    .map((autoseopagesdata: HttpResponse<AutoSeoPage[]>) => autoseopagesdata.body)
    .subscribe((autoseopagesdata: AutoSeoPage[]):void => {
      this.autoseoPagesData = autoseopagesdata;
    }, error => {
      this.getDataError = error.message;
    });
  }
  /**
   * edits the existing autoseopage
   * @param autoseopage 
   */
  editAutoSeoPage(autoseopage: AutoSeoPage): void {
    this.dialogService.showCustomDialog(AutoseoPageDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Edit Auto Seo Page',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: autoseopage,
      yesCallback: (updatedautoseopage: AutoSeoPage) => {
        this.seoAPIService.putAutoSeoItemChanges(updatedautoseopage)
          .map((response: HttpResponse<AutoSeoPage>):AutoSeoPage => {
            return response.body;
          })
          .subscribe((autoseopagedata: AutoSeoPage) => {
            updatedautoseopage = autoseopagedata;
            this.loadIntialData();
            this.dialogService.showNotificationDialog({
              title: 'Upload Completed',
              message: 'AutoSeo Page Changes are Saved.'
            });
          }, 
            error => {
            this.getDataError = error.message;});
      }
    });
 }
}
