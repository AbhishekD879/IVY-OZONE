import { ActivatedRoute } from '@angular/router';

import { QuickLinksHeaderComponent } from './quick-links-header.component';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import QuickLinks from '../../constants/quickLinks';

describe('QuickLinksHeaderComponent', () => {
  let component: QuickLinksHeaderComponent;

  let activatedRoute: ActivatedRoute;
  let routingHelperService: RoutingHelperService;

  beforeEach(() => {
    activatedRoute = {
      firstChild: {
        snapshot: {
          params: {
            sport: 'football'
          }
        }
      }
    } as any;

    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy()
    } as any;

    component = new QuickLinksHeaderComponent(
      activatedRoute,
      routingHelperService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('quickLinks', () => {
    expect(component.quickLinks).toBe(QuickLinks);
  });

  xit('getLinkUrl', () => {
    const sport = activatedRoute.firstChild.snapshot.params.sport;
    const className = 'England';
    const typeName = 'Championship';

    component.getLinkUrl(className, typeName);

    expect(routingHelperService.formCompetitionUrl).toHaveBeenCalledWith({
      sport, typeName, className: `${sport} ${className}`
    });
  });

});
