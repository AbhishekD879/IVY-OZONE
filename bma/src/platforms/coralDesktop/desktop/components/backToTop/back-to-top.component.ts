import { ChangeDetectorRef, Component, OnInit, AfterViewInit } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IConstant } from '@core/services/models/constant.model';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'back-to-top',
  templateUrl: 'back-to-top.component.html',
  styleUrls: ['back-to-top.component.scss']
})
export class BackToTopComponent implements OnInit, AfterViewInit {
  showBackButton: boolean = false;
  windowScrollListener: () => void;
  window: IConstant;
  elmBody: HTMLElement;

  constructor(
    protected renderedService: RendererService,
    protected windowRef: WindowRefService,
    protected domToolsService: DomToolsService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    this.window = this.windowRef.nativeWindow;
    this.elmBody = this.windowRef.document.querySelector('html body');
  }

  ngOnInit() {
    let timeout;
    this.windowScrollListener = this.renderedService.renderer.listen(this.window, 'scroll', () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        this.scroll();
      }, 20);
    });
  }

  ngAfterViewInit() {
    this.changeDetectorRef.detach();
  }

  scrollToTop() {
    this.windowRef.document.body.scrollTop = 0; // For Safari
    this.windowRef.document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }

  scroll() {
    const header = this.domToolsService.HeaderEl;
    const headerHeight = this.domToolsService.getHeight(header);

    const pageYOffset = this.window.pageYOffset - headerHeight;
    if (!this.showBackButton || pageYOffset < 0) {
      this.showBackButton = pageYOffset > 0;
      this.changeDetectorRef.detectChanges();
    }
  }


}
