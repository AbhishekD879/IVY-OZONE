import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';

import {AbstractService} from './transport/abstract.service';
import {CompetitionParticipant, CompetitionParticipantUpdate} from '../../models';

@Injectable()
export class CompetitionParticipantsService extends AbstractService<CompetitionParticipant> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'participant';
  }

  public getSingleParticipant(competitionId: string, participantId: string):
  Observable<HttpResponse<CompetitionParticipant>> {
    const uri = `competition/${competitionId}/${this.uri}/${participantId}`;
    return this.sendRequest<CompetitionParticipant>('get', uri, null);
  }

  public createParticipant(competitionId: string, participant: CompetitionParticipantUpdate):
  Observable<HttpResponse<CompetitionParticipant>> {
    const uri = `competition/${competitionId}/${this.uri}`;
    return this.sendRequest<CompetitionParticipant>('post', uri, participant);
  }

  public editParticipant(participant: CompetitionParticipantUpdate):
  Observable<HttpResponse<CompetitionParticipantUpdate>> {
    const uri = `${this.uri}/${participant.id}`;
    return this.sendRequest<CompetitionParticipantUpdate>('put', uri, participant);
  }

  public deleteParticipant(competitionId: string, participantId: string): Observable<HttpResponse<void>> {
    const uri = `competition/${competitionId}/${this.uri}/${participantId}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public uploadSvg(participantId: string, file: FormData): Observable<HttpResponse<CompetitionParticipant>> {
    const uri = `${this.uri}/${participantId}/image?fileType=svg`;
    return this.sendRequest<CompetitionParticipant>('post', uri, file);
  }

  public removeSvg(participantId: string): Observable<HttpResponse<CompetitionParticipant>> {
    const uri = `${this.uri}/${participantId}/image?fileType=svg`;
    return this.sendRequest<CompetitionParticipant>('delete', uri, null);
  }
}
