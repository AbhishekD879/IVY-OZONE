import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { BetpackReviewHomepageComponent } from '@app/betpackReview/components/betpackReviewHomePage/betpack-review-homepage.component';
import { BetpackReviewRoutingModule } from '@app/betpackReview/betpack-review.routing.module';
import { CommonModule } from '@angular/common';
import { BetpackCmsModule } from '@app/lazy-modules/betpackPage/betpack-cms.module';

@NgModule({
  imports: [

    SharedModule,
    CommonModule,
    BetpackCmsModule,
    BetpackReviewRoutingModule
  ],
  declarations: [
    BetpackReviewHomepageComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BetpackReviewModule { }