import { NgModule } from '@angular/core';
import { FlagHelperService } from '@app/lazy-modules/flagSource/services/flag-helper.service';
@NgModule({
  declarations: [
  ],
  imports: [
  ],
  exports: [
  ],
  providers: [
    FlagHelperService
  ]
})
export class FlagSourceModule {
  constructor(private flagHelperService:  FlagHelperService){}
}