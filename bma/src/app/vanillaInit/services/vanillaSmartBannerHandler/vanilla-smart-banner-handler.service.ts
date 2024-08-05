import { Injectable, OnDestroy } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Injectable({
  providedIn: 'root'
})
export class VanillaSmartBannerHandlerService implements OnDestroy {
  private document: HTMLDocument;
  private mutationObserverConfig = { childList: true };

  private vnSmartBanner: HTMLElement;
  private fixStyleNodes: { [key: string]: HTMLStyleElement } = {};
  private smartBannerBottom = 0;
  private scrollListener: Function;

  private readonly marginTopFixClass = 'vn-smart-banner-margin-top';

  constructor(
    private windowRef: WindowRefService,
    private rendererService: RendererService,
  ) {
    this.document = this.windowRef.document;
  }

  ngOnDestroy(): void {
    this.removeScrollListener();
  }

  init(): void {
    const vnApp = this.document.querySelector('vn-app');
    if (!vnApp) {
      return;
    }

    const observer = new this.windowRef.nativeWindow.MutationObserver((mutationsList) => {
      if (mutationsList && mutationsList.length) {
        this.initSmartBannerTracking();
        observer.disconnect();
      }
    });
    observer.observe(vnApp, this.mutationObserverConfig);
  }

  private initSmartBannerTracking(): void {
    this.vnSmartBanner = this.document.querySelector('vn-smart-banner');
    if (!this.vnSmartBanner) {
      return;
    }

    const observer = new this.windowRef.nativeWindow.MutationObserver((mutationsList) => {
      if (!mutationsList || !mutationsList.length) {
        return;
      }
      if (mutationsList[0].addedNodes.length) {
        this.toggleSmartBannerFix();
        this.initScrollListener();
      } else if (mutationsList[0].removedNodes.length) {
        this.cleanUpFixes();
        this.removeScrollListener();
        observer.disconnect();
      }
    });
    observer.observe(this.vnSmartBanner, this.mutationObserverConfig);
  }

  private toggleSmartBannerFix(): void {
    const smartBannerBottom = this.vnSmartBanner.getBoundingClientRect().bottom,
      bottom = smartBannerBottom > 0 ? smartBannerBottom : 0;
    if (this.smartBannerBottom !== bottom) {
      this.applyMarginTopFix(bottom);
      this.smartBannerBottom = bottom;
    }
  }

  private applyMarginTopFix(value: number): void {
    this.applyStyleFix(this.marginTopFixClass,
      `.${this.marginTopFixClass} { margin-top: ${value}px; } .${this.marginTopFixClass} .modal { padding-top: ${value}px; }`);
  }

  private applyStyleFix(key: string, cssRule: string): void {
    if (this.fixStyleNodes[key]) {
      this.fixStyleNodes[key].innerHTML = cssRule;
    } else {
      const styleNode = this.windowRef.document.createElement('style');
      styleNode.innerHTML = cssRule;
      this.windowRef.document.head.appendChild(styleNode);
      this.fixStyleNodes[key] = styleNode;
    }
  }

  private cleanUpFixes(): void {
    Object.keys(this.fixStyleNodes).forEach(className => {
      const elements = this.windowRef.document.getElementsByClassName(className);
      Array.prototype.slice.call(elements).forEach((element: HTMLElement) =>
        this.rendererService.renderer.removeClass(element, className));

      const styleNode = this.fixStyleNodes[className];
      if (styleNode.parentNode) {
        styleNode.parentNode.removeChild(styleNode);
      }
      styleNode.innerHTML = '';
    });
  }

  private initScrollListener(): void {
    this.scrollListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'scroll',
      () => this.toggleSmartBannerFix());
  }

  private removeScrollListener(): void {
    if (this.scrollListener) {
      this.scrollListener();
    }
  }
}
