import { ResolveService } from './resolve.service';

describe('ResolveService', () => {
  let service: ResolveService;

  beforeEach(() => {
    service = new ResolveService();
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should get/set/reset data (resolve)', () => {
    const newPromise = new Promise(resolve => resolve('test'));

    service.set(newPromise, 'newdata').then(() => {
      expect(service.get('newdata')).toBe('test');
      expect(service.get('newdata1')).toBe(null);
    });

    service.reset('newdata');
    expect(service.get('newdata')).toBe(null);
  });

  it('should get/set/reset data (reject)', () => {
    const newPromise = new Promise((resolve, reject) => reject());

    service.set(newPromise, 'newdata').then(() => {}).catch(e => {
      expect(service.get('newdata')).toBe(null);
    });
  });
});
