import { Component, ElementRef, HostListener, Input, OnInit } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISelections } from '@racing/components/racingYourcallSpecials/selections.model';
import { RacingGaService } from '@racing/services/racing-ga.service';
import * as _ from 'underscore';
import { IRacingYourCallMarket } from '@core/models/racing-your-call-market.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'racing-yourcall-specials',
  templateUrl: './racing-yourcall-specials.html'
})
export class RacingYourcallSpecialsComponent implements OnInit {

  @Input() data: IRacingYourCallMarket[];
  @Input() type?: string;

  isExpanded: boolean = true;
  ycWidgetFilter = 'Featured';
  switchersWidth: number;
  offsetTop: number;
  switchers: any[];
  title: string;

  private container: HTMLElement;

  constructor(
    protected filtersService: FiltersService,
    private deviceService: DeviceService,
    private racingGaService: RacingGaService,
    private elementRef: ElementRef,
    private rendererService: RendererService,
    private windowRef: WindowRefService,
    private locale: LocaleService
  ) {
    this.title = this.locale.getString('racing.yourcallSpecials');
  }

  ngOnInit(): void {
    this.container = this.elementRef.nativeElement;
    _.forEach(this.data, market => {
      market.selections = this.filtersService.orderBy(market.selections, ['displayOrder']);
    });

    if (this.type === 'widget') {
      this.data[0].selections = _.sortBy(this.data[0].selections, 'displayOrder').slice(0, 3);
    } else {
      this.prepareSwitchers();
    }
  }

  @HostListener('scroll')
  checkPositionAndToggleSticky(): void {
    if (this.deviceService.isMobileOrigin) {
      const switchers = this.container.querySelector('.switchers-parent'),
        topFixedMargin = this.container.querySelector('#header').clientHeight +
          this.container.querySelector('.top-bar-inner').clientHeight,
        scrollY = this.windowRef.nativeWindow.scrollY,
        switchersHeight = switchers.clientHeight,
        content = this.container.querySelector('.yc-specials-content'),
        contentOffset = content.clientHeight + content.clientTop;

      this.setOffsetTop(switchers);
      this.switchersWidth = content.clientWidth;
      this.toggleSwitchersVisibility(scrollY, contentOffset, switchers);

      if (scrollY + topFixedMargin >= this.offsetTop) {
        this.rendererService.renderer.setStyle(switchers, 'position', 'fixed');
        this.rendererService.renderer.setStyle(switchers, 'width', `${this.switchersWidth}px`);
        this.rendererService.renderer.setStyle(switchers, 'top', `${topFixedMargin}px`);
        this.rendererService.renderer.setStyle(switchers, 'z-index', '1');
        this.rendererService.renderer.setStyle(switchers, 'box-shadow', '0 2px 4px 0 rgba(0, 0, 0, 0.3)');

        this.rendererService.renderer.setStyle(content, 'margin-top', `${switchersHeight}px`);
      } else {
        this.setDefaultStyles(switchers, content);
      }
    }
  }

  @HostListener('resize')
  resize(): void {
    if (this.deviceService.isMobileOrigin) {
      this.offsetTop = 0;
      this.checkPositionAndToggleSticky();
    }
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackById(index: number, value: IMarket | IOutcome): string {
    return `${index}${value.id}`;
  }

  /**
   * changeFilter()
   * @param {sting} viewByFilters
   */
  changeFilter(viewByFilters: string): void {
    this.ycWidgetFilter = viewByFilters;
  }

  /**
   * trackYourcallSpecials()
   */
  trackYourcallSpecials(): void {
    this.racingGaService.trackYourcallSpecials();
  }

  /**
   * prepareSwitchers()
   */
  protected prepareSwitchers(): void {
    this.switchers = [];

    this.data = this.filtersService.orderBy(this.data, ['displayOrder']);

    _.each(this.data, (selections: ISelections) => {
      this.switchers.push({
        name: selections.name,
        viewByFilters: selections.name,
        onClick: this.changeFilter.bind(this)
      });
    });

    this.ycWidgetFilter = this.switchers[0].viewByFilters;
  }

  /**
   * setOffsetTop()
   * @param {Element} switchers
   */
  private setOffsetTop(switchers: Element): void {
    const position = switchers.getAttribute('position');

    if (position === 'static' || position === 'relative' || !this.offsetTop) {
      this.offsetTop = switchers.clientTop;
    }
  }

  /**
   * toggleSwitchersVisibility()
   * @param {number} scrollY
   * @param {number} contentOffset
   * @param {Element} switchers
   */
  private toggleSwitchersVisibility(scrollY: number, contentOffset: number, switchers: Element): void {
    if (scrollY >= contentOffset) {
      this.rendererService.renderer.setStyle(switchers, 'display', 'none');
    } else {
      this.rendererService.renderer.setStyle(switchers, 'display', 'flex');
    }
  }

  /**
   * setDefaultStyles()
   * @param {Element} switchers
   * @param {Element} content
   */
  private setDefaultStyles(switchers: Element, content: Element): void {
    this.rendererService.renderer.setStyle(switchers, 'width', '100%');
    this.rendererService.renderer.setStyle(switchers, 'position', 'relative');
    this.rendererService.renderer.setStyle(switchers, 'top', '0px');
    this.rendererService.renderer.setStyle(switchers, 'box-shadow', 'none');

    this.rendererService.renderer.setStyle(content, 'margin-top', '0px');
  }
}
