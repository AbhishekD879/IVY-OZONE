import { Component, EventEmitter, Input, OnInit, OnDestroy, Output, ChangeDetectorRef, ElementRef } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SeoDataService } from '@core/services/seoData/seo-data.service';

@Component({
  selector: 'top-bar',
  templateUrl: 'top-bar.component.html',
  styleUrls: ['top-bar.component.scss']
})
export class TopBarComponent implements OnInit, OnDestroy {
  @Output() readonly backFunc?: EventEmitter<void> = new EventEmitter();
  @Output() readonly titleFunc?: EventEmitter<void> = new EventEmitter();
  @Input() iconId?: string;
  @Input() iconSvg?: string;
  @Input() path?: string;
  @Input() innerContent?: boolean;
  @Input() isHorseRacingDetailPage: boolean;
  @Input() isRouteRequestSuccess: boolean = true;

  linkPath: string;
  titleText: string;

  private _title: string;
  private iObserver: IntersectionObserver;
  seoEnabledInCms: boolean = false;

  @Input() set title(value: string) {
    this._title = value;
    this.titleText = this.getText();
  }

  constructor(
    private locale: LocaleService,
    private changeDetectorRef: ChangeDetectorRef,
    private pubSubService: PubSubService,
    private domToolsService: DomToolsService,
    private elementRef: ElementRef,
    private seoDataService: SeoDataService
  ) {}

  ngOnInit() {
    this.linkPath = this.getPath();
    this.titleText = this.getText();
    this.changeDetectorRef.detectChanges();
    this.pubSubService.subscribe('TopBarComponent', this.pubSubService.API.PIN_TOP_BAR,
      (pin: boolean) => { pin ? this.pinTopBar() : this.unpinTopBar(); });
    this.seoDataService.seoSubjObservable.subscribe((seoInCms: boolean) => {
      this.seoEnabledInCms = seoInCms;
    });
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe('TopBarComponent');
    this.disconnectObserver();
  }

  /**
   * Form redirect path
   * @return {string}
   */
  getPath(): string {
    return this.path || '';
  }

  /**
   * Top Bar title (Show localised title or bind title)
   * @type {string}
   */
  getText(): string {
    if (/^[a-zA-Z]*\.[a-zA-Z0-9]*$/.test(this._title)) {
      return this.locale.getString(this._title);
    } else {
      return this._title;
    }
  }

  titleClickHandler(): boolean {
    this.titleFunc.emit();
    return false;
  }

  backClickHandler(): void {
    this.backFunc.emit();
  }

  private pinTopBar(): void {
    const headerHeight = this.domToolsService.getHeight(this.domToolsService.HeaderEl),
      topBarHeight = this.domToolsService.getHeight(this.elementRef.nativeElement),
      extraMargin = headerHeight + 2 * topBarHeight,
      options = { root: null, rootMargin: `${-extraMargin}px 0px 0px 0px`, threshold: 0 };

    this.disconnectObserver();
    this.iObserver = this.createObserver(options);
    this.iObserver.observe(this.domToolsService.ContentEl);
  }

  private unpinTopBar(): void {
    this.fixPosition(false);
    this.disconnectObserver();
  }

  private fixPosition(fixed: boolean = false): void {
    const topBarEl = this.elementRef.nativeElement,
      topBarHeight = this.domToolsService.getHeight(topBarEl);

    topBarEl.style.position = fixed ? 'fixed' : null;
    topBarEl.parentElement.style.paddingTop = fixed ? `${topBarHeight}px` : null;
  }

  private createObserver(options: IntersectionObserverInit): IntersectionObserver {
    return new IntersectionObserver((iEntries: IntersectionObserverEntry[]) => {
      this.fixPosition(iEntries && iEntries[0] && iEntries[0].isIntersecting === false);
    }, options);
  }

  private disconnectObserver(): void {
    if (this.iObserver) {
      this.iObserver.disconnect();
    }
  }
}
