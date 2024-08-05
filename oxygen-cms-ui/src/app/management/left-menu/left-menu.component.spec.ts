import { LeftMenuComponent } from './left-menu.component';

describe('Object', () => {
  let component: LeftMenuComponent;
  let route;

  beforeEach(() => {
    route = {
      snapshot: {
        data: {
          mainData: [{
            body: { menu: [] }
          }]
        }
      }
    };
    component = new LeftMenuComponent(route);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.links).toBeDefined();
  });
});
