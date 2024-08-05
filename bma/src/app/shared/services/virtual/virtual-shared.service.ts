import { Injectable, OnDestroy } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IVirtualSportAliasesDto } from '@core/services/cms/models/virtual-sports.model';

@Injectable({
  providedIn: 'root',
})
export class VirtualSharedService implements OnDestroy {
  private readonly classIdToAliases: Map<string, IVirtualSportAliasesDto> =
    new Map<string, IVirtualSportAliasesDto>();
  private readonly cmsInitialDataSubscription;

  constructor(private cmsService: CmsService) {
    this.cmsInitialDataSubscription = this.cmsService.getVirtualSportAliases()
      .subscribe((aliases: IVirtualSportAliasesDto[]) =>
        (aliases || []).forEach(alias => this.classIdToAliases.set(alias.classId, alias))
      );
  }

  ngOnDestroy(): void {
    this.cmsInitialDataSubscription.unsubscribe();
  }

  getVirtualSilkSrc(event: ISportEvent, silkName: string): string {
    const aliases = this.classIdToAliases.get(event.classId.toString());

    if (aliases) {
      const eventAlias = this.findEventAlias(aliases, event);

      return `${environment.CMS_ROOT_URI}/images/uploads/virtuals/${aliases.parent}
              /${aliases.child}/${eventAlias ? `${eventAlias}/` : ''}${silkName}.png`
        .replace(/\s/g, '')
        .toLowerCase();
    }
  }

  formVirtualEventUrl(event: ISportEvent): string {
    const aliases = this.classIdToAliases.get(String(event.classId));
    if (aliases) {
      return `virtual-sports/sports/${aliases.parent}/${aliases.child}/${event.id}`;
    }
  }

  formVirtualTypeUrl(classId: string): string {
    const aliases = this.classIdToAliases.get(String(classId));

    if (aliases) {
      return `virtual-sports/sports/${aliases.parent}/${aliases.child}`;
    } else {
      return 'virtual-sports/sports';
    }
  }

  isVirtual(categoryId: string): boolean {
    return categoryId && categoryId === environment.CATEGORIES_DATA.virtuals[0].id;
  }

  /**
   * It's possible to configure several sets of silks for the same child. In such case the silks are bounded
   * to the specific event rather than child itself. E.g. let's say we have the following parent-child combination
   * configured on CMS: Virtual Horse Racing --> Virtual Grand National. In such case the general path for silks
   * would be {baseUrl}/virtual-horse-racing/virtual-grand-national/{silkName}. Then say content manager
   * configures another set of silks for Laddies Leap's Lane event. In this case the path would become
   * {baseUrl}/virtual-horse-racing/virtual-grand-national/laddies-leap-s-lane/{silkName}.
   */
  private findEventAlias(aliases: IVirtualSportAliasesDto, event: ISportEvent): string {
    let eventAlias;

    if (aliases.events) {
      eventAlias = aliases.events[event.name];

      if (!eventAlias) {
        const matchingKey = Object.keys(aliases.events).find(alias => event.name.includes(alias));

        eventAlias = aliases.events[matchingKey];
      }
    }
    return eventAlias;
  }
}
