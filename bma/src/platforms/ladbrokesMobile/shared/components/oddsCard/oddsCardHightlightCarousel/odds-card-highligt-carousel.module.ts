import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesOddsCardHighlightCarouselComponent } from './odds-card-highlight-carousel.component';

@NgModule({
    imports: [
        SharedModule,
        CommonModule,
        NgOptimizedImage 
    ],
    providers: [
    ],
    declarations: [
        LadbrokesOddsCardHighlightCarouselComponent
    ],
    exports: [
        LadbrokesOddsCardHighlightCarouselComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class OddsCardHighlightCarouselModule {
    static entry = LadbrokesOddsCardHighlightCarouselComponent;
}
