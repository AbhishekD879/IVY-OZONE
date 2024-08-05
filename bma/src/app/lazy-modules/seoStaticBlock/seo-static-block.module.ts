import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { SeoStaticBlockComponent } from '@lazy-modules/seoStaticBlock/components/seo-static-block.component';
import { SeoAutomatedTagsService } from '@lazy-modules/seoStaticBlock/seoAutoTags/seo-automated-tags.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [
    SeoStaticBlockComponent
  ],
  providers: [
    SeoAutomatedTagsService
  ],
  exports: [
    SeoStaticBlockComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SeoStaticBlockModule {
  static entry = SeoStaticBlockComponent;

  constructor() {}
}
