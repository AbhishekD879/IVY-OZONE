import { Injectable } from '@angular/core';
import {
    FiveASideEntryInfoService
        as AppFiveASideEntryInfoService
} from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
@Injectable({
    providedIn: FiveASideShowDownApiModule
})
export class FiveASideEntryInfoService extends AppFiveASideEntryInfoService {

    constructor(public fracToDecService: FracToDecService) { super(fracToDecService); }
}
