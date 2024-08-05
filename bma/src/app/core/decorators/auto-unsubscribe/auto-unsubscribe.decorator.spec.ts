import { AutoUnsubscribe } from '@core/decorators/auto-unsubscribe/auto-unsubscribe.decorator';

const mockSubscription1 = {
  unsubscribe: jasmine.createSpy('unsubscribe')
};

const mockSubscription2 = {
  unsubscribe: jasmine.createSpy('unsubscribe')
};

describe('@AutoUnsubscribe() decorator', () => {

  afterEach(() => {
    mockSubscription1.unsubscribe.calls.reset();
    mockSubscription2.unsubscribe.calls.reset();
  });

  it('should call unsubscribe twice (mockSubscription1, mockSubscription2) on destroy', () => {

    // eslint-disable-next-line max-classes-per-file
    @AutoUnsubscribe()
    class FakeComponent {

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription1$ = mockSubscription1;
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription2$ = mockSubscription2;

      // eslint-disable-next-line 
      ngOnDestroy(): void {
      }
    }

    new FakeComponent().ngOnDestroy();

    expect(mockSubscription1.unsubscribe).toHaveBeenCalledTimes(1);
    expect(mockSubscription2.unsubscribe).toHaveBeenCalledTimes(1);
  });

  it('should call only one unsubscribe (mockSubscription1) on destroy', () => {

    // eslint-disable-next-line max-classes-per-file
    @AutoUnsubscribe(['fakeSubscription2$'])
    class FakeComponent {

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription1$ = mockSubscription1;
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription2$ = mockSubscription2;

      // eslint-disable-next-line 
      ngOnDestroy(): void {
      }
    }

    new FakeComponent().ngOnDestroy();

    expect(mockSubscription1.unsubscribe).toHaveBeenCalledTimes(1);
    expect(mockSubscription2.unsubscribe).toHaveBeenCalledTimes(0);
  });

  it('shouldn\'t call unsubscribe on destroy', () => {

    // eslint-disable-next-line max-classes-per-file
    @AutoUnsubscribe(['fakeSubscription1$', 'fakeSubscription2$'])
    class FakeComponent {

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription1$ = mockSubscription1;
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      private fakeSubscription2$ = mockSubscription2;

      // eslint-disable-next-line
      ngOnDestroy(): void {
      }
    }

    new FakeComponent().ngOnDestroy();

    expect(mockSubscription1.unsubscribe).toHaveBeenCalledTimes(0);
    expect(mockSubscription2.unsubscribe).toHaveBeenCalledTimes(0);
  });
});
