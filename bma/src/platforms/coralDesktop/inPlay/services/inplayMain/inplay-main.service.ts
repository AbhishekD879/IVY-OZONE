import { InplayMainService as AppInplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayMainService extends AppInplayMainService { }
