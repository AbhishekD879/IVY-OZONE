import { Iterator } from './iterator.class';

describe('Iterator', () => {
  let iterator: Iterator;

  beforeEach(() => {
    iterator = new Iterator();
  });

  it('constructor', () => {
    expect(iterator).toBeTruthy();
    expect(iterator.items).toEqual(jasmine.any(Array));
  });

  it('start', () => {
    const callback = () => {};
    iterator.first = jasmine.createSpy();

    iterator.start(callback);

    expect(iterator['onFinishCallback']).toBe(callback);
    expect(iterator['isStartedFlag']).toBe(true);
    expect(iterator.first).toHaveBeenCalled();
  });

  it('isStarted', () => {
    iterator['isStartedFlag'] = true;
    expect(iterator.isStarted()).toBe(true);

    iterator['isStartedFlag'] = false;
    expect(iterator.isStarted()).toBe(false);
  });

  it('startFrom', () => {
    const index = 1;
    const callback = jasmine.createSpy();
    iterator.next = jasmine.createSpy();

    iterator.startFrom(index, callback);

    expect(callback).toHaveBeenCalled();
    expect(iterator['index']).toBe(index);
    expect(iterator['isStartedFlag']).toBe(true);
    expect(iterator.next).toHaveBeenCalled();
  });

  it('add', () => {
    iterator.items = [{}] as any[];
    iterator['isStartedFlag'] = true;
    iterator.next = jasmine.createSpy();

    iterator.add([{}] as any[]);

    expect(iterator.items.length).toBe(2);
    expect(iterator.next).toHaveBeenCalled();
  });

  it('first', () => {
    iterator.next = jasmine.createSpy();

    iterator.first();

    expect(iterator['index']).toBe(0);
    expect(iterator.next).toHaveBeenCalled();
  });

  it('next', () => {
    iterator.hasNext = jasmine.createSpy().and.returnValue(true);
    iterator['index'] = 0;
    iterator.items = [{
      run: jasmine.createSpy(), data: {}
    }];

    iterator.next();

    expect(iterator.hasNext).toHaveBeenCalled();
    expect(iterator['index']).toBe(1);
    expect(iterator.items[0].run).toHaveBeenCalledWith(iterator, iterator.items[0].data);
  });

  it('next (no next items)', () => {
    iterator.hasNext = jasmine.createSpy().and.returnValue(false);
    iterator.stop = jasmine.createSpy();
    iterator['onFinishCallback'] = jasmine.createSpy();

    iterator.next();

    expect(iterator.hasNext).toHaveBeenCalled();
    expect(iterator.stop).toHaveBeenCalled();
    expect(iterator['onFinishCallback']).toHaveBeenCalled();
  });

  it('hasNext', () => {
    iterator.items = [{}] as any[];

    iterator['index'] = 0;
    expect(iterator.hasNext()).toBeTruthy();

    iterator['index'] = 1;
    expect(iterator.hasNext()).toBeFalsy();
  });

  it('reset', () => {
    iterator.reset();
    expect(iterator['index']).toBe(0);
    expect(iterator['isStartedFlag']).toBeFalsy();
    expect(iterator['iterating']).toBeFalsy();
    expect(iterator.items).toEqual([]);
  });

  it('stop', () => {
    iterator.stop();
    expect(iterator['iterating']).toBeFalsy();
  });
});
