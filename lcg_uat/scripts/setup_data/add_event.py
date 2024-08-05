import argparse
from crlat_ob_client.openbet_config import OBConfig
from crlat_ob_client.utils.helpers import generate_name


class CreateSportEvent(OBConfig):
    """
    Create sport event (including event with score or set)
    cli examples:
    football event: python scripts/setup_data/add_event.py -cl_id 16291 -cat_id 16 -type_id 3756 -mr_tem_id 552754 -t1 D -t2 C -env tst2 -br bma
    volleyball event: python scripts/setup_data/add_event.py -cl_id 269 -cat_id 36 -type_id 1715 -mr_tem_id 134093 -t1 D -t2 C -sc 25-18 -env tst2 -br bma -set (2):(0) -live True -stream True
    handball event: python scripts/setup_data/add_event.py -cl_id 203 -cat_id 20 -type_id 1273 -mr_tem_id 117027 -t1 D -t2 C -sc 25-18 -env tst2 -br bma -live True -stream True
    """
    def __init__(self, env, brand):
        super(CreateSportEvent, self).__init__(env, brand)

    def add_event(self, **params):
        """
        :params: score handball format for example: score '25-18'
        expected: "Dinamik Genclik 25-18 Cevhertepe"
        :params: score and set for [volleyball format for example: score '25-18', set '(2):(0)'
        expected: "Dinamik Genclik (2) 25-18 (0) Cevhertepe"""
        if self.brand == 'bma':
            default_market_name = '|Match Result|'
        else:
            default_market_name = '|Match Betting|'
        created_events = {}
        for _ in range(int(params.get('events_number'))):
            if not params.get('team1') and not params.get('team2'):
                team1, team2 = f'{generate_name()}', f'{generate_name()}'
            else:
                team1, team2 = params.get('team1'), params.get('team2')
                # remove team1 and team2 from the parameters to prevent the creation of different
                # events that have the same name
            params.pop('team1') if 'team1' in params.keys() else None
            params.pop('team2') if 'team2' in params.keys() else None
            ev = self.add_sport_event(default_market_name=default_market_name, team1=team1, team2=team2, **params)
            created_events[f'{ev.team1} v {ev.team2}'] = ev.event_id
        self._logger.info(f'*** CREATED EVENTS: "{created_events}"')
        return created_events

    @staticmethod
    def configure_arg_parser():
        """
        Initiate the parser and add arguments
        """
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--class_id", "-cl_id", help="Class id", required=True, type=int)
        arg_parser.add_argument("--category_id", "-cat_id", help="Category id", required=True, type=int)
        arg_parser.add_argument("--type_id", "-type_id", help="Type id", required=True, type=int)
        arg_parser.add_argument("--market_template_id", "-mr_tem_id", help="Market template id", required=True,
                                type=int)
        arg_parser.add_argument("--team1", "-t1", help="Team 1", type=str)
        arg_parser.add_argument("--team2", "-t2", help="Team 2", type=str)
        arg_parser.add_argument("--env", "-env", help="Environment name", required=True, type=str)
        arg_parser.add_argument("--brand", "-br", help="Brand name", required=True, type=str)
        arg_parser.add_argument("--score", "-sc", help="Score", type=str)
        arg_parser.add_argument("--set", "-set", help="Sets", type=str)
        arg_parser.add_argument("--is_live", "-live", help="Is live", type=bool)
        arg_parser.add_argument("--img_stream", "-stream", help="Img stream", type=bool)
        arg_parser.add_argument("--events_number", "-events_number", help="Number of events", default=1, type=int)
        return arg_parser


if __name__ == "__main__":
    parser = CreateSportEvent.configure_arg_parser()
    # read arguments from the command line
    args = parser.parse_args()
    parameters = {}
    for param, value in vars(args).items():
        if param == 'set' or value is None:
            continue
        else:
            parameters[param] = value

    if 'set' in vars(args).keys() and vars(args)['set'] is not None:
        parameters['score'] = {'current': parameters['score'], 'set': vars(args)['set']}
    else:
        if 'score' in parameters.keys():
            parameters['score'] = {'current': parameters['score']}

    a = CreateSportEvent(args.env, args.brand)
    event = a.add_event(**parameters)
