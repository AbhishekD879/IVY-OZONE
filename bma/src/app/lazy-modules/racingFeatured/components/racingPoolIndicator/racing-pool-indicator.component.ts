import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models/system-config';
import { IRacingPoolIndicator } from '@core/models/race-grid-meeting.model';

@Component({
  selector: 'racing-pool-indicator',
  templateUrl: 'racing-pool-indicator.component.html'
})
export class RacingPoolIndicatorComponent implements OnInit {

  @Input() events: ISportEvent[];
  @Input() emitEvent: boolean=false;
  @Output() overlayMenuClose = new EventEmitter<void>();
  uKToteEnabled: boolean = false;
  poolIndicators: IRacingPoolIndicator[];

  constructor(
    private gtmService: GtmService,
    private ukToteService: UkToteService,
    private cmsService: CmsService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
      const UKToteEnabled: boolean = config.TotePools && config.TotePools.Enable_UK_Totepools;
      if (UKToteEnabled) {
        this.uKToteEnabled = UKToteEnabled;
        this.poolIndicators = this.getPoolIndicators();
      }
    });
  }

  trackById(index: number, event: ISportEvent): string {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  /**
   * Go to event with pool and push to GTM
   * @param {string} path to go
   * @param {string} poolType to go
   */
  goToEvent(path: string, poolType: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'uk tote',
      eventAction: 'entry',
      eventLabel: poolType
    });
    if(this.emitEvent) {
      this.overlayMenuClose.emit();
    }
    this.router.navigateByUrl(path);
  }

  /**
   * Get pool indicators for landing page UK/IRE events
   * @return {array} array of pool indicators
   */
  private getPoolIndicators(): IRacingPoolIndicator[] {
    return this.ukToteService.getPoolIndicators(this.events);
  }
}
