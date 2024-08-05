import { Directive, ElementRef, Input, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { Subscription } from 'rxjs';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  // eslint-disable-next-line
  selector: '[i18n]'
})
export class LocaleDirective implements OnInit, OnChanges, OnDestroy {
  @Input() i18n: string;
  @Input() i18nArgs: any;

  private readonly translationModuleLoadedSub: Subscription;

  constructor(
    private rendererService: RendererService,
    public element: ElementRef,
    private localeService: LocaleService
  ) {
    if (!this.localeService.isTranslationModuleLoaded.value) {
      this.translationModuleLoadedSub = this.localeService.isTranslationModuleLoaded
        .subscribe(() => {}, () => {}, () => {
          this.render();
        });
    }
  }

  ngOnInit(): void {
    this.render();
  }

  ngOnChanges(): void {
    this.render();
  }

  ngOnDestroy(): void {
    this.translationModuleLoadedSub && this.translationModuleLoadedSub.unsubscribe();
  }

  render(): void {
    this.rendererService.renderer
      .setProperty(
        this.element.nativeElement, 'innerHTML',
        this.localeService.getString(this.i18n, this.i18nArgs)
      );
  }
}
