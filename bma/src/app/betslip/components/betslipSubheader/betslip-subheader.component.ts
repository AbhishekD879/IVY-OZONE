import { Component, Output, EventEmitter, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef, Input } from '@angular/core';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BetslipService } from '@betslipModule/services/betslip/betslip.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'betslip-subheader',
  templateUrl: './betslip-subheader.component.html',
  styleUrls: ['./betslip-subheader.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipSubheaderComponent implements OnInit, OnDestroy {
  @Output() readonly clear = new EventEmitter();
  @Output() readonly remove = new EventEmitter();
  @Input() suspendedOutcomesCounter: number;
  public isMobile: boolean = environment.CURRENT_PLATFORM === 'mobile';
  public isCoralMobile:boolean;

  count: number;

  constructor(
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private pubSubService: PubSubService,
    private betSlipService: BetslipService,
    private gtmService: GtmService,
    public serviceClosureService: ServiceClosureService,
    private changeDetection:ChangeDetectorRef
  ) {
    this.isCoralMobile = environment && environment.brand === 'bma' && this.isMobile;
  }

  ngOnInit(): void {
    this.count = this.betSlipService.count();
    this.serviceClosureService.updateClosureFlag();
    this.pubSubService.subscribe(
      'BetslipSubheaderComponent',
      this.pubSubService.API.BETSLIP_COUNTER_UPDATE,
      (count: number) => {
      this.count = count;
      this.changeDetection.detectChanges();
      }
    );
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('BetslipSubheaderComponent');
  }

  /**
   * @memberof BetslipSubheaderComponent
   */
  removeSuspended(): void {
    this.remove.emit();
  }

  showConfirm(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('bs.clearBetslipTitle'),
      this.localeService.getString('bs.confirmClearOfBetSlip'),
      'bs-clear-dialog', undefined, undefined,
      [{
        cssClass: 'btn-style4',
        caption: this.localeService.getString('bs.clearBetslipCancel'),
      }, {
        caption: this.localeService.getString('bs.clearBetslipContinue'),
        cssClass: 'btn-style2',
        handler: () => {
          this.betSlipService.closeNativeBetslipAndWaitAnimation(() => {
            this.clear.emit();
            this.infoDialogService.closePopUp();

            this.gtmService.push('trackEvent', {
              eventAction: 'trackEvent',
              eventCategory: 'betslip',
              eventLabel: 'clear betslip click'
            });
          });
        }
      }]
    );
  }
}
