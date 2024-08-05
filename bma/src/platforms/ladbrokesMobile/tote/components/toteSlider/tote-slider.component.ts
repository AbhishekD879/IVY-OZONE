import { Component, Input } from '@angular/core';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { ToteService } from '@app/tote/services/mainTote/main-tote.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { Router } from '@angular/router';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { TempStorageService } from '@core/services/storage/temp-storage.service';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
@Component({
  selector: 'tote-slider',
  styleUrls: ['tote-slider.component.scss'],
  templateUrl: 'tote-slider.component.html'
})
export class LadbrokesToteSliderComponent extends ToteSliderComponent {
  @Input() sectionTitle?: string;

  constructor(
    protected toteService: ToteService,
    protected gtmService: GtmService,
    protected router: Router,
    private racingGaService: RacingGaService,
    protected locale: LocaleService,
    protected storage: TempStorageService,
    protected buildUtilityService: BuildUtilityService,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(toteService, gtmService, router, locale, storage, buildUtilityService,vEPService);
  }

  trackModule(module: string, sport: string): void {
    this.storage.set(this.SECTION_FLAG, !this.isExpanded);
    this.racingGaService.trackModule(module, sport);
  }
}
