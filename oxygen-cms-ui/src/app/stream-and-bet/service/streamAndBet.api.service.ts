import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import {DialogService} from '../../shared/dialog/dialog.service';
import {SABChildElement} from '../../client/private/models/SABChildElement.model';

@Injectable()
export class StreamAndBetAPIService {
  constructor(private globalLoaderService: GlobalLoaderService,
              private apiClientService: ApiClientService,
              private dialogService: DialogService) {
  }

  /**
   * Get streamAndBet data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getStreamAndBetData() {
    const getData = this.apiClientService.streamAndBets().findAllByBrand();

    return getData;
  }

  getSiteServeEvents(categoryId: number) {
    const getData = this.apiClientService.streamAndBets().fetchEventsCategoryTreeById(categoryId);

    return getData;
  }

  getSiteServeCategories() {
    const getData = this.apiClientService.streamAndBets().fetchAllCategories();

    return getData;
  }

  postNewStreamAndBet() {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.streamAndBets().postNewStreamAndBet();

    return postData;
  }

  /**
   * Save new category to server.
   * @param {SABChildElement} category
   */
  postNewCategory(category: SABChildElement) {
    // API POST CALL
    this.globalLoaderService.showLoader();
    return this.apiClientService
      .streamAndBets()
      .postNewCategoryByBrand(category)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Category saved'
        });
      }, (error) => this.handleRequestError(error));
  }

  /**
   * Save present category changes to server.
   * @param {SABChildElement} category
   */
  putCategoryChanges(category: SABChildElement) {
    // API CALL PUT
    this.globalLoaderService.showLoader();
    this.apiClientService
      .streamAndBets()
      .putCategoryUpdateByBrand(category)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Category saved'
        });
      }, error => this.handleRequestError(error));
  }

  /**
   * Remove present category.
   * @param {SABChildElement} category
   */
  deleteCategory(categoryId: number) {
    // API CALL DELETE with /category.id
    this.globalLoaderService.showLoader();
    this.apiClientService
      .streamAndBets()
      .deleteCategoryByBrand(categoryId)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Stream and bet Saved',
          message: 'Category is removed.'
        });
      }, error => this.handleRequestError(error));
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
