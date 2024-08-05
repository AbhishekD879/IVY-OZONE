import { EventMorePipe } from '@shared/pipes/event-more/event-more.pipe';

describe('EventMorePipe', () => {
  let pipe;

  beforeEach(() => {
    pipe = new EventMorePipe();
  });

  it('should transform vaue (MORE)', () => {
    expect(pipe.transform(0)).toEqual('MORE');
  });

  it('should transform vaue (n MORE)', () => {
    expect(pipe.transform(5)).toEqual('4 MORE');
  });
});
