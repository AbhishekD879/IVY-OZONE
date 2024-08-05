import { Directive, ElementRef, Input, Renderer2 } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
@Directive({
  selector: '[appSymbolBackground]'
})
export class SymbolBackgroundDirective {
  private cachedDataUrls: { [key: string]: string } = {};
  private cmsRootUri: string = environment.CMS_ROOT_URI;
  @Input('appSymbolBackground') set imgObj(value) {
    this.getSymboleObj(value);
  }

  constructor(private el: ElementRef, private renderer: Renderer2) { }

  getSymboleObj(sbObj): void {
    const symbolId = sbObj?.svgBgId;
    const imagePath = sbObj?.svgBgImgPath ? `${this.cmsRootUri}${sbObj?.svgBgImgPath}` : '';
    if (symbolId) {
      const symbolElement = document.getElementById(symbolId);
      if (symbolElement) {
        // Check if the data URL is already cached
        if (!this.cachedDataUrls[symbolId]) {
          const dataUrl = this.createDataUrl(symbolElement);
          this.cachedDataUrls[symbolId] = dataUrl;
        }
        this.applyBackground(this.cachedDataUrls[symbolId]);
      } else {
        this.applyBackground(imagePath);
      }
    } else {
      this.clearBackground();
    }
  }

  private createDataUrl(symbolElement: HTMLElement): string {
    const svgContainer = this.renderer.createElement('svg', 'http://www.w3.org/2000/svg');
    svgContainer.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgContainer.innerHTML = symbolElement.innerHTML;

    const viewBox = symbolElement.getAttribute('viewBox');
    if (viewBox) {
      svgContainer.setAttribute('viewBox', viewBox);
    }
    const svgString = new XMLSerializer().serializeToString(svgContainer);
    return `data:image/svg+xml;base64,${btoa(svgString)}`;
  }

  private applyBackground(dataUrl: string): void {
    this.renderer.addClass(this.el.nativeElement, 'surface-bet-bg-image');
    this.renderer.addClass(this.el.nativeElement, 'image-cls-container');
    this.renderer.setStyle(this.el.nativeElement, 'backgroundImage', `url(${dataUrl})`);
  }
  clearBackground() {
    this.renderer.removeClass(this.el.nativeElement, 'surface-bet-bg-image');
    this.renderer.removeClass(this.el.nativeElement, 'image-cls-container');
    this.renderer.setStyle(this.el.nativeElement, 'backgroundImage', `url()`);
  }
}
