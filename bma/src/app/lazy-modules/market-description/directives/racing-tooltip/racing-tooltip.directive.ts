import { Directive, ElementRef, ComponentFactoryResolver, ViewContainerRef,
     Input, OnInit, TemplateRef, OnDestroy, ComponentRef, Output, EventEmitter,
     Injector } from '@angular/core';
import { TooltipDirective } from '@shared/directives/tooltip.directive';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { RacingTooltipComponent } from '@lazy-modules-module/market-description/components/racing-tooltip/racing-tooltip.component';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Directive({
    selector: '[racingTooltip]'
})
export class RacingTooltipDirective extends TooltipDirective implements OnInit, OnDestroy {
    // eslint-disable-next-line @angular-eslint/no-input-rename
    @Input('racingTooltip') racingTooltip: string | TemplateRef<any> | ComponentRef<any>;
    @Input() marketContainer: HTMLElement;
    @Output() readonly isTooltipSeen: EventEmitter<boolean> = new EventEmitter();
    protected componentRef: ComponentRef<RacingTooltipComponent>;

    constructor(protected element: ElementRef,
        protected rendererService: RendererService,
        protected resolver: ComponentFactoryResolver,
        protected vcr: ViewContainerRef,
        protected locale: LocaleService,
        protected storageService: StorageService,
        protected gtmService: GtmService) {
        super(element, rendererService, resolver, vcr, locale, gtmService);
    }

    ngOnInit() {
        if (this.validateTooltip(this.marketContainer)) {
            this.displayTooltip();
            this.isTooltipSeen.emit(true);
        }
    }

    /**
     * To display tooltip
     */
    displayTooltip(): void {
      const factory = this.resolver.resolveComponentFactory(RacingTooltipComponent);
      const injector = Injector.create([
        {
          provide: 'tooltipConfig',
          useValue: {
            host: this.element.nativeElement
          }
        }
      ]);
      this.componentRef = this.vcr.createComponent(factory, 0, injector, this.generateNgContent());
    }

  /**
   * Method to validate to show or hide tooltip
   */
  validateTooltip( marketContainer: HTMLElement): boolean {
    let hasScrollRight = false;
    if (marketContainer) {
      const innerWidth = this.getInnerWidth(marketContainer);
      hasScrollRight = marketContainer.clientWidth < innerWidth;
    } else {
      hasScrollRight = false;
    }

    if (hasScrollRight) {
      return this.showHideToolTip();
    }
  }

  generateNgContent(): any[][] {
    if ( typeof this.racingTooltip === 'string' ) {
      const text = this.locale.getString(`app.tooltip.${this.racingTooltip}`,
        this.toolTipArgs);
      const element = this.rendererService.renderer.createText(text);
      return [ [ element ] ];
    }
  }

  ngOnDestroy(): void {
    this.destroy();
  }

  /**
   * Get width of scroll inner element
   * @returns {number}
   * @private
   */
  private getInnerWidth(marketContainer: HTMLElement): number {
    if (marketContainer) {
      return marketContainer.children[0].scrollWidth;
    }
    return 0;
  }

  /**
   * To fetch tooltip information from localstorage
   */
  private showHideToolTip(): boolean {
    const tooltipData = this.storageService.get('hrGhEducationToolTipSeen');
    if (tooltipData) {
      return false;
    } else {
      this.storageService.set('hrGhEducationToolTipSeen', true);
      return true;
    }
  }

}
