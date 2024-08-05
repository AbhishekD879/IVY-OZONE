import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ]
})
export class FreeRideHelperModule {
  constructor(private freeRideHelperService: FreeRideHelperService) {
  }
}
