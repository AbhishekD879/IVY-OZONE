import { of as observableOf } from 'rxjs';
import { NavigationEnd } from '@angular/router';

import { TotePageComponent } from '@app/tote/components/totePage/tote-page.component';

describe('#TotePageComponent', () => {
  let component, router, cms, route;

  beforeEach(() => {
    router = {
      events: observableOf(new NavigationEnd(0, '', '')),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    cms = {
      getSystemConfig: () => observableOf({}),
      getItemSvg: () => observableOf({})
    };

    route = {
      snapshot: {
        firstChild: {
          url: [{
            path: 'results'
          }]
        }
      }
    };

    component = new TotePageComponent(router, cms, route);
  });

  it('should select correct tab via setActiveTab()', () => {
    component.ngOnInit();

    expect(component.activeTab.id).toBe('tab-results');
  });

  it('should set default tab', () => {
    component['route'].snapshot.firstChild.url[0].path = 'smth';

    component.ngOnInit();

    expect(component.activeTab.id).toBe('tab-horseracing');
  });

  it('ngOnDestroy', () => {
    component.routeListener = {
      unsubscribe: jasmine.createSpy()
    };
    component.ngOnDestroy();
    expect(component.routeListener.unsubscribe).toHaveBeenCalledWith();
  });

  it('goToDefaultPage', () => {
    component.goToDefaultPage();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });
});


