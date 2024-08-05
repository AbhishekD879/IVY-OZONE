import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { Observable } from 'rxjs';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import environment from '@environment/oxygenEnvConfig';
import { map } from 'rxjs/operators';
import { BannerModel, BetPackLabels, BetPackModel, FilterModel } from '@app/betpackReview/components/betpack-review.model';
import { BetPackOnBoardingCMSConfig } from '@app/lazy-modules/betpackOnboarding/models/betpack-onboarding.model';
import { IAccGetLimitsResponse, IBppResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { KycStatusService } from '@frontend/vanilla/shared/kyc';

@Injectable({
  providedIn: 'root'
})

export class BetpackCmsService {
  cmsUri: string = environment.CMS_ROOT_URI;
  CMS_ENDPOINT: string;
  brand: string = environment.brand;
  sliderBackgroundImg: string;
  currentActiveBP: BetPackModel;
  disableBuyBtn: boolean;
  getLimitsData: number;
  getFreeBets: IFreebetToken[];
  betpackLabels: BetPackLabels;
  enableBetPack: boolean = false;
  isLoaded: boolean = false;
  socketStorage = new Map();
  userloginLoaded: boolean;
  kycVerified: boolean = true;
  verificationStatus: string = '';

  constructor(
    private bppService: BppService,
    protected http: HttpClient,
    private pubSubService: PubSubService,
    private kycService: KycStatusService
  ) {
    this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
    this.getCmsBetPackLabels();
    this.pubSubService.subscribe('BetPackCMS-Login', [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.APP_IS_LOADED, this.pubSubService.API.RELOAD_COMPONENTS], () => {
      this.kycService.kycStatus.subscribe(val => {
        if (val) {
          this.kycVerified = val.kycVerified; //// kyc flags
          this.verificationStatus = val.verificationStatus;
        }
      });
    });
    ////Free bets one user logged in
    this.pubSubService.subscribe('', 'FREEBET_UPDATE_LOGIN', (data: IFreebetToken[]) => {
      this.getFreeBets = data;
    });
  }

  /**
   * @param  {string} url
   * @param  {any={}} params
   * @returns Observable
   */
  getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }
  //Betpack details
  /**
   * @returns Observable
   */
  getBetPackDetails(): Observable<BetPackModel[]> {
    return this.getData(`bet-pack`)
      .pipe(
        map((data: HttpResponse<BetPackModel[]>) => data.body
        )
      );
  }
  //Betpack Labels
  /**
   * @returns Observable
   */
  getBetPackLabels(): Observable<BetPackLabels> {
    return this.getData(`bet-pack/label`)
      .pipe(
        map((data: HttpResponse<BetPackLabels>) => data.body
        )
      );
  }
  //Betpack Filters
  /**
   * @returns Observable
   */
  getBetPackFilters(): Observable<FilterModel[]> {
    return this.getData(`bet-pack/filter`)
      .pipe(
        map((data: HttpResponse<FilterModel[]>) => data.body
        )
      );
  }
  //Betpack banners
  /**
   * @returns Observable
   */
  getBetPackBanners(): Observable<BannerModel> {
    return this.getData(`bet-pack/banner`)
      .pipe(
        map((data: HttpResponse<BannerModel>) => data.body
        )
      );
  }
  //Betpack Onboarding
  /**
   * @returns Observable
   */
  getBetPackOnboarding(): Observable<any> {
    return this.getData(`bet-pack/onboarding`)
      .pipe(
        map((data: HttpResponse<BetPackOnBoardingCMSConfig>) => data.body)
      );
  }
  /**
   * @returns Observable
   */
  getAccountLevelLimits(): Observable<IBppResponse> {
    return this.bppService.send('accountGetLimits')
      .pipe(
        map((res: IAccGetLimitsResponse) => res));
  }
  /**
   * @returns void
   */
  private getCmsBetPackLabels(): void {
    this.getBetPackLabels().subscribe((data: BetPackLabels) => {
      this.betpackLabels = data;
      if (this.betpackLabels.backgroundImage) {
        this.sliderBackgroundImg = `${this.cmsUri}${this.betpackLabels.backgroundImage.path}/${this.betpackLabels.backgroundImage.filename}`;
      }
      this.isLoaded = true;
    });
  }
}
