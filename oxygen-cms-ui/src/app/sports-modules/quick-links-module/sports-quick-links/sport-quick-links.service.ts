import { Injectable } from '@angular/core';

import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { mergeMap } from 'rxjs/operators';

import { SportsQuickLink } from '@app/client/private/models/sportsquicklink.model';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ConfigStructureAPIService } from '@app/system-configuration/structure-page/service/structure.api.service';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { IQuickLinkGroups } from '@app/sports-modules/quick-links-module/sports-quick-links/models/sports-quick-links.models';

@Injectable()
export class SportQuickLinksService {
  maxLinksAmount: number = 3;
  currentLinksList: SportsQuickLink[];
  isLinksListValid: boolean = true;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private configStructureAPIService: ConfigStructureAPIService
  ) {
  }

  loadMaxAmountOfLinks(): Observable<void> {
    return this.configStructureAPIService.getStructureData()
      .map(data => {
        return data[0].body;
      })
      .map(config => {
        const linksConfig = config['Sport Quick Links'];

        this.maxLinksAmount = (linksConfig &&
                                linksConfig.maxAmount &&
                                  parseInt(linksConfig.maxAmount, 10)) || 6;
      });
  }

  isValidLinksList(sportsQuickLinksList: SportsQuickLink[]): boolean {
    let isLinksListValid = true;

    sportsQuickLinksList.forEach((sportsQuickLink: SportsQuickLink) => {
      const isValidLiksPeriodsMatch = this.isValidLink(sportsQuickLink, sportsQuickLinksList);

      sportsQuickLink.isValid = isValidLiksPeriodsMatch;

      if (!isValidLiksPeriodsMatch) {
        isLinksListValid = false;
      }
    });

    return isLinksListValid;
  }

  validateLinks(sportsQuickLinksList: SportsQuickLink[]): SportsQuickLink[] {
    this.isLinksListValid = this.isValidLinksList(sportsQuickLinksList);

    return sportsQuickLinksList;
  }

  isValidLink(sportsQuickLink: SportsQuickLink, sportsQuickLinksList: SportsQuickLink[]): boolean {
    return sportsQuickLink.disabled || this.isValidLinkPeriod(sportsQuickLink, sportsQuickLinksList);
  }

  isValidLinkPeriod(sportsQuickLink: SportsQuickLink, currentLinksList: SportsQuickLink[]): boolean {
    const quickLinkGroups = this.createMatchesGroups(currentLinksList);
    this.setGroupsValidity(quickLinkGroups, 'matches');
    // Iterate one more time with range matches to find intersections
    this.setGroupsValidity(quickLinkGroups, 'matchedGroups');

    return quickLinkGroups[sportsQuickLink.id].isValid;
  }

  createMatchesGroups(quickLinksList: SportsQuickLink[]): IQuickLinkGroups {
    const groups: IQuickLinkGroups = {};

    quickLinksList.forEach((sportsQuickLink: SportsQuickLink) => {
      groups[sportsQuickLink.id] = {
        isValid: true,
        matches: [],
        matchedGroupsCount: 0,
        disabled: sportsQuickLink.disabled,
        name: sportsQuickLink.title,
        matchedGroups: []
      };

      const periodStampStart = new Date(sportsQuickLink.validityPeriodStart);
      const periodStampEnd = new Date(sportsQuickLink.validityPeriodEnd);

      quickLinksList.forEach((quickLink: SportsQuickLink) => {
        if (quickLink.disabled === true || quickLink.id === sportsQuickLink.id) {
          return;
        }
        const checkPeriodStampStart = new Date(quickLink.validityPeriodStart);
        const checkPeriodStampEnd = new Date(quickLink.validityPeriodEnd);

        if (this.isPeriodsOverlapped(periodStampStart, periodStampEnd, checkPeriodStampStart, checkPeriodStampEnd)) {
          groups[sportsQuickLink.id].matches.push(quickLink);
        }
      });
    });

    return groups;
  }

  isLimitForPeriodReached(samePeriodLinks: number): boolean  {
    return samePeriodLinks >= this.maxLinksAmount;
  }

  setGroupsValidity(groups: IQuickLinkGroups, propToCheck: string): void {
    for (const groupId in groups) {
      if (!groups.hasOwnProperty(groupId)) {
        continue;
      }
      const matchedGroups = [];
      const groupToValidate = groups[groupId];

      if (!this.isLimitForPeriodReached(groupToValidate[propToCheck].length))  {
        continue;
      }

      groupToValidate[propToCheck].forEach((quickLink) => {
        const samePeriodLinks = [];
        const groupToCompare = groups[quickLink.id];
        if (!this.isLimitForPeriodReached(groupToCompare[propToCheck].length)) {
          return;
        }

        // if matched link group has more than max allowed matches
        // compare matched link group matches with current group matches
        // check if matched link group has the same matched links as in base group
        groupToCompare[propToCheck].forEach((matchedQuickLink) => {
          if (matchedQuickLink.id === groupId || groupToValidate[propToCheck].findIndex(x => x.id === matchedQuickLink.id) >= 0)  {
            samePeriodLinks.push(matchedQuickLink);
          }
        });

        // if matched link group has same links as in base group, and amount bigger than allowed too
        // count matched link group as on the same scheduled not valid period
        if (this.isLimitForPeriodReached(samePeriodLinks.length)) {
          matchedGroups.push(quickLink);
        }
      });

      // if matched link groups bigger than allowed links at the same time, set validity state.
      if (this.isLimitForPeriodReached(matchedGroups.length)) {
        groupToValidate.isValid = false;
      } else {
        groupToValidate.isValid = true;
      }
      groupToValidate.matchedGroupsCount = matchedGroups.length;
      groupToValidate.matchedGroups = matchedGroups;
    }
  }

  getHubIndex(hubId: string): Observable<number> {
    return this.apiClientService.eventHub().getEventHubById(hubId)
      .map((hubData: IEventHub) => {
        return hubData.indexNumber;
      });
  }

  isPeriodsOverlapped(periodStampStart, periodStampEnd, checkPeriodStampStart, checkPperiodStampEnd): boolean {
    return (periodStampStart <= checkPeriodStampStart && periodStampEnd >= checkPeriodStampStart) ||
      (periodStampStart >= checkPeriodStampStart && periodStampStart <= checkPperiodStampEnd);
  }

  loadQuickLinks(sportId?: string, pageType?: string): Observable<SportsQuickLink[]> {
    return this.loadMaxAmountOfLinks()
      .pipe(mergeMap(() => {
          return this.apiClientService.sportsQuickLink()
            .findAllByBrand(sportId, pageType)
            .map(response => {
              return response.body;
            })
            .map((data: SportsQuickLink[]) => {
              this.globalLoaderService.hideLoader();
              this.currentLinksList = data;
              return this.validateLinks(this.currentLinksList);
            });
        }));
  }

  loadSegmentQuickLinks(segment, pageId, pageType) {
    return this.loadMaxAmountOfLinks()
    .pipe(mergeMap(() => {
        return this.apiClientService.sportsQuickLink().getSportsQuickLinksBySegment(segment, pageId, pageType)
          .map(response => {
            return response.body;
          })
          .map((data: SportsQuickLink[]) => {
            this.globalLoaderService.hideLoader();
            this.currentLinksList = data;
            return this.validateLinks(this.currentLinksList);
          });
      }));
  }

  saveNewQuickLink(sportsQuickLink: SportsQuickLink, imageToUpload: any): Observable<SportsQuickLink> {
    return this.apiClientService.sportsQuickLink().save(sportsQuickLink)
      .map((data: HttpResponse<SportsQuickLink>) => {
        return data.body;
      })
      .map((createdSportsQuickLink: SportsQuickLink) => {
        if (imageToUpload) {
          this.uploadFile(createdSportsQuickLink, imageToUpload)
            .map((uploadResponseData: HttpResponse<SportsQuickLink>) => {
              return uploadResponseData && uploadResponseData.body;
            })
            .subscribe(() => {},
              (error: HttpErrorResponse) => {
                return Observable.throw('Sport Quick link was created, but Image not uploaded. Error: ' + error.error.message);
              });
        }

        return createdSportsQuickLink;
      }, (error: HttpErrorResponse) => {
        return Observable.throw('Something goes wrong. Error: ' + error.error.message);
      });
  }

  /**
   * Upload file on new link save.
   */
  uploadFile(sportsQuickLink, file): Observable<HttpResponse<SportsQuickLink>> {
    const formData = new FormData();
    // uploaded file
    formData.append('file', file);
    return this.apiClientService.sportsQuickLink().uploadIcon(sportsQuickLink.id, formData);
  }
}
