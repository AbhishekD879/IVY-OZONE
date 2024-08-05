import { ParticipantsService } from '@app/bigCompetitions/services/participants/participants.service';

describe('ParticipantsService', () => {
  let service;
  let filtersService;

  beforeEach(() => {
    filtersService = {
      getTeamName: jasmine.createSpy('getTeamName').and.callFake((name, index) => index ? ' awayName ' : ' homeName ')
    };
    service = new ParticipantsService(filtersService);
  });

  it('should set participants', () => {
    const participants = [];

    service.store(participants);
    expect(service.participants).toBe(participants);
  });

  it('should return svg strings', () => {
    service.participants = [
      {
        svg: 'svg1'
      },
      {
        svg: 'svg2'
      },
      {
        svg: 'svg3'
      }
    ];
    const result = service.getFlagsList();

    expect(result).toBe('svg1svg2svg3');
  });

  it('should return empty string', () => {
    service.participants = [{
        svg: ''
    }];

    const result = service.getFlagsList();

    expect(result).toBe('');
  });

  it('should parse participants from name', () => {
    service['getParticipant'] = jasmine.createSpy('getParticipant').and.callFake(name => name);
    const result = service.parseParticipantsFromName('name');

    expect(filtersService.getTeamName).toHaveBeenCalledWith('name', 0);
    expect(filtersService.getTeamName).toHaveBeenCalledWith('name', 1);
    expect(service['getParticipant']).toHaveBeenCalledWith('homeName');
    expect(service['getParticipant']).toHaveBeenCalledWith('awayName');
    expect(result).toEqual(jasmine.objectContaining({ HOME: 'homeName', AWAY: 'awayName' }));
  });

  it('should parse participants from name whe no home name was returned', () => {
    filtersService.getTeamName = jasmine.createSpy('getParticipant').and.callFake((name, index) => index ? ' awayName ' : '');
    service['getParticipant'] = jasmine.createSpy('getParticipant').and.callFake(name => name);
    const result = service.parseParticipantsFromName('name');

    expect(filtersService.getTeamName).toHaveBeenCalledWith('name', 0);
    expect(filtersService.getTeamName).toHaveBeenCalledWith('name', 1);
    expect(service['getParticipant']).toHaveBeenCalledWith('name');
    expect(service['getParticipant']).toHaveBeenCalledWith('awayName');
    expect(result).toEqual(jasmine.objectContaining({ HOME: 'name', AWAY: 'awayName' }));
  });

  it('should return participant by name', () => {
    const participant = {};
    service.participants = [ participant ];
    const result = service['getParticipant']('0');

    expect(result).toBe(participant);
  });

  it('should return new participant when was not found by name in existing ones', () => {
    service['createAbbreviation'] = jasmine.createSpy('createAbbreviation').and.returnValue('abbreviation');
    const result = service['getParticipant']('name');

    expect(service['createAbbreviation']).toHaveBeenCalledWith('name');
    expect(result).toEqual(jasmine.objectContaining({ name: 'name', abbreviation: 'abbreviation' }));
  });

  it('should return new participant with empty name, when was not found by name in existing ones', () => {
    service['createAbbreviation'] = jasmine.createSpy('createAbbreviation').and.returnValue('abbreviation');
    const result = service['getParticipant']();

    expect(service['createAbbreviation']).toHaveBeenCalledWith('');
    expect(result).toEqual(jasmine.objectContaining({ name: '', abbreviation: 'abbreviation' }));
  });

  it('should create abbreviation', () => {
    const result = service['createAbbreviation']('abservation');

    expect(result).toBe('ABS');
  });
});
