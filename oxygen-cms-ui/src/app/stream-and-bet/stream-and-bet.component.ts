import {Component, OnInit} from '@angular/core';
import {DialogService} from '../shared/dialog/dialog.service';
import { MatDialog } from '@angular/material/dialog';
import {AppConstants} from '../app.constants';
import {GlobalLoaderService} from '../shared/globalLoader/loader.service';
import {StreamAndBetAPIService} from './service/streamAndBet.api.service';

import {AddStreamAndBetNodeComponent} from './add-stream-and-bet-node/add-stream-and-bet-node.component';
import {SABChildElement} from '../client/private/models/SABChildElement.model';
import {StreamAndBet} from '../client/private/models/streamandbet.model';

@Component({
  selector: 'app-stream-and-bet',
  templateUrl: './stream-and-bet.component.html',
  styleUrls: ['./stream-and-bet.component.scss'],
  providers: [StreamAndBetAPIService]
})
export class StreamAndBetComponent implements OnInit {

  /**
   * main streamAndBet object
   */
  public streamAndBetData: StreamAndBet;

  /**
   * categories groups
   */
  public categoriesArray;

  /**
   * loading data flag
   */
  public isLoading: boolean;

  /**
   * Category search string
   * @type {string}
   */
  public searchField: string = '';

  /**
   * Temporary store new created categories to send POST request to server.
   * @type {array[]}
   */
  public newCategories: Array<SABChildElement> = [];

  public availableCategoryList;

  constructor(private dialog: MatDialog,
              private dialogService: DialogService,
              private globalLoaderService: GlobalLoaderService,
              private streamAndBetAPIService: StreamAndBetAPIService) {
  }

  private updateSuggestionsList() {
    const valuesToRemove = [];
    for (let i = 0, len_i = this.availableCategoryList.length; i < len_i; i++) {
      for (let j = 0, len_j = this.categoriesArray.length; j < len_j; j++) {
        if (this.availableCategoryList[i].id === this.categoriesArray[j].siteServeId) {
          valuesToRemove.push(i);
        }
      }
    }
    valuesToRemove.sort(function (a, b) {
      return b - a;
    });
    for (let i = 0, len = valuesToRemove.length; i < len; i++) {
      this.availableCategoryList.splice(valuesToRemove[i], 1);
    }
  }

  createNewCategory() {
    this.updateSuggestionsList();
    const dialogRef = this.dialog.open(AddStreamAndBetNodeComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        title: 'Add New Category',
        yesOption: 'Save',
        noOption: 'Cancel',
        possibleValues: this.availableCategoryList
      }
    });
    dialogRef.afterClosed().subscribe(newCategoryNode => {
      if (newCategoryNode) {
        newCategoryNode.selection = 'category';
        newCategoryNode.parentId = '';
        newCategoryNode.children = [];
        this.categoriesArray.push(newCategoryNode);
        this.newCategories.push(newCategoryNode);
      }
    });

  }

  /**
   * Categories list to view on page
   * could be filtered with search bar.
   * @returns {any}
   */
  public get categoriesList() {
    if (this.searchField.length > 0) {
      return this.categoriesArray.filter((item) => {
        return ~item.name.toLowerCase().indexOf(this.searchField.toLowerCase());
      });
    } else {
      return this.categoriesArray;
    }
  }

  /**
   * Is group was not saved before.
   * @param {SABChildElement} category
   * @returns {boolean}
   */
  isNewCategory(category: SABChildElement) {
    return this.newCategories.some(node => node.name === category.name);
  }

  /**
   * New group will be not "new" after first update,
   * so next updates will be as PUT instead of POST.
   * @param categories
   */
  removeNewCategory(categories) {
    const index = this.newCategories.indexOf(categories);
    if (index !== -1) {
      this.newCategories.splice(index, 1);
    }
  }

  /**
   * Apply changes after changing Category.
   * save data to server
   */
  applyCategoryChanges(category: SABChildElement) {
    if (this.isNewCategory(category)) {
      this.removeNewCategory(category);
      return this.streamAndBetAPIService.postNewCategory(category);
    } else if (category.siteServeId !== null && category.siteServeId !== undefined) {
      this.streamAndBetAPIService.putCategoryChanges(category);
    } else {
      this.dialogService.showNotificationDialog({
        title: 'Save error',
        message: 'Category Won`t Be Saved'
      });
    }
  }

  /**
   * Remove group from main list and send DELETE request.
   * @param {SABChildElement} category
   */
  callRemoveCategory(category: SABChildElement) {
    const index = this.categoriesArray.indexOf(category);

    if (index !== -1 && category.siteServeId) {
      // remove group from groups array
      this.categoriesArray.splice(index, 1);

      // make request
      this.streamAndBetAPIService.deleteCategory(category.siteServeId);
    } else if (index !== -1 && !category.siteServeId) {
      // remove group from groups array
      this.categoriesArray.splice(index, 1);
    } else {
      this.dialogService.showNotificationDialog({
        title: 'StreamAndBet Save Error',
        message: 'Couldn`t Find Category to Remove, Please Reload Page and Try Again.'
      });
    }
  }

  /**
   * initial method. get load from server
   */
  ngOnInit(): void {
    this.loadStreamAndBetFromDB();
    this.loadCategoriesList();
  }

  private loadStreamAndBetFromDB() {
    this.isLoading = true;
    this.globalLoaderService.showLoader();
    this.streamAndBetAPIService.getStreamAndBetData()
      .map((data: any) => {
        return data;
      }).subscribe((data: any) => {
      this.globalLoaderService.hideLoader();
      this.isLoading = false;

      if (data.body.length <= 0) {
        this.createEmptyStreamAndBet();
      } else {
        // streamAndBet data - as-is object from db
        this.streamAndBetData = data.body[0];
        // categories list
        this.categoriesArray = data.body[0].children;
        for (let i = 0, len = this.categoriesArray.length; i < len; i++) {
          const grandChildren = this.categoriesArray[i].children;
          if (!grandChildren) {
            continue;
          }
          this.setParent(this.categoriesArray[i].siteServeId, grandChildren);
        }
      }
    }, () => {
      this.isLoading = false;
      this.globalLoaderService.hideLoader();
    });
  }

  private loadCategoriesList() {
    this.isLoading = true;
    this.globalLoaderService.showLoader();
    this.streamAndBetAPIService.getSiteServeCategories().map((data: any) => {
      return data;
    }).subscribe((data: any) => {
      this.globalLoaderService.hideLoader();
      this.isLoading = false;
      this.availableCategoryList = data.body;
    }, () => {
      this.isLoading = false;
      this.globalLoaderService.hideLoader();
    });
  }

  private createEmptyStreamAndBet() {
    this.isLoading = true;
    this.globalLoaderService.showLoader();
    this.streamAndBetAPIService.postNewStreamAndBet().map((data: any) => {
      return data;
    }).subscribe((data: any) => {
      this.globalLoaderService.hideLoader();
      this.isLoading = false;
      // should be empty objects here
      this.streamAndBetData = data.body[0];
      this.categoriesArray = [];
    }, () => {
      this.isLoading = false;
      this.globalLoaderService.hideLoader();
    });
  }

  private setParent(parentId: number, children: Array<SABChildElement>) {
    if (!children) {
      return;
    }
    for (let i = 0, len = children.length; i < len; i++) {
      if (!parent) {
        continue;
      }
      children[i].parentId = parentId;
      const grandChildren = children[i].children;
      if (!grandChildren) {
        continue;
      }
      this.setParent(children[i].siteServeId, grandChildren);
    }
  }

}

