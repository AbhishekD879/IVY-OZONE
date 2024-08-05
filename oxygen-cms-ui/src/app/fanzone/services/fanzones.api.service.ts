import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ClubPromo, Fanzone, FzPreferences, IFanzoneComingBack, IFzOptinEmail, Syc, INewSignPosting, IPopUp } from '@app/client/private/models/fanzone.model';


@Injectable()
export class FanzonesAPIService {

  constructor(private globalLoaderService: GlobalLoaderService, private apiClientService: ApiClientService) { }

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
        if (response instanceof HttpErrorResponse && response.status !== 400) {
          this.handleRequestError(response.error);
        }

        this.globalLoaderService.hideLoader();
        return Observable.throw(response);
      });
  }

  /**
  * Handle networking error.
  * Notify user.
  */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }

  /**
   * to create fanzone
   * @param fanzone
   * @returns created fanzone with ID
   */

  createFanzone(fanzone: Fanzone): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().createFanzone(fanzone);
    return this.wrappedObservable(data);
  }

  /**
   * to get all the fanzones
   * @returns all fanzones
   */
  getAllFanzones(): Observable<Fanzone[]> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getAllFanzones();
    return this.wrappedObservable(data);
  }

  /**
   * to get the fanzone based on ID
   * @param id
   * @returns fanzone
   */
  getFanzoneDetails(id: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getFanzoneDetails(id);
    return this.wrappedObservable(data);
  }

  /**
   * to update the fanzone based on ID
   * @param id
   * @returns fanzone
   */
  updateFanzoneDetails(id: string, fanzone: Fanzone) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().updateFanzoneDetails(id, fanzone);
    return this.wrappedObservable(data);
  }

  /**
   * to delete the fanzones based on ID
   * @param id
   * @returns void
   */
  deleteFanzone(id: string | string[]): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().deleteFanzone(id);
    return this.wrappedObservable(data);
  }

  /**
    * to save or update the fanzone SYC
    * @param method, syc, id
    * @returns Syc
    */
  saveFanzoneSyc(method: string, syc: Syc, id: string): Observable<HttpResponse<Syc>> {
    const data = this.apiClientService.fanzoneService().saveFanzoneSyc(method, syc, id);
    return this.wrappedObservable(data);
  }

  /**
   * to get Fanzone show your colors information
   * @returns Syc
   */
  getFanzoneSyc() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getFanzoneSyc();
    return this.wrappedObservable(data);
  }

  /**
   * to get Fanzone OptinEmail information
   * @returns Syc
   */
    getFanzoneOptinEmail() {
      this.globalLoaderService.showLoader();
      const data = this.apiClientService.fanzoneService().getFanzoneOptinEmail();
      return this.wrappedObservable(data);
    }

  getFanzoneComingBackDetails() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getFanzoneComingBackDetails();
    return this.wrappedObservable(data);
  }

  /**
    * to save or update the fanzone coming back details
    * @param method, fzComingBack, id
    * @returns IFanzoneComingBack
    */
  saveFanzoneComingBackData(method: string, fzComingBack: IFanzoneComingBack, id: string): Observable<HttpResponse<IFanzoneComingBack>> {
    const data = this.apiClientService.fanzoneService().saveFanzoneComingBackData(method, fzComingBack, id);
    return this.wrappedObservable(data);
  }
  
  /**
    * to save or update the fanzone Optin Email details
    * @param method, fzOptinEmail, id
    * @returns IFzOptinEmail
    */
  saveOptinEmail(method: string, fzOptinEmail: IFzOptinEmail, id: string): Observable<HttpResponse<IFzOptinEmail>> {
      const data = this.apiClientService.fanzoneService().saveOptinEmail(method, fzOptinEmail, id);
      return this.wrappedObservable(data);
    }
  

  getFanzoneNewSeasonDetails() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getFanzoneNewSeasonDetails();
    return this.wrappedObservable(data);
  }

  /**
    * to save or update the fanzone coming back details
    * @param method, fzComingBack, id
    * @returns IFanzoneComingBack
    */
  saveFanzoneNewSeasonData(method: string, fzComingBack: IFanzoneComingBack, id: string): Observable<HttpResponse<IFanzoneComingBack>> {
    const data = this.apiClientService.fanzoneService().saveFanzoneNewSeasonData(method, fzComingBack, id);
    return this.wrappedObservable(data);
  }

  /**
   * to get fanzone club
   * @param clubs
   * @returns void
   */
  getFanzoneClub(id: string): Observable<HttpResponse<any>> {
    const data = this.apiClientService.fanzoneService().getFanzoneClub(id);
    return this.wrappedObservable(data);
  }

  /**
   * to get all fanzone clubs
   * @param clubs
   * @returns void
   */
  getAllFanzoneClubs(): Observable<HttpResponse<any>> {
    const data = this.apiClientService.fanzoneService().getAllFanzoneClubs();
    return this.wrappedObservable(data);
  }

  /**
   * to save fanzone club
   * @param clubs
   * @returns void
   */
  saveFanzoneClub(clubs: ClubPromo): Observable<HttpResponse<any>> {
    const data = this.apiClientService.fanzoneService().saveFanzoneClub(clubs);
    return this.wrappedObservable(data);
  }

  /**
   * to update fanzone club
   * @param id, clubs
   * @returns void
   */
  updateFanzoneClub(id: string, clubs: ClubPromo): Observable<HttpResponse<any>> {
    const data = this.apiClientService.fanzoneService().updateFanzoneClub(id, clubs);
    return this.wrappedObservable(data);
  }

  /**
   * to delete fanzone club
   * @param id
   * @returns void
   */
  deleteFanzoneClub(id: string | string[]): Observable<HttpResponse<any>> {
    const data = this.apiClientService.fanzoneService().deleteFanzoneClub(id);
    return this.wrappedObservable(data);
  }

  /**
   * to get Fanzone Preferences
   * @returns Syc
   */
  getFanzonePreferences(): Observable<HttpResponse<FzPreferences>> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getFanzonePreferences();
    return this.wrappedObservable(data);
  }

  /**
   * to save Fanzone Notification Preferences
   * @returns Syc
   */
  saveFanzonePreferences(method: string, preferences: FzPreferences, id: string): Observable<HttpResponse<FzPreferences>> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().saveFanzonePreferences(method, preferences, id);
    return this.wrappedObservable(data);
  }

  /**
   * gets the Fanzone NewSignPosting information
   * @returns NewSignPosting
   */
  getNewSignPosting() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getNewSignPosting();
    return this.wrappedObservable(data);
  }

  /**
   * saves NewSignPosting information
   * @param method, newSignPosting, id
   * @returns NewSignPosting
   */
  saveNewSignPosting(method: string, newSignPosting: INewSignPosting, id: string): Observable<HttpResponse<INewSignPosting>> {
    const data = this.apiClientService.fanzoneService().saveNewSignPosting(method, newSignPosting, id);
    return this.wrappedObservable(data);
  }  

  /**
   * gets the Fanzone PopUp information
   * @returns PopUp
   */
  getNewGamingPopUp() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.fanzoneService().getNewGamingPopUp();
    return this.wrappedObservable(data);
  }

  /**
   * saves PopUp information
   * @param method, popUp, id
   * @returns PopUp
   */
  saveNewGamingPopUp(method: string, popUp: IPopUp, id: string): Observable<HttpResponse<IPopUp>> {
    const data = this.apiClientService.fanzoneService().saveNewGamingPopUp(method, popUp, id);
    return this.wrappedObservable(data);
  }  
}
