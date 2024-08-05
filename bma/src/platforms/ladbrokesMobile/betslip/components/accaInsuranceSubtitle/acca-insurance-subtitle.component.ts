import { Component, OnInit, OnDestroy, Input, Output, EventEmitter, SecurityContext, ViewEncapsulation } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

import { Bet } from '@betslip/services/bet/bet';
import { IStaticBlock } from '@core/services/cms/models';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { AccaService } from '@betslip/services/acca/acca.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IConstant } from '@core/services/models/constant.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'acca-insurance-subtitle',
  templateUrl: './acca-insurance-subtitle.component.html',
  styleUrls: ['./acca-insurance-subtitle.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class AccaInsuranceSubtitleComponent implements OnInit, OnDestroy {

  @Input() bet: Bet;
  @Output() readonly passMessageConfigFn: EventEmitter<IConstant> = new EventEmitter();

  staticBlockContent: string = '';
  isAccaInsurance: boolean;

  constructor(private cmsService: CmsService,
              private domSanitizer: DomSanitizer,
              private accaService: AccaService,
              private localeService: LocaleService,
              private pubSubService: PubSubService) {
    this.passMessageConfig = this.passMessageConfig.bind(this);
  }

  ngOnInit(): void {
    this.isAccaInsurance = this.accaService.isAccaInsuranceEligible(this.bet);

    if (this.isAccaInsurance) {
      const offerTriggerMaxBonus = this.accaService.getAccaOfferMaxBonus(this.bet);

      this.cmsService.getStaticBlock('acca-insurance-content')
        .subscribe((cmsContent: IStaticBlock) => {
          this.staticBlockContent =
            this.domSanitizer.sanitize(SecurityContext.HTML, this.domSanitizer.bypassSecurityTrustHtml(cmsContent.htmlMarkup));
          this.staticBlockContent = this.cmsService.parseContent(this.staticBlockContent as string, [offerTriggerMaxBonus]);
        });
    }

    this.passMessageConfig();

    this.pubSubService.subscribe('AccaInsuranceSubtitleComponent',
      this.pubSubService.API['show-slide-out-betslip-true'], this.passMessageConfig);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('AccaInsuranceSubtitleComponent');
  }

  /**
   * Emit message config to show overlay message in betslip
   */
  passMessageConfig(): void {
    const overlayMsgConfig: IConstant = { message: '', type: 'ACCA' };

    if (this.isAccaInsurance) {
      overlayMsgConfig.message = this.localeService.getString('bs.accaInsuranceQualifyMsg');
    } else  if (this.accaService.isAccaInsuranceSuggested(this.bet)) {
      overlayMsgConfig.message = this.localeService.getString('bs.accaInsuranceAddOneMoreMsg');
    }

    if (overlayMsgConfig.message) {
      this.passMessageConfigFn.emit(overlayMsgConfig);
    }
  }

  /**
   * Open Acca Insurance Info Dialog
   */
  openAccaInsuranceInfoDialog(): void {
   this.accaService.accaInsurancePopup(this.staticBlockContent);
  }
}
