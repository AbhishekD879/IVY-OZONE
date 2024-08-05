import { IAccountFreebetsResponse } from '@bpp/services/bppProviders/bpp-providers.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { of, Observable, forkJoin, from, throwError } from 'rxjs';
import { map, catchError, take, switchMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { ExistNewUserService } from '@core/services/existNewUser/exist-new-user.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';

import { PromotionDialogComponent } from '@promotionsModule/components/promotionDialog/promotion-dialog.component';
import { PromotionOverlayDialogComponent } from '@promotions/components/promotionOverlayDialog/promotion-overlay-dialog.component';

import { TAG_NAMES_CONFIG } from '@promotions/constants/tag-names-config.constant';
import { CONNECT_PROMOTION_CATEGORY_ID } from '@core/services/cms/cms.constants';

import { IPromotionsSiteCoreBanner, ISpPromotion } from '@promotions/models/sp-promotion.model';
import { ICheckStatusResponse, IOffersWithPromotions } from '@promotions/models/response.model';
import { IPromotionSection, IPromotionsList, ISystemConfig } from '@core/services/cms/models';
import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import { IOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { DeviceService } from '@core/services/device/device.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { ISiteCoreTeaserFromServer, ItermsAndConditionsLink } from '@core/models/aem-banners-section.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
@Injectable({
  providedIn: 'root'
})
export class PromotionsService {

  readonly ITEMIDREGEXP: RegExp = /^[{]?[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}[}]?$/ ;
  readonly PATH: string = 'content/teasers?path=promotion';
  readonly HREFPROP: string = 'href';
  readonly TARGETPROP: string = 'target';
  // Signposting Promotions
  private spPromotionData = {};
  private offers: IOffer[];
  private AUTH_ERROR_CODE: number = 401;

  constructor(
    protected http: HttpClient,
    protected domSanitizer: DomSanitizer,
    protected userService: UserService,
    protected existNewUserService: ExistNewUserService,
    protected cmsService: CmsService,
    protected dialogService: DialogService,
    protected gtmService: GtmService,
    protected casinoLinkService: CasinoLinkService,
    protected filtersService: FiltersService,
    protected domToolsService: DomToolsService,
    protected rendererService: RendererService,
    protected bppService: BppService,
    protected commandService: CommandService,
    protected windowRefService: WindowRefService,
    protected device: DeviceService,
    protected infoDialog: InfoDialogService,
    protected awsService: AWSFirehoseService,
    protected vanillaApiService: VanillaApiService,
  ) {
    this.sendGTM = this.sendGTM.bind(this);
    this.commandService.register(this.commandService.API.PROMOTIONS_SHOW_OVERLAY, (flag: string) => this.openPromotionOverlay(flag));
  }

  /**
   * Changing button text.
   * @param  {String} message - button message.
   * @param  {Object} btn - element button.
   */
  changeBtnLabel(message: string, btn: HTMLElement): void {
    const label = btn.querySelector('.btn-label');
    label.textContent = message;

    const statusInfo = btn.querySelector('.btn-status-info');
    this.domToolsService.removeClass(statusInfo, 'btn-spinner');
    this.domToolsService.addClass(statusInfo, 'checked');
  }

  /**
   * Checking if user already opted In.
   * @param  {Number} requestId - Opt In id.
   * @return {Object} observable.
   */
  checkStatus(requestId: string): Observable<ICheckStatusResponse | HttpResponse<ICheckStatusResponse>> {
    return this.checkOptInStatus(requestId, this.userService.username, this.userService.bppToken).pipe(
      map((response: HttpResponse<ICheckStatusResponse>) => {
        const result = response.body;
        this.awsService.addAction('GetPromoOptInSuccess', { result, triggerId: requestId });
        return result;
      }),
      catchError((error: ICheckStatusResponse): Observable<ICheckStatusResponse> | Observable<HttpResponse<ICheckStatusResponse>> => {
        this.awsService.addAction('GetPromoOptInError', { error, triggerId: requestId });
        return this.isAuthError(error) ?
        from(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE))
          .pipe(switchMap((): Observable<HttpResponse<ICheckStatusResponse>> => {
              return this.checkOptInStatus(requestId, this.userService.username, this.userService.bppToken);
            })) :
          throwError(error);
      }),
      take(1)
    );
  }

  /**
   * Save Opt In for user.
   * @param  {Number} requestId - Opt In id.
   * @return {Object} observable.
   */
  storeId(requestId: string): Observable<ICheckStatusResponse> {
    return this.storeOptInId(
      requestId, this.userService.username, this.userService.bppToken
    ).pipe(
      map((result: ICheckStatusResponse) => {
        this.awsService.addAction('UpdatePromoOptInSuccess', { result, triggerId: requestId });
        return result;
      }),
      catchError((error: ICheckStatusResponse): Observable<ICheckStatusResponse> => {
        this.awsService.addAction('UpdatePromoOptInError', { error, triggerId: requestId });
        return this.isAuthError(error) ?
          from(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE))
            .pipe(switchMap((): Observable<ICheckStatusResponse> => {
              return this.storeOptInId(requestId, this.userService.username, this.userService.bppToken);
            })) :
            throwError(error);
      })
    );
  }

  isUserLoggedIn(): boolean {
    return !!this.userService.username;
  }

  /**
   * Enables button by adding handler and adding css styles
   * @param button
   * @param handlerFn
   */
  enableOptInButton(button: HTMLElement, handlerFn: (event: any) => void): Function {
    const statusInfo = button.querySelector('.btn-status-info');
    this.domToolsService.removeClass(statusInfo, 'btn-spinner');

    this.domToolsService.removeClass(button, 'disabled');
    return this.rendererService.renderer.listen(button, 'click', handlerFn);
  }

  /**
   * Disables button by removing handler and adding css styles
   * @param button
   * @param optInButtonListeners remove listener functions (returned by renderer2.listen)
   */
  disableOptInButton(button: HTMLElement, optInButtonListeners: Function[]): void {
    const statusInfo = button.querySelector('.btn-status-info');
    this.domToolsService.addClass(statusInfo, 'btn-spinner');

    this.domToolsService.addClass(button, 'disabled');
    _.each(optInButtonListeners, removeEventListener => {
      removeEventListener();
    });
  }

  /**
   * Get Signposting Promotions
   * @param {boolean} isLight - get light version or all fields
   * @returns {Observable}
   */
  getSpPromotionData(isLight: boolean = true): Observable<ISpPromotion[]> {
    const prop = isLight ? 'light' : 'all';

    const spPromotionData = this.spPromotionData;

    if (spPromotionData[prop]) {
      return of(
        this._filterPromotionsByVipLevel(spPromotionData[prop])
      );
    }
 if(isLight) {
    return this.cmsService.getSignpostingPromotionsLight().pipe(
      map(response => {
        const data = response.promotions;

        spPromotionData[prop] = _.map(data,
          (item: any) => _.extend(item, _.find(TAG_NAMES_CONFIG,
            ci => item.marketLevelFlag === ci.marketFlag || item.eventLevelFlag === ci.eventFlag || (ci.marketName && ci.marketName.includes(item.templateMarketName)))));
        return this._filterPromotionsByVipLevel(spPromotionData[prop]);
      }));
    } else {
        return this.cmsService.getAllPromotions().pipe(
          map(response => {
            const data =  _.filter(response.promotions, (item: any) => item.isSignpostingPromotion);
            spPromotionData[prop] = _.map(data,
              (item: any) => _.extend(item, _.find(TAG_NAMES_CONFIG,
                ci => item.marketLevelFlag === ci.marketFlag || item.eventLevelFlag === ci.eventFlag || (ci.marketName && ci.marketName.includes(item.templateMarketName)))));
            return this._filterPromotionsByVipLevel(spPromotionData[prop]);
        }));
    }
  }

  /**
   * Open promotion overlay
   */
  openPromotionOverlay(flag: string): void {
    if (!flag) {
      return;
    }

    this.getSpPromotionData().subscribe(promotions => {
      if (
        _.find(promotions, p => flag === p.templateMarketName || flag === p.marketLevelFlag || flag === p.eventLevelFlag)
      ) {
        const dialogParams = {
          flag,
          getSpPromotionData: isLight => this.getSpPromotionData(isLight),
          decorateLinkAndTrust: data => this.decorateLinkAndTrust(data)
        };

        this.dialogService.openDialog(
          DialogService.API.promotionOverlayDialog,
          PromotionOverlayDialogComponent,
          true,
          dialogParams
        );
      }
    });
  }

  /**
   * Open promotion dialog
   */
  openPromotionDialog(flag: string): void {
    if (!flag) { return; }

    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
      return;
    }

    this.getSpPromotionData().subscribe(promotions => {
      if (!_.find(promotions, p => flag === p.templateMarketName || flag === p.marketLevelFlag || flag === p.eventLevelFlag)) { return; }

      const dialogParams = {
        flag,
        getSpPromotionData: isLight => this.getSpPromotionData(isLight),
        openPromotionOverlay: () => this.openPromotionOverlay(flag),
        onBeforeClose: () => {
          this.windowRefService.document.body.classList.remove('promotion-modal-open');
        }
      };

      this.dialogService.openDialog(
        DialogService.API.promotionDialog,
        PromotionDialogComponent,
        true,
        dialogParams,
      );
    });
  }

  /**
   * Decorate casino link in html and trust as html
   */
  decorateLinkAndTrust(data: string): SafeHtml {
    const html = this.casinoLinkService.decorateCasinoLinkInHtml(data).replace(/href="(?!https:)/g, 'data-routerlink="');
    return this.domSanitizer.bypassSecurityTrustHtml(html);
  }

  /**
   * Inserting sitecore promotions into promotionArray based on the ItemId
   * @param promotionArray
   * @param sitecorePromotions
   */
  preparePromotions(promotionArray: ISpPromotion[], sitecorePromotions: ISiteCoreTeaserFromServer[]): ISpPromotion[] {
    const showsitecorePromotions = sitecorePromotions && sitecorePromotions.length === 0;
    const promotions = _.map(promotionArray, promotion => {
      if(promotion.useDirectFileUrl && showsitecorePromotions && !((this.ITEMIDREGEXP).test(promotion.directFileUrl))) {
        promotion.uriMedium = promotion.directFileUrl;
      } else if (sitecorePromotions && sitecorePromotions.length > 0) {
       sitecorePromotions.forEach((promoBanner:ISiteCoreTeaserFromServer) => {
        if (promotion.useDirectFileUrl && promotion.directFileUrl === promoBanner.itemId) {
          promotion.sitecoreBanner = promoBanner;
          promotion.showsitecoreBanner = true;
        } else if (promotion.useDirectFileUrl && !((this.ITEMIDREGEXP).test(promotion.directFileUrl))) {
          promotion.uriMedium = promotion.directFileUrl;
        }
      });
    }
    return promotion;
    });

    return Array.from(
      _.each(this.existNewUserService.filterExistNewUserItems(promotions as any[]), promotion => {
        promotion.targetUri = this.filtersService.filterLink(`promotions/details/${promotion.promoKey}`);
      })
    );
  }

  filterByOfferId(promotions: ISpPromotion[]): ISpPromotion[] {
    const freeBetOfferIDs = _.map(this.offers, (offer: IOffer) => offer.freebetOfferId);

    return _.filter(promotions, (promotion: ISpPromotion) => {
      return promotion.openBetId ? this.isUserLoggedIn() && freeBetOfferIDs.length &&
        freeBetOfferIDs.indexOf(promotion.openBetId) > -1 : true;
    });
  }

  sendGTM(promotion: ISpPromotion, info: any, isInternalButton: boolean) {
    this.gtmService.push('trackEvent', {
      eventCategory: 'promotions',
      vipLevel: this.userService.vipLevel || '',
      eventAction: isInternalButton ? 'link click' : 'cta click',
      eventLabel: promotion.title,
      promoAction: !isInternalButton || _.contains(info.target.classList, 'btn') ? info.target.text : info.target.dataset.routerlink
    });
  }

  /**
   * GA for tracking showBogDialog
   */
  trackBogDialog( eventMarket: string, eventLabel: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'promotions',
      eventMarket: eventMarket,
      eventAction: 'Best Odds Guaranteed',
      eventLabel: eventLabel,
    });
  }

  /**
   * Retrieves list of all digital promotions from cms
   * @return {object}
   */
  promotionsDigitalData(): Observable<IPromotionsList | null> {
    return forkJoin(this.doRequest(false)).pipe(map((result: any) => {
      const res: IPromotionsList = this.getPromotions(result);
      if (res) {
        res.promotions = res.promotions.filter(
          promotion => (promotion.categoryId && (promotion.categoryId.length !== 1 || (promotion.categoryId.length === 1
            && promotion.categoryId[0] !== CONNECT_PROMOTION_CATEGORY_ID))) || !promotion.categoryId);
      }
      return res || null;
    }));
  }

  promotionsGroupedData(): Observable<IPromotionsList> {
    return forkJoin(this.doRequest()).pipe(map((result: any) => {
      const res = this.getPromotions(result);
      res.promotionsBySection = _.sortBy(res.promotionsBySection, (section: IPromotionSection) => section.sortOrder);
      _.each(res.promotionsBySection, (section: IPromotionSection) => {
        section.unassigned = section.name === 'Unassigned promotions';
        section.promotions = _.filter(section.promotions, (promo: IPromotion) => {
          return !_.isEqual(promo.categoryId, [CONNECT_PROMOTION_CATEGORY_ID]);
        });
      });
      return res;
    }));
  }

  /**
   * Retrieves list of Connect promotions from cms
   * @return {object}
   */
  promotionsRetailData(): Observable<IPromotionsList | null> {
    return this.cmsService.getRetailPromotions();
  }

  /**
   * Retrieves list of promotions from sitecore
   *  @return {Observable<IPromotionsSiteCoreBanner>}
   */
  getPromotionsFromSiteCore(): Observable<IPromotionsSiteCoreBanner[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(this.PATH,'', APIOPTIONS);
  }

  /**
   * Retrieves promotion by promoKey from cms
   * @param {string} promoKey
   * @return {object}
   */
  promotionData(promoKey: string): Observable<IPromotion | null> {
    return this.cmsService.getAllPromotions().pipe(
      map((result: IPromotionsList) => {
        return (result && _.findWhere(result.promotions, { promoKey })) || null;
      }));
  }

  isGroupBySectionsEnabled(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(
      map((res: ISystemConfig) => {
        return !!(res.Promotions && res.Promotions.groupBySections);
      })
    );
  }
  /**
   * checking for isempty values
   * @return string
   */
  isEmptyPromotionValue(bannerLink: ItermsAndConditionsLink, tcLink: ItermsAndConditionsLink | string | any,  prop: string): string {
    if(prop === this.HREFPROP) {
      return tcLink ? tcLink.url: (bannerLink? bannerLink.url : '');
    } else if(prop === this.TARGETPROP) {
      return tcLink ? tcLink.attributes.target: (bannerLink? bannerLink.attributes.target : '');
    }
  }
 
  protected getPromotions(result: IOffersWithPromotions): IPromotionsList {
    this.offers = result.length > 1 ? (result[0] as IAccountFreebetsResponse).response.model.freebetOffer : [];
    return (result.length > 1 ? result[1] : result[0]) as IPromotionsList;
  }

  protected doRequest(isGroupped: boolean =  true): Observable<IOffersWithPromotions>[] {
    const requests = [];
    if (this.isUserLoggedIn()) {
      requests.push(this.bppService.send('accountOffers', null));
    }

    requests.push(isGroupped ? this.cmsService.getGroupedPromotions() : this.cmsService.getAllPromotions());
    return requests;
  }
  private checkOptInStatus<T>(requestId: string, userName: string, sessionToken: string): Observable<HttpResponse<T>> {
    const endpointUrl = `${environment.OPT_IN_ENDPOINT}/api/trigger/${requestId}`;

    return this.http.get<T>(endpointUrl, {
      observe: 'response',
      headers: { user: userName, token: sessionToken }
    });
  }

  private storeOptInId(requestId: string, userName: string, sessionToken: string): Observable<ICheckStatusResponse> {
    const endpointUrl = `${environment.OPT_IN_ENDPOINT}/api/trigger/`;

    return this.http.put<ICheckStatusResponse>(
      endpointUrl,
      { trigger_id: requestId },
      {
        headers: { user: userName, token: sessionToken }
      });
  }

  private isAuthError(response: ICheckStatusResponse): boolean {
    return response.error.code === this.AUTH_ERROR_CODE;
  }

  /**
   * Filter promotions by vip level
   */
  private _filterPromotionsByVipLevel(promotions: ISpPromotion[]): ISpPromotion[] {
    return this.existNewUserService.filterExistNewUserItems(promotions, false);
  }
  /**
   * gtm tracking for signPosting
   * @param title eventAction
   * @param iconFlag eventMarket
   * @param marketLevelFlag marketLevelFlag
   */
  trackSignPosting(title: string, iconFlag: string, marketLevelFlag: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'promotions',
      eventAction: title,
      eventLabel: 'ok',
      eventMarket: marketLevelFlag || iconFlag
    });
  }
}
