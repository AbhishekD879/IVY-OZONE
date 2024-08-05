import { InPlayStorageService as AppInPlayStorageService } from '@app/inPlay/services/inplayStorage/in-play-storage.service';
import { Injectable } from '@angular/core';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';

@Injectable({
  providedIn: InplayApiModule
})
export class InPlayStorageService extends AppInPlayStorageService { }
