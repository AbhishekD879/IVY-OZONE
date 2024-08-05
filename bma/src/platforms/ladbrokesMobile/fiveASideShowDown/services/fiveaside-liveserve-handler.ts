import { Injectable } from '@angular/core';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import {
  FiveASideLiveServeHandlerService
    as AppFiveASideLiveServeHandlerService
} from '@app/fiveASideShowDown/services/fiveaside-liveserve-handler';

@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveASideLiveServeHandlerService extends AppFiveASideLiveServeHandlerService {
}
