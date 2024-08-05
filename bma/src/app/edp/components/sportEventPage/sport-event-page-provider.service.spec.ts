import { SportEventPageProviderService } from '@edp/components/sportEventPage/sport-event-page-provider.service';
import { BehaviorSubject } from 'rxjs';

describe('SportEventPageProviderService', () => {
  let service;

  beforeEach(() => {
    service = new SportEventPageProviderService();
  });

  it('should create service', () => {
    expect(service).toBeDefined();
  });

  it('should define sportDataSubject', () => {
    expect(service['sportDataSubject']).toEqual(jasmine.any(BehaviorSubject));
  });

  it('should return sportDataSubject', () => {
    expect(service.sportData).toEqual(service['sportDataSubject']);
  });
});
