import { NoEventsComponent } from '@shared/components/noEvents/no-events.component';

describe("NoEventsComponent", () => {
  let component: NoEventsComponent;
  beforeEach(() => {
    component = new NoEventsComponent();
  });

  it('NoEventsComponent', () => {
    expect(component).toBeTruthy();
  });
});