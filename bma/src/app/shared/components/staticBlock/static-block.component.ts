import { finalize } from 'rxjs/operators';
import { Router } from '@angular/router';
import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  ElementRef,
  HostListener,
  Input,
  OnInit,
  OnChanges,
  SimpleChanges
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import * as _ from 'underscore';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { StorageService } from '@core/services/storage/storage.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { IStaticBlock } from '@core/services/cms/models';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

@Component({
  selector: 'static-block',
  templateUrl: 'static-block.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class StaticBlockComponent extends AbstractOutletComponent implements OnInit, OnChanges {
  @Input() service: string;
  @Input() cmsContent: IStaticBlock;
  @Input() params: string;
  @Input() expand: boolean;
  @Input() removeContainer: boolean;
  @Input() loader: boolean;

  useLoader?: boolean;
  isLoading: boolean = false;
  innerHtml: SafeHtml;

  private lang: string;
  private vipLevelNumber = Number(this.storageService.get('vipLevel'));
  private bronzeLevel = this.vipLevelNumber === 11; // 11 - bronze level
  // 12, 13, 14, 15 - silver, gold, platinum level
  private silverGoldPlatinumLevel = _.contains([12, 13, 14, 15], this.vipLevelNumber);

  constructor(
    private cmsService: CmsService,
    private locale: LocaleService,
    private storageService: StorageService,
    private elementRef: ElementRef,
    private domToolsService: DomToolsService,
    private rendererService: RendererService,
    private domSanitizer: DomSanitizer,
    private router: Router,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super();
  }

  ngOnInit(): void {
    this.lang = this.locale.getLocale().toLowerCase();
    this.useLoader = !!this.loader;

    if (this.cmsContent) {
      this.setHtml(this.cmsContent);
      this.hideSpinner();
    } else {
      if (!this.service) {
        console.warn('Incorrect usage of staticBlock directive.');
        return;
      }
      this.isLoading = true;
      this.cmsService.getStaticBlock(this.service, this.lang).pipe(
        finalize(() => {
          this.hideSpinner();
        })).subscribe((cmsContent: IStaticBlock) => {
          this.isLoading = false;
          this.cmsContent = cmsContent;
          if (cmsContent.htmlMarkup) {
            this.setHtml(cmsContent);
            this.changeDetectorRef.markForCheck();
          }
      }, () => this.showError());
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.cmsContent && this.cmsContent) {
      this.setHtml(this.cmsContent);
      this.hideSpinner();
    }
  }

  @HostListener('click', ['$event'])
  checkRedirect(event: MouseEvent): void {
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;

    if (redirectUrl) {
      this.router.navigateByUrl(redirectUrl);
    }
  }

  /**
   * Replace href attr for router links
   * @params{htmlMarkup} string
   */
  replaceHref(htmlMarkup: string): string {
    return htmlMarkup ? htmlMarkup.replace(/href="\.\.\//g, 'data-routerlink="') : '';
  }

  /**
   * Rendering htmlMarkup
   * @params{cmsContent} html template
   */
  private setHtml(cmsContent: IStaticBlock): void {
    if (this.service && this.service.match('acca-notification')) {
      this.cmsContent.htmlMarkup = this.cmsService.parseContent(cmsContent.htmlMarkup, this.params);
    }
    const htmlMarkupWithoutHref: string = this.replaceHref(cmsContent.htmlMarkup);

    // Renders cms content
    this.innerHtml = this.domSanitizer.bypassSecurityTrustHtml(htmlMarkupWithoutHref);

    this.windowRef.nativeWindow.setTimeout(() => {
      if (this.bronzeLevel || this.silverGoldPlatinumLevel) {
        this.elementRef.nativeElement.querySelectorAll('.normalMail, .normalTel').forEach((element: HTMLElement) => {
          this.rendererService.renderer.addClass(element, 'ng-hide');
        });
      }
      if (this.bronzeLevel) {
        this.elementRef.nativeElement.querySelectorAll('.bronzeLevelTel, .bronzeLevelMail').forEach((element: HTMLElement) => {
          this.rendererService.renderer.removeClass(element, 'ng-hide');
        });
      }
      if (this.silverGoldPlatinumLevel) {
        this.elementRef.nativeElement.querySelectorAll('.silverGoldPlatinumLevelTel, ' +
          '.silverGoldPlatinumLevelMail').forEach((element: HTMLElement) => {
          this.rendererService.renderer.removeClass(element, 'ng-hide');
        });
      }

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
    }, 500);
  }
}
