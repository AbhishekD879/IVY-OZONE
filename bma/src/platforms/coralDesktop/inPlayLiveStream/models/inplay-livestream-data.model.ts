import { ISportEvent } from '@core/models/sport-event.model';
import { IFooter } from '@inPlayLiveStream/models/footer.model';
import { ICompetitionGroupFormatted } from '@inPlayLiveStream/models/competition-group.model';

export interface InplayLivestreamData {
  events: ISportEvent[];
  footer: IFooter;
  competitions: ICompetitionGroupFormatted[];
}
