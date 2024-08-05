import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('EventNamePipe', () => {
  let pipe;

  beforeEach(() => {
    pipe = new EventNamePipe();
  });

  it('should transform remove unwanted combinations in parentheses', () => {
    const eventName = pipe.transform('Baltimore Orioles (home) @ Detroit Tigers (away) (women) (SS) (bg) (Bo1)   ');
    expect(eventName).toBe('Baltimore Orioles (home) @ Detroit Tigers (away) (women)');
  });

  it('should transform remove unwanted combinations in pipes', () => {
    const eventName = pipe.transform('Baltimore Orioles |home| VS Detroit Tigers |away| |women| |SS| |bg| |Bo20|   ');
    expect(eventName).toBe('Baltimore Orioles |home| VS Detroit Tigers |away| |women|');
  });

  it('should return empty string', () => {
    expect(pipe.transform()).toBe('');
  });

  it('should return empty string if null', () => {
    expect(pipe.transform(null)).toBe('');
  });
});
