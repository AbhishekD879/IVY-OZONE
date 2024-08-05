import {
  Directive,
  OnInit,
  OnDestroy,
  Input,
  Output,
  EventEmitter,
  TemplateRef,
  ComponentRef,
  ElementRef,
  Injector,
  ComponentFactoryResolver,
  ViewContainerRef,
  HostListener,
  SimpleChanges
} from '@angular/core';

import { TooltipComponent } from '@sharedModule/components/tooltip/tooltip.component';

import { LocaleService } from '@core/services/locale/locale.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { MAXPAY_OUT } from '@app/lazy-modules/maxpayOutErrorContainer/constants/maxpayout-error-container.constants';
import environment from '@environment/oxygenEnvConfig';

@Directive({
  // eslint-disable-next-line
  selector: '[tooltip]'
})
export class TooltipDirective implements OnInit, OnDestroy {
  // eslint-disable-next-line
  @Input('tooltip') tooltip: string | TemplateRef<any> | ComponentRef<any>;
  @Input() showTooltip: boolean;
  @Input() showOnce?: boolean;
  @Input() toolTipArgs: { [key: string]: string; };
  @Input() createElementTag?: boolean = false;
  @Input() gtmInfo?: string;
  @Input() dynamicTooltipTitle?: boolean = false;
  @Input() enableTooltip?: boolean = true;
  @Input() mouseOver?: boolean = false;

  @Output() readonly toggleTooltip = new EventEmitter<any>();
  @Output() readonly arrowToggle: EventEmitter<boolean> = new EventEmitter();
  protected componentRef: ComponentRef<TooltipComponent>;
  coralCss: string = 'maxPay-Coral';

  constructor(protected element: ElementRef,
    protected rendererService: RendererService,
    protected resolver: ComponentFactoryResolver,
    protected vcr: ViewContainerRef,
    protected locale: LocaleService,
    protected gtmService: GtmService) {
  }

  ngOnInit(): void {
    if (this.showTooltip) {
      this.displayTooltip();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes && changes.showTooltip && !changes.showTooltip.currentValue) {
      this.destroy();
    }
  }

  @HostListener('click')
  click(): void {
    if (this.componentRef || this.showOnce) {
      this.destroy();
    } else {
      if (this.enableTooltip) {
        this.displayTooltip();
      }
    }
  }

  @HostListener('mouseover')
  onMouseHover(): void {
    if (this.mouseOver) {
      this.click();
    }
  }

  @HostListener('document:click', ['$event'])
  @HostListener('document:touchend', ['$event'])
  clickOutside(event: MouseEvent): void {
    if (!this.element.nativeElement.contains(event.target)) {
      this.destroy();
    }
  }

  @HostListener('document:mouseout', ['$event'])
  onMouseOut(event: MouseEvent): void {
    if (this.mouseOver) {
      this.clickOutside(event);
    }
  }

  displayTooltip(): void {
    const factory = this.resolver.resolveComponentFactory(TooltipComponent);
    const injector = Injector.create([
      {
        provide: 'tooltipConfig',
        useValue: {
          host: this.element.nativeElement
        }
      }
    ]);
    if (this.createElementTag) {
      this.componentRef = this.vcr.createComponent(factory, 0, injector, this.generateElement());
    } else {
      this.componentRef = this.vcr.createComponent(factory, 0, injector, this.generateNgContent());
    }
  }

  generateNgContent(): any[][] {
    if (typeof this.tooltip === 'string') {
      let text = '';
      if (this.dynamicTooltipTitle) {
        text = this.toolTipArgs[this.tooltip];
      } else {
        text = this.locale.getString(`app.tooltip.${this.tooltip}`,
          this.toolTipArgs);
      }
      const element = this.rendererService.renderer.createText(text);
      return [[element]];
    }
  }

  generateElement(): any {
    this.arrowToggle.emit(true);
    const div1 = this.rendererService.renderer.createElement('div');
    const message = this.rendererService.renderer.createText(this.toolTipArgs.maxpayout + ' ');
    this.rendererService.renderer.appendChild(div1, message);
    const text1 = this.rendererService.renderer.createElement('a');
    const clicktext = this.rendererService.renderer.createText(this.toolTipArgs.click);
    text1.setAttribute('href', this.toolTipArgs.link);
    this.rendererService.renderer.appendChild(text1, clicktext);
    this.rendererService.renderer.appendChild(div1, text1);
    if (environment.brand === 'bma') {
      this.rendererService.renderer.addClass(text1, this.coralCss);
    } else {
      text1.classList.add('hyperlink-color-lads');
    }
    this.rendererService.renderer.listen(text1, 'click', (evt) => {
      this.sendGTMData();
    });
    return [[div1]];
  }

  destroy(): void {
    this.componentRef && this.componentRef.destroy();
    this.componentRef = null;
    this.arrowToggle.emit(false);
  }

  ngOnDestroy(): void {
    this.destroy();
  }

  /**
 * Sends data to GA tracking
 * @returns void
 */
  private sendGTMData(): void {
    const gtmData = {
      eventAction: MAXPAY_OUT.eventAction[0],
      eventCategory: MAXPAY_OUT.eventCategory,
      eventLabel: this.gtmInfo
    };
    this.gtmService.push(MAXPAY_OUT.trackEvent, gtmData);
  }
}
