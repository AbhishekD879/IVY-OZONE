import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';

@Component({
  selector: 'bet-finder',
  templateUrl: 'bet-finder.component.html'
})
export class LadbrokesMobileBetFinderComponent extends BetFinderComponent implements OnInit, OnDestroy {
  outsideDropdownTouchListener: () => void;

  constructor(
    protected storageService: StorageService,
    protected domToolsService: DomToolsService,
    protected windowRefService: WindowRefService,
    protected localeService: LocaleService,
    protected gtm: GtmService,
    protected router: Router,
    protected betFinderHelperService: BetFinderHelperService,
    protected pubsub: PubSubService,
    protected rendererService: RendererService
  ) {
    super(
      storageService,
      domToolsService,
      windowRefService,
      localeService,
      gtm,
      router,
      betFinderHelperService,
      pubsub
    );
  }

  ngOnInit(): void {
    super.ngOnInit();

    this.outsideDropdownTouchListener = this.rendererService.renderer.listen(this.window, 'touchstart',
      event => this.hideDropdown(event));
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();
    this.outsideDropdownTouchListener && this.outsideDropdownTouchListener();
  }

  protected hideDropdown(event: any): void {
    const bfDropdown = this.document.querySelector('.bf-meetings-list');
    const targetClassName = event.target.className;
    const dropdownClasses = ['meetings-title', 'title', 'bf-meetings-list', 'bf-meeting-item'];
    if (bfDropdown && dropdownClasses.indexOf(targetClassName) === -1) {
      this.isActiveDropDown = false;
    }
  }
}
