import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { ArcUserService } from '@lazy-modules/arcUser/service/arcUser.service';

@NgModule({
  providers: [ArcUserService],
  schemas: [NO_ERRORS_SCHEMA]
})

export class ArcUserModule {
  constructor(arcUserService:ArcUserService) {
  }
}
