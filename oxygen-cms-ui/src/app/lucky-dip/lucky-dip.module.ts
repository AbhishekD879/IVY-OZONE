import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { LuckyDipComponent } from './lucky-dip.component';
import { LuckyDipRoutingModule } from './lucky-dip.routing.module';
import { LuckyDipCreateComponent } from './lucky-dip-create/lucky-dip-create.component';
import { LuckyDipMappingComponent } from './lucky-dip-mapping/lucky-dip-mapping.component';
import { LuckyDipMappingCreateComponent } from './lucky-dip-mapping-create/lucky-dip-mapping-create.component';
import { LuckyDipEditComponent } from './lucky-dip-edit/lucky-dip-edit.component';
import { LuckyDipMappingEditComponent } from './lucky-dip-mapping-edit/lucky-dip-mapping-edit.component';
import { LuckyDipCloneComponent } from './lucky-dip-clone/lucky-dip-clone.component';
import { SportsSurfaceBetsService } from '../sports-modules/surface-bets/surface-bets.service';
import { LuckyDipV2Component } from './lucky-dip-v2/lucky-dip-v2.component';

@NgModule({
  imports: [
    SharedModule,
    LuckyDipRoutingModule
  ],
  declarations: [
    LuckyDipComponent,
    LuckyDipV2Component,
    LuckyDipCreateComponent,
    LuckyDipMappingComponent,
    LuckyDipMappingCreateComponent,
    LuckyDipEditComponent,
    LuckyDipMappingEditComponent,
    LuckyDipCloneComponent
  ],
  entryComponents: [
    LuckyDipComponent,
    LuckyDipV2Component
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers:[SportsSurfaceBetsService]
})

export class LuckyDipModule {
}
