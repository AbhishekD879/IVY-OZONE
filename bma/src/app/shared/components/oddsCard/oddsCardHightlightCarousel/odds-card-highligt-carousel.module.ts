import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { OddsCardHighlightCarouselComponent } from './odds-card-highlight-carousel.component';

@NgModule({
    imports: [
        SharedModule, CommonModule,NgOptimizedImage
    ],
    providers: [
    ],
    declarations: [
        OddsCardHighlightCarouselComponent
    ],
    exports: [
        OddsCardHighlightCarouselComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class OddsCardHighlightCarouselModule {
    static entry = OddsCardHighlightCarouselComponent;
}
