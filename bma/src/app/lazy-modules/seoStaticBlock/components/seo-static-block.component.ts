import { Component, ElementRef, OnDestroy, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISeoPage } from '@core/services/cms/models';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { Router, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';
import { filter } from 'rxjs/operators';
import { SeoAutomatedTagsService } from '@lazy-modules-module/seoStaticBlock/seoAutoTags/seo-automated-tags.service';

@Component({
  selector: 'seo-static-block',
  templateUrl: './seo-static-block.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SeoStaticBlockComponent implements OnInit, OnDestroy {
  seoStaticBlockContent: SafeHtml;
  isExpanded: boolean = false;
  isSeoContent: boolean = true;
  seoPageTitleBlock: string = 'SPORTS BETTING ONLINE';

  private timeOutOneID: any; // Timer
  private routeChangeSuccessHandler: Subscription;

  constructor(
    private domSanitizer: DomSanitizer,
    private pubSub: PubSubService,
    private seoAutomatedTagsService: SeoAutomatedTagsService,
    private rendererService: RendererService,
    private elementRef: ElementRef,
    private domToolsService: DomToolsService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private deviceService: DeviceService,
    protected router: Router
  ) {
    this.updateDOM = this.updateDOM.bind(this);
  }

  ngOnInit(): void {
    this.isExpanded =  this.deviceService.isDesktop;
    this.subscribeToRouterEvents();
    // Initial update
    this.seoAutomatedTagsService.getPage().subscribe(this.updateDOM);

    // Dynamic updates
    this.pubSub.subscribe('seoStaticBlockComponent', this.pubSub.API.SEO_DATA_UPDATED, this.updateDOM);
    this.addListeners();
  }

  ngOnDestroy(): void {
    this.routeChangeSuccessHandler.unsubscribe();
    this.pubSub.unsubscribe('seoStaticBlockComponent');
    this.windowRef.nativeWindow.clearTimeout(this.timeOutOneID);
  }

  /**
   * Toggle off seo content during page navigation
   */
   protected subscribeToRouterEvents(): void {
    this.routeChangeSuccessHandler = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.seoStaticBlockContent = false;
        this.changeDetectorRef.detectChanges();
      });
  }

  /**
   * Add static block content
   * @param {Object} data
   */
  private updateDOM(data: ISeoPage): void {
    this.seoStaticBlockContent = data.staticBlock ? this.domSanitizer.bypassSecurityTrustHtml(data.staticBlock) : null;
    this.seoPageTitleBlock = (data && data.staticBlockTitle) || 'SPORTS BETTING ONLINE';
    this.windowRef.nativeWindow.clearTimeout(this.timeOutOneID);
    this.addListeners();
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Add listener to handle expand/collapse panel
   */
  private addListeners(): void {
    // After seoStaticBlockContent is inserted into DOM (on next tick) - add handlers for Collapsible Panels
    // Timeout needed to render html
    this.timeOutOneID = this.windowRef.nativeWindow.setTimeout(() => {
      this.elementRef.nativeElement.querySelectorAll('.page-container').forEach(pageContainer => {
        pageContainer.querySelectorAll('.toggle-header').forEach(toggleHeaderElement => {
          this.rendererService.renderer.listen(toggleHeaderElement, 'click', () => {
            this.domToolsService.toggleClass(pageContainer, 'is-expanded');

            pageContainer.querySelectorAll('.text-section').forEach(textSection => {
              this.domToolsService.toggleVisibility(textSection);
            });
          });
        });
      });
    }, 100);
  }
}
