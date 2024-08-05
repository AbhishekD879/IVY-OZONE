import { Observable, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { GRID_PROMOTION_CATEGORY_ID } from '@ladbrokesMobile/core/services/cms/cms.constants';
import { PromotionsService as OxygenpromotionsService } from '@promotions/services/promotions/promotions.service';
import { IPromotionSection, IPromotionsList } from '@core/services/cms/models';
import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import * as _ from 'underscore';
import { HttpClient } from '@angular/common/http';
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
import { DomSanitizer } from '@angular/platform-browser';
import { CommandService } from '@core/services/communication/command/command.service';
import { DeviceService } from '@core/services/device/device.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { LocaleService } from '@coreModule/services/locale/locale.service';

@Injectable({
  providedIn: 'root'
})
export class PromotionsService extends OxygenpromotionsService {


  constructor( protected http: HttpClient,
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
    protected localeService: LocaleService) {
    super(http, domSanitizer, userService, existNewUserService,cmsService, dialogService, gtmService,
      casinoLinkService, filtersService, domToolsService, rendererService, bppService, commandService, windowRefService,
      device, infoDialog, awsService, vanillaApiService);
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
            && promotion.categoryId[0] !== GRID_PROMOTION_CATEGORY_ID))) || !promotion.categoryId);
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
          return !_.isEqual(promo.categoryId, [GRID_PROMOTION_CATEGORY_ID]);
        });
      });
      return res;
    }));
  }
}
