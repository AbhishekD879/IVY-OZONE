export class EventScore {
  eventId: string;
  eventPosition: number;
  actualScores: number[];

  constructor({eventId, eventPosition, actualScores}:
                { eventId?: string, eventPosition?: number, actualScores?: number[] } = {}) {
    this.eventId = eventId;
    this.eventPosition = Number(eventPosition);
    if (actualScores.length) {
      actualScores.forEach((actualScore, index) => {
        actualScores[index] = Number(actualScore);
      });
    }

    this.actualScores = actualScores;
  }
}
