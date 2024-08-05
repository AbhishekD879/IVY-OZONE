import { IteratorService } from './iterator.service';
import { Iterator } from './iterator.class';

describe('IteratorService', () => {
  let service: IteratorService;

  beforeEach(() => {
    service = new IteratorService();
  });

  it('create', () => {
    expect(service.create([])).toEqual(jasmine.any(Iterator));
  });
});
