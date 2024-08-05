import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { ClubPromo, Fanzone, FzPreferences, IFanzoneComingBack, IFanzoneNewSeason, IFzOptinEmail, INewSignPosting, Syc, IPopUp } from '@app/client/private/models/fanzone.model';

@Injectable()
export class FanzoneService extends AbstractService<Fanzone[]> {
  sycUri: string;
  fz_preference_url: string;
  fz_coming_back_url: string;
  fz_new_season_url: string;
  fz_email_optin_url: string;
  newSignPostingUri: string;
  popUpUri: string;
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `${brand}/fanzone`;
    this.sycUri = `${brand}/fanzone-syc`;
    this.fz_preference_url = `${brand}/fanzone-preference-center`;
    this.fz_coming_back_url = `${brand}/fanzone-coming-back`;
    this.fz_new_season_url = `${brand}/fanzone-new-season`;
    this.fz_email_optin_url = `${brand}/fanzones/fanzone-optin-email`;
    this.newSignPostingUri = `${brand}/fanzone-new-signposting`;
    this.popUpUri = `${brand}/fanzone-new-gaming-pop-up`;
  }

  /**
   * creates the Fanzone
   * @param fanzone  { Fanzone }
   * @returns { HttpResponse<Fanzone> }
   */
  public createFanzone(fanzone: Fanzone): Observable<HttpResponse<Fanzone>> {
    return this.sendRequest<Fanzone>('post', this.uri, fanzone);
  }

  /**
   * gets all the Fanzones
   * @returns { HttpResponse<Fanzone[]> }
   */
  public getAllFanzones(): Observable<HttpResponse<Fanzone[]>> {
    return this.sendRequest<Fanzone[]>('get', `${this.uri}`, null);
  }

  /**
   * gets the Fanzone data based on ID
   * @param id  { id }
   * @returns { HttpResponse<Fanzone> }
   */
  public getFanzoneDetails(id: string): Observable<HttpResponse<Fanzone>> {
    return this.sendRequest<Fanzone>('get', `${this.uri}/id/${id}`, null);
  }

  /**
   * udpates the Fanzone data based on ID
   * @param id, fanzone  { id, fanzone }
   * @returns { HttpResponse<Fanzone> }
   */
  public updateFanzoneDetails(id: string, fanzone: Fanzone): Observable<HttpResponse<Fanzone[]>> {
    return this.sendRequest<Fanzone[]>('put', `${this.uri}/id/${id}`, fanzone);
  }

  /**
   * deletes the Fanzones based on ID's
   * @param id  { id }
   * @returns { HttpResponse<Fanzone> }
   */
  public deleteFanzone(id: string | string[]): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.uri}/id/${id}`, null);
  }

  /**
   * gets all the Fanzone clubs
   * @returns { HttpResponse<Fanzone[]> }
   */
  public getAllFanzoneClubs(): Observable<HttpResponse<ClubPromo[]>> {
    return this.sendRequest<ClubPromo[]>('get', `${this.uri}-club`, null);
  }

  /**
   * to get fanzone club
   * @param id
   * @returns { HttpResponse<Fanzone> }
   */
  public getFanzoneClub(id: string): Observable<HttpResponse<any>> {
    return this.sendRequest<ClubPromo>('get', `${this.uri}-club/id/${id}`, null);
  }

  /**
   * to save fanzone club
   * @param club
   * @returns { HttpResponse<Fanzone> }
   */
  public saveFanzoneClub(club: ClubPromo): Observable<HttpResponse<any>> {
    return this.sendRequest<ClubPromo>('post', `${this.uri}-club`, club);
  }

  /**
   * to update fanzone club
   * @param id, club
   * @returns { HttpResponse<Fanzone> }
   */
  public updateFanzoneClub(id: string, club: ClubPromo): Observable<HttpResponse<any>> {
    return this.sendRequest<ClubPromo>('put', `${this.uri}-club/id/${id}`, club);
  }

  /**
   * to delete fanzone club
   * @param id, club
   * @returns { HttpResponse<Fanzone> }
   */
  public deleteFanzoneClub(id: string | string[]): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.uri}-club/id/${id}`, null);
  }

  /**
   * saves fanzone show your colors information
   * @param method, syc, id  { method, syc, id }
   * @returns { HttpResponse<Syc> }
   */
  public saveFanzoneSyc(method: string, syc: any, id: string): Observable<HttpResponse<Syc>> {
    const url = id ? `${this.sycUri}/id/${id}` : `${this.sycUri}`;
    return this.sendRequest<Syc>(method, url, syc);
  }

  /**
   * gets the Fanzone show your colors information
   * @returns { HttpResponse<Syc> }
   */
  public getFanzoneSyc(): Observable<HttpResponse<Syc>> {
    return this.sendRequest<Syc>('get', `${this.sycUri}`, null);
  }

    /**
   * gets the Fanzone OptinEmail information
   * @returns { HttpResponse<IFzOptinEmail> }
   */
    public getFanzoneOptinEmail(): Observable<HttpResponse<IFzOptinEmail>> {
      return this.sendRequest<IFzOptinEmail>('get', `${this.fz_email_optin_url}`, null);
    }
  

  /**
   * gets the Fanzone coming back information
   * @returns { HttpResponse<IFanzoneComingBack> }
   */
  public getFanzoneComingBackDetails(): Observable<HttpResponse<IFanzoneComingBack>> {
    return this.sendRequest<IFanzoneComingBack>('get', `${this.fz_coming_back_url}`, null);
  }

  /**
   * saves fanzone coming back information
   * @param method, fzComingBack, id  { method, fzComingBack, id }
   * @returns { HttpResponse<IFanzoneComingBack> }
   */
  public saveFanzoneComingBackData(method: string, fzComingBack: any, id: string): Observable<HttpResponse<IFanzoneComingBack>> {
    const url = id ? `${this.fz_coming_back_url}/id/${id}` :`${this.fz_coming_back_url}`;
    return this.sendRequest<IFanzoneComingBack>(method, url, fzComingBack);
  }

    /**
   * saves fanzone coming back information
   * @param method, fzComingBack, id  { method, fzComingBack, id }
   * @returns { HttpResponse<IFanzoneComingBack> }
   */
    public saveOptinEmail(method: string, fzOptinEmail: any, id: string): Observable<HttpResponse<IFzOptinEmail>> {
      const url = id ? `${this.fz_email_optin_url}/${id}` :`${this.fz_email_optin_url}`;
      return this.sendRequest<IFzOptinEmail>(method, url, fzOptinEmail);
    }

  /**
   * gets the Fanzone new season information
   * @returns { HttpResponse<IFanzoneNewSeason> }
   */
  public getFanzoneNewSeasonDetails(): Observable<HttpResponse<IFanzoneNewSeason>> {
    return this.sendRequest<IFanzoneNewSeason>('get', `${this.fz_new_season_url}`, null);
  }
  
  /**
   * saves fanzone new season information
   * @param method, fzNewSeason, id  { method, fzNewSeason, id }
   * @returns { HttpResponse<IFanzoneNewSeason> }
   */
  public saveFanzoneNewSeasonData(method: string, fzNewSeason: any, id: string): Observable<HttpResponse<IFanzoneNewSeason>> {
    const url = id ? `${this.fz_new_season_url}/id/${id}` : `${this.fz_new_season_url}`;
    return this.sendRequest<IFanzoneNewSeason>(method, url, fzNewSeason);
  }

  /**
   * gets the Fanzone Preferences
   * @returns { HttpResponse<FzPreferences> }
   */
  public getFanzonePreferences(): Observable<HttpResponse<FzPreferences>> {
    return this.sendRequest<FzPreferences>('get', `${this.fz_preference_url}`, null);
  }

  /**
   * saves the Fanzone Preferences
   * @returns { HttpResponse<FzPreferences> }
   */
  public saveFanzonePreferences(method: string, sycPreferences: any, id: string): Observable<HttpResponse<FzPreferences>> {
    const url = id ? `${this.fz_preference_url}/id/${id}` : `${this.fz_preference_url}`;
    return this.sendRequest<FzPreferences>(method, url, sycPreferences);
  }

  /**
   * gets the Fanzone NewSignPosting information
   * @returns { HttpResponse<NewSignPosting> }
   */
  public getNewSignPosting(): Observable<HttpResponse<Syc>> {
    return this.sendRequest<INewSignPosting>('get', `${this.newSignPostingUri}`, null);
  }

  /**
   * saves NewSignPosting information
   * @param method, newSignPosting, id  { method, newSignPosting, id }
   * @returns { HttpResponse<NewSignPosting> }
   */
  public saveNewSignPosting(method: string, newSignPosting: INewSignPosting, id: string): Observable<HttpResponse<INewSignPosting>> {
    const url = id ? `${this.newSignPostingUri}/id/${id}` : `${this.newSignPostingUri}`;
    return this.sendRequest<INewSignPosting>(method, url, newSignPosting);
  }

  /**
   * gets the Fanzone PopUp information
   * @returns { HttpResponse<PopUp> }
   */
  public getNewGamingPopUp(): Observable<HttpResponse<IPopUp>> {
    return this.sendRequest<IPopUp>('get', `${this.popUpUri}`, null);
  }

  /**
   * saves PopUp information
   * @param method, popUp, id  { method, popUp, id }
   * @returns { HttpResponse<PopUp> }
   */
  public saveNewGamingPopUp(method: string, popUp: IPopUp, id: string): Observable<HttpResponse<IPopUp>> {
    const url = id ? `${this.popUpUri}/id/${id}` : `${this.popUpUri}`;
    return this.sendRequest<IPopUp>(method, url, popUp);
  }
}
