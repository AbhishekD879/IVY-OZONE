import { Injectable } from '@angular/core';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { TimeService } from '@core/services/time/time.service';
import { EventService } from '@sb/services/event/event.service';
import { TemplateService } from '@shared/services/template/template.service';
import { ladbrokesGreyhoundConfig } from '../config/greyhound.config';
import { DailyRacingService } from '@core/services/racing/dailyRacing/daily-racing.service';
import { TimeFormService } from '@core/services/racing/timeForm/time-form.service';
import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RacingPostService } from '@coreModule/services/racing/racingPost/racing-post.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

@Injectable()
export class GreyhoundService extends RacingService {
  constructor(
    protected timeformService: TimeFormService,
    protected ukToteService: UkToteService,
    protected dailyRacingService: DailyRacingService,
    protected eventFactory: EventService,
    protected templateService: TemplateService,
    protected timeService: TimeService,
    protected filtersService: FiltersService,
    protected liveUpdatesWSService: LiveUpdatesWSService,
    protected channelService: ChannelService,
    protected lpAvailabilityService: LpAvailabilityService,
    protected commandService: CommandService,
    protected localeService: LocaleService,
    protected racingYourcallService: RacingYourCallService,
    protected pubSubService: PubSubService,
    protected racingPostService: RacingPostService,
    protected cmsService: CmsService,
    protected routingHelperService: RoutingHelperService
  ) {
    super(
      timeformService,
      ukToteService,
      dailyRacingService,
      eventFactory,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      lpAvailabilityService,
      commandService,
      localeService,
      racingYourcallService,
      pubSubService,
      cmsService,
      racingPostService,
      routingHelperService
    );
    super.setConfig(ladbrokesGreyhoundConfig);
  }
}
