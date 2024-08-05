import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { GamificationData, SeasonData } from '@root/app/one-two-free/constants/otf.model'
import { AssetManagement } from '@root/app/client/private/models/assetManagement.model';
@Injectable({
  providedIn: 'root'
})
export class SeasonsApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) { }

  /**
  * Wrap request to handle success/error.
  * @param observableDate
  */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }
        return Observable.throw(response);
      });
  }

  /**
   * Get all seasons
   * @param showLoader 
   * @returns {Observable<HttpResponse<SeasonData[]>>}
   */
  getAllSeasons(showLoader: boolean = true): Observable<HttpResponse<SeasonData[]>> {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfSeasonBadgeService().getAllSeasons();
    return this.wrappedObservable(getData);
  }

  /**
   * Get all gamification
   * @param showLoader 
   * @returns {Observable<HttpResponse<GamificationData[]>>}
   */
  getAllGamification(showLoader: boolean = true): Observable<HttpResponse<SeasonData[]>> {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfSeasonBadgeService().getAllGamification();
    return this.wrappedObservable(getData);
  }

  /**
   * Get all Season list
   * @param showLoader 
   * @returns {Observable<HttpResponse<SeasonData[]>>}
   */
  getAllSeasonsList(showLoader: boolean = true): Observable<HttpResponse<SeasonData[]>> {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfSeasonBadgeService().getAllSeasonsList();
    return this.wrappedObservable(getData);
  }

  /**
   * Get all teams data
   * @param showLoader 
   * @returns {Observable<HttpResponse<AssetManagement[]>>}
   */
  getAllTeams(showLoader: boolean = true): Observable<HttpResponse<AssetManagement[]>> {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.assetManagements().findAllAssetManagements();
    return this.wrappedObservable(getData);
  }

  /**
   * Create Season
   * @param seasonData 
   * @returns {Observable<HttpResponse<SeasonData[]>>}
   */
  createSeason(seasonData: SeasonData): Observable<HttpResponse<SeasonData>> {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().postnewSeasonData(seasonData);
    return this.wrappedObservable(postData);
  }

  /**
   * Update Season
   * @param seasonData 
   * @param flag 
   * @returns {Observable<HttpResponse<SeasonData[]>>}
   */
  updateSeason(seasonData: SeasonData, flag: boolean): Observable<HttpResponse<SeasonData>> {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().putSeasonChanges(seasonData, flag);
    return this.wrappedObservable(postData);
  }

  /**
   * Create Gamification
   * @param gamificationData 
   * @returns {Observable<HttpResponse<GamificationData>>}
   */
  createGamification(gamificationData: GamificationData): Observable<HttpResponse<GamificationData>> {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().postnewGamification(gamificationData);
    return this.wrappedObservable(postData);
  }

  /**
   * update gamification data
   * @param gamificationData 
   * @returns Observable<HttpResponse<GamificationData>>}
   */
  updateGamification(gamificationData: GamificationData): Observable<HttpResponse<GamificationData>> {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().putGamificationChanges(gamificationData);
    return this.wrappedObservable(postData);
  }

  /**
   * delete Season
   * @param id string
   * @returns Observable<HttpResponse<void>>}
   */
  deleteSeason(id: string): Observable<HttpResponse<void>> {
    const deleteSeason = this.apiClientService.otfSeasonBadgeService().deleteSeason(id);
    return this.wrappedObservable(deleteSeason);
  }

  /**
   * delete gamification
   * @param id 
   * @returns Observable<HttpResponse<void>>}
   */
  deleteGamification(id: string): Observable<HttpResponse<void>> {
    const deleteGamification = this.apiClientService.otfSeasonBadgeService().deleteGamification(id);
    return this.wrappedObservable(deleteGamification);
  }

  /**
  * Load single season data to edit.
  * @param {string} id
  * @returns Observable<HttpResponse<SeasonData>>}
  */
  getSingleSeasonData(id: string): Observable<HttpResponse<SeasonData>> {
    const getData = this.apiClientService.otfSeasonBadgeService().getSingleSeason(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Get gamification by id
   * @param id 
   * @returns Observable<HttpResponse<GamificationData>>}
   */
  getGamificationById(id: string): Observable<HttpResponse<GamificationData>> {
    const getData = this.apiClientService.otfSeasonBadgeService().getSingleGamification(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Handle Request Error
   * @param error 
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
